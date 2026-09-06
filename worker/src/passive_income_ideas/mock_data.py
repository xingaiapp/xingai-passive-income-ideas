from __future__ import annotations

from datetime import date, datetime, timezone

from .config import load_operator_profile
from .models import EvidenceItem, IdeaSnapshot, OperatorProfile, SourceRef

try:
    _PROFILE = load_operator_profile()
except Exception:  # noqa: BLE001
    _PROFILE = OperatorProfile(
        age=53,
        location="Austin, Texas, USA",
        background="软件工程、.NET、云平台、AI 与工程管理",
        goals="财富自由与长期被动收入",
        constraints=(
            "不接受赌博式或高杠杆方案",
            "不接受难以核实的承诺",
            "不接受需长期高强度全职投入才能启动的方案",
            "适合 53 岁财富积累阶段：可兼职验证、可外包/自动化",
        ),
        skills=(".NET", "cloud", "AI", "eng-management"),
    )

DEFAULT_PROFILE = _PROFILE


def build_mock_snapshot(report_day: date | None = None) -> IdeaSnapshot:
    """Deterministic mock Idea for offline PDF/email tests. Not live research."""
    day = report_day or date.today()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sources = {
        "s1": SourceRef(
            title="BLS U.S. Occupational Employment (software developers) — mock citation shape",
            url="https://www.bls.gov/oes/",
            as_of="2026-05-01",
            verified=False,
            note="骨架引用：正式上线前必须换成与 Idea 直接相关的核实来源",
        ),
        "s2": SourceRef(
            title="IRS self-employment tax overview",
            url="https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes",
            as_of="2026-01-15",
            verified=True,
            note="税务提醒页面存在；非对本 Idea 收入的预测",
        ),
    }
    return IdeaSnapshot(
        report_date=day.isoformat(),
        generated_at=now,
        idea_id=f"mock-ops-checklist-{day.isoformat()}",
        idea_name="垂直行业 AI 运维检查清单（订阅制）",
        one_liner="把你熟悉的云/.NET/运维检查项产品化成小团队可订阅的清单+提醒，而不是再做一个通用 ChatGPT 壳。",
        continuity="new",
        fit_score=8,
        passive_score=6,
        why_fit=(
            f"画像：{DEFAULT_PROFILE.age} 岁，{DEFAULT_PROFILE.location}，背景 "
            f"{DEFAULT_PROFILE.background}。该 Idea 复用你已有的工程与管理语言，"
            "可用兼职访谈验证，交付可逐步模板化与外包，不要求立刻全职创业。"
        ),
        income_kind="business_revenue",
        income_band="商业收入（非投资收益）估计：验证后 90 天约 $0–2,000/月（模拟区间，未做付费验证）",
        startup_capital="启动资金约 $0–500（域名、邮箱、基础托管）；无需融资",
        time_per_week="验证期每周 4–6 小时；若无人付费意向则停止",
        first_revenue_eta="若 10 次访谈中出现付费意向，最早 2–4 周可收第一笔（预售/试点）",
        scalability="中：可从单一垂直扩展到相邻行业；自动化检查与邮件提醒可产品化",
        do_today="30 分钟：列出 5 个你认识的工程负责人，约其中 3 人做 15 分钟访谈（只问：哪些检查仍靠表格/聊天？）",
        dont_today="不要买广告、不要先写完整 SaaS、不要注册复杂公司结构",
        biggest_risk="礼貌兴趣 ≠ 付费意愿；若 10 次访谈零付费意向，立即停止并换题",
        stop_rules=(
            "10 次目标用户访谈仍无明确付费意向",
            "需要全职 3 个月以上才能做出最小可售版本",
            "依赖无法核实的流量/收益承诺渠道",
        ),
        day7_plan=(
            "D1：完成 3 次访谈预约与问题清单",
            "D2–D3：完成至少 5 次访谈并记录痛点频率",
            "D4：起草一页价值主张（谁、什么痛、价格锚点）",
            "D5：用 Notion/文档做出 1 份可交付检查清单样例",
            "D6：向 2 位访谈对象展示样例，问是否愿付 $29–$99/月试点",
            "D7：写下 go/no-go：付费意向数量、反对理由、下一周是否继续",
        ),
        day30_goals=(
            "至少 15 次访谈记录",
            "1 个可重复交付的清单模板",
            "至少 1 个付费试点或书面预购意向",
            "明确停止或进入自动化路线的书面决定",
        ),
        automation_path=(
            "周报/提醒邮件自动发送",
            "检查项版本化与客户空间隔离",
            "后期可加轻量规则引擎；LLM 仅作辅助，不作唯一真理来源",
        ),
        market_evidence=(
            EvidenceItem(
                kind="inference",
                text="中小团队仍常用表格/聊天做发布与巡检（基于你的职业经验推断，非正式调研统计）。",
                source_ids=(),
            ),
            EvidenceItem(
                kind="fact",
                text="美国自雇者需了解 self-employment tax 义务（IRS 页面存在）。",
                source_ids=("s2",),
            ),
            EvidenceItem(
                kind="recommendation",
                text="先卖清单与提醒，再考虑软件化；用预售验证价格。",
                source_ids=(),
            ),
        ),
        business_model=(
            "订阅制商业收入：基础清单 $29/月，含提醒与月度更新的团队版 $99/月。"
            "这不是分红或投资回报率。"
        ),
        competition=(
            "通用项目管理与 ChatGPT 工作流是替代品；差异化在于你沉淀的垂直检查项与责任边界说明，"
            "而不是又一个空白 AI 对话框。"
        ),
        sources=sources,
        is_mock=True,
    )
