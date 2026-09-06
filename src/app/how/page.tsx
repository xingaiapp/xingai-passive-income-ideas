"use client";

import Link from "next/link";
import { usePrefs } from "@/components/prefs-provider";

export default function HowPage() {
  const { t } = usePrefs();

  return (
    <div className="page-pad">
      <header className="page-head">
        <h1>{t.how.title}</h1>
        <p>{t.how.subtitle}</p>
      </header>
      <ol className="how-steps">
        {t.how.steps.map((step, i) => (
          <li key={step.title}>
            <span className="how-index" aria-hidden>
              {i + 1}
            </span>
            <div>
              <h2>{step.title}</h2>
              <p>{step.body}</p>
            </div>
          </li>
        ))}
      </ol>
      <p className="muted">
        <Link href="/">{t.nav.today}</Link>
      </p>
    </div>
  );
}
