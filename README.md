# XingAI Passive Income Idea 智报

**Version:** 0.1.1

Daily **one-Idea** passive-income research for a defined operator profile (software / .NET / cloud / AI / eng-management; Austin, US; wealth-building stage).

- **Product URL (target):** https://passive.xingai.app/
- **Repository:** https://github.com/xingaiapp/xingai-passive-income-zhibao (private)

## What this product does

- Picks **exactly one** Idea per day (continuity over novelty).
- Delivers like 《XingAI 每日投资智报》: short email **Summary** (简体中文) + full **A4 PDF**.
- Separates facts / inference / recommendations; cites sources; marks `未核实`.
- Separates **investment returns** vs **business revenue**. No gambling-style or leveraged schemes.

## Stack

| Layer | Path |
|-------|------|
| Public Next.js shell | repo root (`src/app`) — chrome, en/zh/ko, light/dark, legal, SEO/AEO |
| Report worker (scaffold) | `worker/` — PDF + Resend pipeline **not implemented yet** |

## Local development (web)

```bash
npm install
npm run dev
```

Open http://localhost:3000. Set `NEXT_PUBLIC_SITE_URL=https://passive.xingai.app` for production metadata.

## Environment

See [`.env.example`](./.env.example). Never commit secrets.

Optional Google OAuth (not required for v0.1 shell): create a **new** OAuth client before login ships — do not reuse another product’s client.

- Prod callback: `https://passive.xingai.app/api/auth/callback/google`
- Local: `http://localhost:3000/api/auth/callback/google`

## Current version notes

### 0.1.1

- **project-init baseline:** Next.js mobile chrome (top + drawer + bottom tabs + desktop side nav), en/zh/ko, light/dark, legal EN/zh/ko, robots/sitemap/llms.txt, hero light/dark, mock Today Idea board.
- Registered on xingai-dot-app as **Soon** (`passive-income` → `passive.xingai.app`).
- Python worker remains under `worker/` (CLI stub).

### 0.1.0

- Private repo scaffold + PLAN + DISCLAIMER only.

## Disclaimer

See [`DISCLAIMER.md`](./DISCLAIMER.md). Informational only — not financial advice.

## License

Proprietary — XingAI private repository.
