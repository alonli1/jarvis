import pytest
from mcp import Client

from jarvis import mcp_server
from jarvis.models import Chunk, SearchHit


def sample_hits() -> list[SearchHit]:
    return [
        SearchHit(
            chunk=Chunk(
                id="chunk-1",
                text="A heavy scalar generates curvature-squared operators.",
                source_path="knowledge/papers/scalar.pdf",
                page=12,
                visibility="public",
            ),
            score=0.9,
        )
    ]


@pytest.mark.anyio
async def test_mcp_search_returns_structured_citations(monkeypatch):
    monkeypatch.setattr(mcp_server, "retrieve_hits", lambda *args, **kwargs: sample_hits())
    async with Client(mcp_server.mcp, mode="legacy", read_timeout_seconds=5) as client:
        result = await client.call_tool("search_knowledge", {"query": "heavy scalar", "limit": 1})
    assert result.is_error is False
    assert result.structured_content["query"] == "heavy scalar"
    assert result.structured_content["sources"][0]["id"] == "S1"


def test_mcp_visibility_defaults_to_public(monkeypatch):
    monkeypatch.delenv("JARVIS_MCP_MAX_VISIBILITY", raising=False)
    assert mcp_server.configured_max_visibility() == "public"
