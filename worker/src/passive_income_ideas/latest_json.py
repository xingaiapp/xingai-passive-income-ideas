from __future__ import annotations

import json
import shutil
from pathlib import Path

from .config import repo_root, worker_root
from .memory import snapshot_to_public_dict
from .models import IdeaSnapshot
from .pdf_report import pdf_filename


def _update_archive_index(public_dir: Path, snapshot: IdeaSnapshot, payload: dict) -> Path:
    index_path = public_dir / "archive-index.json"
    items: list[dict] = []
    if index_path.exists():
        try:
            raw = json.loads(index_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict) and isinstance(raw.get("items"), list):
                items = [x for x in raw["items"] if isinstance(x, dict)]
        except (json.JSONDecodeError, OSError):
            items = []

    entry = {
        "report_date": snapshot.report_date,
        "idea_id": snapshot.idea_id,
        "idea_name": snapshot.idea_name,
        "one_liner": snapshot.one_liner,
        "continuity": snapshot.continuity,
        "income_kind": snapshot.income_kind,
        "is_mock": snapshot.is_mock,
        "json_url": f"/data/ideas/{snapshot.report_date}.json",
        "pdf_url": payload.get("pdf_url") or "",
        "locales": {
            lang: {
                "idea_name": pack.get("idea_name"),
                "one_liner": pack.get("one_liner"),
            }
            for lang, pack in (snapshot.locales or {}).items()
            if isinstance(pack, dict)
        },
    }
    items = [x for x in items if x.get("report_date") != snapshot.report_date]
    items.append(entry)
    items.sort(key=lambda x: str(x.get("report_date") or ""), reverse=True)

    out = {"updated_at": snapshot.generated_at, "items": items}
    index_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return index_path


def write_latest(snapshot: IdeaSnapshot, pdf_path: Path | None = None) -> tuple[Path, Path]:
    """Write dated + latest JSON under worker/output and publish UI artifacts under public/."""
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
    ideas_dir = public_dir / "ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)

    public_latest = public_dir / "latest-idea.json"
    public_latest.write_text(text, encoding="utf-8")
    (ideas_dir / f"{snapshot.report_date}.json").write_text(text, encoding="utf-8")
    _update_archive_index(public_dir, snapshot, payload)

    if pdf_path and pdf_path.is_file():
        reports = repo_root() / "public" / "reports"
        reports.mkdir(parents=True, exist_ok=True)
        dest = reports / pdf_filename(snapshot)
        shutil.copy2(pdf_path, dest)

    return latest, public_latest
