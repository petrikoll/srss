from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlparse, urlencode, quote
from digital_tools import build_digital_tools, build_nno_system
from system_pages import build_business_system, build_team_portal, build_elai
from portfolio_extensions import build_esf_generator, build_opz_tools, build_bio_registry

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CATALOG = json.loads((ROOT / "src/catalog.json").read_text(encoding="utf-8"))
LEGACY = CATALOG["legacy"]
SOURCES = {item["id"]: item for item in LEGACY["zdroje"]}

ILLUSTRATIONS = {
    "about-team": "Ilustrace spolupráce obcí, organizací a veřejnosti u společného stolu",
    "service-debt": "Ilustrace respektujícího rozhovoru dvou dospělých v poradně",
    "debt-scene": "Ilustrace diskrétního poradenského rozhovoru ve světlé místnosti",
    "service-community": "Ilustrace pracovní skupiny nad mapou dostupných služeb",
    "service-evaluation": "Ilustrace společného vyhodnocování plánu a výsledků projektu",
    "projects-process": "Ilustrace přípravy projektu a jeho přínosu pro místní komunitu",
    "documents": "Přehledně uspořádané dokumenty a složka",
    "contact-region": "Ilustrační pohled na město pod horami; nejde o skutečné sídlo společnosti",
    "project-family": "Ilustrace rodiny při společném rozhovoru s poradcem",
    "project-prevention": "Ilustrace praktické konzultace a prevence dluhů",
    "project-training": "Ilustrace odborného vzdělávání pracovníků v sociální oblasti",
    "project-access": "Ilustrace dostupného komunitního centra a jeho návštěvníků",
    "project-cooperation": "Ilustrace spolupráce organizací a veřejnosti",
}

ICON_PATHS = {
    "advice": '<path d="M20 11a8 8 0 0 1-8 8H8l-5 3 1.5-5A8 8 0 1 1 20 11Z"/><path d="m8 11 2.5 2.5 5-5"/>',
    "map": '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z"/><path d="M9 3v15M15 6v15"/>',
    "project": '<rect x="4" y="4" width="16" height="17" rx="2"/><path d="M9 4V2h6v2M8 16v-3M12 16v-6M16 16V8"/>',
    "report": '<path d="M14 2H5v20h14V7l-5-5Z"/><path d="M14 2v5h5M8 17v-3M12 17v-6M16 17v-4"/>',
    "form": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h1M12 8h5M8 12h1M12 12h5M8 16h1M12 16h5"/>',
    "method": '<path d="M12 5c-3-2-7-2-10-1v15c3-1 7-1 10 1 3-2 7-2 10-1V4c-3-1-7-1-10 1ZM12 5v15"/>',
    "verified": '<path d="M14 2H5v20h14V7l-5-5Z"/><path d="M14 2v5h5m-10 8 2 2 4-5"/>',
    "location": '<path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "workflow": '<rect x="2" y="3" width="7" height="5" rx="1"/><rect x="15" y="16" width="7" height="5" rx="1"/><path d="M5.5 8v10.5H15M9 5.5h9.5V16m-3-3 3 3 3-3"/>',
    "evaluation": '<path d="M3 3v18h18M7 16v-4M11 16V8M15 16v-2m0-8 2 2 4-5"/>',
    "strategy": '<path d="M14 2H4v20h16V8l-6-6ZM14 2v6h6M8 12h8M8 16h3m2 0h3M8 19h8"/>',
    "insolvency": '<rect x="3" y="3" width="13" height="17" rx="2"/><path d="M6 7h7M6 11h4M6 15h3"/><circle cx="16" cy="15" r="4"/><path d="m19 18 3 3"/>',
    "scan": '<path d="M7 3H3v4M17 3h4v4M3 17v4h4M21 17v4h-4M2 12h20"/><path d="M7 8h10M7 16h6"/>',
    "calculator": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M7 5h10v4H7zM7 13h2M15 13h2M8 12v2M7 17h2M15 17h2M15 20h2M8 16v2"/>',
}


def icon(name: str, css_class: str = "") -> str:
    return f'<span class="line-icon {esc(css_class)}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[name]}</svg></span>'


def illustration(name: str, css_class: str = "", eager: bool = False, decorative: bool = False) -> str:
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    alt = "" if decorative else ILLUSTRATIONS[name]
    return f'<img class="illustration illustration--{esc(name)} {esc(css_class)}" src="/assets/illustrations/{esc(name)}.webp" width="1200" height="800" alt="{esc(alt)}" {loading} decoding="async">'


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def safe_link(url: str, label: str, cls: str = "") -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return ""
    return f'<a class="{esc(cls)}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'


CONTACT_NAME = "Bc. Lenka Tichavská"
CONTACT_PHONE = "+420 736 472 168"
CONTACT_TEL = "+420736472168"
CONTACT_EMAIL = "srssjesenik@gmail.com"
DEBT_MAILTO = "mailto:" + CONTACT_EMAIL + "?" + urlencode({"subject": "Konzultace v dluhové poradně"}, quote_via=quote)
PROFESSIONAL_MAILTO = "mailto:" + CONTACT_EMAIL + "?" + urlencode({"subject": "Poptávka odborných služeb"}, quote_via=quote)

