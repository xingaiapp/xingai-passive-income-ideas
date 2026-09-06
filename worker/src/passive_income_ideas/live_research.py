from __future__ import annotations

import logging
from datetime import date, datetime, timezone
from typing import Any

from .config import load_app_config, load_idea_catalog
from .memory import connect, find_duplicate, list_recent, recent_pick_for_id, upsert_pick
from .models import (
    UNVERIFIED,
    EvidenceItem,
    IdeaSnapshot,
    OperatorProfile,
    SourceRef,
    ensure_unverified_income_band,
)

log = logging.getLogger(__name__)


def _score_idea(profile: OperatorProfile, item: dict[str, Any]) -> int:
    idea_skills = {str(s).lower() for s in (item.get("skills") or [])}
    profile_skills = {s.lower() for s in profile.skills}
    overlap = len(idea_skills & profile_skills)
    base = int(item.get("fit_score") or 5)
    # Prefer business_revenue for this operator's wealth-building constraints
    kind = str(item.get("income_kind") or "")
    kind_bonus = 1 if kind == "business_revenue" else (-2 if kind == "investment_return" else 0)
    return base * 10 + overlap * 3 + kind_bonus


def _sources(item: dict[str, Any]) -> dict[str, SourceRef]:
    out: dict[str, SourceRef] = {}
    for sid, raw in (item.get("sources") or {}).items():
        out[str(sid)] = SourceRef(
            title=str(raw.get("title") or sid),
            url=str(raw.get("url") or ""),
            as_of=str(raw.get("as_of") or ""),
            verified=bool(raw.get("verified")),
            note=str(raw.get("note") or ""),
        )
    return out


def _evidence(item: dict[str, Any]) -> tuple[EvidenceItem, ...]:
    items: list[EvidenceItem] = []
    for ev in item.get("market_evidence") or []:
        kind = str(ev.get("kind") or "inference")
        if kind not in {"fact", "inference", "recommendation"}:
            kind = "inference"
        # Fail-closed: fact without verified source ids becomes inference
        source_ids = tuple(str(x) for x in (ev.get("source_ids") or ()))
        text = str(ev.get("text") or "")
        if kind == "fact" and not source_ids:
            kind = "inference"
            text = f"{text}（{UNVERIFIED}：无来源 id）"
        items.append(EvidenceItem(kind=kind, text=text, source_ids=source_ids))  # type: ignore[arg-type]
    return tuple(items)


def _progress_overlay(item: dict[str, Any], times: int) -> tuple[str, str]:
    """Slightly advance do_today when the same Idea continues."""
    base_do = str(item.get("do_today") or "")
    note = f"连续性更新（第 {times + 1} 次选中）：在昨日动作之上推进下一步验证，不换题。"
    do_today = f"{note} {base_do}"
    return "progress", do_today


