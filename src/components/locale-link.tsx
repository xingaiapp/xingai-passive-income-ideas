"use client";

import Link from "next/link";
import type { ComponentProps } from "react";
import { usePrefs } from "@/components/prefs-provider";
import { localizedPath } from "@/lib/i18n/paths";

type Props = Omit<ComponentProps<typeof Link>, "href"> & { href: string };

/** next/link that keeps the visitor in their language for internal paths. */
export default function LocaleLink({ href, ...rest }: Props) {
  const { locale } = usePrefs();
  const target = href.startsWith("/") ? localizedPath(locale, href) : href;
  return <Link href={target} {...rest} />;
}
