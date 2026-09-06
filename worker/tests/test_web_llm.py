from __future__ import annotations

from passive_income_ideas.llm_polish import _sanitize_polish
from passive_income_ideas.models import IdeaSnapshot, SourceRef
from passive_income_ideas.web_research import enrich_sources, evidence_from_probes


def _snap(**kwargs) -> IdeaSnapshot:
    base = dict(
        report_date="2026-09-06",
        generated_at="2026-09-06T00:00:00Z",
        idea_id="ops-checklist-sub",
        idea_name="垂直行业 AI 运维检查清单（订阅制）",
        one_liner="把检查项产品化",
        continuity="new",
        fit_score=8,
        passive_score=6,
        why_fit="适合 .NET 背景",
        income_kind="business_revenue",
        income_band="估计 $0–2,000/月（未核实）",
        startup_capital="$0–500",
        time_per_week="4–6h",
        first_revenue_eta="2–4 周",
        scalability="中",
        do_today="访谈 3 人",
        dont_today="不要买广告",
        biggest_risk="无付费意向",
        stop_rules=(),
        day7_plan=(),
        day30_goals=(),
        automation_path=(),
        market_evidence=(),
        business_model="订阅 $29/月",
        competition="ChatGPT",
        sources={
            "s1": SourceRef(
                title="IRS",
                url="https://www.irs.gov/example",
                as_of="2026-01-01",
                verified=True,
            )
        },
        is_mock=False,
    )
    base.update(kwargs)
    return IdeaSnapshot(**base)  # type: ignore[arg-type]


def test_sanitize_strips_new_url_and_money():
    snap = _snap()
    polished = {
        "why_fit": "适合 .NET，详见 https://evil.example/new 以及 $99,999/月",
        "do_today": "访谈 3 人",
        "dont_today": "不要买广告",
        "biggest_risk": "无付费意向",
        "one_liner": "把检查项产品化",
    }
    out = _sanitize_polish(snap, polished)
    assert "evil.example" not in out["why_fit"]
    assert "99999" not in out["why_fit"].replace(",", "")
    assert "访谈" in out["do_today"]


def test_enrich_sources_fail_closed(monkeypatch):
    from passive_income_ideas import web_research as wr

    def fake_probe(url: str, *, timeout: float = 12.0):
        if "ok.example" in url:
            return True, 200, "OK Page"
        return False, 404, "HTTP 404"

    monkeypatch.setattr(wr, "probe_url", fake_probe)
    sources = {
        "ok": SourceRef("A", "https://ok.example/a", "2026-01-01", True),
        "bad": SourceRef("B", "https://bad.example/b", "2026-01-01", True),
    }
    out = enrich_sources(sources, as_of="2026-09-06")
    assert out["ok"].verified is True
    assert "web probe OK" in out["ok"].note
    assert out["bad"].verified is False
    assert "未核实" in out["bad"].note

    snap = _snap(sources=out)
    evidence = evidence_from_probes(out, snap.market_evidence)
    kinds = {e.kind for e in evidence}
    assert "inference" in kinds
