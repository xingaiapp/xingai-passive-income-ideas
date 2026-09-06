from __future__ import annotations

import io
import re
from pathlib import Path


REQUIRED_SECTION_MARKERS = (
    "Executive Action Summary",
    "今日唯一主 Idea",
    "适合度与被动程度评分",
    "市场与需求证据",
    "商业模式与收入模型",
    "启动成本与时间投入",
    "竞争与差异化",
    "今日 30 分钟行动",
    "7 天 MVP",
    "30 天目标",
    "自动化路线",
    "风险、停止条件",
    "来源与时间戳",
)


def validate_pdf_bytes(data: bytes) -> list[str]:
    errors: list[str] = []
    if not data.startswith(b"%PDF"):
        errors.append("not a PDF (missing %PDF header)")
        return errors
    try:
        from pypdf import PdfReader
    except ImportError:
        errors.append("pypdf not installed")
        return errors

    reader = PdfReader(io.BytesIO(data))
    n = len(reader.pages)
    if n < 2:
        errors.append(f"too few pages: {n} (need ≥2)")
    if n > 40:
        errors.append(f"too many pages: {n}")

    texts: list[str] = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        if "\ufffd" in t:
            errors.append(f"page {i + 1}: replacement char \\ufffd")
        if len(t.strip()) < 20:
            errors.append(f"page {i + 1}: extracted text too short ({len(t.strip())})")
        texts.append(t)
    blob = "\n".join(texts)
    for marker in REQUIRED_SECTION_MARKERS:
        if marker not in blob:
            errors.append(f"missing section marker: {marker}")
    if not re.search(r"[\u4e00-\u9fff]", blob):
        errors.append("no CJK characters found — font embedding may have failed")
    return errors


def qa_file(pdf_path: Path) -> list[str]:
    data = pdf_path.read_bytes()
    errs = validate_pdf_bytes(data)
    if len(data) < 2000:
        errs.append("PDF file suspiciously small")
    return errs
