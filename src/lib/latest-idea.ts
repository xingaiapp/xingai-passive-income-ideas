import { readFileSync, existsSync } from "fs";
import path from "path";

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
