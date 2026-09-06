from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

from .email_report import build_subject, resolve_recipient, send_report
from .latest_json import write_latest
from .live_research import build_live_snapshot, resolve_mode
from .mock_data import build_mock_snapshot
from .pdf_report import pdf_filename, render_pdf
from .qa import qa_file, validate_pdf_bytes

log = logging.getLogger(__name__)


def _output_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "output" / "pdf"


def generate(
    report_day: date | None = None,
    *,
    mode: str | None = None,
    web_fetch: bool | None = None,
    llm_polish: bool | None = None,
    force_llm: bool = False,
) -> tuple[object, Path]:
    resolved = resolve_mode(mode)
    if resolved == "mock":
        snapshot = build_mock_snapshot(report_day)
    else:
        snapshot = build_live_snapshot(
            report_day,
            web_fetch=web_fetch,
            llm_polish=llm_polish,
            force_llm=force_llm,
        )

    pdf_bytes = render_pdf(snapshot)
    errs = validate_pdf_bytes(pdf_bytes)
    if errs:
        raise RuntimeError("PDF QA failed:\n- " + "\n- ".join(errs))
    out = _output_dir()
    out.mkdir(parents=True, exist_ok=True)
    path = out / pdf_filename(snapshot)
    path.write_bytes(pdf_bytes)
    latest, public_latest = write_latest(snapshot)
    log.info("wrote %s (%s bytes) mode=%s", path, len(pdf_bytes), resolved)
    log.info("latest json %s ; ui %s", latest, public_latest)
    return snapshot, path


def run_daily(
    *,
    dry_run: bool = True,
    report_day: date | None = None,
    force: bool = False,
    mode: str | None = None,
    web_fetch: bool | None = None,
    llm_polish: bool | None = None,
    force_llm: bool = False,
) -> int:
    try:
        snapshot, path = generate(
            report_day,
            mode=mode,
            web_fetch=web_fetch,
            llm_polish=llm_polish,
            force_llm=force_llm,
        )
    except Exception as exc:  # noqa: BLE001
        log.error("generate failed: %s", exc)
        return 3
    file_errs = qa_file(path)
    if file_errs:
        log.error("qa_file failed: %s", file_errs)
        return 3
    pdf_bytes = path.read_bytes()
    result = send_report(
        snapshot,
        pdf_bytes,
        path.name,
        dry_run=dry_run,
        force=force,
    )
    if not result.ok:
        log.error("send failed: %s", result.message)
        return 4
    print(
        f"OK dry_run={result.dry_run} mode={resolve_mode(mode)} "
        f"mock={getattr(snapshot, 'is_mock', True)} "
        f"to={resolve_recipient()} subject={build_subject(snapshot)!r} "
        f"attachment={path.name} key={result.idempotency_key}"
    )
    return 0
