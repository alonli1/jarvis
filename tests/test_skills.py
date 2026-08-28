from pathlib import Path

import yaml


def test_exactly_four_foundational_agent_skills_exist():
    root = Path(__file__).parents[1]
    skills = root / ".agents/skills"
    expected = {
        "library-management",
        "literature-understanding",
        "research-ideation",
        "reproducible-computation",
    }
    assert {path.name for path in skills.iterdir() if path.is_dir()} == expected
    for name in expected:
        text = (skills / name / "SKILL.md").read_text()
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        assert frontmatter["name"] == name
        assert frontmatter["description"]


def test_literature_surveillance_is_a_mode_not_a_fifth_skill():
    root = Path(__file__).parents[1]
    skill = root / ".agents/skills/literature-understanding"
    instructions = (skill / "SKILL.md").read_text()
    mode = skill / "references/literature-surveillance.md"

    assert mode.exists()
    assert "references/literature-surveillance.md" in instructions
    assert "Do not open a GitHub issue automatically" in " ".join(mode.read_text().split())
