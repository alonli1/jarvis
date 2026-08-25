from __future__ import annotations

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
from .answering import answer_question
from .antigravity import install_global_mcp
from .citations import sync_citations, sync_pdf_citations
from .config import find_repo_root, load_config
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
from .novelty import evaluate_project, render_markdown
from .retrieval import render_retrieval_prompt, retrieve_hits
from .taxonomy import normalize_tag

app = typer.Typer(
    no_args_is_help=True, help="Model-agnostic scientific assistant for physics research groups"
)
console = Console()


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
            path, resolved, unresolved = sync_citations(
                cfg.root, cfg.literature.user_agent
            )
    except (httpx.HTTPError, ValueError) as exc:
        console.print(f"[red]Citation sync failed:[/red] {exc}")
        console.print("Set SEMANTIC_SCHOLAR_API_KEY if the public endpoint is rate-limited.")
        raise typer.Exit(code=1) from exc
    console.print(
        f"[green]Saved[/green] {resolved} sources to {path}; {unresolved} unresolved."
    )


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
        else cfg.root
        / "literature"
        / "reports"
        / f"graph-{normalize_tag(origin['id'])}.{suffix}"
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
