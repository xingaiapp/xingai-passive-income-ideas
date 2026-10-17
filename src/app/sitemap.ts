import type { MetadataRoute } from "next";
import { getSiteUrl } from "@/lib/site-url";
import { localizedPath } from "@/lib/i18n/paths";
import { locales } from "@/lib/i18n/messages";

const base = getSiteUrl();

export default function sitemap(): MetadataRoute.Sitemap {
  const paths = ["/", "/archive", "/how", "/legal/privacy", "/legal/terms", "/legal/disclaimer"];
  const now = new Date();
  const url = (locale: (typeof locales)[number], path: string) => {
    const p = localizedPath(locale, path);
    return `${base}${p === "/" ? "" : p}`;
  };
  // Legal pages are one trilingual document with an English canonical, so list them once.
  return paths.flatMap((path) =>
    (path.startsWith("/legal") ? (["en"] as const) : locales).map((locale) => ({
      url: url(locale, path),
      lastModified: now,
      changeFrequency: path === "/" ? ("daily" as const) : ("weekly" as const),
      priority: path === "/" ? 1 : 0.6,
      ...(path.startsWith("/legal")
        ? {}
        : {
            alternates: {
              languages: { en: url("en", path), "zh-CN": url("zh", path), ko: url("ko", path) },
            },
          }),
    })),
  );
}
