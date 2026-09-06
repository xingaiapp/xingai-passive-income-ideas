import type { MetadataRoute } from "next";
import { getSiteUrl } from "@/lib/site-url";

const base = getSiteUrl();

export default function sitemap(): MetadataRoute.Sitemap {
  const paths = ["/", "/archive", "/how", "/legal/privacy", "/legal/terms", "/legal/disclaimer"];
  const now = new Date();
  return paths.map((path) => ({
    url: `${base}${path === "/" ? "" : path}`,
    lastModified: now,
    changeFrequency: path === "/" ? "daily" : "weekly",
    priority: path === "/" ? 1 : 0.6,
  }));
}
