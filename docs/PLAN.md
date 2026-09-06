# Passive Income Idea 智报 — Delivery Plan

> Status: **repo bootstrap only** (2026-09-06). No generator yet.

## Phase 0 — Contract

- [x] Private GitHub repo + README / DISCLAIMER / PLAN
- [ ] ADR-001: product boundary (personal daily Idea report vs Invest 智报 vs Opportunity Radar)
- [ ] Operator profile config (age/locale/skills/constraints) as versioned YAML
- [ ] Idea memory store (SQLite/Turso) for anti-repeat + “still best → progress update”

## Phase 1 — Offline MVP

- [ ] Pydantic snapshot models (Idea, fit scores, capital, hours, revenue band, sources, risks)
- [ ] Mock-first research snapshot + fixtures
- [ ] ReportLab PDF renderer matching XingAI 智报 visual template (A4, Noto Sans SC, black text, yellow/orange accents)
- [ ] PDF render-to-image QA gate (no Thin/Light fonts; all text #000000; in-bounds)
- [ ] Email Summary builder (简体中文) + Resend send (dry-run default)
- [ ] CLI: `generate | validate-pdf | send | run-daily`

## Phase 2 — Live research

- [ ] Source adapters with citations + `未核实` fail-closed
- [ ] Dedup / continuity policy against Idea memory
- [ ] Scheduled run (GitHub Actions or worker cron)
- [ ] Idempotent send per calendar day

## Phase 3 — Product surface (optional)

- [ ] Public or gated UI only if needed; then full project-init (chrome, en/zh/ko, legal, SEO/AEO, `xingai-dot-app`)

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

Shared XingAI 日报 PDF template: A4 white; all text `#000000`; Noto Sans SC Regular/Bold only; cover title ≥22pt; H1 ≥17pt; body ≥10.5pt; table ≥8.5pt (footer/sources ≥8.2pt min); exec summary `#FFF4CC` fill + `#E07000` border; wrap-safe table cells; QA render before attach.
