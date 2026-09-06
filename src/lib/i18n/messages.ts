export type Locale = "en" | "zh" | "ko";

export const locales: Locale[] = ["en", "zh", "ko"];

export type Messages = {
  brand: string;
  brandMark: string;
  tagline: string;
  nav: { today: string; archive: string; how: string; legal: string };
  today: {
    title: string;
    titleAccent: string;
    subtitle: string;
    ideaLabel: string;
    ideaName: string;
    whyFit: string;
    whyFitBody: string;
    incomeBand: string;
    incomeBandBody: string;
    capital: string;
    timeWeek: string;
    firstRevenue: string;
    fitScore: string;
    passiveScore: string;
    evidence: string;
    evidenceKinds: { fact: string; inference: string; recommendation: string };
    day7: string;
    sources: string;
    verified: string;
    unverified: string;
    doToday: string;
    doTodayBody: string;
    dontToday: string;
    dontTodayBody: string;
    risk: string;
    riskBody: string;
    pdfNote: string;
    mockBadge: string;
    liveBadge: string;
    liveProgressBadge: string;
    ctaHow: string;
    ctaArchive: string;
    ctaPdf: string;
  };
  archive: {
    title: string;
    subtitle: string;
    empty: string;
    openJson: string;
  };
  how: {
    title: string;
    subtitle: string;
    steps: { title: string; body: string }[];
  };
  legal: {
    privacy: string;
    terms: string;
    disclaimer: string;
    footerNote: string;
  };
  theme: { light: string; dark: string };
  lang: { en: string; zh: string; ko: string };
  soon: string;
  menu: string;
  close: string;
  sidebar: string;
  faq: { title: string; items: { q: string; a: string }[] };
};

