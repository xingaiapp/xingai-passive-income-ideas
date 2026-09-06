from __future__ import annotations

import base64
import json
import logging
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from .models import IdeaSnapshot, SendResult

log = logging.getLogger(__name__)


def _logs_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "logs"


def build_subject(snapshot: IdeaSnapshot) -> str:
    return f"XingAI 每日被动收入 Idea 智报｜{snapshot.report_date}｜今日Idea：{snapshot.idea_name}"


def build_body(snapshot: IdeaSnapshot) -> str:
    mock = "【模拟报告 — fixture】\n" if snapshot.is_mock else ""
    return (
        f"{mock}"
        f"今日结论：{snapshot.idea_name}\n"
        f"{snapshot.one_liner}\n\n"
        f"为什么适合我：\n{snapshot.why_fit}\n\n"
        f"现实收入区间：\n{snapshot.income_band}\n\n"
        f"今天做什么：\n{snapshot.do_today}\n\n"
        f"今天不要做什么：\n{snapshot.dont_today}\n\n"
        f"最大风险：\n{snapshot.biggest_risk}\n\n"
        f"PDF 附件：完整详细内容与执行步骤见附件 "
        f"XingAI_Daily_Passive_Income_Idea_Report_{snapshot.report_date}.pdf\n\n"
        f"{snapshot.disclaimer}\n"
    )


def idempotency_key(report_date: str, recipient: str) -> str:
    return f"passive-income-zhibao:{report_date}:{recipient.strip().lower()}"


def already_sent(key: str) -> bool:
    path = _logs_dir() / f"sent-{key.replace(':', '_')}.json"
    return path.exists()


def mark_sent(key: str, payload: dict) -> Path:
    _logs_dir().mkdir(parents=True, exist_ok=True)
    path = _logs_dir() / f"sent-{key.replace(':', '_')}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def resolve_recipient() -> str:
    return (
        os.environ.get("PASSIVE_INCOME_REPORT_TO")
        or os.environ.get("INVEST_AI_PICK_EMAIL_TO")
        or "xing@xingai.app"
    ).strip()


def resolve_from() -> str:
    return (
        os.environ.get("PASSIVE_INCOME_REPORT_FROM")
        or os.environ.get("INVEST_AI_PICK_EMAIL_FROM")
        or os.environ.get("INVEST_AI_PICK_EMAIL_FALLBACK_FROM")
        or "XingAI Passive Income <onboarding@resend.dev>"
    ).strip()


def send_report(
    snapshot: IdeaSnapshot,
    pdf_bytes: bytes,
    pdf_name: str,
    *,
    dry_run: bool = True,
    force: bool = False,
) -> SendResult:
    recipient = resolve_recipient()
    key = idempotency_key(snapshot.report_date, recipient)
    if already_sent(key) and not force and not dry_run:
        return SendResult(False, False, "duplicate send blocked — pass force=True to override", key)

    subject = build_subject(snapshot)
    body = build_body(snapshot)

    if dry_run:
        mark_sent(
            key + f"-dryrun-{int(time.time())}",
            {
                "dry_run": True,
                "to": recipient,
                "subject": subject,
                "pdf_name": pdf_name,
                "pdf_bytes": len(pdf_bytes),
                "body_preview": body[:500],
            },
        )
        log.info("dry-run ok subject=%s to=%s pdf=%s (%s bytes)", subject, recipient, pdf_name, len(pdf_bytes))
        return SendResult(True, True, "dry-run ok", key)

    api_key = (
        os.environ.get("PASSIVE_INCOME_RESEND_API_KEY")
        or os.environ.get("INVEST_AI_RESEND_API_KEY")
        or os.environ.get("RESEND_API_KEY")
        or ""
    ).strip()
    if not api_key:
        return SendResult(False, False, "missing RESEND_API_KEY / INVEST_AI_RESEND_API_KEY", key)

    enabled = (os.environ.get("PASSIVE_INCOME_REPORT_ENABLED") or "").strip().lower()
    if enabled in {"0", "false", "no"}:
        return SendResult(False, False, "PASSIVE_INCOME_REPORT_ENABLED is false", key)

    payload = {
        "from": resolve_from(),
        "to": [recipient],
        "subject": subject,
        "text": body,
        "attachments": [
            {
                "filename": pdf_name,
                "content": base64.b64encode(pdf_bytes).decode("ascii"),
            }
        ],
        "headers": {"Idempotency-Key": key},
    }
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            mark_sent(
                key,
                {
                    "dry_run": False,
                    "to": recipient,
                    "subject": subject,
                    "pdf_name": pdf_name,
                    "response": raw,
                },
            )
            return SendResult(True, False, f"sent ok http={resp.status}", key)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return SendResult(False, False, f"Resend HTTP {exc.code}: {detail[:500]}", key)
    except Exception as exc:  # noqa: BLE001
        return SendResult(False, False, f"send failed: {exc}", key)
