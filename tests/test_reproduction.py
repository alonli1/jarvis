from jarvis.reproduction import (
    EquationMapEntry,
    ImplementationSpecification,
    PaperSpecification,
    dump_paper_specification,
    load_paper_specification,
    write_reproduction_report,
)


def test_reproduction_specification_preserves_equation_locator_and_conventions(tmp_path):
    paper = PaperSpecification(
        paper_id="arxiv:example",
        source_path="knowledge/papers/example.pdf",
        source_locator="p. 7, Eq. 19",
        target_result="A bounded identity",
        equations=[
            EquationMapEntry(
                label="E1",
                locator="p. 7, Eq. 19",
                expression="x=y",
                conventions={"units": "natural"},
            )
        ],
    )
    spec_path = dump_paper_specification(paper, tmp_path / "spec.json")
    spec = ImplementationSpecification(
        paper=load_paper_specification(spec_path),
        engine="python",
        scripts=["scripts/main.py"],
        checks=["symbolic identity"],
    )
    report = write_reproduction_report(spec, "run-1", tmp_path / "report.md")

    assert "knowledge/papers/example.pdf" in report.read_text()
    assert "p. 7, Eq. 19" in report.read_text()
