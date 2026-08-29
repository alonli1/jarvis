from __future__ import annotations

import json
import os
import webbrowser
from datetime import date, timedelta
from pathlib import Path

import httpx
import typer
import yaml
from rich.console import Console
from rich.table import Table

from . import __version__
from .antigravity import install_global_mcp
from .citations import sync_citations, sync_pdf_citations
from .cloud_library import add_document, resolve_conflict, sync_dropbox
from .config import find_repo_root, load_config
from .dropbox_client import (
    DropboxClient,
    DropboxSettings,
    authorize,
    project_app_key,
    save_refresh_token,
    save_settings,
)
from .evaluation import evaluate_cases, load_cases
from .graph_server import create_graph_server
from .graph_view import render_graph_html
from .index import HybridIndex
from .library_sync import sync_library
from .literature import search_all
from .literature_graph import (
    build_graph,
    find_node,
    render_graph_markdown,
    save_graph,
)
from .retrieval import render_retrieval_prompt, retrieve_hits
from .taxonomy import normalize_tag
from .workflows import (
    execute_computation,
    prepare_computation,
    prepare_ideation,
    prepare_literature,
    tool_status,
)
from .workflows import handoff as export_handoff

app = typer.Typer(
    no_args_is_help=True, help="Provider-neutral research harness for physics research groups"
)
console = Console()
library_app = typer.Typer(no_args_is_help=True, help="Manage the shared research library.")
run_app = typer.Typer(no_args_is_help=True, help="Prepare provider-neutral research workflows.")
compute_app = typer.Typer(no_args_is_help=True, help="Execute explicit computation workbenches.")
eval_app = typer.Typer(no_args_is_help=True, help="Run deterministic evidence/tool evaluations.")
app.add_typer(library_app, name="library")
app.add_typer(run_app, name="run")
app.add_typer(compute_app, name="compute")
app.add_typer(eval_app, name="eval")


def _print_cloud_result(result, dry_run: bool = False) -> None:
    prefix = "Would apply" if dry_run else "Applied"
    console.print(
        f"[green]{prefix}[/green] {result.uploaded} uploads, {result.downloaded} downloads, "
        f"{result.unchanged} unchanged, {result.conflicts} conflicts, "
        f"{result.remote_deletions} Dropbox deletions preserved."
    )
    for action in result.actions:
        if action.action not in {"unchanged", "removed-both"}:
            console.print(
                f"- {action.action}: {action.relative}"
                + (f" ({action.detail})" if action.detail else "")
            )


@app.command()
def doctor() -> None:
    """Check the repository and show active configuration."""
    cfg = load_config()
    console.print(f"[bold]Jarvis {__version__}[/bold]")
    console.print(f"Repository: {cfg.root}")
    console.print(f"Default model: {cfg.assistant.default_model}")
    console.print(f"Index mode: {cfg.index.mode}")
    console.print(f"Dense model: {cfg.index.dense_model}")
    console.print(f"Sparse model: {cfg.index.sparse_model}")
    for folder in ["knowledge", "group", "topics", "literature"]:
        ok = (cfg.root / folder).exists()
        console.print(f"{'[green]OK[/green]' if ok else '[red]MISSING[/red]'} {folder}/")
    settings = cfg.root / ".jarvis" / "settings.toml"
    console.print(
        f"{'[green]OK[/green]' if settings.exists() else '[yellow]NOT CONFIGURED[/yellow]'} Dropbox"
    )
    try:
        import keyring

        secure_keyring = getattr(keyring.get_keyring(), "priority", 0) > 0
    except (ImportError, RuntimeError):
        secure_keyring = False
    console.print(
        f"{'[green]OK[/green]' if secure_keyring else '[yellow]UNAVAILABLE[/yellow]'} OS keyring"
    )
    for tool in tool_status(cfg.root):
        status = tool["status"]
        color = "green" if status == "available" else "yellow"
        version = f" {tool.get('version')}" if tool.get("version") else ""
        console.print(f"[{color}]{status.upper()}[/{color}] {tool['id']}{version}")