PAGES = [
    ("/", "Úvod"),
    ("/dluhova-poradna/", "Pomoc s dluhy"),
    ("/oblasti-podpory/", "Pro obce a organizace"),
    ("/digitalni-nastroje/", "Digitální nástroje"),
    ("/projekty/", "Projekty"),
    ("/o-spolecnosti/", "O nás"),
    ("/dokumenty/", "Dokumenty"),
    ("/kontakty/", "Kontakt"),
]
SEO_TITLES = {
    "/": "Dluhová poradna a rozvoj sociálních služeb | SRSS Jeseník",
    "/dluhova-poradna/": "Dluhová poradna Jeseník – bezplatná pomoc s dluhy | SRSS",
    "/oblasti-podpory/": "Služby pro obce a organizace | SRSS Jeseník",
    "/digitalni-nastroje/": "Digitální nástroje a informační systémy na míru | SRSS Jeseník",
    "/digitalni-nastroje/projektova-evidence-a-evaluace/": "Projektová evidence a evaluace pro NNO | SRSS Jeseník",
    "/digitalni-nastroje/firemni-systemy/": "Firemní informační systémy na míru | SRSS Jeseník",
    "/digitalni-nastroje/tymovy-portal/": "Týmový portál pro sociální služby a projekty | SRSS Jeseník",
    "/digitalni-nastroje/elai/": "E.L.A.I. – AI asistent pro dluhové poradce | SRSS Jeseník",
    "/digitalni-nastroje/generator-importu-esf/": "Generátor importů do IS ESF 21+ | SRSS Jeseník",
    "/digitalni-nastroje/nastroje-pro-opz/": "Nástroje pro OPZ+ – importy, rozpočet a evaluace | SRSS Jeseník",
    "/digitalni-nastroje/bio-registry/": "BIO Registry – evropské bio firmy v jedné databázi | SRSS Jeseník",
    "/projekty/": "Projekty a reference | SRSS Jeseník",
    "/o-spolecnosti/": "O nás | Středisko rozvoje sociálních služeb Jeseník",
    "/dokumenty/": "Dokumenty | SRSS Jeseník",
    "/kontakty/": "Kontakt | SRSS Jeseník",
}


def shell(title: str, description: str, path: str, main: str) -> str:
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == path or (href == "/digitalni-nastroje/" and path.startswith(href)) else ""}{ " class=\"nav-cta\"" if href == "/kontakty/" else ""}>{esc(name)}</a>'
        for href, name in PAGES if href != "/"
    )
    footer_nav = "".join(f'<a href="{href}">{esc(name)}</a>' for href, name in PAGES[1:])
    return f'''<!doctype html>
<html lang="cs"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#ffffff">
<meta name="description" content="{esc(description)}">
<title>{esc(SEO_TITLES.get(path, title))}</title>
<link rel="stylesheet" href="/assets/site.css?v=19">
</head><body>
<a class="skip" href="#obsah">Přejít na obsah</a>
<header class="site-header"><div class="wrap nav-wrap">
<a class="brand" href="/" aria-label="Středisko rozvoje sociálních služeb – úvod"><span class="brand-image" role="img" aria-label="Logo Střediska rozvoje sociálních služeb"></span></a>
<button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false">Menu <span aria-hidden="true">☰</span></button>
<nav id="site-nav" class="nav-links" aria-label="Hlavní navigace">{nav}</nav>
</div></header>
<main id="obsah">{main}</main>
<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div><div class="footbrand">Středisko rozvoje<br>sociálních služeb, o.p.s.</div><p>Na Stráni 297/22, 790 01 Jeseník – Bukovice<br>IČO 27847977 · datová schránka bkyt4gn</p></div>
<div><h3>Dluhová poradna</h3><p class="footer-contact-name">{CONTACT_NAME}<br>Dluhová poradkyně</p><nav aria-label="Kontakty"><a href="tel:{CONTACT_TEL}">{CONTACT_PHONE}</a><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><a href="/kontakty/">Vybrat správný kontakt →</a></nav><p class="footer-general"><a href="{PROFESSIONAL_MAILTO}">Napsat SRSS za obec či organizaci →</a></p></div>
<div><h3>Na webu</h3><nav>{footer_nav}</nav></div>
</div>
<div class="footer-bottom"><span>© 2026 Středisko rozvoje sociálních služeb, o.p.s.</span><span>Podpora · Rozvoj · Příležitosti</span></div>
</div></footer>
<script src="/assets/site.js?v=3" defer></script></body></html>'''


def page_hero(title: str, subtitle: str, breadcrumb: str, visual: str = "", compact: bool = False, extra_content: str = "") -> str:
    classes = "page-hero" + (" page-hero--illustrated" if visual else "") + (" page-hero--compact" if compact else "")
    picture = f'<figure class="page-hero-art">{illustration(visual, eager=True)}' if visual else ""
    if visual == "contact-region":
        picture += '<figcaption>Ilustrační motiv regionu</figcaption>'
    if picture:
        picture += '</figure>'
    return f'''<section class="{classes}"><div class="wrap"><div class="page-hero-copy"><div class="breadcrumbs"><a href="/">Úvod</a> / {esc(breadcrumb)}</div><h1>{esc(title)}</h1><p>{esc(subtitle)}</p>{extra_content}</div>{picture}</div></section>'''


def section(title: str, body: str, eyebrow: str = "", alt: bool = False, anchor: str = "", heading_icon: str = "") -> str:
    label = f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    identifier = f' id="{esc(anchor)}"' if anchor else ""
    heading = f'<div class="icon-heading">{icon(heading_icon)}<h2>{esc(title)}</h2></div>' if heading_icon else f'<h2>{esc(title)}</h2>'
    return f'<section class="section{" alt" if alt else ""}"{identifier}><div class="wrap">{label}{heading}{body}</div></section>'


def write_page(path: str, title: str, desc: str, body: str):
    target = DIST / path.lstrip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(shell(title, desc, path, body), encoding="utf-8")


def project_card(title: str, category: str, summary: str, url: str = "") -> str:
    source = safe_link(url, "Archivní článek ↗", "link-arrow") if url else ""
    return f'<article class="record"><small>{esc(category)}</small><h3>{esc(title)}</h3><p>{esc(summary)}</p>{source}</article>'


REFERENCE_ANCHORS = {
    "Jesenicko proti dluhům III": "jesenicko-proti-dluhum-iii",
    "Jesenicko proti dluhům II": "jesenicko-proti-dluhum-ii",
    "Jesenicko proti dluhům": "jesenicko-proti-dluhum-i",
    "Střednědobé plánování na SO ORP Mohelnice": "planovani-mohelnicko",
    "Podpora střednědobého plánování sociálních služeb Konicka": "planovani-konicko",
    "Dluhové a pracovní poradenství na Osoblažsku II": "poradenstvi-osoblazsko",
}


