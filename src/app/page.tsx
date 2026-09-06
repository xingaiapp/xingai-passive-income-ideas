import { TodayClient } from "@/components/today-client";
import { loadLatestIdea } from "@/lib/latest-idea";

export default function TodayPage() {
  const idea = loadLatestIdea();
  return <TodayClient idea={idea} />;
}