export const messages: Record<Locale, Messages> = {
  en: {
    brand: "Passive Income Idea",
    brandMark: "XingAI",
    tagline: "One verified Idea per day — fit for your skills, capital, and stage. Not a list of random tips.",
    nav: { today: "Today", archive: "Archive", how: "How it works", legal: "Legal" },
    today: {
      title: "Today’s only Idea",
      titleAccent: "worth acting on.",
      subtitle: "Full report fields load from today’s research snapshot when available.",
      ideaLabel: "Primary Idea",
      ideaName: "Niche AI ops checklist product (mock)",
      whyFit: "Why it fits you",
      whyFitBody:
        "Uses software/.NET/cloud/AI leadership skills; can start part-time from Austin without a new full-time job (mock).",
      incomeBand: "Realistic income band",
      incomeBandBody: "Business revenue estimate only — not investment yield. Mock band: $0–2k/mo in 90 days if validated.",
      capital: "Startup capital",
      timeWeek: "Time per week",
      firstRevenue: "First revenue ETA",
      fitScore: "Fit",
      passiveScore: "Passive",
      evidence: "Market evidence",
      evidenceKinds: { fact: "Fact", inference: "Inference", recommendation: "Advice" },
      day7: "7-day MVP plan",
      sources: "Sources (probed)",
      verified: "verified page",
      unverified: "未核实",
      doToday: "Do today (30 min)",
      doTodayBody: "Interview 3 peers about a painful ops checklist they still do by hand (mock).",
      dontToday: "Don’t do today",
      dontTodayBody: "Don’t buy ads, form an LLC, or build a full SaaS yet (mock).",
      risk: "Biggest risk",
      riskBody: "Demand may be polite interest only — stop if 10 talks yield zero paid intent (mock).",
      pdfNote: "Full A4 report PDF",
      mockBadge: "Mock Idea — offline fixture",
      liveBadge: "Live Idea — from today’s research",
      liveProgressBadge: "Live Idea — progress update",
      ctaHow: "How delivery works",
      ctaArchive: "Past Ideas",
      ctaPdf: "Open PDF",
    },
    archive: {
      title: "Idea archive",
      subtitle: "Continuity memory: prefer progress on yesterday’s Idea when it still wins.",
      empty: "No archived Ideas yet. Daily runs will land here after the worker ships.",
      openJson: "Open JSON",
    },
    how: {
      title: "How delivery works",
      subtitle: "Same pattern as XingAI Daily Investment 智报: short email Summary + full A4 PDF.",
      steps: [
        {
          title: "One Idea",
          body: "Markets and digital businesses are researched; only the single best Idea for your profile is kept.",
        },
        {
          title: "Email Summary",
          body: "Subject: XingAI 每日被动收入 Idea 智报｜date｜Idea name. Body: conclusion, fit, income band, do/don’t, risk.",
        },
        {
          title: "PDF attachment",
          body: "Full plan with 30-minute action, 7-day MVP, 30-day goals, sources, and stop rules — black text on A4.",
        },
        {
          title: "Honest labels",
          body: "Facts, inference, and advice stay separate. Unverified claims are marked 未核实. No fabricated numbers.",
        },
      ],
    },
    legal: {
      privacy: "Privacy",
      terms: "Terms",
      disclaimer: "Disclaimer",
      footerNote:
        "Informational only — not financial, tax, or business advice. No income guarantees. Verify before you act.",
    },
    theme: { light: "Light", dark: "Dark" },
    lang: { en: "EN", zh: "中文", ko: "한국어" },
    soon: "Soon",
    menu: "Menu",
    close: "Close",
    sidebar: "Sidebar",
    faq: {
      title: "FAQ",
      items: [
        {
          q: "What is Passive Income Idea 智报?",
          a: "A daily report that picks one passive-income or cash-flow Idea fit for your profile, with email Summary + PDF. Domain: passive.xingai.app.",
        },
        {
          q: "Is this investment advice?",
          a: "No. Ideas may include business revenue or cash-flow investments, but the product is educational. Separates investment returns from business income.",
        },
        {
          q: "Will it guarantee passive income?",
          a: "No. Bands are estimates when sourced; unknowns stay 未核实. You decide what to run.",
        },
        {
          q: "How is this different from Opportunity Radar?",
          a: "Radar picks XingAI product bets. This report picks one personal wealth-building Idea for a defined operator profile.",
        },
      ],
    },
  },
  zh: {
    brand: "被动收入 Idea",
    brandMark: "XingAI",
    tagline: "每天只给 1 个值得执行的 Idea——贴合你的技能、资金与阶段，不是点子清单。",
    nav: { today: "今日", archive: "归档", how: "如何送达", legal: "法律" },
    today: {
      title: "今日唯一 Idea",
      titleAccent: "值得动手。",
      subtitle: "有今日研究快照时，页面会加载完整字段。",
      ideaLabel: "主 Idea",
      ideaName: "垂直 AI 运维清单产品（模拟）",
      whyFit: "为什么适合你",
      whyFitBody: "复用软件/.NET/云/AI 管理背景；可在 Austin 兼职启动，不必立刻全职（模拟）。",
      incomeBand: "现实收入区间",
      incomeBandBody: "仅商业收入估计——不是投资收益率。模拟：验证后 90 天内约 $0–2k/月。",
      capital: "启动资金",
      timeWeek: "每周投入",
      firstRevenue: "首笔收入预估",
      fitScore: "适合度",
      passiveScore: "被动度",
      evidence: "市场与需求证据",
      evidenceKinds: { fact: "事实", inference: "推断", recommendation: "建议" },
      day7: "7 天 MVP 计划",
      sources: "来源（已探测）",
      verified: "页面已核实可达",
      unverified: "未核实",
      doToday: "今天做（30 分钟）",
      doTodayBody: "找 3 位同行，问他们是否仍手工做某类运维清单（模拟）。",
      dontToday: "今天不要做",
      dontTodayBody: "不要买广告、不要急着开公司、不要先做完整 SaaS（模拟）。",
      risk: "最大风险",
      riskBody: "热情不等于付费意愿——若 10 次访谈仍无付费意向则停止（模拟）。",
      pdfNote: "完整 A4 PDF 报告",
      mockBadge: "模拟 Idea — 离线 fixture",
      liveBadge: "今日研究 · 实时 Idea",
      liveProgressBadge: "今日研究 · 连续性推进",
      ctaHow: "如何送达",
      ctaArchive: "往日 Idea",
      ctaPdf: "打开 PDF",
    },
    archive: {
      title: "Idea 归档",
      subtitle: "连续性记忆：若昨日 Idea 仍最优，报告进度而非硬换题。",
      empty: "暂无归档。Worker 上线后，每日运行会落在这里。",
      openJson: "打开 JSON",
    },
    how: {
      title: "如何送达",
      subtitle: "与《XingAI 每日投资智报》相同：精简邮件 Summary + 完整 A4 PDF。",
      steps: [
        { title: "只选 1 个", body: "研究市场与数字生意后，只保留最适合你画像的主 Idea。" },
        {
          title: "邮件 Summary",
          body: "主题：XingAI 每日被动收入 Idea 智报｜日期｜Idea 名。正文：结论、适合度、收入区间、做/不做、风险。",
        },
        {
          title: "PDF 附件",
          body: "含 30 分钟行动、7 天 MVP、30 天目标、来源与停止条件——A4 黑字专业日报。",
        },
        {
          title: "诚实标注",
          body: "事实 / 推断 / 建议分开。无法核实标「未核实」。禁止编造数字。",
        },
      ],
    },
    legal: {
      privacy: "隐私",
      terms: "条款",
      disclaimer: "免责声明",
      footerNote: "仅供参考——非金融、税务或商业建议。不保证收入。行动前请自行核实。",
    },
    theme: { light: "浅色", dark: "深色" },
    lang: { en: "EN", zh: "中文", ko: "한국어" },
    soon: "即将推出",
    menu: "菜单",
    close: "关闭",
    sidebar: "侧栏",
    faq: {
      title: "常见问题",
      items: [
        {
          q: "被动收入 Idea 智报是什么？",
          a: "每日选出 1 个贴合你画像的被动收入/现金流 Idea，邮件 Summary + PDF。域名：passive.xingai.app。",
        },
        {
          q: "这是投资建议吗？",
          a: "不是。可能涉及商业收入或现金流投资，但产品定位为信息参考；会严格区分投资收益与商业收入。",
        },
        {
          q: "能保证被动收入吗？",
          a: "不能。区间仅为有来源的估计；未知标「未核实」。是否执行由你决定。",
        },
        {
          q: "和 Opportunity Radar 有何不同？",
          a: "Radar 选 XingAI 产品立项；本报告为个人财富积累阶段选出 1 个可执行 Idea。",
        },
      ],
    },
  },
  ko: {
    brand: "수동소득 Idea",
    brandMark: "XingAI",
    tagline: "하루 하나의 검증 Idea — 기술·자본·단계에 맞춤. 잡다한 팁 목록이 아닙니다.",
    nav: { today: "오늘", archive: "보관", how: "전달 방식", legal: "법적" },
    today: {
      title: "오늘의 단 하나 Idea",
      titleAccent: "실행할 가치.",
      subtitle: "오늘 리서치 스냅샷이 있으면 전체 필드가 표시됩니다.",
      ideaLabel: "메인 Idea",
      ideaName: "니치 AI 운영 체크리스트 제품 (목)",
      whyFit: "왜 맞는지",
      whyFitBody: "소프트웨어/.NET/클라우드/AI 리더십을 쓰며 Austin에서 파트타임으로 시작 가능 (목).",
      incomeBand: "현실 수입 구간",
      incomeBandBody: "사업 매출 추정만 — 투자 수익률 아님. 목: 검증 후 90일 $0–2k/월.",
      capital: "시작 자본",
      timeWeek: "주당 시간",
      firstRevenue: "첫 매출 ETA",
      fitScore: "적합도",
      passiveScore: "수동도",
      evidence: "시장 증거",
      evidenceKinds: { fact: "사실", inference: "추론", recommendation: "제안" },
      day7: "7일 MVP 계획",
      sources: "출처 (탐침됨)",
      verified: "페이지 확인됨",
      unverified: "未核实",
      doToday: "오늘 할 일 (30분)",
      doTodayBody: "동료 3명에게 아직 수작업인 운영 체크리스트가 있는지 인터뷰 (목).",
      dontToday: "오늘 하지 말 것",
      dontTodayBody: "광고 구매·법인 설립·풀 SaaS 구축은 아직 (목).",
      risk: "최대 리스크",
      riskBody: "관심만 있고 지불 의사가 없을 수 있음 — 10회 인터뷰 후 유료 의도 없으면 중단 (목).",
      pdfNote: "전체 A4 PDF 리포트",
      mockBadge: "목 Idea — 오프라인 fixture",
      liveBadge: "오늘 리서치 · 라이브 Idea",
      liveProgressBadge: "오늘 리서치 · 연속 업데이트",
      ctaHow: "전달 방식",
      ctaArchive: "지난 Idea",
      ctaPdf: "PDF 열기",
    },
    archive: {
      title: "Idea 보관",
      subtitle: "연속성: 어제 Idea가 여전히 최선이면 주제 교체 대신 진행 상황을 보고합니다.",
      empty: "보관된 Idea 없음. Worker 이후 일일 실행이 여기에 쌓입니다.",
      openJson: "JSON 열기",
    },
    how: {
      title: "전달 방식",
      subtitle: "XingAI 일일 투자 지보와 동일: 짧은 메일 Summary + A4 PDF.",
      steps: [
        { title: "Idea 하나", body: "시장·디지털 사업을 조사한 뒤 프로필에 맞는 단 하나의 Idea만 남깁니다." },
        {
          title: "메일 Summary",
          body: "제목: XingAI 每日被动收入 Idea 智报｜날짜｜Idea. 본문: 결론·적합도·수입·할/말 것·리스크.",
        },
        {
          title: "PDF 첨부",
          body: "30분 행동, 7일 MVP, 30일 목표, 출처, 중단 조건 — A4 검정 텍스트.",
        },
        {
          title: "정직한 표시",
          body: "사실/추론/제안을 구분. 미확인은 未核实. 숫자 날조 금지.",
        },
      ],
    },
    legal: {
      privacy: "개인정보",
      terms: "이용약관",
      disclaimer: "면책",
      footerNote: "정보 제공용 — 금융·세무·사업 조언 아님. 수입 보장 없음. 실행 전 직접 검증하세요.",
    },
    theme: { light: "라이트", dark: "다크" },
    lang: { en: "EN", zh: "中文", ko: "한국어" },
    soon: "곧",
    menu: "메뉴",
    close: "닫기",
    sidebar: "사이드바",
    faq: {
      title: "FAQ",
      items: [
        {
          q: "수동소득 Idea 지보란?",
          a: "프로필에 맞는 수동소득/현금흐름 Idea를 하루 하나 고르고 메일 Summary + PDF로 보냅니다. 도메인: passive.xingai.app.",
        },
        {
          q: "투자 조언인가요?",
          a: "아닙니다. 교육·정보 목적이며 투자 수익과 사업 매출을 구분합니다.",
        },
        {
          q: "수동소득을 보장하나요?",
          a: "아니요. 구간은 출처 있는 추정이며 미확인은 未核实입니다.",
        },
        {
          q: "Opportunity Radar와 차이는?",
          a: "Radar는 XingAI 제품 베팅. 이 리포트는 개인 자산 축적용 Idea 하나입니다.",
        },
      ],
    },
  },
};
