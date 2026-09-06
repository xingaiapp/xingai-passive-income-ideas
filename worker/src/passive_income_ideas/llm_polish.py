from __future__ import annotations

import json
import logging
import os
import re
import urllib.error
import urllib.request
from dataclasses import replace
from typing import Any

from .models import IdeaSnapshot

log = logging.getLogger(__name__)

_URL_RE = re.compile(r"https?://[^\s)\]\"'<>]+", re.I)
_MONEY_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?|\d+\s?%\s*(?:/|每)?\s*(?:月|年|mo|yr)?", re.I)

_POLISH_FIELDS = ("why_fit", "do_today", "dont_today", "biggest_risk", "one_liner")


def load_openai_key() -> tuple[str, str]:
    key = (
        os.environ.get("PASSIVE_INCOME_OPENAI_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    ).strip()
    model = (os.environ.get("PASSIVE_INCOME_OPENAI_MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-4o-mini").strip()
    return key, model


def _collect_urls(*texts: str) -> set[str]:
    found: set[str] = set()
    for t in texts:
        found.update(_URL_RE.findall(t or ""))
    return found


def _collect_money(*texts: str) -> set[str]:
    found: set[str] = set()
    for t in texts:
        for m in _MONEY_RE.findall(t or ""):
            found.add(re.sub(r"\s+", "", m.lower()))
    return found


def _sanitize_polish(
    original: IdeaSnapshot,
    polished: dict[str, str],
) -> dict[str, str]:
    allowed_urls = _collect_urls(
        original.why_fit,
        original.do_today,
        original.dont_today,
        original.biggest_risk,
        original.one_liner,
        original.income_band,
        original.business_model,
        *[s.url for s in original.sources.values()],
        *[s.note for s in original.sources.values()],
    )
    allowed_money = _collect_money(
        original.why_fit,
        original.do_today,
        original.dont_today,
        original.biggest_risk,
        original.one_liner,
        original.income_band,
        original.business_model,
        original.first_revenue_eta,
        original.startup_capital,
    )
    out: dict[str, str] = {}
    for field in _POLISH_FIELDS:
        text = str(polished.get(field) or "").strip()
        if not text:
            continue
        # Drop any newly invented URLs
        for url in _URL_RE.findall(text):
            if url not in allowed_urls:
                text = text.replace(url, "")
                log.warning("llm polish stripped new URL from %s: %s", field, url)
        # Drop new money tokens not in original snapshot
        for tok in _MONEY_RE.findall(text):
            norm = re.sub(r"\s+", "", tok.lower())
            if norm not in allowed_money:
                text = text.replace(tok, "")
                log.warning("llm polish stripped new money token from %s: %s", field, tok)
        text = re.sub(r"\s{2,}", " ", text).strip()
        if text:
            out[field] = text
    return out


def _call_openai(snapshot: IdeaSnapshot, key: str, model: str) -> dict[str, str]:
    system = (
        "You polish Chinese copy for a personal passive-income Idea report. "
        "Return ONLY JSON with keys: why_fit, do_today, dont_today, biggest_risk, one_liner. "
        "Rules: keep meaning; do not invent facts, URLs, companies, statistics, or income numbers "
        "that are not already in the input; do not remove 未核实 / estimate disclaimers; "
        "keep investment vs business revenue separation; concise, actionable Chinese."
    )
    user = json.dumps(
        {
            "idea_name": snapshot.idea_name,
            "one_liner": snapshot.one_liner,
            "why_fit": snapshot.why_fit,
            "do_today": snapshot.do_today,
            "dont_today": snapshot.dont_today,
            "biggest_risk": snapshot.biggest_risk,
            "income_band": snapshot.income_band,
            "income_kind": snapshot.income_kind,
            "continuity": snapshot.continuity,
        },
        ensure_ascii=False,
    )
    payload = {
        "model": model,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    content = body["choices"][0]["message"]["content"]
    data = json.loads(content)
    return {k: str(data.get(k) or "") for k in _POLISH_FIELDS}


def maybe_polish_snapshot(
    snapshot: IdeaSnapshot,
    *,
    force_llm: bool = False,
    enabled: bool = True,
) -> IdeaSnapshot:
    """Optional OpenAI polish. Fail-closed to original copy if no key / error / sanitize empty."""
    if not enabled:
        return snapshot
    key, model = load_openai_key()
    if not key:
        if force_llm:
            raise RuntimeError("OPENAI_API_KEY (or PASSIVE_INCOME_OPENAI_API_KEY) required with --force-llm")
        log.info("llm polish skipped — no API key")
        return snapshot
    try:
        raw = _call_openai(snapshot, key, model)
        polished = _sanitize_polish(snapshot, raw)
        if not polished:
            log.warning("llm polish produced empty safe fields; keeping original")
            return snapshot
        return replace(
            snapshot,
            why_fit=polished.get("why_fit") or snapshot.why_fit,
            do_today=polished.get("do_today") or snapshot.do_today,
            dont_today=polished.get("dont_today") or snapshot.dont_today,
            biggest_risk=polished.get("biggest_risk") or snapshot.biggest_risk,
            one_liner=polished.get("one_liner") or snapshot.one_liner,
        )
    except Exception as exc:  # noqa: BLE001
        if force_llm:
            raise
        log.warning("llm polish failed (%s); keeping original", exc)
        return snapshot
