from __future__ import annotations

from typing import Any

from .models import EvidenceItem, IdeaSnapshot, OperatorProfile, SourceRef, UNVERIFIED

LOCALES = ("zh", "en", "ko")

_COPY_FIELDS = (
    "idea_name",
    "one_liner",
    "income_band",
    "startup_capital",
    "time_per_week",
    "first_revenue_eta",
    "scalability",
    "do_today",
    "dont_today",
    "biggest_risk",
    "business_model",
    "competition",
)

_LIST_FIELDS = ("stop_rules", "day7_plan", "day30_goals", "automation_path")


def _as_map(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def profile_text(profile: OperatorProfile, raw_cfg: dict[str, Any], locale: str) -> tuple[str, str]:
    """Return (background, goals) for UI locale. PDF/email keep zh defaults on profile."""
    op = _as_map((_as_map(raw_cfg.get("operator"))).get("i18n"))
    pack = _as_map(op.get(locale))
    background = str(pack.get("background") or profile.background)
    goals = str(pack.get("goals") or profile.goals)
    return background, goals


def why_fit_text(
    *,
    locale: str,
    age: int,
    location: str,
    background: str,
    goals: str,
    skills: str,
    one_liner: str,
) -> str:
    if locale == "en":
        return (
            f"Profile: age {age}, {location}; background {background}. "
            f"Goal: {goals}. Skills match: {skills or '(none configured)'}. "
            f"This Idea: {one_liner}"
        )
    if locale == "ko":
        return (
            f"프로필: {age}세, {location}, 배경 {background}. "
            f"목표: {goals}. 기술 매칭: {skills or '(없음)'}. "
            f"이 Idea: {one_liner}"
        )
    return (
        f"画像：{age} 岁，{location}，背景 {background}。"
        f"目标：{goals}。技能匹配：{skills or '（未配置）'}。"
        f"该 Idea：{one_liner}"
    )


def progress_do_today(locale: str, times: int, day7: list[str], fallback_do: str) -> str:
    step_idx = min(max(times, 0), max(len(day7) - 1, 0)) if day7 else 0
    step = day7[step_idx] if day7 else fallback_do
    n = times + 1
    total = max(len(day7), 1)
    if locale == "en":
        return (
            f"Continuity update (pick #{n}, same primary Idea): "
            f"advance 7-day plan to step {step_idx + 1}/{total}. "
            f"Today (30 min): {step}"
        )
    if locale == "ko":
        return (
            f"연속 업데이트({n}번째 선택, 동일 메인 Idea): "
            f"7일 계획 단계 {step_idx + 1}/{total}로 진행. "
            f"오늘 30분: {step}"
        )
    return (
        f"连续性更新（第 {n} 次选中，仍为本主 Idea）："
        f"按 7 天计划推进到步骤 {step_idx + 1}/{total}。"
        f"今天 30 分钟：{step}"
    )


def probe_evidence_text(locale: str, reachable: list[str], failed: list[str]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    if reachable:
        if locale == "en":
            text = (
                f"Catalog sources probed for reachability: {', '.join(reachable)} opened. "
                "This does not prove market demand or income figures."
            )
        elif locale == "ko":
            text = (
                f"카탈로그 출처 접근성 확인: {', '.join(reachable)} 열림. "
                "수요나 수입 숫자를 증명하지 않습니다."
            )
        else:
            text = (
                f"已对目录来源做可达性探测：{', '.join(reachable)} 可打开。"
                "这不证明市场需求或收入数字。"
            )
        items.append(EvidenceItem(kind="inference", text=text, source_ids=tuple(reachable)))
    if failed:
        if locale == "en":
            text = f"These sources failed probing and stay {UNVERIFIED}: {', '.join(failed)}."
        elif locale == "ko":
            text = f"다음 출처 탐침 실패, {UNVERIFIED} 표시: {', '.join(failed)}."
        else:
            text = f"以下来源探测失败，已标 {UNVERIFIED}：{', '.join(failed)}。"
        items.append(EvidenceItem(kind="inference", text=text, source_ids=tuple(failed)))
    return items


def merge_idea_locale(item: dict[str, Any], locale: str) -> dict[str, Any]:
    """zh fields live at root; en/ko under item['locales'][lang]."""
    out = dict(item)
    if locale == "zh":
        return out
    pack = _as_map(_as_map(item.get("locales")).get(locale))
    for key in _COPY_FIELDS:
        if key in pack and pack[key] is not None:
            out[key] = pack[key]
    for key in _LIST_FIELDS:
        if key in pack and pack[key] is not None:
            out[key] = pack[key]
    if "market_evidence" in pack and pack["market_evidence"] is not None:
        out["market_evidence"] = pack["market_evidence"]
    src_notes = _as_map(pack.get("source_notes"))
    if src_notes:
        sources = {**_as_map(out.get("sources"))}
        for sid, note in src_notes.items():
            raw = sources.get(sid)
            if isinstance(raw, dict):
                sources[sid] = {**raw, "note": note}
        out["sources"] = sources
    return out


def disclaimer_for(locale: str) -> str:
    if locale == "en":
        return (
            "Informational only — not financial, tax, or business advice. No income guarantees. "
            "Investment returns and business revenue are labeled separately. "
            f"Unverified claims stay marked {UNVERIFIED}."
        )
    if locale == "ko":
        return (
            "정보 제공용 — 금융·세무·사업 조언이 아닙니다. 수입을 보장하지 않습니다. "
            "투자 수익과 사업 매출을 구분합니다. "
            f"미확인 내용은 {UNVERIFIED}로 표시합니다."
        )
    return (
        "仅供参考，不构成金融、税务或商业建议。不保证收入。"
        "投资收益与商业收入已分开标注。未核实内容不得当作事实。"
    )


def localized_sources(
    base: dict[str, SourceRef],
    localized_item: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    notes = {}
    raw_sources = _as_map(localized_item.get("sources"))
    for sid, raw in raw_sources.items():
        if isinstance(raw, dict) and raw.get("note"):
            notes[sid] = str(raw["note"])
    # also accept source_notes map
    notes.update({str(k): str(v) for k, v in _as_map(localized_item.get("source_notes")).items()})

    out: dict[str, dict[str, Any]] = {}
    for sid, s in base.items():
        out[sid] = {
            "title": s.title,
            "url": s.url,
            "as_of": s.as_of,
            "verified": s.verified,
            "note": notes.get(sid, s.note),
        }
    return out


def build_locale_payload(
    snapshot: IdeaSnapshot,
    *,
    locale: str,
    localized_item: dict[str, Any],
    why_fit: str,
    do_today: str,
    evidence: tuple[EvidenceItem, ...],
) -> dict[str, Any]:
    return {
        "idea_name": str(localized_item.get("idea_name") or snapshot.idea_name),
        "one_liner": str(localized_item.get("one_liner") or snapshot.one_liner),
        "why_fit": why_fit,
        "income_band": str(localized_item.get("income_band") or snapshot.income_band),
        "startup_capital": str(localized_item.get("startup_capital") or snapshot.startup_capital),
        "time_per_week": str(localized_item.get("time_per_week") or snapshot.time_per_week),
        "first_revenue_eta": str(localized_item.get("first_revenue_eta") or snapshot.first_revenue_eta),
        "scalability": str(localized_item.get("scalability") or snapshot.scalability),
        "do_today": do_today,
        "dont_today": str(localized_item.get("dont_today") or snapshot.dont_today),
        "biggest_risk": str(localized_item.get("biggest_risk") or snapshot.biggest_risk),
        "stop_rules": [str(x) for x in (localized_item.get("stop_rules") or snapshot.stop_rules)],
        "day7_plan": [str(x) for x in (localized_item.get("day7_plan") or snapshot.day7_plan)],
        "day30_goals": [str(x) for x in (localized_item.get("day30_goals") or snapshot.day30_goals)],
        "business_model": str(localized_item.get("business_model") or snapshot.business_model),
        "competition": str(localized_item.get("competition") or snapshot.competition),
        "market_evidence": [
            {"kind": ev.kind, "text": ev.text, "source_ids": list(ev.source_ids)} for ev in evidence
        ],
        "disclaimer": disclaimer_for(locale),
        "sources": localized_sources(snapshot.sources, localized_item),
    }


def parse_evidence(item: dict[str, Any]) -> tuple[EvidenceItem, ...]:
    items: list[EvidenceItem] = []
    for ev in item.get("market_evidence") or []:
        kind = str(ev.get("kind") or "inference")
        if kind not in {"fact", "inference", "recommendation"}:
            kind = "inference"
        source_ids = tuple(str(x) for x in (ev.get("source_ids") or ()))
        text = str(ev.get("text") or "")
        if kind == "fact" and not source_ids:
            kind = "inference"
            text = f"{text}（{UNVERIFIED}：无来源 id）"
        items.append(EvidenceItem(kind=kind, text=text, source_ids=source_ids))  # type: ignore[arg-type]
    return tuple(items)


def attach_locales(
    snapshot: IdeaSnapshot,
    *,
    chosen: dict[str, Any],
    profile: OperatorProfile,
    raw_cfg: dict[str, Any],
    continuity: str,
    times_picked: int,
    probe_reachable: list[str] | None = None,
    probe_failed: list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Build en/zh/ko UI packs. Snapshot root fields stay Chinese for PDF/email."""
    reachable = probe_reachable or []
    failed = probe_failed or []
    packs: dict[str, dict[str, Any]] = {}
    skills = ", ".join(profile.skills)

    for locale in LOCALES:
        item = merge_idea_locale(chosen, locale)
        background, goals = profile_text(profile, raw_cfg, locale)
        one_liner = str(item.get("one_liner") or "")
        why = why_fit_text(
            locale=locale,
            age=profile.age,
            location=profile.location,
            background=background,
            goals=goals,
            skills=skills,
            one_liner=one_liner,
        )
        day7 = [str(x) for x in (item.get("day7_plan") or ())]
        if continuity == "progress":
            do_today = progress_do_today(
                locale, times_picked, day7, str(item.get("do_today") or "")
            )
        else:
            do_today = str(item.get("do_today") or "")

        evidence_list = list(parse_evidence(item))
        fixed: list[EvidenceItem] = []
        for ev in evidence_list:
            if ev.kind == "fact":
                for sid in ev.source_ids:
                    src = snapshot.sources.get(sid)
                    if src is None or not src.verified:
                        ev = EvidenceItem(
                            kind="inference",
                            text=f"{ev.text}（{UNVERIFIED}）",
                            source_ids=ev.source_ids,
                        )
                        break
            fixed.append(ev)
        fixed.extend(probe_evidence_text(locale, reachable, failed))

        packs[locale] = build_locale_payload(
            snapshot,
            locale=locale,
            localized_item=item,
            why_fit=why,
            do_today=do_today,
            evidence=tuple(fixed),
        )
    return packs
