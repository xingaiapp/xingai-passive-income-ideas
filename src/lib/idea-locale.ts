import type { Locale } from "@/lib/i18n/messages";
import type { LatestIdea } from "@/lib/latest-idea-types";

export type {
  ArchiveIndex,
  IdeaEvidence,
  IdeaLocalePack,
  IdeaSource,
  LatestIdea,
} from "@/lib/latest-idea-types";

/** Merge root snapshot with locale pack so EN/zh/ko UI stays consistent. */
export function ideaForLocale(idea: LatestIdea, locale: Locale): LatestIdea {
  const pack = idea.locales?.[locale];
  if (!pack) return idea;
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
