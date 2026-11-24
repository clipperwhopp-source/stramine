#!/usr/bin/env python3
"""Build STRAMINE's bilingual static site from data/apps.json.

The generated docs/ tree is committed and served by GitHub Pages. No runtime
JavaScript, cookies, external fonts, analytics, or backend is required.
"""

from __future__ import annotations

import html
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
CSS_VERSION = hashlib.sha256((OUT / "assets/site.css").read_bytes()).hexdigest()[:10]
APPS = [app for app in json.loads((ROOT / "data/apps.json").read_text(encoding="utf-8")) if app.get("published")]
BASE_PATH = os.environ.get("STRAMINE_BASE_PATH", "/stramine").rstrip("/")
SITE_URL = os.environ.get("STRAMINE_SITE_URL", "https://clipperwhopp-source.github.io/stramine").rstrip("/")
CONTACT = "clipper.whopp@gmail.com"

T = {
    "en": {
        "nav": [("Apps", "apps/"), ("Studio", "about/"), ("Support", "support/"), ("Privacy", "privacy/")],
        "switch": "Türkçe",
        "tagline": "Made to be felt.",
        "hero": "Small ideas.<br><em>Lasting feeling.</em>",
        "hero_lead": "STRAMINE is an independent home for purposeful apps and playful games — crafted with care, built for real life.",
        "hero_aside": "Two published iOS experiences. One place to find their stories, official links, support and privacy information.",
        "explore": "Explore the work",
        "about": "Meet the studio",
        "work": "Selected work",
        "work_sub": "Different experiences, one attention to how they feel in your hands.",
        "approach": "Digital experiences with a human pulse.",
        "approach_body": "From a private moment shared between two people to the rhythm of a busy food shop, every product starts with a clear feeling and an honest purpose.",
        "see_all": "All apps",
        "view": "Explore app",
        "ios": "Available on the App Store",
        "android": "Android listing not verified",
        "app_store": "View on the App Store",
        "features": "The experience",
        "screens": "Inside the app",
        "related": "Another STRAMINE experience",
        "legal": "Support & privacy",
        "privacy": "Privacy policy",
        "support": "Support",
        "original": "Open the current official page",
        "privacy_note": "The app's current policy remains at its original public URL. This page is a directory to that app-specific policy and does not replace its legal text.",
        "support_note": "For help with this app, use the official support page or email the published support address. Never send passwords or verification codes.",
        "footer": "Independent apps and games, made with care.",
        "no_android": "No public Google Play listing could be verified in Türkiye on 24 November 2026, so no download button is shown.",
        "policy_date": "Policy last updated",
        "seller": "App Store seller",
    },
    "tr": {
        "nav": [("Uygulamalar", "apps/"), ("Stüdyo", "about/"), ("Destek", "support/"), ("Gizlilik", "privacy/")],
        "switch": "English",
        "tagline": "Hissettirmek için üretildi.",
        "hero": "Küçük fikirler.<br><em>Kalıcı hisler.</em>",
        "hero_lead": "STRAMINE, özenle tasarlanmış uygulamaların ve oyunların bağımsız evi. Her ürünün gerçek hayatta bir karşılığı var.",
        "hero_aside": "Yayındaki iki iOS deneyimi; hikâyeleri, resmî bağlantıları, destek ve gizlilik bilgileri tek yerde.",
        "explore": "Ürünleri keşfet",
        "about": "Stüdyoyu tanı",
        "work": "Seçili işler",
        "work_sub": "Farklı deneyimler; elde bıraktıkları hisse aynı özen.",
        "approach": "İnsana dokunan dijital deneyimler.",
        "approach_body": "İki kişi arasındaki özel bir paylaşımdan hareketli bir yemek dükkânına kadar her ürün, açık bir amaç ve gerçek bir hisle başlar.",
        "see_all": "Tüm uygulamalar",
        "view": "Ürünü keşfet",
        "ios": "App Store'da yayında",
        "android": "Android mağaza kaydı doğrulanmadı",
        "app_store": "App Store'da görüntüle",
        "features": "Deneyim",
        "screens": "Uygulamadan kareler",
        "related": "Başka bir STRAMINE deneyimi",
        "legal": "Destek ve gizlilik",
        "privacy": "Gizlilik politikası",
        "support": "Destek",
        "original": "Güncel resmî sayfayı aç",
        "privacy_note": "Uygulamanın güncel politikası kendi mevcut kamu URL'sinde korunur. Bu sayfa uygulamaya özel politikaya yönlendirir; yasal metnin yerine geçmez.",
        "support_note": "Bu uygulamayla ilgili yardım için resmî destek sayfasını veya yayımlanmış destek e-posta adresini kullanın. Parola veya doğrulama kodu göndermeyin.",
        "footer": "Özenle hazırlanmış bağımsız uygulamalar ve oyunlar.",
        "no_android": "24 Kasım 2026'da Türkiye için herkese açık Google Play kaydı doğrulanamadığından indirme düğmesi gösterilmiyor.",
        "policy_date": "Politika son güncelleme",
        "seller": "App Store satıcısı",
    },
}


