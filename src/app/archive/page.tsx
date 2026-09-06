"use client";

import Link from "next/link";
import { usePrefs } from "@/components/prefs-provider";

export default function ArchivePage() {
  const { t } = usePrefs();

  return (
    <div className="page-pad">
      <header className="page-head">
        <h1>{t.archive.title}</h1>
        <p>{t.archive.subtitle}</p>
      </header>
      <p className="empty-state">{t.archive.empty}</p>
      <p className="muted">
        <Link href="/">{t.nav.today}</Link>
      </p>
    </div>
  );
}
