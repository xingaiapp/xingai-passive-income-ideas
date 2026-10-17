import type { Metadata, Viewport } from "next";
import { notFound } from "next/navigation";
import { Fraunces, Outfit } from "next/font/google";
import { AppChrome } from "@/components/app-chrome";
import { PrefsProvider } from "@/components/prefs-provider";
import { AppThemeProvider } from "@/components/theme";
import { getSiteUrl } from "@/lib/site-url";
import { htmlLang, isLocale, localizedPath } from "@/lib/i18n/paths";
import { locales, type Locale } from "@/lib/i18n/messages";
import "../globals.css";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  display: "swap",
});

const SITE_URL = getSiteUrl();

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

/** Unknown first segments (e.g. /foo.txt) must 404 instead of rendering a locale page. */
export const dynamicParams = false;

function languageAlternates() {
  return {
    en: SITE_URL,
    "zh-CN": `${SITE_URL}${localizedPath("zh", "/")}`,
    ko: `${SITE_URL}${localizedPath("ko", "/")}`,
    "x-default": SITE_URL,
  };
}

const baseMetadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "XingAI Passive Income Idea",
    template: "%s · XingAI Passive Income Idea",
  },
  description:
    "One-Idea passive income research: web board, email Summary + A4 PDF when research runs. Informational only — not financial advice.",
  openGraph: {
    title: "XingAI Passive Income Idea",
    description: "Latest researched Idea for a defined profile — fit, capital, time, risks, and a 30-minute next step.",
    url: SITE_URL,
    siteName: "XingAI Passive Income Idea",
    type: "website",
    images: [{ url: "/og-image.svg", width: 1200, height: 630, alt: "XingAI Passive Income Idea" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "XingAI Passive Income Idea",
    description: "Latest researched Idea for a defined profile — fit, capital, time, risks, and a 30-minute next step.",
    images: ["/og-image.svg"],
  },
  icons: {
    icon: [{ url: "/icon.svg", type: "image/svg+xml" }],
  },
  robots: { index: true, follow: true },
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale: raw } = await params;
  const locale: Locale = isLocale(raw) ? raw : "en";
  const url = locale === "en" ? SITE_URL : `${SITE_URL}${localizedPath(locale, "/")}`;
  return {
    ...baseMetadata,
    alternates: { canonical: url, languages: languageAlternates() },
    openGraph: { ...baseMetadata.openGraph, url, locale: locale === "zh" ? "zh_CN" : locale === "ko" ? "ko_KR" : "en_US" },
  };
}

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#efeaf5" },
    { media: "(prefers-color-scheme: dark)", color: "#1a1a2e" },
  ],
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      name: "XingAI Passive Income Idea",
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      url: SITE_URL,
      description:
        "One-Idea passive income research with web board, email Summary, and PDF. Informational only. Public demo.",
      offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
    },
    {
      "@type": "FAQPage",
      mainEntity: [
        {
          "@type": "Question",
          name: "What is Passive Income Idea 智报?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "A research product that picks one passive-income or cash-flow Idea for a defined operator profile, shown on the web board with optional email Summary plus PDF at passive.xingai.app.",
          },
        },
        {
          "@type": "Question",
          name: "Is this investment advice?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "No. It is informational and educational. Investment returns and business revenue are labeled separately. No income guarantees.",
          },
        },
        {
          "@type": "Question",
          name: "Will it guarantee passive income?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "No. Ideas can fail validation. Income bands are estimates with honest labels such as unverified. You decide whether to act.",
          },
        },
        {
          "@type": "Question",
          name: "How is this different from Opportunity Radar?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Opportunity Radar selects XingAI product bets. This product selects one personal wealth-building Idea for a defined profile.",
          },
        },
      ],
    },
  ],
};

type Props = {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
};

export default async function RootLayout({ children, params }: Props) {
  const { locale: raw } = await params;
  if (!isLocale(raw)) notFound();
  const locale: Locale = raw;
  return (
    <html lang={htmlLang(locale)} suppressHydrationWarning className={`${outfit.variable} ${fraunces.variable}`}>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem('theme');document.documentElement.classList.toggle('dark',t==='dark');}catch(e){}})();`,
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body style={{ fontFamily: "var(--font-outfit), var(--font-sans)" }}>
        <AppThemeProvider>
          <PrefsProvider locale={locale}>
            <AppChrome>{children}</AppChrome>
          </PrefsProvider>
        </AppThemeProvider>
      </body>
    </html>
  );
}