def e(s: object) -> str:
    return html.escape(str(s), quote=True)


def path(locale: str, suffix: str = "") -> str:
    return f"{BASE_PATH}/{locale}/{suffix}" if suffix else f"{BASE_PATH}/{locale}/"


def url(locale: str, suffix: str = "") -> str:
    return f"{SITE_URL}/{locale}/{suffix}" if suffix else f"{SITE_URL}/{locale}/"


def asset(name: str) -> str:
    return f"{BASE_PATH}/assets/{quote(name)}"


def target(app: dict, field: str, locale: str) -> str:
    value = app[field]
    return value[locale] if isinstance(value, dict) else value


def write(route: str, content: str) -> None:
    dest = OUT / route / "index.html" if route else OUT / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")


def shell(
    locale: str,
    route: str,
    title: str,
    description: str,
    body: str,
    *,
    other_route: str | None = None,
    schema: dict | None = None,
    canonical: str | None = None,
) -> str:
    t = T[locale]
    other = "tr" if locale == "en" else "en"
    suffix = route.removeprefix(locale + "/") if route.startswith(locale + "/") else ""
    alternate = other_route if other_route is not None else suffix
    canonical = canonical or (SITE_URL + "/" if route == "" else SITE_URL + "/" + route.rstrip("/") + "/")
    en_url, tr_url = url("en", suffix), url("tr", suffix)
    if route == "":
        en_url, tr_url = url("en"), url("tr")
    nav = "".join(
        f'<a href="{e(path(locale, p))}"' + (' aria-current="page"' if suffix.startswith(p) else "") + f'>{e(label)}</a>'
        for label, p in t["nav"]
    )
    schema_html = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")}</script>' if schema else ""
    social_image = SITE_URL + "/assets/stramine-og.png"
    return f'''<!doctype html>
<html lang="{locale}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · STRAMINE</title><meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}"><link rel="alternate" hreflang="en" href="{e(en_url)}"><link rel="alternate" hreflang="tr" href="{e(tr_url)}"><link rel="alternate" hreflang="x-default" href="{e(SITE_URL + '/')}">
<meta property="og:type" content="website"><meta property="og:site_name" content="STRAMINE"><meta property="og:locale" content="{'tr_TR' if locale == 'tr' else 'en_US'}"><meta property="og:title" content="{e(title)} · STRAMINE"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{e(canonical)}"><meta property="og:image" content="{e(social_image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)} · STRAMINE"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{e(social_image)}">
<meta name="theme-color" content="#101416"><link rel="icon" type="image/svg+xml" href="{e(asset('stramine-mark.svg'))}"><link rel="apple-touch-icon" href="{e(asset('stramine-touch.png'))}"><link rel="stylesheet" href="{e(asset('site.css'))}?v={CSS_VERSION}">
{schema_html}</head><body>
<a class="skip" href="#main">{'Ana içeriğe geç' if locale == 'tr' else 'Skip to content'}</a>
<header class="site-header"><div class="container nav-inner"><a class="brand" href="{e(path(locale))}" aria-label="STRAMINE"><img src="{e(asset('stramine-mark.svg'))}" alt="">STRAMINE</a><nav class="main-nav" aria-label="{'Ana menü' if locale == 'tr' else 'Main navigation'}">{nav}</nav><div class="nav-actions"><a class="lang-link" href="{e(path(other, alternate))}" lang="{other}" hreflang="{other}"><span>↗</span> {e(t['switch'])}</a></div></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="container"><div class="footer-top"><div><a class="brand" href="{e(path(locale))}"><img src="{e(asset('stramine-mark.svg'))}" alt="">STRAMINE</a><p>{e(t['footer'])}</p></div><div><p class="meta">{'Explore' if locale == 'en' else 'Keşfet'}</p><div class="footer-links"><a href="{e(path(locale,'apps/'))}">{e(t['nav'][0][0])}</a><a href="{e(path(locale,'about/'))}">{e(t['nav'][1][0])}</a><a href="{e(path(locale,'contact/'))}">{'Contact' if locale == 'en' else 'İletişim'}</a></div></div><div><p class="meta">{'Help & trust' if locale == 'en' else 'Yardım ve güven'}</p><div class="footer-links"><a href="{e(path(locale,'support/'))}">{e(t['support'])}</a><a href="{e(path(locale,'privacy/'))}">{e(t['privacy'])}</a><a href="mailto:{CONTACT}">{CONTACT}</a></div></div></div><div class="footer-bottom"><span>© 2026 STRAMINE. {'An independent studio identity.' if locale == 'en' else 'Bağımsız stüdyo kimliği.'}</span><span>{'App Store seller identity is shown on each product page.' if locale == 'en' else 'App Store satıcı kimliği her ürün sayfasında belirtilir.'}</span></div></div></footer>
</body></html>'''


