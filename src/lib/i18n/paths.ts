import { locales, type Locale } from "@/lib/i18n/messages";

/** English lives at the root; zh and ko get a URL prefix so each language is crawlable. */
export function isLocale(value: string | undefined): value is Locale {
  return !!value && (locales as string[]).includes(value);
}

export function stripLocale(pathname: string): string {
  const [, first, ...rest] = pathname.split("/");
  if (first === "zh" || first === "ko" || first === "en") return `/${rest.join("/")}`;
  return pathname || "/";
}

export function localizedPath(locale: Locale, path: string): string {
  const clean = path.startsWith("/") ? path : `/${path}`;
  if (locale === "en") return clean;
  return clean === "/" ? `/${locale}` : `/${locale}${clean}`;
}

export function htmlLang(locale: Locale): string {
  return locale === "zh" ? "zh-CN" : locale;
}
