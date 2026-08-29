from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class AssistantConfig:
    name: str
    default_model: str
    max_context_chunks: int
    profiles: dict[str, ModelProfile] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelProfile:
    name: str
    provider: str
    model: str
    capability: str


@dataclass(frozen=True)
class IndexConfig:
    mode: str
    path: str
    url: str
    collection: str
    dense_model: str
    sparse_model: str
    dense_limit: int
    sparse_limit: int


@dataclass(frozen=True)
class RetrievalConfig:
    chunk_chars: int
    chunk_overlap: int
    final_k: int


@dataclass(frozen=True)
class LiteratureConfig:
    default_days: int
    max_results_per_query: int
    user_agent: str


@dataclass(frozen=True)
class NoveltyConfig:
    medium_threshold: float
    high_threshold: float
    critical_threshold: float


@dataclass(frozen=True)
class DropboxConfig:
    app_key: str = ""


@dataclass(frozen=True)
class Config:
    root: Path
    assistant: AssistantConfig
    index: IndexConfig
    retrieval: RetrievalConfig
    literature: LiteratureConfig
    novelty: NoveltyConfig
    dropbox: DropboxConfig


def find_repo_root(start: Path | None = None) -> Path:
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "assistant.toml").exists():
            return candidate
    raise FileNotFoundError("Could not find assistant.toml in this directory or its parents")


def load_config(root: Path | None = None) -> Config:
    root = root or find_repo_root()
    with (root / "assistant.toml").open("rb") as f:
        raw = tomllib.load(f)

    profiles = {}
    for name, values in raw.get("model_profiles", {}).items():
        model = values.get("model") if isinstance(values, dict) else None
        capability = values.get("capability") if isinstance(values, dict) else None
        if not isinstance(model, str) or not model.strip():
            raise ValueError(f"Model profile {name!r} must define a non-empty model")
        if capability not in ("extract", "science_fast", "science_standard", "science_deep", "science_critical"):
            raise ValueError(f"Model profile {name!r} must define a valid capability")
        provider = model.split("/", 1)[0] if "/" in model else "unknown"
        profiles[name] = ModelProfile(
            name=name, provider=provider, model=model, capability=capability
        )

    return Config(
        root=root,
        assistant=AssistantConfig(**raw["assistant"], profiles=profiles),
        index=IndexConfig(**raw["index"]),
        retrieval=RetrievalConfig(**raw["retrieval"]),
        literature=LiteratureConfig(**raw["literature"]),
        novelty=NoveltyConfig(**raw["novelty"]),
        dropbox=DropboxConfig(**raw.get("dropbox", {})),
    )
