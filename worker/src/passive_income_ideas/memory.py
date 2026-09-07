from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from .config import data_dir
from .models import IdeaSnapshot


_TOKEN_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def normalize_name(name: str) -> str:
    return " ".join(_TOKEN_RE.findall(name.lower()))


def tokens(name: str) -> set[str]:
    return set(_TOKEN_RE.findall(name.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass(frozen=True)
class IdeaMemoryRow:
    idea_id: str
    idea_name: str
    name_norm: str
    last_seen_date: str
    times_picked: int
    status: str


@dataclass(frozen=True)
class DuplicateHit:
    idea_id: str
    idea_name: str
    score: float


def default_db_path() -> Path:
    return data_dir() / "idea_memory.sqlite"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or default_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    init_schema(conn)
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS ideas (
          idea_id TEXT PRIMARY KEY,
          idea_name TEXT NOT NULL,
          name_norm TEXT NOT NULL,
          keywords TEXT NOT NULL,
          income_kind TEXT NOT NULL,
          first_seen_date TEXT NOT NULL,
          last_seen_date TEXT NOT NULL,
          times_picked INTEGER NOT NULL DEFAULT 1,
          status TEXT NOT NULL DEFAULT 'active',
          stop_reason TEXT,
          last_progress_note TEXT
        );
        CREATE TABLE IF NOT EXISTS idea_days (
          report_date TEXT NOT NULL PRIMARY KEY,
          idea_id TEXT NOT NULL,
          continuity TEXT NOT NULL,
          snapshot_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_ideas_last_seen ON ideas(last_seen_date);
        """
    )
    conn.commit()


def list_recent(conn: sqlite3.Connection, days: int = 90) -> list[IdeaMemoryRow]:
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    rows = conn.execute(
        "SELECT idea_id, idea_name, name_norm, last_seen_date, times_picked, status "
        "FROM ideas WHERE last_seen_date >= ? ORDER BY last_seen_date DESC",
        (cutoff,),
    ).fetchall()
    return [
        IdeaMemoryRow(
            idea_id=r["idea_id"],
            idea_name=r["idea_name"],
            name_norm=r["name_norm"],
            last_seen_date=r["last_seen_date"],
            times_picked=int(r["times_picked"]),
            status=r["status"],
        )
        for r in rows
    ]


def find_duplicate(
    candidate_name: str,
    history: list[IdeaMemoryRow],
    threshold: float,
) -> DuplicateHit | None:
    cand = tokens(candidate_name)
    best: DuplicateHit | None = None
    for row in history:
        if row.status != "active":
            continue
        score = jaccard(cand, tokens(row.idea_name))
        if score >= threshold and (best is None or score > best.score):
            best = DuplicateHit(row.idea_id, row.idea_name, score)
    return best


def recent_pick_for_id(conn: sqlite3.Connection, idea_id: str, within_days: int) -> IdeaMemoryRow | None:
    cutoff = (date.today() - timedelta(days=within_days)).isoformat()
    row = conn.execute(
        "SELECT idea_id, idea_name, name_norm, last_seen_date, times_picked, status "
        "FROM ideas WHERE idea_id = ? AND last_seen_date >= ? AND status = 'active'",
        (idea_id, cutoff),
    ).fetchone()
    if not row:
        return None
    return IdeaMemoryRow(
        idea_id=row["idea_id"],
        idea_name=row["idea_name"],
        name_norm=row["name_norm"],
        last_seen_date=row["last_seen_date"],
        times_picked=int(row["times_picked"]),
        status=row["status"],
    )


def upsert_pick(conn: sqlite3.Connection, snapshot: IdeaSnapshot) -> None:
    day = snapshot.report_date
    existing = conn.execute("SELECT idea_id FROM ideas WHERE idea_id = ?", (snapshot.idea_id,)).fetchone()
    name_norm = normalize_name(snapshot.idea_name)
    keywords = " ".join(sorted(tokens(snapshot.idea_name)))
    if existing:
        conn.execute(
            "UPDATE ideas SET idea_name=?, name_norm=?, keywords=?, income_kind=?, "
            "last_seen_date=?, times_picked=times_picked+1, last_progress_note=? WHERE idea_id=?",
            (
                snapshot.idea_name,
                name_norm,
                keywords,
                snapshot.income_kind,
                day,
                snapshot.do_today,
                snapshot.idea_id,
            ),
        )
    else:
        conn.execute(
            "INSERT INTO ideas (idea_id, idea_name, name_norm, keywords, income_kind, "
            "first_seen_date, last_seen_date, times_picked, status, last_progress_note) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'active', ?)",
            (
                snapshot.idea_id,
                snapshot.idea_name,
                name_norm,
                keywords,
                snapshot.income_kind,
                day,
                day,
                snapshot.do_today,
            ),
        )
    payload = snapshot_to_public_dict(snapshot)
    conn.execute(
        "INSERT INTO idea_days (report_date, idea_id, continuity, snapshot_json) "
        "VALUES (?, ?, ?, ?) "
        "ON CONFLICT(report_date) DO UPDATE SET idea_id=excluded.idea_id, "
        "continuity=excluded.continuity, snapshot_json=excluded.snapshot_json",
        (day, snapshot.idea_id, snapshot.continuity, json.dumps(payload, ensure_ascii=False)),
    )
    conn.commit()


def snapshot_to_public_dict(snapshot: IdeaSnapshot) -> dict:
    pdf_name = f"XingAI_Daily_Passive_Income_Idea_Report_{snapshot.report_date}.pdf"
    return {
        "report_date": snapshot.report_date,
        "generated_at": snapshot.generated_at,
        "idea_id": snapshot.idea_id,
        "idea_name": snapshot.idea_name,
        "one_liner": snapshot.one_liner,
        "continuity": snapshot.continuity,
        "fit_score": snapshot.fit_score,
        "passive_score": snapshot.passive_score,
        "why_fit": snapshot.why_fit,
        "income_kind": snapshot.income_kind,
        "income_band": snapshot.income_band,
        "startup_capital": snapshot.startup_capital,
        "time_per_week": snapshot.time_per_week,
        "first_revenue_eta": snapshot.first_revenue_eta,
        "scalability": snapshot.scalability,
        "do_today": snapshot.do_today,
        "dont_today": snapshot.dont_today,
        "biggest_risk": snapshot.biggest_risk,
        "stop_rules": list(snapshot.stop_rules),
        "day7_plan": list(snapshot.day7_plan),
        "day30_goals": list(snapshot.day30_goals),
        "business_model": snapshot.business_model,
        "competition": snapshot.competition,
        "market_evidence": [
            {
                "kind": ev.kind,
                "text": ev.text,
                "source_ids": list(ev.source_ids),
            }
            for ev in snapshot.market_evidence
        ],
        "is_mock": snapshot.is_mock,
        "disclaimer": snapshot.disclaimer,
        "pdf_url": f"/reports/{pdf_name}",
        "sources": {
            sid: {
                "title": s.title,
                "url": s.url,
                "as_of": s.as_of,
                "verified": s.verified,
                "note": s.note,
            }
            for sid, s in snapshot.sources.items()
        },
        "locales": snapshot.locales or {},
    }


def get_day(conn: sqlite3.Connection, report_date: str) -> dict | None:
    row = conn.execute(
        "SELECT snapshot_json FROM idea_days WHERE report_date = ?",
        (report_date,),
    ).fetchone()
    if not row:
        return None
    return json.loads(row["snapshot_json"])
