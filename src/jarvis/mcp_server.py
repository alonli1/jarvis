from __future__ import annotations

import os
from typing import Annotated

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import Field

from .config import load_config
from .models import Visibility
from .retrieval import retrieval_result, retrieve_hits

mcp = MCPServer(
    "Jarvis",
    instructions="Search the research group's indexed scientific knowledge with citations.",
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


@mcp.tool(
    title="Search Jarvis knowledge",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
async def search_knowledge(
    query: Annotated[str, Field(min_length=1, description="Scientific question or search query.")],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum retrieved sources.")] = 10,
) -> dict[str, object]:
    """Search the local Jarvis index and return source text, metadata, and citation IDs."""
    hits = retrieve_hits(
        load_config(),
        query,
        limit=limit,
        max_visibility=configured_max_visibility(),
    )
    return retrieval_result(query, hits)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