def reference_card(title: str, category: str, audience: str, role: str, result: str, url: str, registration: str = "", source_label: str = "Více o projektu") -> str:
    registration_html = f'<p class="reference-registration">Reg. č. {esc(registration)}</p>' if registration else ""
    identifier = f' id="{REFERENCE_ANCHORS[title]}"' if title in REFERENCE_ANCHORS else ""
    return f'<article class="project-card"{identifier}><div class="project-card-body"><small>{esc(category)}</small><h3>{esc(title)}</h3><dl class="reference-facts"><div><dt>Pro koho</dt><dd>{esc(audience)}</dd></div><div><dt>Naše role</dt><dd>{esc(role)}</dd></div><div><dt>Výstupy a přínos</dt><dd>{esc(result)}</dd></div></dl>{registration_html}{safe_link(url, source_label + " ↗", "link-arrow")}</div></article>'


DEBT_CONTACT = f'''<div class="contact-person"><strong>{CONTACT_NAME}</strong><span>Dluhová poradkyně</span><a href="tel:{CONTACT_TEL}">{CONTACT_PHONE}</a><a href="{DEBT_MAILTO}">{CONTACT_EMAIL}</a></div>'''
DEBT_ACTIONS = f'''<div class="contact-actions"><a class="button dark" href="tel:{CONTACT_TEL}">Zavolat poradkyni</a><a class="button contact-email" href="{DEBT_MAILTO}">Napsat e-mail</a></div>'''
DEBT_HOURS = '''<table class="opening-hours"><caption>Provozní doba poradny</caption><tbody><tr><th scope="row">Pondělí</th><td>7:30–12:00, 12:30–16:00</td></tr><tr><th scope="row">Úterý</th><td>7:30–12:00, 12:30–16:00</td></tr><tr><th scope="row">Středa</th><td>Ověřte telefonicky</td></tr><tr><th scope="row">Čtvrtek</th><td>7:30–12:00, 12:30–16:00</td></tr><tr><th scope="row">Pátek</th><td>Zavřeno</td></tr></tbody></table><p class="visit-note">Před návštěvou se prosím domluvte s poradkyní na termínu.</p>'''
OFFICE_PHOTO = '''<figure class="office-photo"><a href="/assets/poradna-budova.png" target="_blank" rel="noopener" aria-label="Zvětšit snímek budovy poradny"><img src="/assets/poradna-budova.png" width="1711" height="919" loading="lazy" decoding="async" alt="Pohled na ulici 28. října v Jeseníku; červená šipka označuje modrou budovu, ve které je poradna"></a><figcaption>Šipka označuje budovu poradny na adrese 28. října 896/19. Použijte vedlejší vchod do budovy modrého Zverimaxu.</figcaption></figure>'''


def location_map(title: str, address: str, latitude: float, longitude: float, description: str) -> str:
    query = urlencode({"bbox": f"{longitude-.0035},{latitude-.002},{longitude+.0035},{latitude+.002}", "layer": "mapnik", "marker": f"{latitude},{longitude}"})
    url = "https://www.openstreetmap.org/export/embed.html?" + query
    map_link = f'https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=17/{latitude}/{longitude}'
    return f'<article class="location-card"><div class="location-heading">{icon("location")}<div><h3>{esc(title)}</h3><p>{esc(address)}</p></div></div><p>{esc(description)}</p><iframe title="Mapa: {esc(title)} – {esc(address)}" src="{esc(url)}" loading="lazy" referrerpolicy="no-referrer" allowfullscreen></iframe><div class="map-footer">{safe_link(map_link,"Otevřít větší mapu →","link-arrow")}<span>© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a></span></div></article>'


PROJECT_SERVICES = [
    {
        "id": "tvorba-projektu", "title": "Tvorba projektů", "icon": "project",
        "summary": "Projektový záměr, žádost, rozpočet a plán aktivit na míru.",
        "description": "Konzultujeme váš záměr a zpracujeme projektovou žádost, rozpočet a plán aktivit podle potřeb vaší obce nebo organizace.",
        "service_icon": "workflow", "intro": "Připravíme projekt podle potřeb vaší obce nebo organizace.",
        "includes": ["Konzultace záměru a projektová žádost", "Rozpočet a zdůvodnění nákladů", "Plán aktivit a harmonogram"],
        "url": "/projekty/", "link": "Projekty na míru a reference",
        "home_link": "Jak pomáháme s tvorbou projektů",
    },
    {
        "id": "administrace-a-rizeni", "title": "Administrace a řízení realizace projektů", "icon": "form",
        "summary": "Administrace, koordinace realizace, harmonogram a průběžné zprávy.",
        "description": "Zajistíme administraci projektu, koordinaci jeho realizace, sledování harmonogramu a přípravu průběžných podkladů a zpráv.",
        "service_icon": "form", "intro": "Pohlídáme administrativu i průběh realizace vašeho projektu.",
        "includes": ["Koordinace týmu a harmonogramu", "Administrace a průběžné podklady", "Zprávy o realizaci projektu"],
        "url": "/kontakty/#odborne-sluzby", "link": "Domluvit řízení projektu",
        "home_link": "Administrace a řízení projektů – podrobnosti",
    },
    {
        "id": "zpracovani-evaluaci", "title": "Zpracování evaluací", "icon": "report",
        "summary": "Nastavení hodnocení, práce s daty a zpracování evaluačních zpráv.",
        "description": "Navrhneme způsob hodnocení projektu, nastavíme dokumentaci a nástroje pro evidenci podporovaných osob, vyhodnotíme data a zpracujeme evaluační zprávy.",
        "service_icon": "evaluation", "intro": "Navrhneme hodnocení projektu a pomůžeme s evidencí i vyhodnocením.",
        "includes": ["Nastavení indikátorů a dokumentace", "Evidence podpor, sběr a vyhodnocení dat", "Průběžné a závěrečné evaluační zprávy"],
        "url": "/kontakty/#odborne-sluzby", "link": "Domluvit evaluaci",
        "home_link": "Jak probíhá evaluace",
    },
    {
        "id": "strategicke-a-koncepcni-dokumenty", "title": "Tvorba strategických a koncepčních dokumentů", "icon": "method",
        "summary": "Analýza potřeb, stanovení cílů, návrh opatření a plán jejich naplňování.",
        "description": "Zpracujeme strategické a koncepční dokumenty, které propojí analýzu potřeb, cíle, konkrétní opatření a plán jejich naplňování.",
        "service_icon": "strategy", "intro": "Proměníme potřeby území v jasné cíle a plán opatření.",
        "includes": ["Analýza potřeb a výchozí situace", "Strategické cíle a koncepce", "Návrh opatření a plán jejich naplňování"],
        "url": "/kontakty/#odborne-sluzby", "link": "Domluvit tvorbu strategie",
        "home_link": "Tvorba strategií a koncepcí – podrobnosti",
    },
]

