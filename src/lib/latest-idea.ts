import { readFileSync, existsSync } from "fs";
import path from "path";
import type { ArchiveIndex, LatestIdea } from "@/lib/latest-idea-types";

export type {
  ArchiveIndex,
  IdeaEvidence,
  IdeaLocalePack,
  IdeaSource,
  LatestIdea,
} from "@/lib/latest-idea-types";

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
