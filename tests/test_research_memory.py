import json

from jarvis.research_memory import build_research_memory, write_research_memory


def test_memory_indexes_persisted_claims_without_mutating_runs(tmp_path):
    manifest_path = tmp_path / ".jarvis" / "runs" / "run-1" / "manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest = {
        "version": 2,
        "id": "run-1",
        "workflow": "computation",
        "query": "q",
        "created_at": "2026-08-31T00:00:00+00:00",
        "corpus_revision": "sha256:test",
        "status": "executed",
        "inputs": [],
        "citations": [],
        "tools": [],
        "artifacts": [],
        "claims": [
            {
                "id": "C1",
                "statement": "x",
                "kind": "computed_result",
                "status": "ai_verified",
                "conventions": {"units": "natural"},
            }
        ],
        "verification": [
            {
                "id": "V1",
                "claim_id": "C1",
                "method": "symbolic",
                "outcome": "passed",
                "artifact": "outputs/x",
                "independent": True,
            }
        ],
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    before = manifest_path.read_bytes()

    records = build_research_memory(tmp_path)
    output = write_research_memory(tmp_path)

    assert records[0]["run_id"] == "run-1"
    assert records[0]["verification_ids"] == ["V1"]
    assert json.loads(output.read_text()) == records
    assert manifest_path.read_bytes() == before
