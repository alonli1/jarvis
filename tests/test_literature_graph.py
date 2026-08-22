import yaml

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