def eyebrow(label: str) -> str:
    return f'<p class="eyebrow">{e(label)}</p>'


def button(label: str, href: str, outline: bool = False, external: bool = False) -> str:
    cls = "button button-outline" if outline else "button"
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ""
    return f'<a class="{cls}" href="{e(href)}"{extra}>{e(label)} <span aria-hidden="true">↗</span></a>'


def app_icon(app: dict, *, css_class: str = "product-icon") -> str:
    return f'<img class="{css_class}" src="{e(asset(app["icon"]))}" alt="{e(app["short_name"])} icon" width="68" height="68">'


def product_card(app: dict, locale: str, number: int) -> str:
    copy = app["copy"][locale]
    shot = app["screenshots"][locale][0] if isinstance(app["screenshots"], dict) else app["screenshots"][0]
    href = path(locale, f'apps/{app["slug"]}/')
    return f'''<a class="product-card {app['slug'].replace('bi-durum-usta','bidurum')}" href="{e(href)}"><div class="card-top">{app_icon(app)}<span class="card-number">0{number} / {e(app['short_name'])}</span></div><img class="card-shot" src="{e(asset(shot))}" alt="" loading="lazy" width="600" height="1200"><div class="card-bottom"><div><p class="kicker">{e(copy['eyebrow'])}</p><h3>{e(app['short_name'])}</h3><p>{e(copy['summary'])}</p></div><span class="circle-arrow" aria-hidden="true">↗</span></div></a>'''


def home(locale: str, root: bool = False) -> str:
    t = T[locale]
    cards = "".join(product_card(app, locale, i) for i, app in enumerate(APPS, 1))
    body = f'''<section class="hero"><div class="container"><div class="hero-grid"><div>{eyebrow('Independent app & game studio' if locale == 'en' else 'Bağımsız uygulama ve oyun stüdyosu')}<h1>{t['hero']}</h1><p class="lead">{e(t['hero_lead'])}</p><div class="button-row">{button(t['explore'],path(locale,'apps/'))}{button(t['about'],path(locale,'about/'),True)}</div></div><aside class="hero-aside"><p class="meta">01 — 02 / STRAMINE</p><p>{e(t['hero_aside'])}</p></aside></div><div class="hero-index"><span>STRAMINE / 2026</span><span>{e(t['tagline'])}</span></div></div></section>
<section class="section-tight"><div class="container intro-line"><p class="meta">{'The studio' if locale == 'en' else 'Stüdyo'}</p><p>{e(t['approach_body'])}</p></div></section>
<section class="section container" id="work"><div class="section-head"><div>{eyebrow('Our work' if locale == 'en' else 'İşlerimiz')}<h2>{e(t['work'])}</h2></div><p>{e(t['work_sub'])}</p></div><div class="grid-2">{cards}</div><p style="margin-top:2rem"><a class="text-link" href="{e(path(locale,'apps/'))}">{e(t['see_all'])}</a></p></section>
<section class="statement"><div class="container">{eyebrow('A point of view' if locale == 'en' else 'Bir bakış açısı')}<h2>{e(t['approach'])}</h2><p>{e(t['approach_body'])}</p><p style="margin-top:2rem"><a class="text-link" href="{e(path(locale,'about/'))}">{e(t['about'])}</a></p></div></section>'''
    route = "" if root else f"{locale}/"
    description = t["hero_lead"]
    schema = {"@context": "https://schema.org", "@type": "WebSite", "name": "STRAMINE", "url": SITE_URL + "/", "inLanguage": ["en", "tr"], "description": description}
    return shell(locale, route, t["tagline"], description, body, schema=schema, canonical=url("en") if root else None)