def build_live_snapshot(
    report_day: date | None = None,
    *,
    web_fetch: bool | None = None,
    llm_polish: bool | None = None,
    force_llm: bool = False,
) -> IdeaSnapshot:
    """Pick one Idea from catalog using profile + SQLite anti-repeat. No invented facts."""
    day = report_day or date.today()
    cfg = load_app_config()
    profile = cfg.profile
    settings = cfg.research
    do_web = settings.web_fetch if web_fetch is None else web_fetch
    do_llm = settings.llm_polish if llm_polish is None else llm_polish
    catalog = load_idea_catalog()
    conn = connect()
    try:
        history = list_recent(conn, days=120)
        ranked = sorted(catalog, key=lambda x: _score_idea(profile, x), reverse=True)

        chosen: dict[str, Any] | None = None
        continuity = "new"
        do_today_override: str | None = None

        for item in ranked:
            idea_id = str(item.get("idea_id") or "")
            name = str(item.get("idea_name") or "")
            if not idea_id or not name:
                continue

            # Continuity: if this top idea was picked recently, keep it as progress
            recent = recent_pick_for_id(conn, idea_id, settings.continuity_days)
            if recent and item is ranked[0]:
                continuity, do_today_override = _progress_overlay(item, recent.times_picked)
                chosen = item
                break

            dup = find_duplicate(name, history, settings.min_jaccard_new)
            if dup and dup.idea_id != idea_id:
                log.info("skip near-duplicate %s ~ %s (%.2f)", name, dup.idea_name, dup.score)
                continue
            # Skip if same id was picked in last continuity window but not top anymore
            if recent and item is not ranked[0]:
                continue
            chosen = item
            continuity = "new"
            break

        if chosen is None:
            # Fall back to top-ranked even if duplicate (still better than empty)
            chosen = ranked[0]
            continuity = "progress"
            do_today_override = str(chosen.get("do_today") or "")
            log.warning("catalog exhausted filters; falling back to %s", chosen.get("idea_id"))

        sources = _sources(chosen)
        # Downgrade fact evidence that cites unverified sources
        evidence = []
        for ev in _evidence(chosen):
            if ev.kind == "fact":
                for sid in ev.source_ids:
                    src = sources.get(sid)
                    if src is None or not src.verified:
                        ev = EvidenceItem(
                            kind="inference",
                            text=f"{ev.text}（{UNVERIFIED}：来源未核实）",
                            source_ids=ev.source_ids,
                        )
                        break
            evidence.append(ev)

        income_band = ensure_unverified_income_band(str(chosen.get("income_band") or ""))
        why_fit = (
            f"画像：{profile.age} 岁，{profile.location}，背景 {profile.background}。"
            f"目标：{profile.goals}。技能匹配：{', '.join(profile.skills) or '（未配置）'}。"
            f"该 Idea：{chosen.get('one_liner')}"
        )

        kind_raw = str(chosen.get("income_kind") or "business_revenue")
        if kind_raw not in {"business_revenue", "investment_return", "mixed"}:
            kind_raw = "business_revenue"

        snap = IdeaSnapshot(
            report_date=day.isoformat(),
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            idea_id=str(chosen["idea_id"]),
            idea_name=str(chosen["idea_name"]),
            one_liner=str(chosen.get("one_liner") or ""),
            continuity=continuity,
            fit_score=int(chosen.get("fit_score") or 5),
            passive_score=int(chosen.get("passive_score") or 5),
            why_fit=why_fit,
            income_kind=kind_raw,  # type: ignore[arg-type]
            income_band=income_band,
            startup_capital=str(chosen.get("startup_capital") or ""),
            time_per_week=str(chosen.get("time_per_week") or ""),
            first_revenue_eta=str(chosen.get("first_revenue_eta") or ""),
            scalability=str(chosen.get("scalability") or ""),
            do_today=do_today_override or str(chosen.get("do_today") or ""),
            dont_today=str(chosen.get("dont_today") or ""),
            biggest_risk=str(chosen.get("biggest_risk") or ""),
            stop_rules=tuple(str(x) for x in (chosen.get("stop_rules") or ())),
            day7_plan=tuple(str(x) for x in (chosen.get("day7_plan") or ())),
            day30_goals=tuple(str(x) for x in (chosen.get("day30_goals") or ())),
            automation_path=tuple(str(x) for x in (chosen.get("automation_path") or ())),
            market_evidence=tuple(evidence),
            business_model=str(chosen.get("business_model") or ""),
            competition=str(chosen.get("competition") or ""),
            sources=sources,
            is_mock=False,
        )

        if do_web:
            from .web_research import enrich_snapshot_web

            snap = enrich_snapshot_web(snap)
        if do_llm:
            from .llm_polish import maybe_polish_snapshot

            snap = maybe_polish_snapshot(snap, force_llm=force_llm, enabled=True)

        upsert_pick(conn, snap)
        return snap
    finally:
        conn.close()


def resolve_mode(cli_mode: str | None = None) -> str:
    if cli_mode in {"live", "mock"}:
        return cli_mode
    return load_app_config().research.mode
