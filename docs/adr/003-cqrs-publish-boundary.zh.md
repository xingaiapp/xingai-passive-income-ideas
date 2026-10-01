# ADR 003：CQRS 发布边界 — Worker 写，站点只读

- **状态：** 已接受
- **日期：** 2026-09-07
- **层级：** Worker / Frontend / Data
- **相关：** [ADR 002](002-worker-publish-static-ui.zh.md)（产物清单与语言包）；Invest AI [ADR-008 CQRS 缓存](https://github.com/xingaiapp/xingai-invest-ai/blob/main/docs/adr/008-cqrs-cache-pattern.zh.md)（同一规则，不同存储）

## 背景

ADR 002 已写明 Next.js 站点相对已发布 JSON/PDF 只读。这条线很容易被抹掉：随便加一个 Route Handler 再探测 URL、按需 LLM 润色英文、或在 React 里从原始字段反推适合度/收入。

本产品**目前没有 FastAPI**。共享“缓存”是部署包里的 `public/data/` 与 `public/reports/`。CQRS 仍然成立：**单一写入路径、多方只读、请求路径不做 Idea 计算。**

## 决策

```text
Worker（generate / run-daily）  =  计算 Idea 并写入产物
Next.js 公开站点                 =  读取产物并渲染 / 本地化
React                            =  展示字段；不做决策
```

### 硬规则

1. **Worker 是 Idea 真相的唯一写入者。** 目录挑选、连续性/记忆、网页探测、可选 LLM 润色、PDF QA、语言包组装只在 `worker/`（`generate` / `run-daily`），不得进入 Next `app/api` 或 Server Actions。
2. **已发布产物即契约。** 读取方只消费：
   - `public/data/latest-idea.json`（含 `locales.*`）
   - `public/data/ideas/YYYY-MM-DD.json`
   - `public/data/archive-index.json`
   - `public/reports/*.pdf`
3. **站点只能读与展示。** 允许：读/静态托管上述文件、i18n 壳文案、合并预计算的 `locales[lang]`、链接、主题/语言偏好。请求路径禁止：重新打分、Jaccard 去重、URL 探测、LLM、编造收入区间、改写证据文案。
4. **宁旧勿假。** 产物缺失或过期时，展示 mock/空态/回退 — 不要在 Vercel 上静默重算“今日 Idea”来掩盖漏跑的 worker。
5. **新决策字段顺序与 Invest 相同：** 先写入 worker 快照 → 发布 JSON → 再渲染。UI 不得发明 worker 未写出的分数。
6. **邮件/PDF 归 worker。** Resend 发送与 ReportLab 渲染是命令侧；站点可链到已发布 PDF，但不得按 PV 重新生成。

### 为何这里用 CQRS

| 压力 | 拆分如何帮忙 |
|---|---|
| 诚实的 `未核实` | 探测/LLM 留在离线；请求路径不能“好心”补洞 |
| 成本 / 限额 | URL 探测与可选 OpenAI 按 generate 跑一次，而非每位访客 |
| 部署简单 | Vercel 托管静态 JSON；Web 应用不必持有研究密钥 |
| 可测 | UI 用 fixture JSON；worker 测目录+记忆，不绑 Next |

## 曾考虑的方案

| 方案 | 为何拒绝 |
|---|---|
| **Next Route Handler 按需研究** | 每位访客绑探测/LLM；破坏 fail-closed 与成本控制 |
| **浏览器端“研究”请求** | 更糟：密钥、CORS、可在端上编造数字 |
| **FastAPI 只读 SQLite**（Invest 形） | 以后若要鉴权/限流可加；静态发布够用前不必要。若加，必须对 worker 写入行**只读** — 与 Invest FastAPI 同一 CQRS 侧 |

## 后果

- 任何“加个 API 刷新今日 Idea”的 PR，除非只是*触发*离线任务并仍提供上次产物，否则违反本 ADR。
- Cursor 规则：`.cursor/rules/cqrs-publish-boundary.mdc`。
- 更深的开放网页研究 = 仅 worker/命令侧另开 ADR。

## 已知限制

- 今日常见“写入”是本地 `generate` 后提交/部署 `public/`。计算仍归 worker；CI/cron 可替代人工步骤，但不得把计算挪进 Next。
- 浏览器合并语言包是展示，不是新决策。

## 相关

- 代码：`worker/src/passive_income_ideas/pipeline.py`、`live_research.py`、`latest_json.py`；UI `src/lib/latest-idea.ts`、`src/lib/idea-locale.ts`
- 跨仓：[xingai-invest-ai ADR-008](https://github.com/xingaiapp/xingai-invest-ai/blob/main/docs/adr/008-cqrs-cache-pattern.zh.md)、[ADR-012 决策缓存边界](https://github.com/xingaiapp/xingai-invest-ai/blob/main/docs/adr/012-decision-cache-boundary.md)
