# Passive Income Idea 智报 — Delivery Plan

> Status: **0.2.4** — live at passive.xingai.app  
> Reviewed: 2026-09-06

## Phase 0 — Contract

- [x] Private GitHub repo + README / DISCLAIMER / PLAN
- [x] ADR-001: product boundary (personal daily Idea report vs Invest 智报 vs Opportunity Radar)
- [x] project-init public shell (chrome, i18n, theme, legal, SEO/AEO, dot-app Soon)
- [x] Operator profile config (age/locale/skills/constraints) as versioned YAML
- [x] Idea memory store (SQLite) for anti-repeat + “still best → progress update”

## Phase 1 — Offline MVP (worker)

- [x] Snapshot dataclasses (`IdeaSnapshot` + evidence/source types)
- [x] Mock-first research snapshot + Austin/53/.NET profile fixture
- [x] ReportLab PDF (XingAI 智报 visual template, 13 sections)
- [x] PDF text/section QA gate (`pypdf`; render-to-image still optional later)
- [x] Email Summary (简体中文) + Resend dry-run / `--live`
- [x] CLI: `generate | validate-pdf | send | run-daily`

## Phase 2 — Live research

- [x] Source adapters + `未核实` fail-closed (catalog + verified flags)
- [x] Dedup / continuity policy (SQLite + Jaccard)
- [x] Scheduled run + idempotent send (launchd plist + existing send logs)
- [x] Wire Today UI to real latest Idea (`public/data/latest-idea.json`)
- [x] Publish full snapshot fields + sources/evidence/day7 + public PDF + archive index

## Phase 3 — Product surface polish

- [x] Public shell targeting `passive.xingai.app`
- [x] Live `launchStatus` when domain is up
- [ ] Optional auth (new Google OAuth client)
- [x] Broader live web research / optional LLM polish (still fail-closed)

## PDF fixed outline

1. Cover — Executive Action Summary  
2. 今日唯一主 Idea  
3. 适合度与被动程度评分  
4. 市场与需求证据  
5. 商业模式与收入模型  
6. 启动成本与时间投入  
7. 竞争与差异化  
8. 今日 30 分钟行动  
9. 7 天 MVP 逐日步骤  
10. 30 天目标  
11. 自动化路线  
12. 风险、停止条件与替代方案  
13. 来源与时间戳  

## Hard visual rules

A4 white; text `#000000`; Noto Sans SC Regular/Bold; cover ≥22pt; H1 ≥17pt; body ≥10.5pt; table ≥8.5pt (min 8.2pt); exec `#FFF4CC` + `#E07000`; wrap-safe cells; QA before attach.

## project-init checklist

- [x] Mobile ~375px; top + drawer + bottom tabs; desktop side menu open/collapse
- [x] Icon + hero light/dark + OG
- [x] en / zh / ko; light/dark; legal EN+zh+ko
- [x] metadata, sitemap, robots, llms.txt, FAQ + JSON-LD
- [x] xingai-dot-app Soon registration
- [x] Deploy + DNS `passive.xingai.app`
- [ ] Google OAuth (deferred)