home_project_services = "".join(
    f'<article class="card">{icon(service["icon"], "service-icon")}<h3>{esc(service["title"])}</h3><p>{esc(service["summary"])}</p><a href="/oblasti-podpory/#{service["id"]}">{esc(service["home_link"])} <span aria-hidden="true">→</span></a></article>'
    for service in PROJECT_SERVICES
)

home = f'''
<section class="hero home-hero"><div class="wrap">
<div class="hero-copy"><span class="eyebrow">Podpora · Rozvoj · Příležitosti</span>
<h1>Pomáháme <em>lidem s dluhy</em> a <em>obcím</em> v rozvoji</h1>
<p>V Jeseníku poskytujeme bezplatné a důvěrné dluhové poradenství. Obcím a organizacím nabízíme komunitní plánování, projektovou podporu, evaluace a tvorbu strategických dokumentů.</p>
<div class="hero-actions"><a class="button dark" href="/dluhova-poradna/">Chci pomoc s dluhy</a><a class="button outline" href="/oblasti-podpory/">Služby pro obce a organizace</a></div>
</div><div class="hero-visual">
<img class="hero-illustration" src="/assets/poradenstvi-ilustrace.png" width="1448" height="1086" alt="Ilustrace přátelského poradenského rozhovoru s městem a horami v pozadí" fetchpriority="high">
<aside class="advice-card" aria-labelledby="poradna-title"><div class="advice-heading"><span class="advice-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8A8.5 8.5 0 0 1 12.5 20a8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7A8.4 8.4 0 0 1 4 11.5 8.5 8.5 0 0 1 8.7 3.9a8.4 8.4 0 0 1 3.8-.9H13a8.5 8.5 0 0 1 8 8v.5Z"/><path d="M8.5 10h7M8.5 14h4"/></svg></span><div><h2 id="poradna-title">Dluhová poradna Jeseník</h2><p>Bezplatné a důvěrné poradenství.</p></div></div>
<div class="advice-contact"><strong>{CONTACT_NAME}</strong><span>Dluhová poradkyně</span><a href="tel:{CONTACT_TEL}">{CONTACT_PHONE}</a><a href="{DEBT_MAILTO}">{CONTACT_EMAIL}</a></div>
<p class="advice-address">28. října 896/19, Jeseník</p>
<p class="advice-project">Poradenství v rámci projektu Jesenicko proti dluhům III pokračuje od února 2025.</p>
<div class="advice-actions"><a class="button dark" href="/dluhova-poradna/#kontakt-a-objednani">Domluvit konzultaci</a><a class="textlink" href="/dluhova-poradna/#s-cim-pomuzeme">Jak poradna pomáhá <span aria-hidden="true">→</span></a></div>
</aside>
</div></div></section>
<section class="section services-home" id="jak-pomahame"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Jak pomáháme</span><h2>Pro obce a organizace</h2><p>Pomáháme obcím, poskytovatelům a dalším organizacím plánovat sociální služby, připravovat a řídit projekty, vyhodnocovat jejich výsledky a zpracovávat strategické dokumenty.</p></div></div>
<div class="grid-3 institutional-home">
<article class="card">{icon("map", "service-icon")}<h3>Komunitní plánování</h3><p>Komunitní plánování, analýzy a odborné konzultace pro rozvoj sociálních služeb.</p><a href="/oblasti-podpory/#komunitni-planovani">Komunitní plánování – podrobnosti <span aria-hidden="true">→</span></a></article>
{home_project_services}
</div></div></section>
'''
write_page("/", "Úvod", "Bezplatné a důvěrné dluhové poradenství v Jeseníku. Pro obce a organizace komunitní plánování, projektová podpora, evaluace a strategické dokumenty.", home)

about = '<div class="about-page">' + page_hero("O nás", "Středisko rozvoje sociálních služeb propojuje přímou pomoc lidem s odbornou podporou obcí a organizací. Naše práce vychází ze zkušeností s komunitním plánováním sociálních služeb.", "O nás", compact=True)
about += section("Od komunitního plánování k přímé pomoci lidem", '''<div class="about-story"><div><p>Komunitní plánování propojuje potřeby obyvatel s rozhodováním obcí a prací poskytovatelů. Právě na této spolupráci stojí naše zkušenosti z Jesenicka, Prostějovska, Litovelska a Mohelnicka.</p><p>Postupně jsme rozšířili nabídku o metodické konzultace, vzdělávání, přípravu a administraci projektů i evaluace. Přímou pomoc lidem poskytujeme v dluhové poradně. Obě části naší práce spojuje znalost místních potřeb a hledání řešení, která lze uskutečnit.</p><a class="link-arrow" href="/oblasti-podpory/">Služby pro obce a organizace →</a></div><aside class="about-history" aria-labelledby="historie-title"><h3 id="historie-title">Stručná historie</h3><dl><div><dt>2008</dt><dd>Vznik společnosti se zaměřením na komunitní plánování sociálních služeb.</dd></div><div><dt>2016</dt><dd>Otevření Dluhové poradny Jeseník.</dd></div><div><dt>2025</dt><dd>Zahájení třetí etapy projektu Jesenicko proti dluhům.</dd></div></dl></aside></div>''')
about += section("Zkušenosti z konkrétní práce", '''<div class="about-references">
<article class="about-reference"><h3>Město Mohelnice</h3><p>Realizovali jsme projekt plánování sociálních služeb v partnerství s městem. Vznikly plánovací dokumenty a elektronický katalog služeb Mohelnicka.</p><a href="/projekty/#planovani-mohelnicko" aria-label="Projekt plánování sociálních služeb na Mohelnicku">Projekt →</a></article>
<article class="about-reference"><h3>Charita Konice a město Konice</h3><p>Jako partner jsme se podíleli na metodické podpoře a řízení projektu. Společnými výstupy byly plán na období 2019–2021, akční plán a katalogy služeb.</p><a href="/projekty/#planovani-konicko" aria-label="Projekt plánování sociálních služeb na Konicku">Projekt →</a></article>
<article class="about-reference"><h3>Osoblažský cech, z.ú.</h3><p>V partnerském projektu na období 2023–2026 jsme zajišťovali dluhové poradenství. Lidé na Osoblažsku tak mohli využít odbornou pomoc při řešení dluhů.</p><a href="/projekty/#poradenstvi-osoblazsko" aria-label="Projekt dluhového a pracovního poradenství na Osoblažsku II">Projekt →</a></article>
</div><p class="about-more"><a class="link-arrow" href="/projekty/#realizovane-projekty">Další projekty a spolupráce →</a></p>''', alt=True)
about += section("Kontaktní osoba pro dluhovou poradnu", f'''<div class="about-current-contact">{DEBT_CONTACT}<div><p>Potřebujete poradit s dluhy, oddlužením nebo komunikací s věřiteli? Zavolejte nebo napište a domluvte si konzultaci.</p>{DEBT_ACTIONS}</div></div><p class="about-more"><a class="link-arrow" href="/kontakty/">Kontakty pro poradnu i odbornou spolupráci →</a></p>''')
about += '''<section class="about-identity"><div class="wrap"><h2>Základní údaje</h2><p class="about-legal-name">Středisko rozvoje sociálních služeb, o.p.s.</p><dl><div><dt>Právní forma</dt><dd>Obecně prospěšná společnost</dd></div><div><dt>Sídlo</dt><dd>Na Stráni 297/22, 790 01 Jeseník – Bukovice</dd></div><div><dt>IČO / datová schránka</dt><dd>27847977 / bkyt4gn</dd></div><div><dt>Rejstřík</dt><dd>Krajský soud v Ostravě, sp. zn. O 1009</dd></div></dl></div></section></div>'''
write_page("/o-spolecnosti/", "O nás", "SRSS působí od roku 2008 v oblasti sociálních služeb, komunitního plánování, projektové práce, evaluací a dluhového poradenství.", about)

