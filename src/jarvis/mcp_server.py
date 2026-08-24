from __future__ import annotations

import os
from typing import Annotated

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import Field

from . import graph_queries
from .config import load_config
from .literature_graph import build_graph
from .models import Visibility
from .retrieval import retrieval_result, retrieve_hits

mcp = MCPServer(
    "Jarvis",
    instructions=(
        "Search the research group's indexed scientific knowledge and query its "
        "literature relationship graph."
    ),
)


def configured_max_visibility() -> str:
    value = os.getenv("JARVIS_MCP_MAX_VISIBILITY", "public").lower()
    try:
        Visibility.parse(value)
    except KeyError as exc:
        raise ValueError(
            "JARVIS_MCP_MAX_VISIBILITY must be public, group, or confidential"
        ) from exc
    return value


def _graph() -> dict:
    config = load_config()
    graph = build_graph(config.root, manuscript_neighbors=75)
    return graph_queries.filter_graph_visibility(graph, configured_max_visibility())


@mcp.tool(
    title="Search Jarvis knowledge",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
async def search_knowledge(
    query: Annotated[str, Field(min_length=1, description="Scientific question or search query.")],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum retrieved sources.")] = 10,
    tags: Annotated[
        list[str] | None,
        Field(description="Optional controlled research tags; all supplied tags must match."),
    ] = None,
) -> dict[str, object]:
    """Search the local Jarvis index and return source text, metadata, and citation IDs."""
    hits = retrieve_hits(
        load_config(),
        query,
        limit=limit,
        max_visibility=configured_max_visibility(),
        tags=tags,
    )
    return retrieval_result(query, hits)


@mcp.tool(
    title="Find related papers",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
async def find_related_papers(
    query: Annotated[
        str, Field(min_length=1, description="Paper, manuscript ID, or unique title text.")
    ],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum related papers.")] = 10,
    relationship_types: Annotated[
        list[str] | None,
        Field(
            description="Optional filters: cites, bibliographic_coupling, similar, "
            "relevant_to_manuscript."
        ),
    ] = None,
) -> dict[str, object]:
    """Rank papers directly related through citations, shared references, or topics."""
    return graph_queries.related_papers(_graph(), query, limit, relationship_types)


@mcp.tool(
    title="Explain a literature relationship",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
async def explain_relationship(
    left: Annotated[str, Field(min_length=1, description="First graph node.")],
    right: Annotated[str, Field(min_length=1, description="Second graph node.")],
) -> dict[str, object]:
    """Explain every direct relationship and its graph evidence between two works."""
    return graph_queries.explain_relationship(_graph(), left, right)


@mcp.tool(
    title="Find a citation path",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
async def find_citation_path(
    source: Annotated[str, Field(min_length=1, description="Citing source work.")],
    target: Annotated[str, Field(min_length=1, description="Cited target work.")],
    max_hops: Annotated[int, Field(ge=1, le=12, description="Maximum citation hops.")] = 6,
) -> dict[str, object]:
    """Find the shortest directed path where each work cites the next."""
    return graph_queries.citation_path(_graph(), source, target, max_hops)


@mcp.tool(
    title="Find bridge papers",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
async def find_bridge_papers(
    left: Annotated[str, Field(min_length=1, description="First work or manuscript.")],
    right: Annotated[str, Field(min_length=1, description="Second work or manuscript.")],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum bridge papers.")] = 10,
) -> dict[str, object]:
    """Find papers directly connected to both selected graph nodes."""
    return graph_queries.bridge_papers(_graph(), left, right, limit)


@mcp.tool(
    title="Find papers relevant to a manuscript",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
async def papers_relevant_to_manuscript(
    manuscript: Annotated[
        str, Field(min_length=1, description="Manuscript ID or unique project title.")
    ],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum relevant papers.")] = 10,
) -> dict[str, object]:
    """Rank papers connected to a manuscript through controlled research tags."""
    return graph_queries.manuscript_papers(_graph(), manuscript, limit)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
