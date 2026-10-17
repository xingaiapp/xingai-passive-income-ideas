"use client";

import { createContext, useCallback, useContext, useMemo, type ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";
import { messages, type Locale, type Messages } from "@/lib/i18n/messages";
import { localizedPath, stripLocale } from "@/lib/i18n/paths";

type PrefsCtx = {
  locale: Locale;
  setLocale: (l: Locale) => void;
  t: Messages;
};

const Ctx = createContext<PrefsCtx | null>(null);

/** The URL is the source of truth for the language; the switcher navigates to the same page in another locale. */
export function PrefsProvider({ locale, children }: { locale: Locale; children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();

  const setLocale = useCallback(
    (l: Locale) => {
      try {
        document.cookie = `xingai.locale=${l};path=/;max-age=31536000;SameSite=Lax`;
      } catch {
        // storage can be blocked; navigation still works
      }
      router.push(localizedPath(l, stripLocale(pathname)));
    },
    [router, pathname],
  );

  const value = useMemo(() => ({ locale, setLocale, t: messages[locale] }), [locale, setLocale]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function usePrefs() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("usePrefs outside PrefsProvider");
  return ctx;
}