def service_topic(service: dict) -> str:
    points = "".join(f'<li>{esc(point)}</li>' for point in service["includes"])
    return f'''<article class="service-card service-topic service-topic--{esc(service["id"])}" id="{esc(service["id"])}"><div class="service-card-body"><div class="service-topic-main">{icon(service["service_icon"], "service-icon")}<h3>{esc(service["title"])}</h3><p>{esc(service.get("description", service["intro"]))}</p></div><div class="service-topic-detail"><ul class="service-includes">{points}</ul><a class="button service-action" href="{esc(service["url"])}">{esc(service["link"])} <span aria-hidden="true">→</span></a></div></div></article>'''


community_service = {
    "id": "komunitni-planovani", "title": "Komunitní plánování", "service_icon": "map",
    "intro": "Podporujeme obce a další aktéry při plánování a rozvoji sociálních služeb. Pomáháme s analýzou potřeb, odbornými konzultacemi a nastavením dalšího postupu.",
    "includes": ["Analýza potřeb území", "Metodická podpora a pracovní skupiny", "Plány služeb, vzdělávání a semináře"],
    "url": "/kontakty/#odborne-sluzby", "link": "Domluvit komunitní plánování",
}
service_anchors = [("komunitni-planovani", "Komunitní plánování"), ("tvorba-projektu", "Tvorba projektů"), ("administrace-a-rizeni", "Administrace a řízení"), ("zpracovani-evaluaci", "Evaluace"), ("strategicke-a-koncepcni-dokumenty", "Strategické dokumenty")]
service_jumps = '<nav class="service-jumps" aria-label="Oblasti podpory pro obce a organizace"><div class="service-chips">' + "".join(f'<a href="#{anchor}">{label}</a>' for anchor,label in service_anchors) + '</div></nav>'
services = page_hero("Služby pro obce a organizace", "Pomáháme obcím, poskytovatelům sociálních služeb a dalším organizacím při plánování sociálních služeb, přípravě a řízení projektů, evaluacích a tvorbě strategických a koncepčních dokumentů.", "Pro obce a organizace", compact=True, extra_content=service_jumps)
services += section("S čím vám pomůžeme", '<div class="service-professionals">' + "".join(service_topic(service) for service in [community_service, *PROJECT_SERVICES]) + '</div><p class="service-detail-link">Součástí naší nabídky je také vzdělávání sociálních pracovníků v tématech dluhového poradenství. <a href="/kontakty/#odborne-sluzby">Domluvit vzdělávání →</a></p>', "Projektová a odborná podpora", True, anchor="pro-obce")
services += '''<section class="service-final service-final--institutional"><div class="wrap"><h2>Probereme váš záměr</h2><p>Popište stručně svůj záměr nebo problém, který potřebujete řešit. Společně upřesníme potřebu a očekávaný výstup, navrhneme rozsah spolupráce a domluvíme další postup.</p><div class="contact-actions"><a class="button" href="/kontakty/#odborne-sluzby">Domluvit konzultaci k vašemu záměru <span aria-hidden="true">→</span></a><a class="service-final-link" href="/projekty/#realizovane-projekty">Prohlédnout projekty a reference →</a></div></div></section>'''
write_page("/oblasti-podpory/", "Služby pro obce a organizace", "Komunitní plánování, projektová příprava a řízení, evaluace a strategické dokumenty pro obce a organizace.", services)

