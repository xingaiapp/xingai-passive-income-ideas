"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { usePrefs } from "@/components/prefs-provider";
import { ThemeToggle } from "@/components/theme";
import { locales, type Locale } from "@/lib/i18n/messages";

const tabs = [
  { href: "/", key: "today" as const },
  { href: "/archive", key: "archive" as const },
  { href: "/how", key: "how" as const },
];

export function AppChrome({ children }: { children: React.ReactNode }) {
  const { t, locale, setLocale } = usePrefs();
  const pathname = usePathname();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const langSelect = (
    <>
      <label className="sr-only" htmlFor="lang">
        Language
      </label>
      <select
        id="lang"
        className="lang-select"
        value={locale}
        onChange={(e) => setLocale(e.target.value as Locale)}
        aria-label="Language"
      >
        {locales.map((l) => (
          <option key={l} value={l}>
            {t.lang[l]}
          </option>
        ))}
      </select>
    </>
  );

  const navLinks = (
    <>
      {tabs.map((tab) => (
        <Link
          key={tab.href}
          href={tab.href}
          onClick={() => setDrawerOpen(false)}
          className={pathname === tab.href ? "active" : ""}
        >
          {t.nav[tab.key]}
        </Link>
      ))}
    </>
  );

  return (
    <div className={`app-shell ${sidebarOpen ? "sidebar-open" : "sidebar-collapsed"}`}>
      <header className="top-bar">
        <button type="button" className="touch-btn lg-hide" aria-label={t.menu} onClick={() => setDrawerOpen(true)}>
          {t.menu}
        </button>
        <button
          type="button"
          className="touch-btn sm-hide"
          aria-label={t.sidebar}
          aria-pressed={sidebarOpen}
          onClick={() => setSidebarOpen((v) => !v)}
        >
          {t.menu}
        </button>
        <Link href="/" className="brand">
          <span className="brand-mark" aria-hidden />
          <span className="brand-text">{t.brand}</span>
        </Link>
        <div className="top-actions">
          {langSelect}
          <ThemeToggle lightLabel={t.theme.light} darkLabel={t.theme.dark} />
        </div>
      </header>

      <aside className="side-nav sm-hide" aria-label={t.sidebar}>
        <nav className="side-nav-links">{navLinks}</nav>
        <div className="side-nav-legal">
          <Link href="/legal/privacy">{t.legal.privacy}</Link>
          <Link href="/legal/terms">{t.legal.terms}</Link>
          <Link href="/legal/disclaimer">{t.legal.disclaimer}</Link>
        </div>
      </aside>

      {drawerOpen ? (
        <div className="drawer-backdrop lg-hide" onClick={() => setDrawerOpen(false)} role="presentation">
          <nav className="drawer" onClick={(e) => e.stopPropagation()} aria-label={t.menu}>
            <div className="drawer-head">
              <strong>{t.brand}</strong>
              <button type="button" className="touch-btn" onClick={() => setDrawerOpen(false)} aria-label={t.close}>
                {t.close}
              </button>
            </div>
            <ul className="drawer-links">
              {tabs.map((tab) => (
                <li key={tab.href}>
                  <Link
                    href={tab.href}
                    onClick={() => setDrawerOpen(false)}
                    className={pathname === tab.href ? "active" : ""}
                  >
                    {t.nav[tab.key]}
                  </Link>
                </li>
              ))}
              <li>
                <Link href="/legal/privacy" onClick={() => setDrawerOpen(false)}>
                  {t.legal.privacy}
                </Link>
              </li>
              <li>
                <Link href="/legal/terms" onClick={() => setDrawerOpen(false)}>
                  {t.legal.terms}
                </Link>
              </li>
              <li>
                <Link href="/legal/disclaimer" onClick={() => setDrawerOpen(false)}>
                  {t.legal.disclaimer}
                </Link>
              </li>
            </ul>
            <div className="drawer-prefs">
              {langSelect}
              <ThemeToggle lightLabel={t.theme.light} darkLabel={t.theme.dark} />
            </div>
            <p className="drawer-foot">{t.legal.footerNote}</p>
          </nav>
        </div>
      ) : null}

      <main className="main">{children}</main>

      <nav className="bottom-nav lg-hide" aria-label="Primary">
        {tabs.map((tab) => (
          <Link key={tab.href} href={tab.href} className={pathname === tab.href ? "active" : ""}>
            {t.nav[tab.key]}
          </Link>
        ))}
      </nav>
    </div>
  );
}
