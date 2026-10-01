# ADR 003: CQRS publish boundary — worker writes, shell reads

- **Status:** Accepted
- **Date:** 2026-09-07
- **Layer:** Worker / Frontend / Data
- **Related:** [ADR 002](002-worker-publish-static-ui.md) (artifact list + locales); Invest AI [ADR-008 CQRS cache](https://github.com/xingaiapp/xingai-invest-ai/blob/main/docs/adr/008-cqrs-cache-pattern.md) (same rule, different store)

## Context

ADR 002 already says the Next.js shell is read-only against published JSON/PDF. That line is easy to blur: a “quick” Route Handler that re-probes URLs, an on-demand LLM polish for EN copy, or React that reverse-engineers fit/income from raw fields.

This product has **no FastAPI** today. The shared “cache” is the committed (or deploy-bundled) tree under `public/data/` and `public/reports/`. CQRS still applies: **one writer path, many readers, no request-time Idea computation.**

## Decision

```text
Worker (generate / run-daily)  =  computes Idea + writes artifacts
Next.js public shell           =  reads artifacts + renders / localizes
React                          =  presents fields; does not decide
```

### Hard rules

1. **Worker is the only writer of Idea truth.** Catalog pick, continuity/memory, web probe, optional LLM polish, PDF QA, and locale pack assembly run in `worker/` (`generate` / `run-daily`), never in Next `app/api` or Server Actions.
2. **Published artifacts are the contract.** Readers consume:
   - `public/data/latest-idea.json` (incl. `locales.*`)
   - `public/data/ideas/YYYY-MM-DD.json`
   - `public/data/archive-index.json`
   - `public/reports/*.pdf`
3. **Shell may only read and present.** Allowed: `readFile` / static serve of those files, i18n chrome strings, merging a precomputed `locales[lang]` pack, links, theme/locale prefs. Not allowed on the request path: re-score Ideas, Jaccard dedupe, URL probing, LLM calls, inventing income bands, or patching evidence text.
4. **Stale is better than fake.** If artifacts are missing or old, show mock/empty/fallback UI — do not silently recompute a “fresh” Idea in Vercel to hide a missed worker run.
5. **New decision fields follow the same order as Invest:** add to worker snapshot → publish JSON → then render. UI never invents a score the worker did not write.
6. **Email/PDF stay worker-owned.** Resend send and ReportLab render are command-side; the site may link the published PDF but must not regenerate it per page view.

### Why CQRS here

| Pressure | How the split helps |
|---|---|
| Honest `未核实` | Probe/LLM stay offline; request path cannot “helpfully” fill gaps |
| Cost / rate limits | URL probes and optional OpenAI run once per generate, not per visitor |
| Deploy simplicity | Vercel serves static JSON; no live research credentials required on the web app |
| Testability | UI tests fixture JSON; worker tests catalog + memory without Next |

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| **On-demand research in Next Route Handlers** | Couples every visitor to probes/LLM; breaks fail-closed and cost control |
| **Client-side “research” fetch** | Even worse: secrets, CORS, inventable numbers in the browser |
| **FastAPI read API in front of SQLite** (Invest-shaped) | Valid later if we need auth/rate limits; not required while static publish works. If added, it must stay **read-only** against worker-written rows — same CQRS side as Invest FastAPI |

## Consequences

- Agents and PRs that add “just one API route to refresh today’s Idea” violate this ADR unless they only *trigger* an offline job and still serve last published artifacts.
- Cursor rule: `.cursor/rules/cqrs-publish-boundary.mdc`.
- Deeper open-web research = worker/command-side ADR only.

## Known limitations

- Today the “write” often lands by committing/deploying `public/` after a local `generate`. That is still worker-owned compute; CI/cron may replace the human step without moving compute into Next.
- Locale merge in the browser is presentation, not a new decision.

## Related

- Code: `worker/src/passive_income_ideas/pipeline.py`, `live_research.py`, `latest_json.py`; UI `src/lib/latest-idea.ts`, `src/lib/idea-locale.ts`
- Cross-repo: [xingai-invest-ai ADR-008](https://github.com/xingaiapp/xingai-invest-ai/blob/main/docs/adr/008-cqrs-cache-pattern.md), [ADR-012 decision-cache boundary](https://github.com/xingaiapp/xingai-invest-ai/blob/main/docs/adr/012-decision-cache-boundary.md)
