"use client";

import Image from "next/image";
import Link from "next/link";
import { usePrefs } from "@/components/prefs-provider";
import { ideaForLocale, type LatestIdea } from "@/lib/idea-locale";

function evidenceLabel(kind: string, labels: { fact: string; inference: string; recommendation: string }) {
  if (kind === "fact") return labels.fact;
  if (kind === "recommendation") return labels.recommendation;
  return labels.inference;
}

export function TodayClient({ idea }: { idea: LatestIdea | null }) {
  const { t, locale } = usePrefs();
  const view = idea ? ideaForLocale(idea, locale) : null;
  const live = view && !view.is_mock;
  const badge = !view
    ? t.today.mockBadge
    : live
      ? view.continuity === "progress"
        ? t.today.liveProgressBadge
        : t.today.liveBadge
      : t.today.mockBadge;

  const name = view?.idea_name ?? t.today.ideaName;
  const why = view?.why_fit ?? t.today.whyFitBody;
  const income = view?.income_band ?? t.today.incomeBandBody;
  const doToday = view?.do_today ?? t.today.doTodayBody;
  const dont = view?.dont_today ?? t.today.dontTodayBody;
  const risk = view?.biggest_risk ?? t.today.riskBody;
  const sources = view?.sources ? Object.entries(view.sources) : [];
  const evidence = view?.market_evidence ?? [];
  const day7 = view?.day7_plan ?? [];
  const pdfHref = view?.pdf_url;
  const note = view
    ? `${t.today.pdfNote} · ${view.report_date}`
    : t.today.pdfNote;

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
          <p className="hero-note">{view?.one_liner ?? t.today.subtitle}</p>
          <div className="row-actions">
            {pdfHref ? (
              <a className="btn btn-primary btn-press" href={pdfHref} target="_blank" rel="noreferrer">
                {t.today.ctaPdf}
              </a>
            ) : (
              <Link className="btn btn-primary btn-press" href="/how">
                {t.today.ctaHow}
              </Link>
            )}
            <Link className="btn btn-press" href="/archive">
              {t.today.ctaArchive}
            </Link>
          </div>

          <div className="hero-strip hero-strip-mobile motion-enter motion-delay-1" aria-hidden>
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
        </div>

        <div className="hero-stage">
          <aside className="focus-panel idea-panel motion-enter motion-delay-2" aria-label={t.today.ideaLabel}>
            <header className="focus-panel-head">
              <p className="mock-badge">{badge}</p>
              <h2>{t.today.ideaLabel}</h2>
              <p className="idea-name">{name}</p>
              {view && (view.fit_score != null || view.passive_score != null) ? (
                <p className="score-row">
                  {t.today.fitScore}: {view.fit_score ?? "—"}/10
                  <span aria-hidden> · </span>
                  {t.today.passiveScore}: {view.passive_score ?? "—"}/10
                </p>
              ) : null}
            </header>
            <dl className="idea-facts">
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 0 }}>
                <dt>{t.today.whyFit}</dt>
                <dd>{why}</dd>
              </div>
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 1 }}>
                <dt>{t.today.incomeBand}</dt>
                <dd>{income}</dd>
              </div>
              {view?.startup_capital ? (
                <div className="fact-row motion-stagger" style={{ ["--i" as string]: 2 }}>
                  <dt>{t.today.capital}</dt>
                  <dd>{view.startup_capital}</dd>
                </div>
              ) : null}
              {view?.time_per_week ? (
                <div className="fact-row motion-stagger" style={{ ["--i" as string]: 3 }}>
                  <dt>{t.today.timeWeek}</dt>
                  <dd>{view.time_per_week}</dd>
                </div>
              ) : null}
              {view?.first_revenue_eta ? (
                <div className="fact-row motion-stagger" style={{ ["--i" as string]: 4 }}>
                  <dt>{t.today.firstRevenue}</dt>
                  <dd>{view.first_revenue_eta}</dd>
                </div>
              ) : null}
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 5 }}>
                <dt>{t.today.doToday}</dt>
                <dd>{doToday}</dd>
              </div>
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 6 }}>
                <dt>{t.today.dontToday}</dt>
                <dd>{dont}</dd>
              </div>
              <div className="fact-row motion-stagger" style={{ ["--i" as string]: 7 }}>
                <dt>{t.today.risk}</dt>
                <dd>{risk}</dd>
              </div>
            </dl>

            {evidence.length > 0 ? (
              <section className="idea-block" aria-labelledby="evidence-title">
                <h3 id="evidence-title">{t.today.evidence}</h3>
                <ul className="evidence-list">
                  {evidence.map((ev, i) => (
                    <li key={`${ev.kind}-${i}`}>
                      <span className={`ev-kind ev-${ev.kind}`}>
                        {evidenceLabel(ev.kind, t.today.evidenceKinds)}
                      </span>
                      <span>{ev.text}</span>
                    </li>
                  ))}
                </ul>
              </section>
            ) : null}

            {day7.length > 0 ? (
              <section className="idea-block" aria-labelledby="day7-title">
                <h3 id="day7-title">{t.today.day7}</h3>
                <ol className="plan-list">
                  {day7.map((step) => (
                    <li key={step}>{step}</li>
                  ))}
                </ol>
              </section>
            ) : null}

            {sources.length > 0 ? (
              <section className="idea-block" aria-labelledby="sources-title">
                <h3 id="sources-title">{t.today.sources}</h3>
                <ul className="source-list">
                  {sources.map(([sid, src]) => (
                    <li key={sid}>
                      <a href={src.url} target="_blank" rel="noreferrer">
                        {src.title}
                      </a>
                      <span className="source-meta">
                        {src.verified ? t.today.verified : t.today.unverified}
                        {src.as_of ? ` · ${src.as_of}` : ""}
                      </span>
                      {src.note ? <p className="source-note">{src.note}</p> : null}
                    </li>
                  ))}
                </ul>
              </section>
            ) : null}

            <p className="pdf-note">
              {note}
              {pdfHref ? (
                <>
                  {" · "}
                  <a href={pdfHref} target="_blank" rel="noreferrer">
                    {t.today.ctaPdf}
                  </a>
                </>
              ) : null}
            </p>
            {view?.disclaimer ? <p className="idea-disclaimer">{view.disclaimer}</p> : null}
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
