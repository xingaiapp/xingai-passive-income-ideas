from __future__ import annotations

import io
import logging
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    ListFlowable,
    ListItem,
)

from .models import IdeaSnapshot

log = logging.getLogger(__name__)

BLACK = colors.HexColor("#000000")
YELLOW = colors.HexColor("#FFF4CC")
ORANGE = colors.HexColor("#E07000")
ALT_ROW = colors.HexColor("#FFFBEA")
WHITE = colors.white

_FONT_REG = "NotoSansSC"
_FONT_BOLD = "NotoSansSC-Bold"


def _assets_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "assets"


def _register_fonts() -> tuple[str, str]:
    if _FONT_REG in pdfmetrics.getRegisteredFontNames():
        return _FONT_REG, _FONT_BOLD if _FONT_BOLD in pdfmetrics.getRegisteredFontNames() else _FONT_REG

    # ReportLab TTFont needs TrueType (glyf), not CFF/PostScript OTF.
    assets = _assets_dir()
    candidates = [
        (assets / "NotoSansSC-Regular.ttf", assets / "NotoSansSC-Bold.ttf"),
        (assets / "NotoSansSC-Regular.otf", assets / "NotoSansSC-Bold.otf"),
        (
            Path("/System/Library/Fonts/STHeiti Medium.ttc"),
            Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        ),
        (
            Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
            Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
        ),
        (
            Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"),
        ),
    ]
    for regular, bold in candidates:
        if not regular.exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont(_FONT_REG, str(regular), subfontIndex=0))
            if bold.exists():
                try:
                    pdfmetrics.registerFont(TTFont(_FONT_BOLD, str(bold), subfontIndex=0))
                except Exception:
                    pdfmetrics.registerFont(TTFont(_FONT_BOLD, str(regular), subfontIndex=0))
            else:
                pdfmetrics.registerFont(TTFont(_FONT_BOLD, str(regular), subfontIndex=0))
            return _FONT_REG, _FONT_BOLD
        except Exception as exc:
            log.warning("font register failed %s: %s", regular, exc)
    # Last resort — Latin only (QA may still pass for mixed docs poorly)
    return "Helvetica", "Helvetica-Bold"


def _styles() -> dict[str, ParagraphStyle]:
    reg, bold = _register_fonts()
    return {
        "cover": ParagraphStyle(
            "cover",
            fontName=bold,
            fontSize=22,
            leading=28,
            textColor=BLACK,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName=bold,
            fontSize=17,
            leading=22,
            textColor=BLACK,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName=bold,
            fontSize=12,
            leading=16,
            textColor=BLACK,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            fontName=reg,
            fontSize=10.5,
            leading=15,
            textColor=BLACK,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "small",
            fontName=reg,
            fontSize=8.5,
            leading=12,
            textColor=BLACK,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName=reg,
            fontSize=8.2,
            leading=11,
            textColor=BLACK,
        ),
        "cell": ParagraphStyle(
            "cell",
            fontName=reg,
            fontSize=9,
            leading=12,
            textColor=BLACK,
        ),
        "cell_bold": ParagraphStyle(
            "cell_bold",
            fontName=bold,
            fontSize=9,
            leading=12,
            textColor=BLACK,
        ),
    }


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    return Paragraph(safe, style)


def _kv_table(rows: list[tuple[str, str]], styles: dict[str, ParagraphStyle]) -> Table:
    data = [[_p(k, styles["cell_bold"]), _p(v, styles["cell"])] for k, v in rows]
    table = Table(data, colWidths=[42 * mm, 130 * mm])
    style_cmds = [
        ("TEXTCOLOR", (0, 0), (-1, -1), BLACK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BOX", (0, 0), (-1, -1), 0.5, BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("BACKGROUND", (0, 0), (-1, 0), YELLOW),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, ORANGE),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), ALT_ROW))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), WHITE))
    table.setStyle(TableStyle(style_cmds))
    return table


def _exec_box(snapshot: IdeaSnapshot, styles: dict[str, ParagraphStyle]) -> Table:
    lines = [
        f"<b>今日结论：</b>{snapshot.idea_name} — {snapshot.one_liner}",
        f"<b>为什么适合我：</b>{snapshot.why_fit}",
        f"<b>现实收入区间：</b>{snapshot.income_band}",
        f"<b>今天做什么：</b>{snapshot.do_today}",
        f"<b>今天不要做什么：</b>{snapshot.dont_today}",
        f"<b>最大风险：</b>{snapshot.biggest_risk}",
    ]
    if snapshot.is_mock:
        lines.insert(0, "<b>【模拟报告】</b>内容为 fixture，非正式市场调研结论。")
    body = "<br/><br/>".join(lines)
    inner = Table([[Paragraph(body, styles["body"])]], colWidths=[172 * mm])
    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), YELLOW),
                ("BOX", (0, 0), (-1, -1), 2, ORANGE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), BLACK),
            ]
        )
    )
    return inner


