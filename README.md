**Version:** 0.2.7

One-Idea passive-income research for a defined operator profile (software / .NET / cloud / AI / eng-management; Austin, US; wealth-building stage).

- **Product URL:** https://passive.xingai.app/ (public demo)
- **Repository:** https://github.com/xingaiapp/xingai-passive-income-ideas (public)

## Current version notes (0.2.7)

- ADR-003 CQRS publish boundary (worker writes / shell reads) + Cursor rule; PLAN/ADR index updated.

## Previous notes (0.2.6)

- Privacy Policy rewritten for this product (no Daily Assistant / Gmail paste).
- Honest “latest snapshot” copy — daily cadence returns when the worker runs.
- FAQ JSON-LD includes the 4th question (no income guarantee).
- Repo visibility set public so the catalog GitHub CTA works.

## What this product does

- Picks **exactly one** Idea per day (continuity over novelty).
- Delivers like 《XingAI 每日投资智报》: short email **Summary** (简体中文) + full **A4 PDF**.
- Separates facts / inference / recommendations; cites sources; marks `未核实`.
- Separates **investment returns** vs **business revenue**. No gambling-style or leveraged schemes.

## Stack

| Layer | Path |
|-------|------|
| Public Next.js shell | repo root — Today/Archive read `public/data/*.json` + PDF under `public/reports/` |
| Report worker | `worker/` — catalog pick + web probe + optional LLM polish → PDF → Resend |

## Local development (web)

```bash
npm install
npm run dev
```

Open http://localhost:3000.

## Report worker (live)

```bash
cd worker
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m passive_income_ideas generate                 # live + web probe + LLM if key set
python -m passive_income_ideas generate --no-web --no-llm
python -m passive_income_ideas generate --force-llm     # fail if no OpenAI key
python -m passive_income_ideas run-daily                # dry-run email
# python -m passive_income_ideas run-daily --live
```

Config: `worker/config/operator_profile.yaml` (`web_fetch`, `llm_polish`), `idea_catalog.yaml`, `idea_locales.yaml` (en/ko UI packs), SQLite under `worker/data/`.

**Web research:** probes catalog source URLs (reachability + page title). Never invents market facts from HTML. Failures → `verified=false` + `未核实`.

**Published web artifacts:** each generate writes `public/data/latest-idea.json` (including `locales.en|zh|ko`), dated `public/data/ideas/YYYY-MM-DD.json`, `public/data/archive-index.json`, and copies the PDF to `public/reports/`. PDF/email stay 简体中文; the public UI follows the language switcher.

**LLM polish (optional):** `OPENAI_API_KEY` or `PASSIVE_INCOME_OPENAI_API_KEY` polishes Chinese copy only; strips new URLs and new money tokens. No key → keep catalog copy.

See [`.env.example`](./.env.example). Never commit secrets.

## Current version notes

### 0.2.5

- Idea body follows EN / 中文 / 한국어 (no more EN chrome + Chinese copy mix).
- Desktop Today layout stacks full-width Idea panel under the intro (readable, not clipped).
- Docs: [ADR 002](docs/adr/002-worker-publish-static-ui.md) — worker static publish + read-only UI.
- Docs: [ADR 003](docs/adr/003-cqrs-publish-boundary.md) — hard CQRS rule (worker writes / shell reads); Cursor rule `.cursor/rules/cqrs-publish-boundary.mdc`.

### 0.2.4

- Desktop Today layout: sticky intro column + full-width Idea panel; decorative strip mobile-only; wider main + narrower sidebar.

### 0.2.3

- Today page shows full live fields (scores, capital, evidence, day-7, clickable sources).
- Archive index + public PDF publish path for real on-site data.
- Covered by [ADR 002](docs/adr/002-worker-publish-static-ui.md).

### 0.2.2

- Confirmed deploy: `passive.xingai.app` live; PLAN/dot-app launch status updated.

### 0.2.1

- Web source probing + optional OpenAI polish (fail-closed; `--no-web` / `--no-llm` / `--force-llm`).

### 0.2.0

- Live research MVP: operator YAML + catalog, SQLite memory, Today UI wire-up, launchd script.

### 0.1.7–0.1.0

- Light default theme, button centering, ledger-dusk redesign, project-init shell, rename, mock worker, scaffold.

## Disclaimer

See [`DISCLAIMER.md`](./DISCLAIMER.md). Informational only — not financial advice.

## License

Proprietary — XingAI private repository.
