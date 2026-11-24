#!/usr/bin/env python3
"""Check the generated static site for broken local routes and SEO basics."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PREFIX = "/stramine"
SITE = "https://clipperwhopp-source.github.io/stramine"


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.meta: dict[str, str] = {}
        self.title = ""
        self._title = False
        self.h1 = 0
        self.lang = None
        self.jsonld = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._title = True
        if tag == "h1":
            self.h1 += 1
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"] or "")
        if tag in ("img", "script") and a.get("src"):
            self.links.append(a["src"] or "")
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content") or ""
        if tag == "script" and a.get("type") == "application/ld+json":
            self.jsonld += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._title = False

    def handle_data(self, data: str) -> None:
        if self._title:
            self.title += data


def local_target(link: str) -> Path | None:
    parsed = urlparse(link)
    if parsed.scheme in ("mailto", "tel") or parsed.netloc and not parsed.netloc.endswith("clipperwhopp-source.github.io"):
        return None
    p = unquote(parsed.path)
    if p.startswith(PREFIX):
        p = p[len(PREFIX):]
    elif p.startswith("/"):
        return None
    else:
        return None
    target = DOCS / p.lstrip("/")
    return target / "index.html" if p.endswith("/") else target


def main() -> None:
    errors: list[str] = []
    canonical: dict[str, str] = {}
    count = 0
    for html_file in sorted(DOCS.rglob("*.html")):
        page = Page()
        page.feed(html_file.read_text(encoding="utf-8"))
        rel = html_file.relative_to(DOCS).as_posix()
        if not page.title:
            errors.append(f"{rel}: missing title")
        if not page.lang:
            errors.append(f"{rel}: missing HTML lang")
        if "/en/" in rel or "/tr/" in rel or rel == "index.html":
            if page.h1 != 1:
                errors.append(f"{rel}: expected one h1, got {page.h1}")
            if not page.meta.get("description") or not page.meta.get("og:image") or not page.meta.get("twitter:card"):
                errors.append(f"{rel}: incomplete SEO/social metadata")
            if "apps/" in rel and rel.count("/") == 3 and page.jsonld != 1:
                errors.append(f"{rel}: missing product JSON-LD")
        for link in page.links:
            target = local_target(link)
            if target is not None and not target.exists():
                errors.append(f"{rel}: broken local link {link}")
        count += 1
    for required in ("sitemap.xml", "robots.txt", "404.html", ".nojekyll", "assets/stramine-og.png", "assets/site.css"):
        if not (DOCS / required).exists():
            errors.append(f"missing {required}")
    html_text = "\n".join(p.read_text(encoding="utf-8") for p in DOCS.rglob("*.html"))
    if "play.google.com/store/apps/details" in html_text:
        errors.append("Unverified Google Play link appears in public HTML")
    if "google-analytics.com" in html_text or "googletagmanager.com" in html_text:
        errors.append("Tracking script appears in public HTML")
    if errors:
        print("FAIL", len(errors))
        for item in errors:
            print(item)
        raise SystemExit(1)
    print(f"PASS: {count} HTML files, local links, language, product schema, SEO/social files; no unverified Play buttons or trackers")


if __name__ == "__main__":
    main()
