"use client";

import Image from "next/image";
import Link from "next/link";
import { usePrefs } from "@/components/prefs-provider";

export default function TodayPage() {
  const { t } = usePrefs();

  return (
    <div className="home">
      <section className="hero-board" aria-labelledby="hero-title">
        <div className="hero-copy motion-enter">
          <p className="brand-lockup">
            <Image className="brand-lockup-logo" src="/icon.svg" alt="" width={20} height={20} />
            <span className="brand-lockup-mark">{t.brandMark}</span>
            <span className="brand-lockup-name">{t.brand}</span>
          </p>
          <h1 id="hero-title" className="hero-title">
            <span>{t.today.title}</span>
            <span className="hero-title-accent">{t.today.titleAccent}</span>
          </h1>
          <p className="hero-sub">{t.tagline}</p>
          <p className="hero-note">{t.today.subtitle}</p>
          <div className="row-actions">
            <Link className="btn btn-primary btn-press" href="/how">
              {t.today.ctaHow}
            </Link>
            <Link className="btn btn-press" href="/archive">
              {t.today.ctaArchive}
            </Link>
          </div>
        </div>

        <div className="hero-stage">
          <div className="hero-strip motion-enter motion-delay-1" aria-hidden>
            <Image
              className="hero-img light-only"
              src="/brand/hero-bg-light-visual.svg"
              alt=""
              width={720}
              height={400}
              priority
            />
            <Image
              className="hero-img dark-only"
              src="/brand/hero-bg-visual.svg"
              alt=""
              width={720}
              height={400}
              priority
            />
          </div>

          <aside className="focus-panel idea-panel motion-enter motion-delay-2" aria-label={t.today.ideaLabel}>
            <header className="focus-panel-head">
              <p className="mock-badge">{t.today.mockBadge}</p>
              <h2>{t.today.ideaLabel}</h2>
              <p className="idea-name">{t.today.ideaName}</p>
            </header>
            <dl className="idea-facts">
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 0 }}>
                <dt>{t.today.whyFit}</dt>
                <dd>{t.today.whyFitBody}</dd>
              </div>
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 1 }}>
                <dt>{t.today.incomeBand}</dt>
                <dd>{t.today.incomeBandBody}</dd>
              </div>
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 2 }}>
                <dt>{t.today.doToday}</dt>
                <dd>{t.today.doTodayBody}</dd>
              </div>
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 3 }}>
                <dt>{t.today.dontToday}</dt>
                <dd>{t.today.dontTodayBody}</dd>
              </div>
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 4 }}>
                <dt>{t.today.risk}</dt>
                <dd>{t.today.riskBody}</dd>
              </div>
            </dl>
            <p className="pdf-note">{t.today.pdfNote}</p>
          </aside>
        </div>
      </section>

      <section className="section faq-section motion-enter motion-delay-3" aria-labelledby="faq-title">
        <h2 id="faq-title">{t.faq.title}</h2>
        <div className="faq-stack">
          {t.faq.items.map((item) => (
            <details key={item.q} className="faq-item">
              <summary>{item.q}</summary>
              <p>{item.a}</p>
            </details>
          ))}
        </div>
      </section>

      <footer className="home-foot">
        <p>
          {t.legal.footerNote}{" "}
          <Link href="/legal/privacy">{t.legal.privacy}</Link>
          {" · "}
          <Link href="/legal/terms">{t.legal.terms}</Link>
          {" · "}
          <Link href="/legal/disclaimer">{t.legal.disclaimer}</Link>
        </p>
      </footer>
    </div>
  );
}