def page_hero(locale: str, eyebrow_text: str, title: str, lead: str, cls: str = "") -> str:
    return f'<section class="page-hero {e(cls)}"><div class="container">{eyebrow(eyebrow_text)}<h1>{e(title)}</h1><p class="lead">{e(lead)}</p></div></section>'


def directory(locale: str) -> str:
    t = T[locale]
    title = "Apps & games" if locale == "en" else "Uygulamalar ve oyunlar"
    lead = "Explore the products released under the STRAMINE studio identity. Every store button points to a verified public listing." if locale == "en" else "STRAMINE stüdyo kimliği altında yayımlanan ürünleri keşfedin. Her mağaza düğmesi doğrulanmış bir kamu sayfasına gider."
    cards = "".join(product_card(app, locale, i) for i, app in enumerate(APPS, 1))
    body = page_hero(locale, "The collection" if locale == "en" else "Koleksiyon", title, lead) + f'<section class="section-tight container"><div class="grid-2">{cards}</div><p class="muted" style="margin-top:1.8rem">{e(t["no_android"])}</p></section>'
    return shell(locale, f"{locale}/apps/", title, lead, body)


def product(locale: str, app: dict) -> str:
    t, c = T[locale], app["copy"][locale]
    slug = app["slug"]
    shots = app["screenshots"][locale] if isinstance(app["screenshots"], dict) else app["screenshots"]
    items = "".join(f'<figure><img src="{e(asset(s))}" alt="{e(app["short_name"])} — {"official App Store screenshot" if locale == "en" else "resmî App Store ekran görüntüsü"} {i}" loading="lazy" width="600" height="1200"><figcaption>{e(app["short_name"])} / 0{i}</figcaption></figure>' for i, s in enumerate(shots, 1))
    features = "".join(f'<article class="feature"><p class="meta">0{i} / {e(t["features"])}</p><h3>{e(feature)}</h3></article>' for i, feature in enumerate(c["features"], 1))
    other = next(x for x in APPS if x["slug"] != slug)
    detail_class = "bidurum" if slug == "bi-durum-usta" else "wallpair"
    genre = f'<p class="genre-line">{e(app["genre"][locale])}</p>' if app.get("genre") else ""
    body = f'''<section class="container detail-hero"><div><p class="breadcrumbs"><a href="{e(path(locale,'apps/'))}">{e(t['nav'][0][0])}</a> / <span>{e(app['short_name'])}</span></p>{app_icon(app)}{eyebrow(c['eyebrow'])}<h1>{e(c['headline'])}</h1><p class="lead">{e(c['summary'])}</p>{genre}<div class="button-row">{button(t['app_store'],app['app_store'],external=True)}{button(t['support'],path(locale,f'support/{slug}/'),True)}</div><div class="availability"><span class="status-chip available">iPhone & iPad · {e(t['ios'])}</span><span class="status-chip">{e(t['android'])}</span></div></div><div class="detail-stage {detail_class}"><img src="{e(asset(shots[0]))}" alt="{e(app['short_name'])} — {'official game screenshot' if locale == 'en' else 'resmî oyun ekran görüntüsü'}" width="600" height="1200"></div></section>
<section class="section-tight container"><div class="section-head"><div>{eyebrow('Made for the moment' if locale == 'en' else 'An için tasarlandı')}<h2>{e(t['features'])}</h2></div><p>{e(c['summary'])}</p></div><div class="grid-3">{features}</div></section>
<section class="section container"><div class="section-head"><div>{eyebrow('Real screens' if locale == 'en' else 'Gerçek ekranlar')}<h2>{e(t['screens'])}</h2></div><p>{'Captured from the published App Store materials.' if locale == 'en' else 'Yayımlanmış App Store görsellerinden alınmıştır.'}</p></div><div class="gallery {'gallery-4' if len(shots)>3 else ''}">{items}</div></section>
<section class="section-tight container"><div class="section-head"><div>{eyebrow('Know where you stand' if locale == 'en' else 'Bilgi ve destek')}<h2>{e(t['legal'])}</h2></div><p>{e(t['no_android'])}</p></div><div class="legal-links"><article class="info-card"><p class="meta">{e(t['privacy'])}</p><h3>{e(app['short_name'])}</h3><p>{e(t['privacy_note'])}</p><a class="text-link" href="{e(path(locale,f'privacy/{slug}/'))}">{e(t['privacy'])}</a></article><article class="info-card"><p class="meta">{e(t['support'])}</p><h3>{e(app['short_name'])}</h3><p>{e(t['support_note'])}</p><a class="text-link" href="{e(path(locale,f'support/{slug}/'))}">{e(t['support'])}</a></article></div><p class="muted" style="margin-top:1.7rem">{e(t['seller'])}: {e(app['store_seller'])}. STRAMINE {'is the studio brand, not a separately verified legal entity.' if locale == 'en' else 'stüdyo markasıdır; ayrı bir tüzel kişilik olarak doğrulanmamıştır.'}</p></section>
<section class="statement"><div class="container">{eyebrow(t['related'])}<h2>{e(other['copy'][locale]['headline'])}</h2><p>{e(other['copy'][locale]['summary'])}</p><p style="margin-top:2rem"><a class="text-link" href="{e(path(locale,f'apps/{other["slug"]}/'))}">{e(t['view'])}</a></p></div></section>'''
    schema = {"@context": "https://schema.org", "@type": app["type"], "name": app["name"], "description": c["summary"], "url": url(locale, f"apps/{slug}/"), "image": SITE_URL + "/assets/" + quote(shots[0]), "operatingSystem": "iOS, iPadOS", "applicationCategory": app["category"], "sameAs": app["app_store"], "publisher": {"@type": "Person", "name": app["store_seller"]}}
    seo = app["seo"][locale]
    return shell(locale, f"{locale}/apps/{slug}/", seo["title"], seo["description"], body, schema=schema)


