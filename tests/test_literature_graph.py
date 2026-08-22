import yaml

from jarvis.graph_view import render_graph_html
from jarvis.literature_graph import build_graph, find_node, render_graph_markdown


def test_graph_connects_manuscript_to_relevant_paper(tmp_path):
    (tmp_path / "topics").mkdir()
    (tmp_path / "topics" / "taxonomy.yaml").write_text(
        yaml.safe_dump(
            {
                "research_tags": {
                    "gravitational_eft": {
                        "all": ["gravity", "eft"],
                        "phrases": ["gravitational eft"],
                    }
                }
            }
        )
    )
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "knowledge" / "references.yaml").write_text(
        yaml.safe_dump(
            {
                "references": [
                    {
                        "id": "gravity-paper",
                        "title": "Gravity as an EFT",
                        "topics": ["gravity", "eft"],
                    }
                ]
            }
        )
    )
    project = tmp_path / "group" / "manuscripts" / "draft"
    project.mkdir(parents=True)
    (project / "novelty.yaml").write_text(
        yaml.safe_dump(
            {
                "project": "draft",
                "claims": [
                    {
                        "id": "D-1",
                        "claim": "A gravitational EFT result",
                        "keywords": [],
                    }
                ],
            }
        )
    )

    graph = build_graph(tmp_path)
    manuscript = find_node(graph, "draft")
    edge = next(edge for edge in graph["edges"] if edge["source"] == manuscript["id"])
    assert edge["target"] == "paper:gravity-paper"
    assert edge["shared_tags"] == ["gravitational_eft"]
    assert "```mermaid" in render_graph_markdown(graph, manuscript)
    html = render_graph_html(graph, manuscript)
    assert "<canvas" in html
    assert "https://cdn" not in html


def test_graph_uses_synced_citations_and_shared_references(tmp_path):
    (tmp_path / "topics").mkdir()
    (tmp_path / "topics" / "taxonomy.yaml").write_text("research_tags: {}\n")
    (tmp_path / "knowledge").mkdir()
    references = [
        {"id": "a", "title": "A", "topics": [], "arxiv": "2401.00001"},
        {"id": "b", "title": "B", "topics": [], "arxiv": "2401.00002"},
        {"id": "c", "title": "C", "topics": [], "arxiv": "2401.00003"},
    ]
    (tmp_path / "knowledge" / "references.yaml").write_text(
        yaml.safe_dump({"references": references})
    )
    (tmp_path / "literature").mkdir()
    (tmp_path / "literature" / "citations.yaml").write_text(
        yaml.safe_dump(
            {
                "papers": {
                    "a": {"references": ["arxiv:2401.00002", "x", "y"]},
                    "b": {"references": ["x", "y", "z"]},
                    "c": {"references": ["x", "y"]},
                }
            }
        )
    )
    (tmp_path / "group" / "manuscripts").mkdir(parents=True)

    graph = build_graph(tmp_path)
    kinds = {(edge["source"], edge["target"], edge["kind"]) for edge in graph["edges"]}
    assert ("paper:a", "paper:b", "cites") in kinds
    assert ("paper:a", "paper:c", "bibliographic_coupling") in kinds
