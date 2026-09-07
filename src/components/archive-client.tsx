"use client";

import Link from "next/link";
import { usePrefs } from "@/components/prefs-provider";
import type { ArchiveIndex } from "@/lib/latest-idea";

export function ArchiveClient({ archive }: { archive: ArchiveIndex }) {
  const { t, locale } = usePrefs();
  const items = archive.items ?? [];

  return (
    <div className="page-pad">
      <header className="page-head">
        <h1>{t.archive.title}</h1>
        <p>{t.archive.subtitle}</p>
      </header>

      {items.length === 0 ? (
        <p className="empty-state">{t.archive.empty}</p>
      ) : (
        <ul className="archive-list">
          {items.map((item) => {
            const loc = item.locales?.[locale];
            const name = loc?.idea_name ?? item.idea_name;
            const line = loc?.one_liner ?? item.one_liner;
            return (
              <li key={item.report_date} className="archive-card">
                <p className="archive-date">{item.report_date}</p>
                <h2 className="archive-name">{name}</h2>
                <p className="archive-line">{line}</p>
                <p className="archive-meta">
                  {item.continuity === "progress" ? t.today.liveProgressBadge : t.today.liveBadge}
                  {item.is_mock ? ` · ${t.today.mockBadge}` : ""}
                </p>
                <div className="row-actions archive-actions">
                  {item.pdf_url ? (
                    <a className="btn btn-primary btn-press" href={item.pdf_url} target="_blank" rel="noreferrer">
                      {t.today.ctaPdf}
                    </a>
                  ) : null}
                  {item.json_url ? (
                    <a className="btn btn-press" href={item.json_url} target="_blank" rel="noreferrer">
                      {t.archive.openJson}
                    </a>
                  ) : null}
                </div>
              </li>
            );
          })}
        </ul>
      )}

      <p className="muted">
        <Link href="/">{t.nav.today}</Link>
      </p>
    </div>
  );
}
