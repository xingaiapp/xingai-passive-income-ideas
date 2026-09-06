import type { Metadata, Viewport } from "next";
import { Fraunces, Outfit } from "next/font/google";
import { AppChrome } from "@/components/app-chrome";
import { PrefsProvider } from "@/components/prefs-provider";
import { AppThemeProvider } from "@/components/theme";
import { getSiteUrl } from "@/lib/site-url";
import "./globals.css";

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

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "XingAI Passive Income Idea",
    template: "%s · XingAI Passive Income Idea",
  },
  description:
    "Daily one-Idea passive income research report: email Summary + A4 PDF. Informational only — not financial advice.",
  alternates: { canonical: SITE_URL },
  openGraph: {
    title: "XingAI Passive Income Idea",
    description: "One verified Idea per day — fit, capital, time, risks, and a 30-minute next step.",
    url: SITE_URL,
    siteName: "XingAI Passive Income Idea",
    type: "website",
    images: [{ url: "/og-image.svg", width: 1200, height: 630, alt: "XingAI Passive Income Idea" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "XingAI Passive Income Idea",
    description: "One verified Idea per day — fit, capital, time, risks, and a 30-minute next step.",
    images: ["/og-image.svg"],
  },
  icons: {
    icon: [{ url: "/icon.svg", type: "image/svg+xml" }],
  },
  robots: { index: true, follow: true },
};

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
        "Daily one-Idea passive income research with email Summary and PDF. Informational only.",
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
            text: "A daily report that picks one passive-income or cash-flow Idea for a defined operator profile, delivered as email Summary plus PDF at passive.xingai.app.",
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

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning className={`${outfit.variable} ${fraunces.variable}`}>
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
          <PrefsProvider>
            <AppChrome>{children}</AppChrome>
          </PrefsProvider>
        </AppThemeProvider>
      </body>
    </html>
  );
}
