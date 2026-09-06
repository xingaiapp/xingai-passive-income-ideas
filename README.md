**Version:** 0.1.7

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
| Public Next.js shell | repo root (`src/app`) — chrome, en/zh/ko, light/dark, legal, SEO/AEO |
| Report worker | `worker/` — mock Idea → ReportLab PDF → Resend (dry-run default) |

## Local development (web)

```bash
npm install
npm run dev
```

Open http://localhost:3000. Set `NEXT_PUBLIC_SITE_URL=https://passive.xingai.app` for production metadata.

## Report worker (Phase 1)

```bash
cd worker
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m passive_income_ideas generate
python -m passive_income_ideas run-daily          # dry-run email log
# python -m passive_income_ideas run-daily --live  # needs RESEND_API_KEY
```

PDF lands in `worker/output/pdf/`. Fonts: optional `worker/assets/NotoSansSC-*.ttf` (TrueType; see `worker/assets/README.md`). macOS falls back to system CJK fonts.

Env: see [`.env.example`](./.env.example). Default recipient `PASSIVE_INCOME_REPORT_TO=xing@xingai.app`. Never commit secrets.

Optional Google OAuth (not required for v0.1 shell): create a **new** OAuth client before login ships — do not reuse another product’s client.

- Prod callback: `https://passive.xingai.app/api/auth/callback/google`
- Local: `http://localhost:3000/api/auth/callback/google`

## Current version notes

### 0.1.7

- Default theme is light (system preference no longer auto-enables dark).

### 0.1.6

- Fix CTA button label vertical centering (`inline-flex` + center).

### 0.1.5

- Visual redesign (“Ledger dusk”): lilac paper + ink navy + apricot (not default green); Outfit + Fraunces; refreshed hero/OG/icon.

### 0.1.4

- project-init visual hard gate: product-specific hero light/dark + OG, logo/`icon.svg`, SVG nav icons (Today/Archive/How), primary-route entrance + CTA + fact stagger motion with `prefers-reduced-motion`.

### 0.1.3

- Renamed repo/package to `xingai-passive-income-ideas` (Python module `passive_income_ideas`). Product slug/domain unchanged (`passive-income` / `passive.xingai.app`).

### 0.1.2

- Worker Phase 1: mock Idea snapshot, ReportLab A4 PDF (13 sections, black text / yellow exec box), PDF QA (`pypdf`), 简体中文 email Summary + Resend dry-run / `--live`, CLI `generate | validate-pdf | send | run-daily`.
- Offline pytest covers PDF QA + dry-run send.

### 0.1.1

- **project-init baseline:** Next.js mobile chrome (top + drawer + bottom tabs + desktop side nav), en/zh/ko, light/dark, legal EN/zh/ko, robots/sitemap/llms.txt, hero light/dark, mock Today Idea board.
- Registered on xingai-dot-app as **Soon** (`passive-income` → `passive.xingai.app`).

### 0.1.0

- Private repo scaffold + PLAN + DISCLAIMER only.

## Disclaimer

See [`DISCLAIMER.md`](./DISCLAIMER.md). Informational only — not financial advice.

## License

Proprietary — XingAI private repository.
