"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { messages, type Locale, type Messages } from "@/lib/i18n/messages";

type PrefsCtx = {
  locale: Locale;
  setLocale: (l: Locale) => void;
  t: Messages;
};

const Ctx = createContext<PrefsCtx | null>(null);
const LOCALE_KEY = "xingai-daily-locale";

export function PrefsProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("en");

  useEffect(() => {
    const stored = window.localStorage.getItem(LOCALE_KEY) as Locale | null;
    const next =
      stored === "en" || stored === "zh" || stored === "ko" ? stored : "en";
    setLocaleState(next);
    document.documentElement.lang = next === "zh" ? "zh-CN" : next === "ko" ? "ko" : "en";
  }, []);

  const setLocale = useCallback((l: Locale) => {
    setLocaleState(l);
    window.localStorage.setItem(LOCALE_KEY, l);
    document.documentElement.lang = l === "zh" ? "zh-CN" : l === "ko" ? "ko" : "en";
  }, []);

  const value = useMemo(
    () => ({ locale, setLocale, t: messages[locale] }),
    [locale, setLocale],
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function usePrefs() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("usePrefs outside PrefsProvider");
  return ctx;
}