@app.command()
def setup(
    dropbox_link: str = typer.Option(..., "--dropbox-link", help="Shared Dropbox folder URL."),
    app_key: str | None = typer.Option(None, "--app-key", help="Public Dropbox PKCE app key."),
    open_browser: bool = typer.Option(True, "--open/--no-open"),
) -> None:
    """Authorize Dropbox, synchronize the group library, and build the local index."""
    cfg = load_config()
    try:
        key = project_app_key(app_key or cfg.dropbox.app_key)
        refresh_token, account_id = authorize(
            key, open_browser=webbrowser.open if open_browser else lambda url: console.print(url)
        )
        save_refresh_token(account_id, refresh_token)
        provisional = DropboxSettings(key, account_id, "", "", "", dropbox_link)
        with DropboxClient(provisional, refresh_token=refresh_token) as client:
            folder = client.resolve_shared_folder(dropbox_link)
            settings = DropboxSettings(
                key, account_id, folder["id"], folder["path"], folder["name"], dropbox_link
            )
            client.settings = settings
            client.ensure_layout()
            save_settings(cfg.root, settings)
            result = sync_dropbox(cfg.root, client)
        _print_cloud_result(result)
        index = HybridIndex(cfg)
        for target in (cfg.root / "knowledge", cfg.root / "group"):
            docs, chunks = index.ingest(target)
            console.print(f"Indexed {docs} documents / {chunks} chunks from {target}")
    except (
        FileNotFoundError,
        PermissionError,
        RuntimeError,
        TypeError,
        ValueError,
        httpx.HTTPError,
    ) as exc:
        console.print(f"[red]Setup failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@library_app.command("sync")
def cloud_library_sync(dry_run: bool = typer.Option(False, "--dry-run")) -> None:
    """Synchronize local additions and Dropbox changes without propagating deletions."""
    root = find_repo_root()
    try:
        with DropboxClient.from_repo(root) as client:
            result = sync_dropbox(root, client, dry_run=dry_run)
        _print_cloud_result(result, dry_run)
        if not dry_run and result.changed_local:
            cfg = load_config(root)
            index = HybridIndex(cfg)
            for path in result.changed_local:
                index.ingest(path)
    except (
        FileNotFoundError,
        PermissionError,
        RuntimeError,
        TypeError,
        ValueError,
        httpx.HTTPError,
    ) as exc:
        console.print(f"[red]Library sync failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@library_app.command("status")
def cloud_library_status() -> None:
    """Report pending transfers and conflicts without changing the library."""
    cloud_library_sync(dry_run=True)


@library_app.command("add")
def cloud_library_add(
    file: Path = typer.Argument(..., exists=True, dir_okay=False),  # noqa: B008
    category: str = typer.Option(..., "--category"),
) -> None:
    """Add a document, upload its PDF/sidecar pair, and ingest the local copy."""
    root = find_repo_root()
    try:
        with DropboxClient.from_repo(root) as client:
            destination, result = add_document(root, file, category, client)
        _print_cloud_result(result)
        cfg = load_config(root)
        docs, chunks = HybridIndex(cfg).ingest(destination)
        console.print(f"[green]Added[/green] {destination}: {docs} document / {chunks} chunks")
    except (
        FileNotFoundError,
        FileExistsError,
        PermissionError,
        RuntimeError,
        TypeError,
        ValueError,
        httpx.HTTPError,
    ) as exc:
        console.print(f"[red]Could not add document:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@library_app.command("resolve")
def cloud_library_resolve(
    path: str = typer.Argument(..., help="Provider-relative path such as papers/work.pdf."),
    strategy: str = typer.Option(..., "--use", help="local, dropbox, or keep-both"),
) -> None:
    """Resolve a preserved Dropbox conflict explicitly."""
    root = find_repo_root()
    try:
        with DropboxClient.from_repo(root) as client:
            changed = resolve_conflict(root, client, path, strategy)
        if changed:
            index = HybridIndex(load_config(root))
            for item in changed:
                if not item.name.endswith(".meta.yaml"):
                    index.ingest(item)
        console.print(f"[green]Resolved[/green] {path} using {strategy}.")
    except (
        FileNotFoundError,
        PermissionError,
        RuntimeError,
        TypeError,
        ValueError,
        httpx.HTTPError,
    ) as exc:
        console.print(f"[red]Could not resolve conflict:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command("install-antigravity")
def install_antigravity() -> None:
    """Register Jarvis globally for Antigravity versions without workspace MCP discovery."""
    try:
        path = install_global_mcp(find_repo_root())
    except (FileNotFoundError, TypeError, ValueError, OSError) as exc:
        console.print(f"[red]Could not configure Antigravity:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Registered Jarvis MCP server in {path}[/green]")
    console.print("Refresh MCP Servers or restart Antigravity.")


@app.command()
def ingest(
    path: str | None = typer.Argument(
        None, help="File/folder to ingest; defaults to knowledge + group"
    ),
) -> None:
    """Build/update the local scientific retrieval index."""
    cfg = load_config()
    index = HybridIndex(cfg)
    targets = [cfg.root / path] if path else [cfg.root / "knowledge", cfg.root / "group"]
    total_docs = total_chunks = 0
    for target in targets:
        docs, chunks = index.ingest(target)
        total_docs += docs
        total_chunks += chunks
        console.print(f"Indexed {docs} documents / {chunks} chunks from {target}")
    console.print(f"[bold green]Done:[/bold green] {total_docs} documents, {total_chunks} chunks")


@app.command("library-sync")
def library_sync_command(
    source: Path | None = typer.Argument(  # noqa: B008
        None, help="Mounted provider root; defaults to JARVIS_LIBRARY_ROOT."
    ),
    provider: str = typer.Option("synced-folder", "--provider"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Pull validated documents from Dropbox or another locally synced provider."""
    source = source or (Path(value) if (value := os.getenv("JARVIS_LIBRARY_ROOT")) else None)
    if source is None:
        raise typer.BadParameter("Pass SOURCE or set JARVIS_LIBRARY_ROOT")
    try:
        result = sync_library(find_repo_root(), source, provider=provider, dry_run=dry_run)
    except (FileNotFoundError, FileExistsError, NotADirectoryError, TypeError, ValueError) as exc:
        console.print(f"[red]Library sync failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    verb = "Would sync" if dry_run else "Synced"
    console.print(
        f"[green]{verb}[/green] {result.documents} documents: {result.copied} new, "
        f"{result.updated} updated, {result.unchanged} unchanged; "
        f"{result.sidecars_preserved} curated sidecars preserved."
    )


@app.command()
def ask(
    question: str = typer.Argument(...),
    model: str | None = typer.Option(None, "--model"),
) -> None:
    """Answer a question using retrieved group knowledge and a selected LLM."""
    from .answering import answer_question

    cfg = load_config()
    selected = model or cfg.assistant.default_model
    answer, hits = answer_question(cfg, question, selected)
    console.print(answer)
    if hits:
        console.print("\n[bold]Retrieved sources[/bold]")
        for i, hit in enumerate(hits, start=1):
            c = hit.chunk
            loc = c.source_path + (f":p{c.page}" if c.page else "")
            console.print(f"[S{i}] {loc} (score={hit.score:.3f})")


@app.command()
def retrieve(
    question: str = typer.Argument(...),
    limit: int | None = typer.Option(None, "--limit", min=1, max=50),
    tag: list[str] | None = typer.Option(  # noqa: B008
        None, "--tag", help="Require a research tag."
    ),
) -> None:
    """Retrieve cited context for a web chat or another AI client without calling an LLM."""
    cfg = load_config()
    hits = retrieve_hits(cfg, question, limit=limit, tags=tag)
    console.print(render_retrieval_prompt(question, hits), markup=False)


@eval_app.command("run")
def eval_run(
    cases: Path = typer.Option(Path("evals/cases"), "--cases"),  # noqa: B008
    output: Path | None = typer.Option(None, "--output"),  # noqa: B008
) -> None:
    """Run source-evidence and registered-tool checks without model calls."""
    try:
        config = load_config()
        report = evaluate_cases(
            config, load_cases(cases if cases.is_absolute() else config.root / cases)
        )
        text = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if output:
            output.write_text(text, encoding="utf-8")
        else:
            typer.echo(text, nl=False)
    except (OSError, TypeError, ValueError) as exc:
        typer.echo(f"Evaluation failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc


@run_app.command("literature")
def run_literature(
    question: str = typer.Option(..., "--question"),
    paper: str | None = typer.Option(None, "--paper"),
    limit: int | None = typer.Option(None, "--limit", min=1, max=50),
) -> None:
    """Prepare a page-grounded literature-reading evidence bundle."""
    try:
        bundle = prepare_literature(load_config(), question, paper, limit)
    except (FileNotFoundError, RuntimeError, TypeError, ValueError) as exc:
        console.print(f"[red]Could not prepare literature run:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Prepared[/green] {bundle.id}: {bundle.path}")


@run_app.command("ideation")
def run_ideation(
    topic: str = typer.Option(..., "--topic"),
    project: Path | None = typer.Option(None, "--project"),  # noqa: B008
    limit: int | None = typer.Option(None, "--limit", min=1, max=50),
) -> None:
    """Prepare corpus and graph evidence for testable research directions."""
    try:
        bundle = prepare_ideation(load_config(), topic, project, limit)
    except (FileNotFoundError, RuntimeError, TypeError, ValueError) as exc:
        console.print(f"[red]Could not prepare ideation run:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Prepared[/green] {bundle.id}: {bundle.path}")


@run_app.command("computation")
def run_computation(
    task: str = typer.Option(..., "--task"),
    engine: str = typer.Option("auto", "--engine"),
) -> None:
    """Prepare a Python or Wolfram workbench with provenance."""
    try:
        bundle = prepare_computation(load_config(), task, engine)
    except (FileNotFoundError, RuntimeError, TypeError, ValueError) as exc:
        console.print(f"[red]Could not prepare computation run:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Prepared[/green] {bundle.id}: {bundle.path}")
    console.print(f"Inspect the script, then run `jarvis compute execute {bundle.id} SCRIPT`.")


@compute_app.command("execute")
def compute_execute(
    run_id: str = typer.Argument(...),
    script: Path = typer.Argument(...),  # noqa: B008
    timeout: int = typer.Option(300, "--timeout", min=1, max=86400),
) -> None:
    """Explicitly execute a script contained in a computation run."""
    try:
        code, log = execute_computation(load_config(), run_id, script, timeout)
    except (FileNotFoundError, RuntimeError, TypeError, ValueError, OSError) as exc:
        console.print(f"[red]Computation failed to start:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"Execution exit code {code}; log: {log}")
    if code:
        raise typer.Exit(code=code)


@app.command()
def handoff(
    run_id: str = typer.Argument(...),
    output_format: str = typer.Option("markdown", "--format", help="markdown or zip"),
) -> None:
    """Export a sanitized research run for a browser-only AI provider."""
    try:
        output = export_handoff(load_config(), run_id, output_format)
    except (FileNotFoundError, RuntimeError, TypeError, ValueError) as exc:
        console.print(f"[red]Could not export handoff:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Exported[/green] {output}")


@app.command("literature")
def literature_search(
    query: str = typer.Argument(...),
    days: int = typer.Option(7, "--days", min=1),
    source: list[str] | None = typer.Option(None, "--source"),
) -> None:
    """Search recent scholarly literature across configured sources."""
    cfg = load_config()
    records, errors = search_all(cfg, query, date.today() - timedelta(days=days), source)
    table = Table(title=f"Literature: {query}")
    table.add_column("Date")
    table.add_column("Source")
    table.add_column("Title")
    table.add_column("ID")
    for r in records:
        table.add_row(
            str(r.published or ""), r.source, r.title[:90], r.arxiv_id or r.doi or r.source_id
        )
    console.print(table)
    if errors:
        console.print("[yellow]Some sources failed:[/yellow]")
        for name, err in errors.items():
            console.print(f"- {name}: {err}")


@app.command("graph-build")
def graph_build(
    neighbors: int = typer.Option(8, "--neighbors", min=1, max=50),
) -> None:
    """Build the local literature/manuscript relationship graph."""
    cfg = load_config()
    graph = build_graph(cfg.root, neighbors=neighbors)
    path = save_graph(cfg.root, graph)
    console.print(
        f"[green]Built[/green] {len(graph['nodes'])} nodes / "
        f"{len(graph['edges'])} relationships in {path}"
    )
    if not graph.get("citation_source"):
        console.print("[yellow]No citation cache; run `jarvis citations-sync`.[/yellow]")


@app.command("citations-sync")
def citations_sync(
    source: str = typer.Option("pdf", "--source", help="pdf or semantic-scholar"),
) -> None:
    """Extract local PDF citations or fetch them from Semantic Scholar."""
    cfg = load_config()
    source = source.lower()
    if source not in {"pdf", "semantic-scholar"}:
        raise typer.BadParameter("--source must be pdf or semantic-scholar")
    try:
        if source == "pdf":
            path, resolved, unresolved = sync_pdf_citations(cfg.root)
        else:
            path, resolved, unresolved = sync_citations(cfg.root, cfg.literature.user_agent)
    except (httpx.HTTPError, ValueError) as exc:
        console.print(f"[red]Citation sync failed:[/red] {exc}")
        console.print("Set SEMANTIC_SCHOLAR_API_KEY if the public endpoint is rate-limited.")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Saved[/green] {resolved} sources to {path}; {unresolved} unresolved.")


@app.command("graph")
def graph_report(
    query: str = typer.Argument(..., help="Paper ID, manuscript ID, or unique title text."),
    limit: int = typer.Option(40, "--limit", min=1, max=75),
    output_format: str = typer.Option("html", "--format", help="html or markdown"),
    output: str | None = typer.Option(None, "--output"),
) -> None:
    """Create an interactive HTML or Mermaid graph for a paper or manuscript."""
    output_format = output_format.lower()
    if output_format not in {"html", "markdown"}:
        raise typer.BadParameter("--format must be html or markdown")
    cfg = load_config()
    graph = build_graph(cfg.root, manuscript_neighbors=limit)
    save_graph(cfg.root, graph)
    try:
        origin = find_node(graph, query)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    suffix = "html" if output_format == "html" else "md"
    destination = (
        cfg.root / output
        if output
        else cfg.root / "literature" / "reports" / f"graph-{normalize_tag(origin['id'])}.{suffix}"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    renderer = render_graph_html if output_format == "html" else render_graph_markdown
    destination.write_text(renderer(graph, origin, limit=limit), encoding="utf-8")
    console.print(f"[green]Saved graph:[/green] {destination}")


@app.command("graph-serve")
def graph_serve(
    host: str = typer.Option("127.0.0.1", "--host", help="Interface to bind."),
    port: int = typer.Option(8765, "--port", min=0, max=65535),
    open_browser: bool = typer.Option(True, "--open/--no-open"),
) -> None:
    """Serve one live local interface for the full literature graph."""
    cfg = load_config()
    try:
        server = create_graph_server(cfg.root, host, port)
    except OSError as exc:
        console.print(f"[red]Could not start graph server:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    actual_port = server.server_address[1]
    browser_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
    url = f"http://{browser_host}:{actual_port}/"
    console.print(f"[green]Jarvis graph:[/green] {url}")
    console.print("Press Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\nStopped.")
    finally:
        server.server_close()


@app.command("init-project")
def init_project(name: str = typer.Argument(...)) -> None:
    """Create an active manuscript folder with a novelty-claim template."""
    cfg = load_config()
    dest = cfg.root / "group" / "manuscripts" / name
    dest.mkdir(parents=True, exist_ok=True)
    novelty = dest / "novelty.yaml"
    if novelty.exists():
        raise typer.BadParameter(f"{novelty} already exists")
    data = {
        "project": name,
        "tags": [],
        "claims": [
            {
                "id": f"{name.upper().replace('-', '_')}-01",
                "claim": "Replace this sentence with one precise scientific novelty claim.",
                "keywords": ["replace", "with", "search", "terms"],
                "search_queries": [],
                "status": "active",
            }
        ],
    }
    novelty.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    console.print(f"Created {novelty}")


@app.command()
def novelty(
    project: str = typer.Argument(...),
    days: int = typer.Option(7, "--days", min=1),
    source: list[str] | None = typer.Option(None, "--source"),
    judge_model: str | None = typer.Option(None, "--judge-model"),
) -> None:
    """Check one manuscript's novelty claims against recent literature."""
    from .novelty import evaluate_project, render_markdown

    cfg = load_config()
    project_dir = cfg.root / "group" / "manuscripts" / project
    if not (project_dir / "novelty.yaml").exists():
        raise typer.BadParameter(f"Missing {project_dir / 'novelty.yaml'}")
    matches, errors = evaluate_project(cfg, project_dir, days, source, judge_model)
    report = render_markdown(matches, errors)
    out = cfg.root / "literature" / "reports" / f"{date.today().isoformat()}-{project}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    console.print(report)
    console.print(f"[green]Saved:[/green] {out}")


@app.command()
def watch(
    days: int = typer.Option(2, "--days", min=1),
    source: list[str] | None = typer.Option(None, "--source"),
    judge_model: str | None = typer.Option(None, "--judge-model"),
) -> None:
    """Run novelty surveillance for every manuscript containing novelty.yaml."""
    from .novelty import evaluate_project, render_markdown

    cfg = load_config()
    manuscript_root = cfg.root / "group" / "manuscripts"
    projects = sorted(p.parent for p in manuscript_root.glob("*/novelty.yaml"))
    if not projects:
        console.print("No active project novelty files found.")
        raise typer.Exit(code=0)
    combined: list[str] = [f"# Jarvis daily literature watch — {date.today().isoformat()}", ""]
    for project_dir in projects:
        matches, errors = evaluate_project(cfg, project_dir, days, source, judge_model)
        combined += [f"# Project: {project_dir.name}", "", render_markdown(matches, errors), ""]
    out = cfg.root / "literature" / "reports" / f"{date.today().isoformat()}-daily.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(combined), encoding="utf-8")
    console.print(f"[green]Saved daily report:[/green] {out}")


if __name__ == "__main__":
    app()
