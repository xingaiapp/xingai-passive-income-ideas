# ADR 002：Worker 发布路径 — 面向公开 UI 的静态 Idea 产物

- **状态：** 已接受
- **日期：** 2026-09-07
- **层级：** Worker / Frontend / Data
- **相关：** [ADR 001](001-product-boundary.zh.md)

## 背景

ADR 001 允许公开站点在 worker 上线前展示模拟 Idea，并以邮件/PDF 为主要决策产物。

到 **0.2.3–0.2.5**，worker 已上线，`passive.xingai.app` 却仍可能读到过薄或仅中文的 JSON，而导航语言切换已是 EN/zh/ko。需要划清边界：谁计算 Idea、发布什么、UI 如何在多语言下保持诚实，且不在请求时编造事实。

## 决策

1. **Worker 负责研究与发布。** `python -m passive_income_ideas generate`（目录挑选、可选网页探测、可选 LLM 润色、PDF QA）写入：
   - `public/data/latest-idea.json`
   - `public/data/ideas/YYYY-MM-DD.json`
   - `public/data/archive-index.json`
   - `public/reports/XingAI_Daily_Passive_Income_Idea_Report_YYYY-MM-DD.pdf`
2. **公开站点只读。** Next.js 只加载上述静态文件。不在请求路径上重新打分、探测来源、调用 LLM 或编造收入数字。（与 Invest AI 的 CQRS 精神一致：离线计算，提供预计算结果。）
3. **根字段保持简体中文**，供 PDF + 邮件 Summary。UI 语言包放在同一 JSON 的 `locales.en` / `locales.zh` / `locales.ko`（`idea_locales.yaml` + operator `i18n`）。语言切换在客户端合并语言包；缺失则回退根中文字段。
4. **继续 fail-closed。** 收入区间与未核实主张标注 `未核实`。网页研究仅对目录 URL 做可达性（+ 标题），绝不从正文刮出“市场事实”。
5. **ADR 001 第 4 条中“上线前可用 mock”被本 ADR 取代。** 线上 UI 展示已发布快照；mock 仅用于离线 fixture / 缺文件回退。

## 后果

- 发布新 Idea = 跑 worker（或 CI）后，把更新后的 `public/` 与 Next 应用一起部署（Vercel）。
- Resend `--live` 与 launchd 与站点发布路径分离。
- 超出 URL 探测的开放网页研究需另开 ADR；不得把计算移入 Next 路由。
- Google OAuth 仍为可选项，不在本 ADR 范围。

## 已知限制

- 语言包为人工维护 YAML，不是整份 PDF 的机翻。
- 连续性“progress”文案在发布时按语言生成，共用同一 SQLite 记忆；清空本地 `idea_memory.sqlite` 会重置挑选历史（已 gitignore）。
- 中文根上的探测备注可能仍含英文页标题；语言包可在提供 `source_notes` 时覆盖。

## 相关

- 配置：`worker/config/idea_catalog.yaml`、`worker/config/idea_locales.yaml`、`worker/config/operator_profile.yaml`
- 发布：`worker/src/passive_income_ideas/latest_json.py`、`localize.py`
- UI：`src/lib/idea-locale.ts`、`src/components/today-client.tsx`
