from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field


class EquationMapEntry(BaseModel):
    label: str
    locator: str
    expression: str
    conventions: dict[str, str] = Field(default_factory=dict)


class PaperSpecification(BaseModel):
    paper_id: str
    source_path: str
    source_locator: str
    target_result: str
    equations: list[EquationMapEntry] = Field(min_length=1)
    assumptions: list[str] = Field(default_factory=list)


class ImplementationSpecification(BaseModel):
    paper: PaperSpecification
    engine: str
    scripts: list[str] = Field(min_length=1)
    checks: list[str] = Field(min_length=1)


def load_paper_specification(path: Path) -> PaperSpecification:
    return PaperSpecification.model_validate_json(path.read_text(encoding="utf-8"))


def write_reproduction_report(spec: ImplementationSpecification, run_id: str, output: Path) -> Path:
    lines = [
        "# Reproduction report",
        "",
        f"**Run:** `{run_id}`",
        f"**Paper source:** `{spec.paper.source_path}`, {spec.paper.source_locator}",
        f"**Target:** {spec.paper.target_result}",
        f"**Engine:** {spec.engine}",
        "",
        "## Equation and convention map",
        "",
    ]
    for equation in spec.paper.equations:
        lines += [f"- **{equation.label}** ({equation.locator}): `{equation.expression}`"]
        lines += [f"  - {key}: {value}" for key, value in sorted(equation.conventions.items())]
    lines += ["", "## Assumptions", "", *(f"- {item}" for item in spec.paper.assumptions)]
    lines += ["", "## Implementation", "", *(f"- `{item}`" for item in spec.scripts)]
    lines += ["", "## Required checks", "", *(f"- {item}" for item in spec.checks)]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def dump_paper_specification(spec: PaperSpecification, output: Path) -> Path:
    output.write_text(
        json.dumps(spec.model_dump(mode="json"), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return output
