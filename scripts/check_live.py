#!/usr/bin/env python3
"""Read-only checks for the public deployment and established app URLs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://clipperwhopp-source.github.io/stramine"


class Meta(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.lang = ""
        self.canonical = ""
        self.alternates: set[str] = set()
        self.og_image = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang") or ""
        elif tag == "h1":
            self.h1 += 1
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href") or ""
        elif tag == "link" and a.get("rel") == "alternate":
            self.alternates.add(a.get("hreflang") or "")
        elif tag == "meta" and a.get("property") == "og:image":
            self.og_image = a.get("content") or ""


def get(url: str) -> dict:
    try:
        with urlopen(Request(url, headers={"User-Agent": "STRAMINE-live-audit/1.0"}), timeout=20) as response:
            body = response.read()
            return {"url": url, "status": response.status, "effective_url": response.url, "content_type": response.headers.get("content-type", ""), "body": body}
    except HTTPError as exc:
        return {"url": url, "status": exc.code, "effective_url": exc.url, "content_type": exc.headers.get("content-type", ""), "body": exc.read()}


def main() -> None:
    errors: list[str] = []
    results: list[dict] = []
    sitemap = get(SITE + "/sitemap.xml")
    if sitemap["status"] != 200:
        raise SystemExit(f"sitemap HTTP {sitemap['status']}")
    locs = [x.text for x in ET.fromstring(sitemap["body"]).iter() if x.tag.endswith("loc")]
    for url in locs:
        response = get(url)
        item = {k: v for k, v in response.items() if k != "body"}
        item["bytes"] = len(response["body"])
        if response["status"] != 200:
            errors.append(f"{url}: HTTP {response['status']}")
        else:
            page = Meta()
            page.feed(response["body"].decode("utf-8", errors="replace"))
            if page.h1 != 1 or page.canonical not in (url, SITE + "/en/") or not {"tr", "en", "x-default"} <= page.alternates or not page.og_image:
                errors.append(f"{url}: incomplete page metadata")
            item.update({"lang": page.lang, "canonical": page.canonical, "h1_count": page.h1, "hreflang": sorted(page.alternates)})
        results.append(item)
    for suffix in ("/robots.txt", "/assets/site.css", "/assets/stramine-og.png", "/tr/privacy/wallpair/", "/tr/privacy/bi-durum-usta/", "/tr/support/wallpair/", "/tr/support/bi-durum-usta/"):
        response = get(SITE + suffix)
        if response["status"] != 200:
            errors.append(f"{suffix}: HTTP {response['status']}")
    legacy = json.loads((ROOT / "reports/legacy-url-status.json").read_text(encoding="utf-8"))
    preserved = []
    for name, earlier in legacy["results"].items():
        if earlier["status"] != 200:
            continue
        response = get(earlier["url"])
        preserved.append({"name": name, "url": earlier["url"], "status": response["status"]})
        if response["status"] != 200:
            errors.append(f"old URL {name}: HTTP {response['status']}")
    report = {"checked_utc": datetime.now(timezone.utc).isoformat(), "site": SITE + "/", "canonical_pages": len(locs), "pages": results, "preserved_legacy_urls": preserved, "errors": errors}
    dest = ROOT / "reports/live-http-check.json"
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{'PASS' if not errors else 'FAIL'}: {len(locs)} canonical pages, {len(preserved)} preserved old URLs, {len(errors)} errors; evidence: {dest}")
    for error in errors:
        print(" -", error)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
