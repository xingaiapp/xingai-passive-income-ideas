import { ArchiveClient } from "@/components/archive-client";
import { loadArchiveIndex } from "@/lib/latest-idea";

export default function ArchivePage() {
  const archive = loadArchiveIndex();
  return <ArchiveClient archive={archive} />;
}