def about(locale: str) -> str:
    title = "A studio for things that matter" if locale == "en" else "Önemli hisler için bir stüdyo"
    lead = "STRAMINE is a public-facing independent studio identity for apps and games." if locale == "en" else "STRAMINE, uygulama ve oyunların bağımsız stüdyo kimliğidir."
    body = page_hero(locale, "The studio" if locale == "en" else "Stüdyo", title, lead)
    body += f'''<section class="section-tight container plain-content"><h2>{'A clear purpose in every product' if locale == 'en' else 'Her üründe açık bir amaç'}</h2><p>{'WallPair is built around private sharing between two people. Bi Dürüm Usta! turns familiar street-food preparation into a colorful, hands-on game. These products differ in mood and function, but both are presented here with their real capabilities, store links and app-specific support.' if locale == 'en' else 'WallPair iki kişi arasındaki özel paylaşıma odaklanır. Bi Dürüm Usta! tanıdık sokak lezzetlerini renkli ve dokunarak oynanan bir oyuna dönüştürür. Bu ürünler farklı hisler sunar; ikisi de burada gerçek özellikleri, mağaza bağlantıları ve uygulamaya özel destek bilgileriyle yer alır.'}</p><div class="notice"><p>{'STRAMINE is a studio brand. Store seller and data-controller identities are given in each app’s own listing and legal policy; this site does not claim a separate incorporated company.' if locale == 'en' else 'STRAMINE bir stüdyo markasıdır. Mağaza satıcısı ve veri sorumlusu kimlikleri her uygulamanın kendi mağaza kaydı ve yasal politikasında belirtilir; bu site ayrı bir şirket kurulduğunu iddia etmez.'}</p></div>{button(T[locale]['explore'],path(locale,'apps/'))}</section>'''
    return shell(locale, f"{locale}/about/", title, lead, body)


