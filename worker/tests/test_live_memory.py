from __future__ import annotations

from datetime import date
from pathlib import Path

from passive_income_ideas.live_research import build_live_snapshot
from passive_income_ideas.memory import connect, find_duplicate, jaccard, list_recent, tokens
from passive_income_ideas.models import UNVERIFIED, ensure_unverified_income_band


def test_jaccard_and_duplicate(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PASSIVE_INCOME_DATA_DIR", str(tmp_path))
    conn = connect()
    from passive_income_ideas.models import IdeaSnapshot

    snap = IdeaSnapshot(
        report_date="2026-09-01",
        generated_at="2026-09-01T00:00:00Z",
        idea_id="ops-checklist-sub",
        idea_name="垂直行业 AI 运维检查清单（订阅制）",
        one_liner="x",
        continuity="new",
        fit_score=8,
        passive_score=6,
        why_fit="x",
        income_kind="business_revenue",
        income_band="估计 $0（未核实）",
        startup_capital="x",
        time_per_week="x",
        first_revenue_eta="x",
        scalability="x",
        do_today="x",
        dont_today="x",
        biggest_risk="x",
        stop_rules=(),
        day7_plan=(),
        day30_goals=(),
        automation_path=(),
        market_evidence=(),
        business_model="x",
        competition="x",
        is_mock=False,
    )
    from passive_income_ideas.memory import upsert_pick

    upsert_pick(conn, snap)
    history = list_recent(conn, days=90)
    hit = find_duplicate("垂直行业 AI 运维检查清单 订阅", history, 0.35)
    assert hit is not None
    assert hit.idea_id == "ops-checklist-sub"
    assert jaccard(tokens("abc"), tokens("xyz")) == 0.0
    conn.close()


def test_unverified_income_band():
    assert UNVERIFIED in ensure_unverified_income_band("$1000/mo guaranteed")
    assert ensure_unverified_income_band("估计 $0（未核实）").count(UNVERIFIED) >= 1


def test_live_snapshot_not_mock(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PASSIVE_INCOME_DATA_DIR", str(tmp_path))
    snap = build_live_snapshot(date(2026, 9, 6))
    assert snap.is_mock is False
    assert snap.idea_id
    assert snap.idea_name
    assert UNVERIFIED in snap.income_band or "估计" in snap.income_band
    # facts must cite verified sources only after fail-closed pass
    for ev in snap.market_evidence:
        if ev.kind == "fact":
            assert ev.source_ids
            for sid in ev.source_ids:
                assert snap.sources[sid].verified
