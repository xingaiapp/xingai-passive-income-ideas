"""CLI: python -m passive_income_ideas <command>"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path


def _parse_day(raw: str | None) -> date | None:
    if not raw:
        return None
    return date.fromisoformat(raw)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(prog="passive_income_ideas")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gen = sub.add_parser("generate", help="Render PDF + write latest-idea.json")
    p_gen.add_argument("--date", help="YYYY-MM-DD (default: today)")
    p_gen.add_argument("--mode", choices=("live", "mock"), help="Override research.mode")

    p_val = sub.add_parser("validate-pdf", help="QA an existing PDF file")
    p_val.add_argument("path", type=Path)

    p_send = sub.add_parser("send", help="Generate + email (dry-run unless --live)")
    p_send.add_argument("--date", help="YYYY-MM-DD")
    p_send.add_argument("--live", action="store_true", help="Actually call Resend")
    p_send.add_argument("--force", action="store_true", help="Bypass idempotency lock")
    p_send.add_argument("--mode", choices=("live", "mock"))

    p_run = sub.add_parser("run-daily", help="Same as send (daily entrypoint)")
    p_run.add_argument("--date", help="YYYY-MM-DD")
    p_run.add_argument("--live", action="store_true")
    p_run.add_argument("--force", action="store_true")
    p_run.add_argument("--mode", choices=("live", "mock"))

    args = parser.parse_args(argv)

    if args.cmd == "generate":
        from .pipeline import generate

        snap, path = generate(_parse_day(args.date), mode=getattr(args, "mode", None))
        print(
            f"wrote {path} idea={snap.idea_name!r} date={snap.report_date} "
            f"mock={snap.is_mock} continuity={snap.continuity}"
        )
        return 0

    if args.cmd == "validate-pdf":
        from .qa import qa_file

        errs = qa_file(args.path)
        if errs:
            print("FAIL")
            for e in errs:
                print(f"- {e}")
            return 3
        print(f"OK {args.path}")
        return 0

    if args.cmd in {"send", "run-daily"}:
        from .pipeline import run_daily

        return run_daily(
            dry_run=not args.live,
            report_day=_parse_day(args.date),
            force=args.force,
            mode=getattr(args, "mode", None),
        )

    parser.error(f"unknown command {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