def hub(locale: str, kind: str) -> str:
    privacy = kind == "privacy"
    title = ("Privacy, product by product" if locale == "en" else "Her ürün için ayrı gizlilik") if privacy else ("Support, without the maze" if locale == "en" else "İhtiyacınız olan desteğe ulaşın")
    lead = ("Each app has its own policy. The original published policies remain available at their established URLs." if locale == "en" else "Her uygulamanın kendine ait politikası vardır. Yayımlanmış özgün politikalar mevcut adreslerinde erişilebilir kalır.") if privacy else ("Choose the product you use to reach its official help route and contact details." if locale == "en" else "Kullandığınız ürünü seçerek resmî yardım yoluna ve iletişim bilgilerine ulaşın.")
    cards = ""
    for app in APPS:
        slug = app["slug"]
        cards += f'<article class="info-card">{app_icon(app)}<h3>{e(app["short_name"])}</h3><p>{e(app["copy"][locale]["summary"])}</p><a class="text-link" href="{e(path(locale,f"{kind}/{slug}/"))}">{e(T[locale][kind])}</a></article>'
    body = page_hero(locale, "Help & trust" if locale == "en" else "Yardım ve güven", title, lead) + f'<section class="section-tight container"><div class="grid-2">{cards}</div></section>'
    return shell(locale, f"{locale}/{kind}/", title, lead, body)


def app_info(locale: str, app: dict, kind: str) -> str:
    t = T[locale]
    privacy = kind == "privacy"
    title = f"{app['short_name']} — {t[kind]}"
    lead = t["privacy_note"] if privacy else t["support_note"]
    original = target(app, f"{kind}_original", locale)
    date = app["policy_date"][locale]
    status_text = (f'{e(t["policy_date"])}: {e(date)}. ' if privacy else '') + ('The complete app-specific text is maintained at the link below.' if privacy and locale=='en' else 'Uygulamaya özel tam metin aşağıdaki bağlantıda korunur.' if privacy else 'Use the link below for current support instructions.' if locale=='en' else 'Güncel destek yönergeleri için aşağıdaki bağlantıyı kullanın.')
    content = f'''<section class="section-tight container plain-content"><p class="breadcrumbs"><a href="{e(path(locale,kind+'/'))}">{e(t[kind])}</a> / <span>{e(app['short_name'])}</span></p><div class="notice"><p>{e(lead)}</p></div><h2>{'Current published page' if locale == 'en' else 'Yayındaki mevcut sayfa'}</h2><p>{status_text}</p><p style="margin-top:1.5rem">{button(t['original'],original,external=True)}</p><h2>{'Direct contact' if locale=='en' else 'Doğrudan iletişim'}</h2><p><a href="mailto:{CONTACT}?subject={quote(app['short_name']+' support')}">{CONTACT}</a></p><h2>{'Related links' if locale=='en' else 'İlgili bağlantılar'}</h2><ul><li><a href="{e(app['app_store'])}">{e(t['app_store'])}</a></li><li><a href="{e(path(locale,f'apps/{app["slug"]}/'))}">{e(app['short_name'])}</a></li>'''
    if app.get("delete_original"):
        content += f'<li><a href="{e(app["delete_original"])}">{"Account deletion instructions" if locale=="en" else "Hesap silme talimatları"}</a></li>'
    if app.get("terms_original"):
        content += f'<li><a href="{e(app["terms_original"])}">{"Terms of Use" if locale=="en" else "Kullanım koşulları"}</a></li>'
    content += '</ul></section>'
    body = page_hero(locale, "App-specific information" if locale == "en" else "Uygulamaya özel bilgi", title, lead) + content
    return shell(locale, f"{locale}/{kind}/{app['slug']}/", title, lead, body)


