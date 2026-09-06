/** Canonical site origin for metadata / sitemap. Empty env must not win over the default. */
export function getSiteUrl(): string {
  const raw = process.env.NEXT_PUBLIC_SITE_URL?.trim();
  if (raw) {
    try {
      return new URL(raw).origin;
    } catch {
      // fall through
    }
  }
  return "https://passive.xingai.app";
}
