# ADR 001：产品边界 — 个人被动收入 Idea 智报

- **状态：** 已接受
- **日期：** 2026-09-06
- **层级：** Product / Report worker + 公开站点
- **相关：** [ADR 002](002-worker-publish-static-ui.zh.md)（上线后静态发布路径）

## 背景

XingAI 已有：

- **Invest AI `investment_zhibao`** — 面向持仓/宏观的每日*投资* PDF + 邮件。
- **Opportunity Radar** — XingAI *产品组合* 立项机会。
- **Founder AI** — 创始人简报 / 初创雷达。

新产品需要清晰职责：面向既定操作者画像，每天只给 **1 个**个人被动收入/现金流 Idea，交付工艺对齐 Invest 智报。

## 决策

1. **仓库** `xingai-passive-income-ideas`（由 `xingai-passive-income-zhibao` 更名）同时拥有：
   - Next.js 公开站点 `passive.xingai.app`（project-init 基线），
   - `worker/` 下的 Python 报告 worker（PDF + Resend），参照 Invest `investment_zhibao`。
2. **不是** Opportunity Radar 或 Founder Brief 内容管线的分叉。
3. 所有文案与模型中 **严格区分** 投资收益 vs 商业收入。
4. （历史）公开 UI 可在 worker 上线前展示 mock Idea；邮件/PDF 为主要决策产物。**上线后的只读发布边界见 ADR 002。**

## 后果

- dot-app 注册 slug `passive-income`、域名 `passive.xingai.app`，部署前可为 `coming-soon`。
- 智报 PDF 视觉规则对齐 Invest AI ADR-040/042 工艺，但不共享 Invest 决策缓存。
