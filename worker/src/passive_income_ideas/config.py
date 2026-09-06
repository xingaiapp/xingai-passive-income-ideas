from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .models import OperatorProfile

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore


def worker_root() -> Path:
    return Path(__file__).resolve().parents[2]


def config_dir() -> Path:
    override = (os.environ.get("PASSIVE_INCOME_CONFIG_DIR") or "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return worker_root() / "config"


def data_dir() -> Path:
    override = (os.environ.get("PASSIVE_INCOME_DATA_DIR") or "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return worker_root() / "data"


def repo_root() -> Path:
    return worker_root().parent


@dataclass(frozen=True)
class ResearchSettings:
    mode: str  # live | mock
    continuity_days: int
    min_jaccard_new: float


@dataclass(frozen=True)
class AppConfig:
    profile: OperatorProfile
    research: ResearchSettings
    raw: dict[str, Any]


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install pyyaml")
    if not path.exists():
        raise FileNotFoundError(f"missing config: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config must be a mapping: {path}")
    return data


def load_operator_profile(path: Path | None = None) -> OperatorProfile:
    cfg = _load_yaml(path or (config_dir() / "operator_profile.yaml"))
    op = cfg.get("operator") or {}
    skills = tuple(str(x) for x in (op.get("skills") or ()))
    constraints = tuple(str(x) for x in (op.get("constraints") or ()))
    return OperatorProfile(
        age=int(op.get("age") or 0),
        location=str(op.get("location") or ""),
        background=str(op.get("background") or ""),
        goals=str(op.get("goals") or ""),
        constraints=constraints,
        skills=skills,
        name=str(op.get("name") or ""),
        locale=str(op.get("locale") or "zh-CN"),
        timezone=str(op.get("timezone") or "America/Chicago"),
    )


def load_app_config(path: Path | None = None) -> AppConfig:
    cfg_path = path or (config_dir() / "operator_profile.yaml")
    raw = _load_yaml(cfg_path)
    profile = load_operator_profile(cfg_path)
    research = raw.get("research") or {}
    settings = ResearchSettings(
        mode=str(research.get("mode") or "live").strip().lower(),
        continuity_days=int(research.get("continuity_days") or 7),
        min_jaccard_new=float(research.get("min_jaccard_new") or 0.35),
    )
    return AppConfig(profile=profile, research=settings, raw=raw)


def load_idea_catalog(path: Path | None = None) -> list[dict[str, Any]]:
    data = _load_yaml(path or (config_dir() / "idea_catalog.yaml"))
    ideas = data.get("ideas") or []
    if not isinstance(ideas, list) or not ideas:
        raise ValueError("idea_catalog.yaml must contain a non-empty ideas list")
    return [x for x in ideas if isinstance(x, dict)]
