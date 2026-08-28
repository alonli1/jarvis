import json
from dataclasses import replace

from jarvis.config import load_config
from jarvis.models import Chunk, SearchHit
from jarvis.workflows import execute_computation, handoff, prepare_computation, prepare_literature


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
    monkeypatch.setattr("jarvis.workflows.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(cfg, "Check a symbolic identity", "python")
    script = bundle.path / "scripts/main.py"
    script.write_text("print('checked')\n")

    code, log = execute_computation(cfg, bundle.id, script)
    manifest = json.loads((bundle.path / "manifest.json").read_text())

    assert code == 0
    assert "checked" in log.read_text()
    assert manifest["status"] == "executed"
