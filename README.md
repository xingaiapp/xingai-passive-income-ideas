**Version:** 0.2.0

Daily **one-Idea** passive-income research for a defined operator profile (software / .NET / cloud / AI / eng-management; Austin, US; wealth-building stage).

- **Product URL (target):** https://passive.xingai.app/
- **Repository:** https://github.com/xingaiapp/xingai-passive-income-ideas (private)

## What this product does

- Picks **exactly one** Idea per day (continuity over novelty).
- Delivers like 《XingAI 每日投资智报》: short email **Summary** (简体中文) + full **A4 PDF**.
- Separates facts / inference / recommendations; cites sources; marks `未核实`.
- Separates **investment returns** vs **business revenue**. No gambling-style or leveraged schemes.

## Stack

| Layer | Path |
|-------|------|
| Public Next.js shell | repo root — Today reads `public/data/latest-idea.json` |
| Report worker | `worker/` — live catalog pick + SQLite memory → PDF → Resend |

## Local development (web)

```bash
npm install
npm run dev
```

Open http://localhost:3000. Set `NEXT_PUBLIC_SITE_URL=https://passive.xingai.app` for production metadata.

## Report worker (live)

```bash
cd worker
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m passive_income_ideas generate              # live mode (default)
python -m passive_income_ideas generate --mode mock  # offline fixture
python -m passive_income_ideas run-daily             # dry-run email
# python -m passive_income_ideas run-daily --live    # needs RESEND_API_KEY + ENABLED
```

Config:

- `worker/config/operator_profile.yaml` — profile + `research.mode`
- `worker/config/idea_catalog.yaml` — curated Idea pool (fail-closed sources)
- `worker/data/idea_memory.sqlite` — anti-repeat / continuity (gitignored)

Outputs: PDF under `worker/output/pdf/`, JSON under `worker/output/json/`, UI copy at `public/data/latest-idea.json`.

### Schedule (macOS)

1. Put Resend secrets in your shell env or a local (untracked) env file loaded by launchd.
2. Edit paths in `worker/scripts/com.xingai.passive-income-ideas.plist` if needed.
3. `chmod +x worker/scripts/run-daily.sh`
4. `launchctl load worker/scripts/com.xingai.passive-income-ideas.plist`

Default calendar: 07:10 local. Test with dry-run first (remove `--live` from the plist).

Env: see [`.env.example`](./.env.example). Default recipient `PASSIVE_INCOME_REPORT_TO=xing@xingai.app`. Never commit secrets.

## Current version notes

### 0.2.0

- **Live research MVP:** operator YAML + idea catalog, SQLite anti-repeat/continuity, fail-closed `未核实`, `generate` writes `latest-idea.json`, Today UI renders live Idea, `run-daily` + launchd script for scheduled Resend.

### 0.1.7

- Default theme is light (system preference no longer auto-enables dark).

### 0.1.6

- Fix CTA button label vertical centering (`inline-flex` + center).

### 0.1.5

- Visual redesign (“Ledger dusk”): lilac paper + ink navy + apricot; Outfit + Fraunces.

### 0.1.4

- project-init visual hard gate: heroes, icons, motion.

### 0.1.3

- Renamed repo/package to `xingai-passive-income-ideas`.

### 0.1.2

- Worker Phase 1 mock PDF + Resend dry-run.

### 0.1.1

- project-init web shell + dot-app Soon.

### 0.1.0

- Private repo scaffold.

## Disclaimer

See [`DISCLAIMER.md`](./DISCLAIMER.md). Informational only — not financial advice.

## License

Proprietary — XingAI private repository.
