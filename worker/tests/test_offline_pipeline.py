from __future__ import annotations

from datetime import date

from passive_income_zhibao.email_report import build_body, build_subject, send_report
from passive_income_zhibao.mock_data import build_mock_snapshot
from passive_income_zhibao.pdf_report import pdf_filename, render_pdf
from passive_income_zhibao.qa import validate_pdf_bytes


def test_mock_snapshot_fields():
    snap = build_mock_snapshot(date(2026, 9, 6))
    assert snap.report_date == "2026-09-06"
    assert snap.is_mock is True
    assert snap.income_kind == "business_revenue"
    assert snap.fit_score >= 1
    assert "被动" in snap.disclaimer or "参考" in snap.disclaimer


def test_render_pdf_passes_qa():
    snap = build_mock_snapshot(date(2026, 9, 6))
    data = render_pdf(snap)
    assert data.startswith(b"%PDF")
    assert len(data) > 5000
    errs = validate_pdf_bytes(data)
    assert errs == [], errs
    assert pdf_filename(snap) == "XingAI_Daily_Passive_Income_Idea_Report_2026-09-06.pdf"


def test_email_subject_and_dry_run():
    snap = build_mock_snapshot(date(2026, 9, 6))
    subject = build_subject(snap)
    assert subject.startswith("XingAI 每日被动收入 Idea 智报｜2026-09-06｜")
    assert snap.idea_name in subject
    body = build_body(snap)
    assert "今日结论" in body
    assert "模拟" in body
    pdf = render_pdf(snap)
    result = send_report(snap, pdf, pdf_filename(snap), dry_run=True)
    assert result.ok
    assert result.dry_run
