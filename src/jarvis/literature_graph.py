from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from .taxonomy import classify_tags, load_taxonomy, normalize_tag


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _similarity(left: set[str], right: set[str]) -> tuple[float, list[str]]:
    shared = sorted(left & right)
    return (len(shared) / len(left | right) if shared else 0.0), shared


def _paper_nodes(root: Path, taxonomy: dict[str, dict]) -> list[dict]:
    references = _load_yaml(root / "knowledge" / "references.yaml").get("references", [])
    nodes = []
    for reference in references:
        topics = [normalize_tag(str(tag)) for tag in reference.get("topics", [])]
        research_tags = classify_tags(topics, taxonomy)
        nodes.append(
            {
                "id": f"paper:{reference['id']}",
                "kind": "paper",
                "title": reference["title"],
                "year": reference.get("year"),
                "tier": reference.get("tier"),
                "topics": topics,
                "tags": research_tags,
                "url": reference.get("url"),
            }
        )
    return nodes


def _manuscript_nodes(root: Path, taxonomy: dict[str, dict]) -> list[dict]:
    nodes = []
    for path in sorted((root / "group" / "manuscripts").glob("*/novelty.yaml")):
        data = _load_yaml(path)
        claims = data.get("claims", [])
        text = " ".join(
            [str(data.get("description", ""))]
            + [str(claim.get("claim", "")) for claim in claims]
            + [str(keyword) for claim in claims for keyword in claim.get("keywords", [])]
        )
        explicit = [normalize_tag(str(tag)) for tag in data.get("tags", [])]
        tags = list(dict.fromkeys(explicit + classify_tags([], taxonomy, text)))
        nodes.append(
            {
                "id": f"manuscript:{data.get('project', path.parent.name)}",
                "kind": "manuscript",
                "title": data.get("project", path.parent.name),
                "topics": [],
                "tags": tags,
                "claim_ids": [claim.get("id") for claim in claims],
                "path": str(path.relative_to(root)),
            }
        )
    return nodes


def build_graph(root: Path, neighbors: int = 8) -> dict:
    taxonomy = load_taxonomy(root)
    papers = _paper_nodes(root, taxonomy)
    manuscripts = _manuscript_nodes(root, taxonomy)
    candidates: list[dict] = []

    # honey: O(n^2) is simpler and fast for the curated corpus; revisit above 1,000 papers.
    for index, left in enumerate(papers):
        for right in papers[index + 1 :]:
            tag_score, shared_tags = _similarity(set(left["tags"]), set(right["tags"]))
            topic_score, shared_topics = _similarity(set(left["topics"]), set(right["topics"]))
            score = 0.75 * tag_score + 0.25 * topic_score
            if score:
                candidates.append(
                    {
                        "source": left["id"],
                        "target": right["id"],
                        "kind": "similar",
                        "score": round(score, 4),
                        "shared_tags": shared_tags,
                        "shared_topics": shared_topics,
                    }
                )

    kept: set[tuple[str, str]] = set()
    for node in papers:
        adjacent = [
            edge
            for edge in candidates
            if node["id"] in {edge["source"], edge["target"]}
        ]
        for edge in sorted(adjacent, key=lambda item: item["score"], reverse=True)[:neighbors]:
            kept.add((edge["source"], edge["target"]))
    edges = [edge for edge in candidates if (edge["source"], edge["target"]) in kept]

    for manuscript in manuscripts:
        manuscript_tags = set(manuscript["tags"])
        matches = []
        for paper in papers:
            shared = sorted(manuscript_tags & set(paper["tags"]))
            if shared:
                matches.append(
                    {
                        "source": manuscript["id"],
                        "target": paper["id"],
                        "kind": "relevant_to_manuscript",
                        "score": round(len(shared) / len(manuscript_tags), 4),
                        "shared_tags": shared,
                        "shared_topics": [],
                    }
                )
        ranked = sorted(matches, key=lambda item: item["score"], reverse=True)
        selected: list[dict] = []
        for tag in manuscript["tags"]:
            match = next(
                (
                    edge
                    for edge in ranked
                    if tag in edge["shared_tags"] and edge not in selected
                ),
                None,
            )
            if match:
                selected.append(match)
        selected.extend(edge for edge in ranked if edge not in selected)
        edges.extend(selected[:neighbors])

    references = _load_yaml(root / "knowledge" / "references.yaml").get("references", [])
    known = {reference["id"] for reference in references}
    for reference in references:
        for cited in reference.get("cites", []):
            if cited in known:
                edges.append(
                    {
                        "source": f"paper:{reference['id']}",
                        "target": f"paper:{cited}",
                        "kind": "cites",
                        "score": 1.0,
                        "shared_tags": [],
                        "shared_topics": [],
                    }
                )

    return {
        "version": 1,
        "method": "controlled-tag similarity plus explicit citations",
        "nodes": papers + manuscripts,
        "edges": edges,
    }


def save_graph(root: Path, graph: dict) -> Path:
    path = root / ".jarvis" / "literature_graph.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    return path


def find_node(graph: dict, query: str) -> dict:
    needle = query.lower()
    exact = [
        node
        for node in graph["nodes"]
        if needle in {node["id"].lower(), node["id"].split(":", 1)[-1].lower()}
    ]
    if len(exact) == 1:
        return exact[0]
    matches = [node for node in graph["nodes"] if needle in node["title"].lower()]
    if len(matches) != 1:
        choices = ", ".join(node["id"] for node in (matches or exact)[:8])
        raise ValueError(f"Graph query matched {len(matches or exact)} nodes" + (f": {choices}" if choices else ""))
    return matches[0]


def neighborhood(graph: dict, node_id: str, limit: int = 12) -> list[tuple[dict, dict]]:
    nodes = {node["id"]: node for node in graph["nodes"]}
    related = []
    for edge in graph["edges"]:
        if node_id == edge["source"]:
            related.append((edge, nodes[edge["target"]]))
        elif node_id == edge["target"]:
            related.append((edge, nodes[edge["source"]]))
    return sorted(related, key=lambda item: item[0]["score"], reverse=True)[:limit]


def render_graph_markdown(graph: dict, origin: dict, limit: int = 12) -> str:
    related = neighborhood(graph, origin["id"], limit)
    lines = [f"# Literature graph: {origin['title']}", "", "```mermaid", "graph LR"]
    labels = [(origin, "n0")] + [(node, f"n{index}") for index, (_, node) in enumerate(related, 1)]
    for node, mermaid_id in labels:
        title = re.sub(r'["\n]+', " ", node["title"])
        shape = f'{{{{"{title}"}}}}' if node["kind"] == "manuscript" else f'["{title}"]'
        lines.append(f"  {mermaid_id}{shape}")
    for index, (edge, _) in enumerate(related, 1):
        label = edge["kind"].replace("_", " ") + f" {edge['score']:.2f}"
        lines.append(f'  n0 ---|"{label}"| n{index}')
    lines += ["```", "", "| Related work | Relationship | Score | Shared research tags |", "|---|---:|---:|---|"]
    for edge, node in related:
        lines.append(
            f"| {node['title']} | {edge['kind']} | {edge['score']:.2f} | "
            f"{', '.join(edge['shared_tags']) or '—'} |"
        )
    lines += ["", "Scores describe this curated local corpus, not global scholarly importance.", ""]
    return "\n".join(lines)