def contact(locale: str) -> str:
    title = "Let's connect" if locale == "en" else "İletişime geçelim"
    lead = "For help with an app, choose its support page so your request reaches the right context." if locale == "en" else "Bir uygulamayla ilgili yardım için önce o ürünün destek sayfasını seçin."
    body = page_hero(locale, "Contact" if locale == "en" else "İletişim", title, lead)
    body += f'<section class="section-tight container plain-content"><h2>{"Published support address" if locale=="en" else "Yayımlanmış destek adresi"}</h2><p><a href="mailto:{CONTACT}">{CONTACT}</a></p><p>{"Please do not send passwords, verification codes or payment details." if locale=="en" else "Lütfen parola, doğrulama kodu veya ödeme bilgisi göndermeyin."}</p><p style="margin-top:1.5rem">{button(T[locale]["support"],path(locale,"support/"))}</p></section>'
    return shell(locale, f"{locale}/contact/", title, lead, body)


def delete_account(locale: str) -> str:
    app = APPS[0]
    title = "WallPair account deletion" if locale == "en" else "WallPair hesabını silme"
    lead = "Use the in-app Settings → Delete Account control. The complete, current instructions remain on WallPair's original public page." if locale == "en" else "Uygulamada Ayarlar → Hesabı Sil yolunu kullanın. Tam ve güncel talimatlar WallPair'in mevcut kamu sayfasında korunur."
    body = page_hero(locale, "WallPair" , title, lead)
    body += f'<section class="section-tight container plain-content"><div class="notice"><p>{e(lead)}</p></div>{button(T[locale]["original"],app["delete_original"],external=True)}<h2>{"Need help?" if locale=="en" else "Yardıma mı ihtiyacınız var?"}</h2><p><a href="{e(path(locale,"support/wallpair/"))}">{e(T[locale]["support"])}</a> · <a href="mailto:{CONTACT}">{CONTACT}</a></p></section>'
    return shell(locale, f"{locale}/delete-account/wallpair/", title, lead, body)


def redirect(destination: str, label: str) -> str:
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={e(destination)}"><link rel="canonical" href="{e(destination)}"><title>{e(label)} · STRAMINE</title></head><body><p><a href="{e(destination)}">{e(label)} →</a></p></body></html>'


def build() -> None:
    write("", home("en", root=True))
    routes = [SITE_URL + "/"]
    for locale in ("en", "tr"):
        pages = {
            "": home(locale),
            "apps/": directory(locale),
            "about/": about(locale),
            "support/": hub(locale, "support"),
            "privacy/": hub(locale, "privacy"),
            "contact/": contact(locale),
            "delete-account/wallpair/": delete_account(locale),
        }
        for app in APPS:
            slug = app["slug"]
            pages[f"apps/{slug}/"] = product(locale, app)
            pages[f"privacy/{slug}/"] = app_info(locale, app, "privacy")
            pages[f"support/{slug}/"] = app_info(locale, app, "support")
        for suffix, markup in pages.items():
            write(f"{locale}/{suffix}", markup)
            routes.append(url(locale, suffix))
    for suffix in ("apps/", "about/", "support/", "privacy/", "contact/", "apps/wallpair/", "apps/bi-durum-usta/", "privacy/wallpair/", "privacy/bi-durum-usta/", "support/wallpair/", "support/bi-durum-usta/"):
        write(suffix, redirect(url("en", suffix), "Continue to STRAMINE"))
    write("404", shell("en", "404/", "Page not found", "The page you requested could not be found.", page_hero("en", "404", "A different path.", "This page could not be found. Explore the current apps or return to the studio home.") + f'<section class="section-tight container">{button("Back to STRAMINE",path("en"))}</section>'))
    (OUT / "404.html").write_text((OUT / "404/index.html").read_text(encoding="utf-8").replace('<meta charset="utf-8">', '<meta charset="utf-8"><meta name="robots" content="noindex">', 1), encoding="utf-8")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{e(u)}</loc></url>\n' for u in routes) + '</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n', encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Built {len(routes)} canonical pages plus redirects in {OUT}")


if __name__ == "__main__":
    build()
