# ADR 001: Product boundary — personal Passive Income Idea 智报

- **Status:** Accepted
- **Date:** 2026-09-06
- **Layer:** Product / Report worker + public shell
- **Related:** [ADR 002](002-worker-publish-static-ui.md) (live static publish path)

## Context

XingAI already has:

- **Invest AI `investment_zhibao`** — daily *investment* PDF + email for holdings/macro.
- **Opportunity Radar** — XingAI *portfolio product* opportunities.
- **Founder AI** — founder brief / radar for startups.

The new product needs a clear job: one daily **personal** passive-income / cash-flow Idea for a defined operator profile, with the same delivery craft as Invest 智报.

## Decision

1. **Repo** `xingai-passive-income-ideas` (renamed from `xingai-passive-income-zhibao`) owns both:
   - Next.js public shell at `passive.xingai.app` (project-init baseline),
   - Python report worker under `worker/` (PDF + Resend), modeled on Invest `investment_zhibao`.
2. **Not** a fork of Opportunity Radar or Founder Brief content pipelines.
3. **Strict separation** of investment returns vs business revenue in all copy and models.
4. *(Historical)* Public UI may show mock Idea until worker is live; email/PDF remain the primary decision artifact. **Superseded for the live path by [ADR 002](002-worker-publish-static-ui.md).**

## Consequences

- dot-app registration uses slug `passive-income`, domain `passive.xingai.app`, initially `coming-soon` until deploy.
- Shared 智报 visual PDF template rules stay aligned with Invest AI ADR-040/042 craft, without sharing Invest decision cache.
