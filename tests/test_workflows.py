import hashlib
import json
import zipfile
from dataclasses import replace

import pytest

from jarvis.config import load_config
from jarvis.models import Chunk, ModelUsage, SearchHit
from jarvis.workflows import (
    execute_computation,
    handoff,
    import_provisional_artifact,
    prepare_computation,
    prepare_literature,
    record_model_usage,
)


def config_for(tmp_path):
    source = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages/registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    ecosystem: python\n    executable: python\n"
        "    package: sympy\n    purpose: checks\n    related_topics: []\n"
    )
    skill = tmp_path / ".agents/skills/literature-understanding"
    skill.mkdir(parents=True)
    skill.joinpath("SKILL.md").write_text(
        "---\nname: literature-understanding\ndescription: Test.\n---\nUse evidence.\n"
    )
    return replace(source, root=tmp_path)


def test_literature_run_and_browser_handoff_are_grounded(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    hits = [
        SearchHit(
            chunk=Chunk(id="c1", text="A supported result.", source_path="paper.pdf", page=7),
            score=0.9,
        )
    ]
    monkeypatch.setattr("jarvis.workflows.retrieve_hits", lambda *args, **kwargs: hits)

    bundle = prepare_literature(cfg, "What is supported?")
    manifest = json.loads((bundle.path / "manifest.json").read_text())
    export = handoff(cfg, bundle.id)

    assert manifest["citations"][0]["page"] == 7
    assert "untrusted evidence" in (bundle.path / "evidence.md").read_text()
    assert "[S1] paper.pdf, p. 7" in export.read_text()


def test_python_computation_requires_explicit_execution_and_records_log(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(cfg, "Check a symbolic identity", "python")
    script = bundle.path / "scripts/main.py"
    script.write_text("print('checked')\n")

    code, log = execute_computation(cfg, bundle.id, script)
    manifest = json.loads((bundle.path / "manifest.json").read_text())

    assert code == 0
    assert "checked" in log.read_text()
    assert manifest["status"] == "executed"


def test_imported_provisional_artifact_is_copied_and_in_zip_handoff(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.workflows.retrieve_hits", lambda *args, **kwargs: [])
    bundle = prepare_literature(cfg, "Question")
    source = tmp_path / "external.txt"
    source.write_text("untrusted evidence\n", encoding="utf-8")

    artifact = import_provisional_artifact(
        cfg, bundle.id, source, "external note", "ART-1", "draft"
    )
    manifest = json.loads((bundle.path / "manifest.json").read_text())
    export = handoff(cfg, bundle.id, "zip")
    markdown = handoff(cfg, bundle.id)

    assert (bundle.path / artifact.path).read_text() == "untrusted evidence\n"
    assert artifact.sha256 == hashlib.sha256(source.read_bytes()).hexdigest()
    assert manifest["provisional_artifacts"] == [artifact.model_dump(mode="json")]
    assert artifact.path in manifest["artifacts"]
    with zipfile.ZipFile(export) as archive:
        assert artifact.path in archive.namelist()
        assert archive.read(artifact.path) == source.read_bytes()
    assert "Provisional artifacts" in markdown.read_text()


def test_invalid_provisional_imports_do_not_modify_run(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.workflows.retrieve_hits", lambda *args, **kwargs: [])
    bundle = prepare_literature(cfg, "Question")
    source = tmp_path / "external.txt"
    source.write_text("evidence\n", encoding="utf-8")
    manifest_path = bundle.path / "manifest.json"
    before = manifest_path.read_bytes()
    link = tmp_path / "external-link.txt"
    link.symlink_to(source)

    with pytest.raises(ValueError, match="regular file"):
        import_provisional_artifact(cfg, bundle.id, link, "external", "ART-1")
    assert manifest_path.read_bytes() == before
    with pytest.raises(ValueError, match="single path component"):
        import_provisional_artifact(cfg, bundle.id, source, "external", "../escape")
    with pytest.raises(ValueError, match="not a path"):
        import_provisional_artifact(cfg, bundle.id, source, "/external", "ART-1")
    assert manifest_path.read_bytes() == before
    artifact = import_provisional_artifact(cfg, bundle.id, source, "external", "ART-1")
    after = manifest_path.read_bytes()
    with pytest.raises(ValueError, match="already exists"):
        import_provisional_artifact(cfg, bundle.id, source, "external", artifact.id)
    assert manifest_path.read_bytes() == after


def test_imports_and_usage_require_manifest_v2(tmp_path):
    cfg = config_for(tmp_path)
    run = cfg.root / ".jarvis" / "runs" / "legacy"
    run.mkdir(parents=True)
    manifest_path = run / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "version": 1,
                "id": "legacy",
                "workflow": "literature",
                "query": "Question",
                "created_at": "2026-08-29T00:00:00+00:00",
                "corpus_revision": "sha256:test",
                "status": "prepared",
                "inputs": [],
                "citations": [],
                "tools": [],
                "artifacts": [],
            }
        ),
        encoding="utf-8",
    )
    source = tmp_path / "external.txt"
    source.write_text("evidence\n", encoding="utf-8")
    before = manifest_path.read_bytes()

    with pytest.raises(ValueError, match="Manifest v2"):
        import_provisional_artifact(cfg, "legacy", source, "external", "ART-1")
    with pytest.raises(ValueError, match="Manifest v2"):
        record_model_usage(cfg, "legacy", ModelUsage(provider="local", model="test"))
    assert manifest_path.read_bytes() == before


def test_role_tagged_model_usage_is_persisted(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.workflows.retrieve_hits", lambda *args, **kwargs: [])
    bundle = prepare_literature(cfg, "Question")

    record_model_usage(cfg, bundle.id, ModelUsage(provider="local", model="test", role="drafting"))

    manifest = json.loads((bundle.path / "manifest.json").read_text())
    assert manifest["model_usage"] == [
        {
            "provider": "local",
            "model": "test",
            "role": "drafting",
            "input_tokens": None,
            "output_tokens": None,
            "latency_ms": None,
            "estimated_cost": None,
        }
    ]