debt = '<div class="debt-page">' + page_hero("Dluhová poradna Jeseník", "Potřebujete řešit dluhy, oddlužení nebo komunikaci s věřiteli? Dluhová poradna SRSS v Jeseníku nabízí bezplatné a důvěrné poradenství.", "Dluhová poradna", "debt-scene", compact=True)
debt += section("Kontakt a objednání", f'''<div class="two-col"><div>{DEBT_CONTACT}<p><strong>Poradna:</strong> 28. října 896/19, Jeseník</p>{DEBT_ACTIONS}</div><div class="detail-card">{DEBT_HOURS}</div></div>''', anchor="kontakt-a-objednani")
debt += section("S čím vám pomůžeme", '''<div class="two-col"><ul class="debt-help-list"><li>Řešení dluhové situace</li><li>Oddlužení</li><li>Komunikace s věřiteli</li></ul><div><h3>Domluva první konzultace</h3><p>Ozvěte se telefonicky nebo e-mailem. S poradkyní si domluvte termín konzultace a další postup podle své situace.</p><p>Do prvního e-mailu neposílejte rodné číslo, čísla osobních dokladů ani citlivé přílohy. Podrobnosti můžete probrat při konzultaci.</p></div></div>''', alt=True, anchor="s-cim-pomuzeme")
debt += section("Kde nás najdete", '<p class="lead">Dluhová poradna SRSS · 28. října 896/19, Jeseník</p><p>Najdete nás v budově modrého Zverimaxu. Do poradny vstupujte vedlejším vchodem.</p><div id="mapa-poradny">' + OFFICE_PHOTO + location_map("Dluhová poradna", "28. října 896/19, Jeseník", 50.224855277778, 17.206881388889, "Budova modrého Zverimaxu, vedlejší vchod.") + '</div>', anchor="kde-nas-najdete")
debt += section("O projektu Jesenicko proti dluhům III", '<p>Dluhové poradenství v rámci projektu Jesenicko proti dluhům III pokračuje od února 2025.</p><p class="small">Projekt OP Zaměstnanost plus · CZ.03.02.01/00/24_065/0004961</p><a class="link-arrow" href="/projekty/#jesenicko-proti-dluhum-iii">Detail projektu Jesenicko proti dluhům III →</a>', alt=True)
debt += '</div>'
write_page("/dluhova-poradna/", "Dluhová poradna Jeseník", "Potřebujete řešit dluhy, oddlužení nebo komunikaci s věřiteli? Dluhová poradna SRSS v Jeseníku nabízí bezplatné a důvěrné poradenství.", debt)

projects = '''<section class="page-hero page-hero--compact project-offer"><div class="wrap">
<div class="page-hero-copy"><div class="breadcrumbs"><a href="/">Úvod</a> / Projekty a reference</div>
<h1>Vytvoříme vám projekt <span>na míru.</span></h1>
<p>Pomáháme obcím a organizacím proměnit záměr v dobře připravený projekt. Návrh přizpůsobíme vašim potřebám a cílům.</p>
<div class="project-offer-actions"><a class="button dark" href="/kontakty/#odborne-sluzby">Chci projekt na míru</a><a class="project-offer-link" href="#realizovane-projekty">Projekty a reference <span aria-hidden="true">→</span></a></div>
</div>
<div class="project-success"><p>Úspěšnost při schvalování</p><strong><span>Více než</span>90&nbsp;%</strong><p class="project-success-context">námi připravených projektů</p></div>
</div></section>'''
planning_source = "https://www.konice.charita.cz/res/archive/008/001029.pdf?seek=1611613175"
own = [
    ("Jesenicko proti dluhům III", "Od února 2025 · dluhové poradenství", "Lidé řešící dluhy na Jesenicku.", "Realizace projektu a provoz bezplatné dluhové poradny.", "Poradna otevřená od 1. února 2025 na ulici 28. října 896/19 v Jeseníku.", SOURCES["S06"]["zdroj_url"], "CZ.03.02.01/00/24_065/0004961"),
    ("Jesenicko proti dluhům II", "2020–2022 · dluhové poradenství", "Obyvatelé Jesenicka v dluhové situaci.", "Realizace projektu, poradenství a vzdělávání ve finanční gramotnosti.", "Provoz poradny do června 2022 a navazující besedy do září 2022.", SOURCES["S04"]["zdroj_url"], "CZ.03.2.60/0.0/0.0/18_088/0010305"),
    ("Jesenicko proti dluhům", "Od roku 2016 · první etapa poradny", "Lidé s dluhy na území okresu Jeseník.", "Otevření a zajištění provozu poradny, odborná pomoc a finanční vzdělávání.", "Zahájení činnosti Dluhové poradny Jeseník dne 7. listopadu 2016.", SOURCES["S01"]["zdroj_url"], "CZ.03.2.60/0.0/0.0/15_042/0003827"),
    ("Střednědobé plánování na Prostějovsku", "2017–2019 · komunitní plánování", "Město Prostějov a obce v jeho správním obvodu.", "Realizace plánovacího projektu v partnerství s městem Prostějov.", "Střednědobý a akční plán rozvoje sociálních služeb a aktualizace katalogu poskytovatelů.", planning_source, "CZ.03.2.63/0.0/0.0/16_063/0006528", "Výstupy plánovacích projektů"),
    ("Střednědobé plánování na SO ORP Litovel", "2017–2019 · komunitní plánování", "Město Litovel a obce správního obvodu ORP.", "Realizace projektu v partnerství s městem Litovel; analytická a metodická práce.", "Analýza potřeb území, střednědobý plán na období 2020–2022 a elektronický katalog služeb.", SOURCES["S09"]["zdroj_url"], "CZ.03.2.63/0.0/0.0/16_063/0006530"),
    ("Střednědobé plánování na SO ORP Mohelnice", "2017–2019 · komunitní plánování", "Město Mohelnice a obce správního obvodu ORP.", "Realizace projektu v partnerství s městem Mohelnice.", "Plánovací dokumenty a elektronický katalog sociálních a návazných služeb Mohelnicka.", "https://katalog.mohelnice.cz/", "CZ.03.2.63/0.0/0.0/16_063/0006549", "Katalog služeb Mohelnicka"),
]
projects += section("Vlastní projekty", '<p class="service-group-intro">Zkušenosti z Jesenicka i dalších regionů. U jednotlivých projektů uvádíme lokalitu, období, roli SRSS a konkrétní výstupy, aby bylo zřejmé, co jsme v projektu zajišťovali.</p><div class="project-gallery project-gallery--references">' + "".join(reference_card(*project) for project in own) + '</div>', "Vybrané reference", anchor="realizovane-projekty")
partners = [
    ("Dluhové a pracovní poradenství na Osoblažsku II", "2023–2026 · partnerství", "Klienti projektu Osoblažského cechu, z.ú., na Osoblažsku.", "Partner projektu zajišťující dluhové poradenství.", "Dluhové poradenství jako součást projektu zaměřeného na pracovní a dluhovou situaci obyvatel. Období projektu: únor 2023 až leden 2026.", SOURCES["S05"]["zdroj_url"], "CZ.03.02.01/00/22_018/0000779"),
    ("Podpora střednědobého plánování sociálních služeb Konicka", "2017–2019 · partnerství", "Charita Konice, město Konice a obce Konicka.", "Partnerství v projektu, metodická podpora a projektové řízení.", "Výstupy společného projektu: plán na období 2019–2021, akční plán 2020 a tištěný i elektronický katalog služeb.", "https://www.konice.charita.cz/res/archive/001024.pdf?seek=1611613119", "CZ.03.2.63/0.0/0.0/16_063/0006527", "Výstupy projektu Konicka"),
    ("Projektové žádosti pro další organizace", "Zakázky · tvorba projektů", "Osoblažský cech, Darmoděj, Boétheia SKP, mikroregion Žulovsko a MRC Krteček.", "Zpracování projektových žádostí na zakázku.", "Připravené žádosti pro záměry v oblasti sociálního začleňování a podpory uplatnění na trhu práce.", "https://srssjesenik.cz/projekty/probihajici-sluzby/", "", "Přehled zakázek"),
]
projects += section("Partnerství a zakázky", '<div class="project-gallery project-gallery--references">' + "".join(reference_card(*project) for project in partners) + '</div>', "Spolupráce", True)
projects += section("Hledáte podobnou podporu?", '<p>Prohlédněte si služby pro obce a organizace nebo s námi proberte svůj záměr.</p><div class="contact-actions"><a class="button dark" href="/kontakty/#odborne-sluzby">Domluvit konzultaci</a><a class="link-arrow" href="/oblasti-podpory/">Služby pro obce a organizace →</a></div>')
projects += section("Další projekty a dokumenty", '''<p>Výroční zprávy, projektové podklady a starší články najdete v archivu společnosti.</p><a class="button dark" href="/dokumenty/">Přejít do archivu →</a>''', "Archiv")

