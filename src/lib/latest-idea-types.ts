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
