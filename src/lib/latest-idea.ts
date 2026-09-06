import { readFileSync, existsSync } from "fs";
import path from "path";

export type LatestIdea = {
  report_date: string;
  generated_at?: string;
  idea_id: string;
  idea_name: string;
  one_liner: string;
  continuity: string;
  why_fit: string;
  income_band: string;
  do_today: string;
  dont_today: string;
  biggest_risk: string;
  is_mock: boolean;
  disclaimer?: string;
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
