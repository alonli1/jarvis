from __future__ import annotations

from collections import deque

from .literature_graph import find_node
from .models import Visibility

RELATIONSHIPS = {
    "cites",
    "bibliographic_coupling",
    "similar",
    "relevant_to_manuscript",
}


def filter_graph_visibility(graph: dict, max_visibility: str) -> dict:
    maximum = Visibility.parse(max_visibility)
    nodes = [
        node
        for node in graph["nodes"]
        if Visibility.parse(node.get("visibility", "public")) <= maximum
    ]
    visible = {node["id"] for node in nodes}
    return {
        **graph,
        "nodes": nodes,
        "edges": [
            edge
            for edge in graph["edges"]
            if edge["source"] in visible and edge["target"] in visible
        ],
    }


def node_summary(node: dict) -> dict:
    return {
        key: node[key]
        for key in (
            "id",
            "kind",
            "title",
            "year",
            "tier",
            "topics",
            "tags",
            "url",
            "citation_count",
            "corpus_citation_count",
            "reference_count",
            "claim_ids",
            "path",
        )
        if node.get(key) is not None
    }


def _edge_summary(edge: dict, origin_id: str) -> dict:
    direction = "outgoing" if edge["source"] == origin_id else "incoming"
    return {
        "kind": edge["kind"],
        "direction": direction,
        "score": edge["score"],
        **{
            key: edge[key]
            for key in ("shared_tags", "shared_topics", "shared_references")
            if edge.get(key)
        },
    }


def _relationship_filter(relationship_types: list[str] | None) -> set[str]:
    selected = set(relationship_types or RELATIONSHIPS)
    unknown = selected - RELATIONSHIPS
    if unknown:
        raise ValueError(f"Unknown relationship types: {', '.join(sorted(unknown))}")
    return selected


def related_papers(
    graph: dict,
    query: str,
    limit: int = 10,
    relationship_types: list[str] | None = None,
) -> dict:
    origin = find_node(graph, query)
    nodes = {node["id"]: node for node in graph["nodes"]}
    selected = _relationship_filter(relationship_types)
    grouped: dict[str, list[dict]] = {}
    for edge in graph["edges"]:
        if edge["kind"] not in selected or origin["id"] not in {
            edge["source"],
            edge["target"],
        }:
            continue
        other_id = edge["target"] if edge["source"] == origin["id"] else edge["source"]
        if nodes[other_id]["kind"] == "paper":
            grouped.setdefault(other_id, []).append(_edge_summary(edge, origin["id"]))
    papers = [
        {
            "paper": node_summary(nodes[node_id]),
            "score": max(item["score"] for item in relationships),
            "relationships": sorted(
                relationships, key=lambda item: item["score"], reverse=True
            ),
        }
        for node_id, relationships in grouped.items()
    ]
    papers.sort(key=lambda item: (item["score"], item["paper"]["title"]), reverse=True)
    return {"origin": node_summary(origin), "papers": papers[:limit]}


def explain_relationship(graph: dict, left_query: str, right_query: str) -> dict:
    left, right = find_node(graph, left_query), find_node(graph, right_query)
    relationships = []
    explanations = []
    for edge in graph["edges"]:
        if {edge["source"], edge["target"]} != {left["id"], right["id"]}:
            continue
        relationships.append(_edge_summary(edge, left["id"]))
        if edge["kind"] == "cites":
            source = left if edge["source"] == left["id"] else right
            target = right if source is left else left
            explanations.append(f"{source['title']} cites {target['title']}.")
        elif edge["kind"] == "bibliographic_coupling":
            explanations.append(
                f"They share {edge.get('shared_references', 0)} resolved references."
            )
        elif edge["kind"] == "similar":
            evidence = edge.get("shared_tags") or edge.get("shared_topics") or []
            explanations.append(
                "They overlap through " + ", ".join(evidence) + "."
            )
        else:
            explanations.append(
                "The manuscript and paper share "
                + ", ".join(edge.get("shared_tags", []))
                + "."
            )
    return {
        "left": node_summary(left),
        "right": node_summary(right),
        "connected": bool(relationships),
        "explanation": " ".join(explanations) or "No direct relationship is recorded.",
        "relationships": relationships,
    }


def citation_path(graph: dict, source_query: str, target_query: str, max_hops: int = 6) -> dict:
    source, target = find_node(graph, source_query), find_node(graph, target_query)
    nodes = {node["id"]: node for node in graph["nodes"]}
    adjacency: dict[str, list[str]] = {}
    for edge in graph["edges"]:
        if edge["kind"] == "cites":
            adjacency.setdefault(edge["source"], []).append(edge["target"])
    queue = deque([(source["id"], [source["id"]])])
    visited = {source["id"]}
    path: list[str] | None = None
    while queue:
        current, current_path = queue.popleft()
        if current == target["id"]:
            path = current_path
            break
        if len(current_path) - 1 >= max_hops:
            continue
        for neighbor in adjacency.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, current_path + [neighbor]))
    return {
        "source": node_summary(source),
        "target": node_summary(target),
        "found": path is not None,
        "hops": len(path) - 1 if path else None,
        "path": [node_summary(nodes[node_id]) for node_id in path or []],
    }


def bridge_papers(graph: dict, left_query: str, right_query: str, limit: int = 10) -> dict:
    left, right = find_node(graph, left_query), find_node(graph, right_query)
    nodes = {node["id"]: node for node in graph["nodes"]}

    def adjacent(node_id: str) -> dict[str, list[dict]]:
        result: dict[str, list[dict]] = {}
        for edge in graph["edges"]:
            if node_id not in {edge["source"], edge["target"]}:
                continue
            other = edge["target"] if edge["source"] == node_id else edge["source"]
            result.setdefault(other, []).append(_edge_summary(edge, node_id))
        return result

    left_neighbors, right_neighbors = adjacent(left["id"]), adjacent(right["id"])
    bridges = []
    for node_id in left_neighbors.keys() & right_neighbors.keys():
        if nodes[node_id]["kind"] != "paper":
            continue
        left_score = max(edge["score"] for edge in left_neighbors[node_id])
        right_score = max(edge["score"] for edge in right_neighbors[node_id])
        bridges.append(
            {
                "paper": node_summary(nodes[node_id]),
                "score": round((left_score + right_score) / 2, 4),
                "to_left": left_neighbors[node_id],
                "to_right": right_neighbors[node_id],
            }
        )
    bridges.sort(key=lambda item: (item["score"], item["paper"]["title"]), reverse=True)
    return {
        "left": node_summary(left),
        "right": node_summary(right),
        "bridges": bridges[:limit],
    }


def manuscript_papers(graph: dict, manuscript_query: str, limit: int = 10) -> dict:
    manuscript = find_node(graph, manuscript_query)
    if manuscript["kind"] != "manuscript":
        raise ValueError(f"{manuscript['id']} is not a manuscript")
    result = related_papers(
        graph,
        manuscript["id"],
        limit=limit,
        relationship_types=["relevant_to_manuscript"],
    )
    return {"manuscript": result["origin"], "papers": result["papers"]}
