from __future__ import annotations

import logging
import re
import urllib.error
import urllib.request
from dataclasses import replace
from datetime import date, datetime, timezone
from html import unescape
from typing import Iterable

from .models import UNVERIFIED, EvidenceItem, IdeaSnapshot, SourceRef

log = logging.getLogger(__name__)

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
_UA = "XingAI-PassiveIncomeIdeas/0.2 (+https://passive.xingai.app; research-probe)"


def _extract_title(html: str) -> str:
    m = _TITLE_RE.search(html or "")
    if not m:
        return ""
    title = unescape(re.sub(r"\s+", " ", m.group(1))).strip()
    return title[:160]


def probe_url(url: str, *, timeout: float = 12.0) -> tuple[bool, int, str]:
    """Return (ok, http_status, page_title_or_error). Does not invent facts from body."""
    if not url.startswith(("http://", "https://")):
        return False, 0, "invalid url"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": _UA, "Accept": "text/html,application/xhtml+xml"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = int(getattr(resp, "status", 200) or 200)
            raw = resp.read(80_000)
            charset = "utf-8"
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "charset=" in ctype:
                charset = ctype.split("charset=", 1)[1].split(";")[0].strip() or "utf-8"
            text = raw.decode(charset, errors="replace")
            title = _extract_title(text)
            ok = 200 <= status < 400
            return ok, status, title or f"http {status}"
    except urllib.error.HTTPError as exc:
        return False, int(exc.code), f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001
        return False, 0, f"fetch error: {exc}"


def enrich_sources(
    sources: dict[str, SourceRef],
    *,
    as_of: str | None = None,
) -> dict[str, SourceRef]:
    """Probe each catalog URL. Fail-closed: unreachable → verified=False."""
    day = as_of or date.today().isoformat()
    out: dict[str, SourceRef] = {}
    for sid, src in sources.items():
        ok, status, detail = probe_url(src.url)
        if ok:
            note_bits = [src.note] if src.note else []
            note_bits.append(f"web probe OK {day} (HTTP {status})")
            if detail and detail.lower() not in (src.title or "").lower():
                note_bits.append(f"page title: {detail}")
            out[sid] = replace(
                src,
                verified=bool(src.verified),  # keep catalog verified only if still reachable
                note="；".join(x for x in note_bits if x),
                as_of=day if src.verified else src.as_of,
            )
            log.info("web probe ok %s %s", sid, src.url)
        else:
            note = f"{src.note + '；' if src.note else ''}{UNVERIFIED}：web probe failed ({detail})"
            out[sid] = replace(src, verified=False, note=note)
            log.warning("web probe fail %s %s — %s", sid, src.url, detail)
    return out


def evidence_from_probes(
    sources: dict[str, SourceRef],
    existing: Iterable[EvidenceItem],
) -> tuple[EvidenceItem, ...]:
    """Append reachability inferences only — never turn probes into market facts."""
    items = list(existing)
    reachable = [sid for sid, s in sources.items() if "web probe OK" in (s.note or "")]
    failed = [sid for sid, s in sources.items() if "web probe failed" in (s.note or "")]
    if reachable:
        items.append(
            EvidenceItem(
                kind="inference",
                text=(
                    f"已对目录来源做可达性探测：{', '.join(reachable)} 可打开。"
                    f"这不证明市场需求或收入数字。"
                ),
                source_ids=tuple(reachable),
            )
        )
    if failed:
        items.append(
            EvidenceItem(
                kind="inference",
                text=f"以下来源探测失败，已标 {UNVERIFIED}：{', '.join(failed)}。",
                source_ids=tuple(failed),
            )
        )
    # Re-apply fact fail-closed after probe may have cleared verified
    fixed: list[EvidenceItem] = []
    for ev in items:
        if ev.kind == "fact":
            for sid in ev.source_ids:
                src = sources.get(sid)
                if src is None or not src.verified:
                    ev = EvidenceItem(
                        kind="inference",
                        text=f"{ev.text}（{UNVERIFIED}：来源未核实或探测失败）",
                        source_ids=ev.source_ids,
                    )
                    break
        fixed.append(ev)
    return tuple(fixed)


def enrich_snapshot_web(snapshot: IdeaSnapshot) -> IdeaSnapshot:
    enriched = enrich_sources(snapshot.sources)
    evidence = evidence_from_probes(enriched, snapshot.market_evidence)
    return replace(snapshot, sources=enriched, market_evidence=evidence)
