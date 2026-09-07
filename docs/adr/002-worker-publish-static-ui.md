# ADR 002: Worker publish path — static Idea artifacts for the public UI

- **Status:** Accepted
- **Date:** 2026-09-07
- **Layer:** Worker / Frontend / Data
- **Related:** [ADR 001](001-product-boundary.md)

## Context

ADR 001 allowed the public shell to show a mock Idea until the worker was live, and treated email/PDF as the primary decision artifact.

By **0.2.3–0.2.5** the worker was live and `passive.xingai.app` was reading thin or Chinese-only JSON while the chrome followed EN/zh/ko. We needed a clear boundary: who computes the Idea, what gets published, and how the UI stays honest across locales without inventing facts at request time.

## Decision

1. **Worker owns research and publish.** `python -m passive_income_ideas generate` (catalog pick, optional web probe, optional LLM polish, PDF QA) writes:
   - `public/data/latest-idea.json`
   - `public/data/ideas/YYYY-MM-DD.json`
   - `public/data/archive-index.json`
   - `public/reports/XingAI_Daily_Passive_Income_Idea_Report_YYYY-MM-DD.pdf`
2. **Public shell is read-only.** Next.js loads those static files at build/request time. It does **not** re-score Ideas, probe sources, call LLMs, or invent income numbers. (Same CQRS spirit as Invest AI: compute offline, serve precomputed.)
3. **Root snapshot fields stay 简体中文** for PDF + email Summary. UI language packs live under `locales.en` / `locales.zh` / `locales.ko` in the same JSON (`idea_locales.yaml` + operator `i18n`). The language switcher merges a pack client-side; missing pack → root Chinese fields.
4. **Fail-closed labeling stays.** Income bands and unverified claims use `未核实`. Web research is reachability (+ title) on catalog URLs only — never market facts scraped from page bodies.
5. **ADR 001 §4 is superseded for “mock until live.”** Live UI shows the published snapshot; mock remains only for offline fixtures / missing file fallback.

## Consequences

- Deploying a new Idea means running the worker (or CI) then shipping the updated `public/` artifacts with the Next app (Vercel).
- Resend `--live` and launchd stay separate from the site publish path.
- Enriching open-web research beyond URL probes is a future ADR; it must not move computation into Next route handlers.
- Google OAuth remains optional and out of scope here.

## Known limitations

- Locale packs are curated YAML, not machine translation of every PDF section.
- Continuity “progress” text is generated per locale at publish time from the same SQLite memory; wiping local `idea_memory.sqlite` resets pick history (gitignored).
- Source probe notes on the Chinese root may still appear in English page titles after a probe; locale packs override `source_notes` where provided.

## Related

- Config: `worker/config/idea_catalog.yaml`, `worker/config/idea_locales.yaml`, `worker/config/operator_profile.yaml`
- Publish: `worker/src/passive_income_ideas/latest_json.py`, `localize.py`
- UI: `src/lib/idea-locale.ts`, `src/components/today-client.tsx`
