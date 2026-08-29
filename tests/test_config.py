from pathlib import Path

import pytest

from jarvis.config import load_config


def _write_config(tmp_path, profiles: str = "") -> None:
    source = Path(__file__).parents[1] / "assistant.toml"
    text = source.read_text(encoding="utf-8")
    text = text.replace(
        '[model_profiles.local]\nmodel = "ollama/qwen3:14b"\ncapability = "science_fast"\n\n', profiles
    )
    (tmp_path / "assistant.toml").write_text(text, encoding="utf-8")


def test_config_without_profiles_remains_valid(tmp_path):
    _write_config(tmp_path)

    assert load_config(tmp_path).assistant.profiles == {}


def test_model_profile_requires_model_and_infers_provider(tmp_path):
    _write_config(
        tmp_path, '[model_profiles.fast]\nmodel = "openai/gpt-5.6"\ncapability = "science_fast"\n\n'
    )

    profile = load_config(tmp_path).assistant.profiles["fast"]
    assert (profile.name, profile.provider, profile.model, profile.capability) == (
        "fast", "openai", "openai/gpt-5.6", "science_fast"
    )

    _write_config(tmp_path, "[model_profiles.invalid]\n")
    with pytest.raises(ValueError, match="non-empty model"):
        load_config(tmp_path)


def test_duplicate_model_profile_names_are_rejected(tmp_path):
    _write_config(
        tmp_path,
        '[model_profiles.fast]\nmodel = "openai/gpt-5.6"\ncapability = "science_fast"\n\n'
        '[model_profiles.fast]\nmodel = "ollama/qwen3:14b"\ncapability = "extract"\n\n',
    )

    with pytest.raises(Exception, match="Cannot declare"):
        load_config(tmp_path)
