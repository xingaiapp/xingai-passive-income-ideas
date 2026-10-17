import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PREFIXED = new Set(["zh", "ko"]);

/** English stays at the root; /zh and /ko are real URLs. Internally every page lives under /[locale]. */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.startsWith("/reports") ||
    pathname.startsWith("/data") ||
    /\.[a-zA-Z0-9]+$/.test(pathname)
  ) {
    return NextResponse.next();
  }

  const first = pathname.split("/")[1];

  if (first === "en") {
    const url = request.nextUrl.clone();
    url.pathname = pathname.slice(3) || "/";
    return NextResponse.redirect(url, 308);
  }
  if (PREFIXED.has(first)) return NextResponse.next();

  const url = request.nextUrl.clone();
  url.pathname = pathname === "/" ? "/en" : `/en${pathname}`;
  return NextResponse.rewrite(url);
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"] };
