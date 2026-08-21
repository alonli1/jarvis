from __future__ import annotations

from datetime import date, timedelta

import typer
import yaml
from rich.console import Console
from rich.table import Table

from . import __version__
from .answering import answer_question
from .antigravity import install_global_mcp
from .config import find_repo_root, load_config
from .index import HybridIndex
from .literature import search_all
from .novelty import evaluate_project, render_markdown
from .retrieval import render_retrieval_prompt, retrieve_hits

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


@app.command()
def ask(
    question: str = typer.Argument(...),
    model: str | None = typer.Option(None, "--model"),
    allow_private: bool = typer.Option(
        False, "--allow-private", help="Allow group/confidential context to external models"
    ),
) -> None:
    """Answer a question using retrieved group knowledge and a selected LLM."""
    cfg = load_config()
    selected = model or cfg.assistant.default_model
    answer, hits = answer_question(cfg, question, selected, allow_private=allow_private)
    console.print(answer)
    if hits:
        console.print("\n[bold]Retrieved sources[/bold]")
        for i, hit in enumerate(hits, start=1):
            c = hit.chunk
            loc = c.source_path + (f":p{c.page}" if c.page else "")
            console.print(f"[S{i}] {loc} (score={hit.score:.3f}, visibility={c.visibility})")


@app.command()
def retrieve(
    question: str = typer.Argument(...),
    limit: int | None = typer.Option(None, "--limit", min=1, max=50),
    max_visibility: str = typer.Option("public", "--max-visibility"),
) -> None:
    """Retrieve cited context for a web chat or another AI client without calling an LLM."""
    visibility = max_visibility.lower()
    if visibility not in {"public", "group", "confidential"}:
        raise typer.BadParameter("--max-visibility must be public, group, or confidential")
    cfg = load_config()
    hits = retrieve_hits(cfg, question, limit=limit, max_visibility=visibility)
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
