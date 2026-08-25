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
            ),
            score=0.9,
        )
    ]


def sample_graph() -> dict:
    return {
        "nodes": [
            {"id": "paper:a", "kind": "paper", "title": "A"},
            {"id": "paper:b", "kind": "paper", "title": "B"},
            {"id": "paper:c", "kind": "paper", "title": "C"},
            {"id": "manuscript:draft", "kind": "manuscript", "title": "Draft"},
        ],
        "edges": [
            {"source": "paper:a", "target": "paper:b", "kind": "cites", "score": 1.0},
            {"source": "paper:b", "target": "paper:c", "kind": "cites", "score": 1.0},
            {
                "source": "manuscript:draft",
                "target": "paper:b",
                "kind": "relevant_to_manuscript",
                "score": 1.0,
                "shared_tags": ["gravity"],
            },
        ],
    }


@pytest.mark.anyio
async def test_mcp_search_returns_structured_citations(monkeypatch):
    monkeypatch.setattr(mcp_server, "retrieve_hits", lambda *args, **kwargs: sample_hits())
    async with Client(mcp_server.mcp, mode="legacy", read_timeout_seconds=5) as client:
        result = await client.call_tool("search_knowledge", {"query": "heavy scalar", "limit": 1})
    assert result.is_error is False
    assert result.structured_content["query"] == "heavy scalar"
    assert result.structured_content["sources"][0]["id"] == "S1"


@pytest.mark.anyio
async def test_mcp_graph_tools_return_structured_results(monkeypatch):
    monkeypatch.setattr(mcp_server, "_graph", sample_graph)
    async with Client(mcp_server.mcp, mode="legacy", read_timeout_seconds=5) as client:
        related = await client.call_tool("find_related_papers", {"query": "a"})
        explanation = await client.call_tool(
            "explain_relationship", {"left": "a", "right": "b"}
        )
        path = await client.call_tool(
            "find_citation_path", {"source": "a", "target": "c"}
        )
        bridges = await client.call_tool(
            "find_bridge_papers", {"left": "a", "right": "c"}
        )
        manuscript = await client.call_tool(
            "papers_relevant_to_manuscript", {"manuscript": "draft"}
        )
    assert related.structured_content["papers"][0]["paper"]["id"] == "paper:b"
    assert explanation.structured_content["connected"] is True
    assert path.structured_content["hops"] == 2
    assert bridges.structured_content["bridges"][0]["paper"]["id"] == "paper:b"
    assert manuscript.structured_content["papers"][0]["paper"]["id"] == "paper:b"
