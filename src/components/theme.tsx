"use client";

import { ThemeProvider, useTheme } from "next-themes";
import { useEffect, useState, type ReactNode } from "react";

export function AppThemeProvider({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      <ThemeColorSync />
      {children}
    </ThemeProvider>
  );
}

function ThemeColorSync() {
  const { resolvedTheme } = useTheme();
  useEffect(() => {
    const meta = document.querySelector('meta[name="theme-color"]');
    if (!meta) return;
    meta.setAttribute("content", resolvedTheme === "dark" ? "#141a14" : "#f6f8f5");
  }, [resolvedTheme]);
  return null;
}

export function ThemeToggle({ lightLabel, darkLabel }: { lightLabel: string; darkLabel: string }) {
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) {
    return (
      <button type="button" className="touch-btn" aria-label={lightLabel}>
        ·
      </button>
    );
  }
  const dark = resolvedTheme === "dark";
  return (
    <button
      type="button"
      className="touch-btn"
      onClick={() => setTheme(dark ? "light" : "dark")}
      aria-label={dark ? lightLabel : darkLabel}
    >
      {dark ? lightLabel : darkLabel}
    </button>
  );
}
