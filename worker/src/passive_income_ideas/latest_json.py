from __future__ import annotations

import json
from pathlib import Path

from .config import repo_root, worker_root
from .memory import snapshot_to_public_dict
from .models import IdeaSnapshot


def write_latest(snapshot: IdeaSnapshot) -> tuple[Path, Path]:
    """Write dated + latest JSON under worker/output and copy to public/data for the UI."""
    payload = snapshot_to_public_dict(snapshot)
    text = json.dumps(payload, ensure_ascii=False, indent=2)

    out_dir = worker_root() / "output" / "json"
    out_dir.mkdir(parents=True, exist_ok=True)
    dated = out_dir / f"{snapshot.report_date}.json"
    latest = out_dir / "latest.json"
    dated.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")

    public_dir = repo_root() / "public" / "data"
    public_dir.mkdir(parents=True, exist_ok=True)
    public_latest = public_dir / "latest-idea.json"
    public_latest.write_text(text, encoding="utf-8")
    return latest, public_latest