def _bullets(items: tuple[str, ...] | list[str], styles: dict[str, ParagraphStyle]) -> ListFlowable:
    return ListFlowable(
        [ListItem(_p(x, styles["body"]), leftIndent=8, bulletColor=BLACK) for x in items],
        bulletType="bullet",
        start="•",
    )


def render_pdf(snapshot: IdeaSnapshot) -> bytes:
    styles = _styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"XingAI Passive Income Idea {snapshot.report_date}",
        author="XingAI",
    )

    story: list = []
    story.append(_p("XingAI 每日被动收入 Idea 智报", styles["cover"]))
    story.append(
        _p(
            f"报告日 {snapshot.report_date} ｜生成 {snapshot.generated_at} ｜连续性：{snapshot.continuity}",
            styles["small"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(_p("1. Executive Action Summary", styles["h1"]))
    story.append(_exec_box(snapshot, styles))
    story.append(Spacer(1, 10))

    story.append(_p("2. 今日唯一主 Idea", styles["h1"]))
    story.append(
        _kv_table(
            [
                ("Idea 名称", snapshot.idea_name),
                ("一句话", snapshot.one_liner),
                ("Idea ID", snapshot.idea_id),
                ("收入类型", snapshot.income_kind),
            ],
            styles,
        )
    )

    story.append(_p("3. 适合度与被动程度评分", styles["h1"]))
    story.append(
        _kv_table(
            [
                ("适合度 (1–10)", str(snapshot.fit_score)),
                ("被动程度 (1–10)", str(snapshot.passive_score)),
                ("为什么适合", snapshot.why_fit),
            ],
            styles,
        )
    )

    story.append(_p("4. 市场与需求证据", styles["h1"]))
    for ev in snapshot.market_evidence:
        label = {"fact": "事实", "inference": "推断", "recommendation": "建议"}[ev.kind]
        src = "、".join(ev.source_ids) if ev.source_ids else "无直接来源"
        story.append(_p(f"【{label}】{ev.text}（来源：{src}）", styles["body"]))

    story.append(_p("5. 商业模式与收入模型", styles["h1"]))
    story.append(_p(snapshot.business_model, styles["body"]))
    story.append(_p(snapshot.income_band, styles["body"]))

    story.append(_p("6. 启动成本与时间投入", styles["h1"]))
    story.append(
        _kv_table(
            [
                ("启动资金", snapshot.startup_capital),
                ("每周时间", snapshot.time_per_week),
                ("首笔收入", snapshot.first_revenue_eta),
                ("可扩展性", snapshot.scalability),
            ],
            styles,
        )
    )

    story.append(_p("7. 竞争与差异化", styles["h1"]))
    story.append(_p(snapshot.competition, styles["body"]))

    story.append(_p("8. 今日 30 分钟行动", styles["h1"]))
    story.append(_p(snapshot.do_today, styles["body"]))
    story.append(_p(f"不要做：{snapshot.dont_today}", styles["body"]))

    story.append(_p("9. 7 天 MVP 逐日步骤", styles["h1"]))
    story.append(_bullets(snapshot.day7_plan, styles))

    story.append(_p("10. 30 天目标", styles["h1"]))
    story.append(_bullets(snapshot.day30_goals, styles))

    story.append(_p("11. 自动化路线", styles["h1"]))
    story.append(_bullets(snapshot.automation_path, styles))

    story.append(_p("12. 风险、停止条件与替代方案", styles["h1"]))
    story.append(_p(f"最大风险：{snapshot.biggest_risk}", styles["body"]))
    story.append(_p("停止条件：", styles["h2"]))
    story.append(_bullets(snapshot.stop_rules, styles))

    story.append(_p("13. 来源与时间戳", styles["h1"]))
    for sid, src in snapshot.sources.items():
        flag = "已核实" if src.verified else "未核实"
        story.append(
            _p(
                f"[{sid}] {src.title} ｜ {flag} ｜ as_of {src.as_of} ｜ {src.url}"
                + (f" ｜ {src.note}" if src.note else ""),
                styles["small"],
            )
        )
    story.append(Spacer(1, 8))
    story.append(_p(snapshot.disclaimer, styles["footer"]))

    def _on_page(canvas, _doc) -> None:
        canvas.saveState()
        canvas.setFillColor(BLACK)
        canvas.setFont(_register_fonts()[0], 8.2)
        canvas.drawString(16 * mm, A4[1] - 12 * mm, "XingAI 每日被动收入 Idea 智报")
        canvas.drawRightString(A4[0] - 16 * mm, A4[1] - 12 * mm, f"第 {canvas.getPageNumber()} 页")
        canvas.drawCentredString(
            A4[0] / 2,
            10 * mm,
            "仅供参考 · 非投资建议 · 不保证收入",
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return buf.getvalue()


def pdf_filename(snapshot: IdeaSnapshot) -> str:
    return f"XingAI_Daily_Passive_Income_Idea_Report_{snapshot.report_date}.pdf"