write_page("/projekty/", "Projekty a reference", "Přehled projektů a spolupráce SRSS v oblasti dluhového poradenství, sociálních služeb, projektové podpory a evaluací.", projects)

docs = page_hero("Dokumenty", "Přehled výročních zpráv, projektových podkladů a odborných výstupů Střediska rozvoje sociálních služeb. Starší informace o naší činnosti najdete v archivu.", "Dokumenty", "documents", compact=True)
docs += '<nav class="document-nav wrap" aria-label="Kategorie dokumentů">' + ''.join(f'<a href="#{anchor}">{icon(symbol)}<span>{label}</span></a>' for anchor,symbol,label in [("vyrocni-zpravy","report","Výroční zprávy"),("projektove-podklady","project","Projektové podklady"),("archiv","method","Archiv stránek")]) + '</nav>'
docs += section("Výroční zprávy", f'''<p>Výroční zprávy za roky 2009–2015 zde zatím nejsou dostupné ke stažení. O konkrétní zprávu nás můžete požádat e-mailem.</p><a class="link-arrow" href="mailto:{CONTACT_EMAIL}?subject=V%C3%BDro%C4%8Dn%C3%AD%20zpr%C3%A1va">Požádat o výroční zprávu →</a><div class="doc-list pad-top">''' + "".join(f'<div class="doc">{icon("report", "doc-symbol")}<div><strong>Výroční zpráva {year}</strong><small>Soubor zatím není k dispozici</small></div></div>' for year in range(2009, 2016)) + '''</div>''', "Výroční zprávy společnosti", anchor="vyrocni-zpravy", heading_icon="report")

docs_items = []
for document in LEGACY["dokumenty"]:
    name = document.get("nazev", "Dokument")
    if name.startswith("Výroční zpráva"):
        continue
    year = document.get("roky", "")
    direct_url = document.get("soubor_url") or ""
    parent_url = document.get("rodic_url") or ""
    link = safe_link(direct_url, name + " – původní soubor ↗") if direct_url else safe_link(parent_url, name + " – archivní stránka ↗") if parent_url else ""
    normalized = name.lower()
    doc_icon = "form" if any(word in normalized for word in ("přihláška", "krycí", "prohlášení", "smlouvy", "harmonogram")) else "method" if any(word in normalized for word in ("metod", "postup", "plán")) else "report" if any(word in normalized for word in ("zpráva", "analýza", "výzkum")) else "verified"
    docs_items.append(f'<div class="doc">{icon(doc_icon, "doc-symbol")}<div><strong>{esc(name)}</strong><small>{esc(year)} · Soubor na tomto webu není k dispozici</small><br>{link}</div></div>')
docs += section("Projektové podklady", '<p>Přehled analýz, plánů a dalších projektových materiálů. Odkazy vedou na archivní umístění; některé mohou být nedostupné.</p><div class="doc-list pad-top">' + "".join(docs_items) + '</div>', "Historické dokumenty", True, anchor="projektove-podklady", heading_icon="project")
archive = []
for item in LEGACY["zdroje"]:
    url = item.get("zdroj_url") or ""
    title = item.get("nazev") or "Záznam"
    summary = item.get("zjisteni") or ""
    year = item.get("roky") or ""
    # A number of the research entries have only the domain root as a
    # placeholder; do not present that as a source link to the specific item.
    if url.rstrip("/") in {"https://srssjesenik.cz", "http://srssjesenik.cz"}:
        url = ""
    archive.append(project_card(title, year or item.get("typ", "Archiv"), summary, url))
docs += section("Archiv stránek a článků", '<p>Starší články a informace o činnosti společnosti. Adresy, kontakty a provozní údaje v historických záznamech odpovídají době jejich zveřejnění.</p><div class="records pad-top">' + "".join(archive) + '</div><p class="source-note">Přehled obsahuje shrnutí archivních záznamů. Plné texty a přílohy nejsou součástí tohoto webu; dostupnost externích odkazů se může měnit.</p>', "Archiv veřejného obsahu", anchor="archiv", heading_icon="method")
write_page("/dokumenty/", "Dokumenty", "Přehled dokumentů a materiálů Střediska rozvoje sociálních služeb Jeseník, výročních zpráv, projektových podkladů a archivních článků.", docs)

