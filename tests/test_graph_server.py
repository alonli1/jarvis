import json

import yaml

from jarvis.graph_server import graph_response


def test_live_graph_server_serves_app_and_json(tmp_path):
    (tmp_path / "topics").mkdir()
    (tmp_path / "topics" / "taxonomy.yaml").write_text("research_tags: {}\n")
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "knowledge" / "references.yaml").write_text(
        yaml.safe_dump(
            {"references": [{"id": "paper", "title": "Test Paper", "topics": []}]}
        )
    )
    (tmp_path / "group" / "manuscripts").mkdir(parents=True)
    html_status, _, html_body = graph_response(tmp_path, "/")
    graph_status, _, graph_body = graph_response(tmp_path, "/api/graph")
    health_status, _, health_body = graph_response(tmp_path, "/health")
    graph, health = json.loads(graph_body), json.loads(health_body)
    html = html_body.decode()
    assert (html_status, graph_status, health_status) == (200, 200, 200)
    assert "Jarvis Atlas" in html
    assert 'id="focus"' in html
    assert 'id="tag"' in html
    assert graph["nodes"][0]["id"] == "paper:paper"
    assert health == {"status": "ok"}
