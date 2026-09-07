import { readFileSync, existsSync } from "fs";
import path from "path";
import type { Locale } from "@/lib/i18n/messages";

export type IdeaSource = {
  title: string;
  url: string;
  as_of: string;
  verified: boolean;
  note?: string;
};

export type IdeaEvidence = {
  kind: "fact" | "inference" | "recommendation" | string;
  text: string;
  source_ids?: string[];
};

export type IdeaLocalePack = {
  idea_name?: string;
  one_liner?: string;
  why_fit?: string;
  income_band?: string;
  startup_capital?: string;
  time_per_week?: string;
  first_revenue_eta?: string;
  scalability?: string;
  do_today?: string;
  dont_today?: string;
  biggest_risk?: string;
  stop_rules?: string[];
  day7_plan?: string[];
  day30_goals?: string[];
  business_model?: string;
  competition?: string;
  market_evidence?: IdeaEvidence[];
  disclaimer?: string;
  sources?: Record<string, IdeaSource>;
};

export type LatestIdea = {
  report_date: string;
  generated_at?: string;
  idea_id: string;
  idea_name: string;
  one_liner: string;
  continuity: string;
  fit_score?: number;
  passive_score?: number;
  why_fit: string;
  income_kind?: string;
  income_band: string;
  startup_capital?: string;
  time_per_week?: string;
  first_revenue_eta?: string;
  scalability?: string;
  do_today: string;
  dont_today: string;
  biggest_risk: string;
  stop_rules?: string[];
  day7_plan?: string[];
  day30_goals?: string[];
  business_model?: string;
  competition?: string;
  market_evidence?: IdeaEvidence[];
  is_mock: boolean;
  disclaimer?: string;
  pdf_url?: string;
  sources?: Record<string, IdeaSource>;
  locales?: Partial<Record<Locale, IdeaLocalePack>>;
};

export type ArchiveIndex = {
  updated_at?: string;
  items: {
    report_date: string;
    idea_id: string;
    idea_name: string;
    one_liner: string;
    continuity: string;
    income_kind?: string;
    is_mock: boolean;
    json_url?: string;
    pdf_url?: string;
    locales?: Partial<Record<Locale, Pick<IdeaLocalePack, "idea_name" | "one_liner">>>;
  }[];
};

export function loadLatestIdea(): LatestIdea | null {
  const file = path.join(process.cwd(), "public", "data", "latest-idea.json");
  if (!existsSync(file)) return null;
  try {
    const raw = JSON.parse(readFileSync(file, "utf8")) as LatestIdea;
    if (!raw?.idea_name || !raw?.report_date) return null;
    return raw;
  } catch {
    return null;
  }
}

export function loadArchiveIndex(): ArchiveIndex {
  const file = path.join(process.cwd(), "public", "data", "archive-index.json");
  if (!existsSync(file)) return { items: [] };
  try {
    const raw = JSON.parse(readFileSync(file, "utf8")) as ArchiveIndex;
    if (!Array.isArray(raw?.items)) return { items: [] };
    return raw;
  } catch {
    return { items: [] };
  }
}

/** Merge root snapshot with locale pack so EN/zh/ko UI stays consistent. */
export function ideaForLocale(idea: LatestIdea, locale: Locale): LatestIdea {
  const pack = idea.locales?.[locale];
  if (!pack) {
    // Fallback: zh root; for en/ko without packs keep structure but prefer English chrome fallbacks only
    return idea;
  }
  return {
    ...idea,
    idea_name: pack.idea_name ?? idea.idea_name,
    one_liner: pack.one_liner ?? idea.one_liner,
    why_fit: pack.why_fit ?? idea.why_fit,
    income_band: pack.income_band ?? idea.income_band,
    startup_capital: pack.startup_capital ?? idea.startup_capital,
    time_per_week: pack.time_per_week ?? idea.time_per_week,
    first_revenue_eta: pack.first_revenue_eta ?? idea.first_revenue_eta,
    scalability: pack.scalability ?? idea.scalability,
    do_today: pack.do_today ?? idea.do_today,
    dont_today: pack.dont_today ?? idea.dont_today,
    biggest_risk: pack.biggest_risk ?? idea.biggest_risk,
    stop_rules: pack.stop_rules ?? idea.stop_rules,
    day7_plan: pack.day7_plan ?? idea.day7_plan,
    day30_goals: pack.day30_goals ?? idea.day30_goals,
    business_model: pack.business_model ?? idea.business_model,
    competition: pack.competition ?? idea.competition,
    market_evidence: pack.market_evidence ?? idea.market_evidence,
    disclaimer: pack.disclaimer ?? idea.disclaimer,
    sources: pack.sources ?? idea.sources,
  };
}
