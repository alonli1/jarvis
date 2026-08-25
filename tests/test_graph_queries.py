import pytest

from jarvis.graph_queries import (
    bridge_papers,
    citation_path,
    explain_relationship,
    manuscript_papers,
    related_papers,
)


@pytest.fixture
def graph():
    nodes = [
        {"id": "paper:a", "kind": "paper", "title": "A"},
        {"id": "paper:b", "kind": "paper", "title": "B"},
        {"id": "paper:c", "kind": "paper", "title": "C"},
        {
            "id": "manuscript:draft",
            "kind": "manuscript",
            "title": "Draft",
        },
    ]
    edges = [
        {"source": "paper:a", "target": "paper:b", "kind": "cites", "score": 1.0},
        {"source": "paper:b", "target": "paper:c", "kind": "cites", "score": 1.0},
        {
            "source": "paper:a",
            "target": "paper:c",
            "kind": "similar",
            "score": 0.5,
            "shared_tags": ["gravity"],
        },
        {
            "source": "manuscript:draft",
            "target": "paper:b",
            "kind": "relevant_to_manuscript",
            "score": 0.8,
            "shared_tags": ["gravity"],
        },
    ]
    return {"nodes": nodes, "edges": edges}


def test_related_and_relationship_explanation(graph):
    related = related_papers(graph, "a")
    assert [item["paper"]["id"] for item in related["papers"]] == ["paper:b", "paper:c"]
    explanation = explain_relationship(graph, "a", "c")
    assert explanation["connected"] is True
    assert "gravity" in explanation["explanation"]


def test_citation_path_and_bridge_papers(graph):
    path = citation_path(graph, "a", "c")
    assert [node["id"] for node in path["path"]] == ["paper:a", "paper:b", "paper:c"]
    assert bridge_papers(graph, "a", "c")["bridges"][0]["paper"]["id"] == "paper:b"


def test_manuscript_relevance(graph):
    result = manuscript_papers(graph, "draft")
    assert result["papers"][0]["paper"]["id"] == "paper:b"