contact = page_hero("Kontakt", "Vyberte kontakt podle toho, s čím se na nás obracíte.", "Kontakt", compact=True)
contact += section("S čím se na nás obracíte?", f'''<div class="contact-options">
<article class="contact-option" id="pomoc-s-dluhy">{icon("advice", "service-icon")}<h3>Potřebuji pomoc s dluhy</h3><p>Bezplatné a důvěrné poradenství. Zavolejte nebo napište poradkyni a domluvte si konzultaci.</p>{DEBT_CONTACT}<p><strong>Dluhová poradna:</strong><br>28. října 896/19, Jeseník</p>{DEBT_ACTIONS}<p class="contact-detail-link"><a href="/dluhova-poradna/">Jak poradna pomáhá →</a></p></article>
<article class="contact-option" id="odborne-sluzby">{icon("project", "service-icon")}<h3>Jsem obec nebo organizace</h3><p>Potřebujete komunitní plánování, projektovou podporu, evaluaci nebo strategický dokument? Napište nám stručně svůj záměr a domluvíme další postup.</p><div class="contact-person"><strong>Kontakt SRSS pro odbornou spolupráci</strong><a href="tel:{CONTACT_TEL}">{CONTACT_PHONE}</a><a href="{PROFESSIONAL_MAILTO}">{CONTACT_EMAIL}</a></div><p class="contact-hint">Do e-mailu stačí uvést organizaci, stručný záměr a telefon pro zpětný kontakt.</p><a class="button dark" href="{PROFESSIONAL_MAILTO}">Domluvit konzultaci k vašemu záměru →</a></article>
</div>''', "Spojte se s námi")
contact += section("Návštěva dluhové poradny", f'''<div class="office-layout"><div><p class="lead">28. října 896/19, Jeseník</p><p>Budova modrého Zverimaxu, vedlejší vchod.</p>{DEBT_HOURS}<a class="link-arrow" href="#mapy">Zobrazit mapu →</a></div>{OFFICE_PHOTO}</div>''', "Jak nás najdete", True)
contact += section("Kde nás najdete", '<div class="locations-grid">' + location_map("Dluhová poradna", "28. října 896/19, Jeseník", 50.224855277778, 17.206881388889, "Pracoviště poradny v budově modrého Zverimaxu, vedlejší vchod.") + location_map("Sídlo společnosti", "Na Stráni 297/22, Jeseník – Bukovice", 50.223438611111, 17.212241666667, "Sídlo společnosti. Osobní schůzku si prosím domluvte předem.") + '</div>', "Pracoviště a sídlo", anchor="mapy")
contact += section("Identifikační údaje", '''<div class="detail-card organisation-details"><dl><dt>Název</dt><dd>Středisko rozvoje sociálních služeb, o.p.s.</dd><dt>Sídlo</dt><dd>Na Stráni 297/22, 790 01 Jeseník – Bukovice</dd><dt>IČO</dt><dd>27847977</dd><dt>Datová schránka</dt><dd>bkyt4gn</dd><dt>Rejstřík</dt><dd>Krajský soud v Ostravě, sp. zn. O 1009</dd><dt>Zápis</dt><dd>21. června 2008</dd></dl></div>''', "Středisko rozvoje sociálních služeb, o.p.s.", True)
write_page("/kontakty/", "Kontakt", "Kontakty na Středisko rozvoje sociálních služeb a dluhovou poradnu v Jeseníku, sídlo společnosti a identifikační údaje.", contact)

write_page("/digitalni-nastroje/", "Digitální nástroje", "Nástroje pro poradenství, řízení a evaluaci projektů, sociální práci a rozvoj týmu. Specializované aplikace i firemní informační systémy na míru.", build_digital_tools(icon, CONTACT_EMAIL))
write_page("/digitalni-nastroje/projektova-evidence-a-evaluace/", "Projektová evidence a evaluace pro NNO", "Klientská práce, case management, řízení projektu a evaluace v jedné evidenci. Plány podpory, indikátory, výkazy a průběžné i závěrečné evaluační zprávy.", build_nno_system(CONTACT_EMAIL))
write_page("/digitalni-nastroje/firemni-systemy/", "Firemní informační systémy na míru", "Zákazníci, nabídky, zakázky, sklad, fakturace a komunikace v jednom systému podle procesu vaší firmy. Ukázkové řešení ThermoVan.", build_business_system(CONTACT_EMAIL))
write_page("/digitalni-nastroje/tymovy-portal/", "Týmový portál", "Pracovní výkazy, hodnocení, vzdělávací plány, supervize, porady a úkoly. Týmový portál pro sociální služby, NNO a projekty s metodickým spořičem.", build_team_portal(CONTACT_EMAIL))
write_page("/digitalni-nastroje/elai/", "E.L.A.I.", "AI asistent pro dluhové poradce. Čistopis pracovních poznámek, kazuistika a metodická kontrola zápisu s odborným posouzením poradcem.", build_elai(CONTACT_EMAIL))
write_page("/digitalni-nastroje/generator-importu-esf/", "Generátor importů do IS ESF 21+", "Převod Excelu na importní CSV podpořených osob a podpor. Kontrola údajů, číselníků, duplicit a adres RÚIAN přímo v prohlížeči.", build_esf_generator(CONTACT_EMAIL))
write_page("/digitalni-nastroje/nastroje-pro-opz/", "Nástroje pro OPZ+", "Generátor importů IS ESF, Sledovač čerpání rozpočtu OPZ+ a projektová evidence s evaluací. Tři nástroje pro práci na projektech.", build_opz_tools(CONTACT_EMAIL))
write_page("/digitalni-nastroje/bio-registry/", "BIO Registry", "Desktopová databáze pro Windows sjednocující evropské registry bio firem, certifikace a veřejné kontakty. Vyhledávání, aktualizace a export do XLSX a CSV.", build_bio_registry(CONTACT_EMAIL))


(DIST / "assets/site.js").write_text('''const toggle=document.querySelector(".menu-toggle"),nav=document.querySelector("#site-nav");if(toggle&&nav){toggle.addEventListener("click",()=>{const open=toggle.getAttribute("aria-expanded")==="true";toggle.setAttribute("aria-expanded",String(!open));nav.classList.toggle("open",!open)});nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{toggle.setAttribute("aria-expanded","false");nav.classList.remove("open")}))}''', encoding="utf-8")
print(f"Generated {len(list(DIST.rglob('index.html')))} pages and {len(archive)} archival entries")
