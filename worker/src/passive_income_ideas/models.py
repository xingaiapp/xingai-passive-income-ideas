from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


EvidenceKind = Literal["fact", "inference", "recommendation"]

UNVERIFIED = "未核实"


def ensure_unverified_income_band(text: str) -> str:
    """Fail-closed: income bands must not read as verified facts."""
    t = (text or "").strip()
    if not t:
        return f"收入区间{UNVERIFIED}"
    markers = (UNVERIFIED, "未做付费验证", "估计", "不预测")
    if any(m in t for m in markers):
        return t
    return f"{t}（{UNVERIFIED}）"


@dataclass(frozen=True)
class OperatorProfile:
    age: int
    location: str
    background: str
    goals: str
    constraints: tuple[str, ...]
    skills: tuple[str, ...] = ()
    name: str = ""
    locale: str = "zh-CN"
    timezone: str = "America/Chicago"


@dataclass(frozen=True)
class SourceRef:
    title: str
    url: str
    as_of: str
    verified: bool
    note: str = ""


@dataclass(frozen=True)
class EvidenceItem:
    kind: EvidenceKind
    text: str
    source_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class IdeaSnapshot:
    report_date: str
    generated_at: str
    idea_id: str
    idea_name: str
    one_liner: str
    continuity: str  # "new" | "progress"
    fit_score: int  # 1-10
    passive_score: int  # 1-10
    why_fit: str
    income_kind: Literal["business_revenue", "investment_return", "mixed"]
    income_band: str
    startup_capital: str
    time_per_week: str
    first_revenue_eta: str
    scalability: str
    do_today: str
    dont_today: str
    biggest_risk: str
    stop_rules: tuple[str, ...]
    day7_plan: tuple[str, ...]
    day30_goals: tuple[str, ...]
    automation_path: tuple[str, ...]
    market_evidence: tuple[EvidenceItem, ...]
    business_model: str
    competition: str
    sources: dict[str, SourceRef] = field(default_factory=dict)
    is_mock: bool = True
    disclaimer: str = (
        "仅供参考，不构成金融、税务或商业建议。不保证收入。"
        "投资收益与商业收入已分开标注。未核实内容不得当作事实。"
    )


@dataclass(frozen=True)
class SendResult:
    ok: bool
    dry_run: bool
    message: str
    idempotency_key: str
