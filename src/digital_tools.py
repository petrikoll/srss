"""Owner-supplied digital-tool offer, with working enquiry links."""

from html import escape
from urllib.parse import quote, urlencode


TOOLS = [
    {
        "id": "isir",
        "name": "ISIR",
        "icon": "insolvency",
        "heading": "Insolvence pod kontrolou",
        "intro": "Kontrola insolvenčních řízení nemusí znamenat opakované ruční vyhledávání v rejstříku.",
        "description": "Aplikace umožňuje kontrolovat jednotlivé klienty i větší skupinu klientů, sledovat stav řízení, nové dokumenty a důležité lhůty. Dokumenty z insolvenčního řízení lze zobrazit, archivovat a vybrané podklady také analyzovat.",
        "features": [
            "Hromadná i jednotlivá kontrola klientů v ISIR",
            "Přehled insolvenčních řízení a jejich stavu",
            "Upozornění na nové dokumenty a důležité lhůty",
            "Zobrazení a archivace dokumentů insolvenčního řízení",
            "Strukturovaná analýza vybraných dokumentů a možnost vytvoření kazuistiky",
        ],
        "summary": "Zjistit více o ISIR",
        "cta": "Zeptat se na ISIR",
    },
    {
        "id": "generator-dokumentu",
        "name": "Generátor dokumentů",
        "icon": "form",
        "heading": "Dokument za pár minut místo ručního přepisování",
        "intro": "Vytváření opakujících se žádostí a podání zabírá čas, který lze využít lépe.",
        "description": "Generátor pomáhá připravit dokumenty pro exekutory, věřitele, soudy a další instituce. Uživatel vybere typ dokumentu, doplní potřebné údaje a získá připravený výstup pro další kontrolu a použití.",
        "features": [
            "Žádosti o součinnost, splátkový kalendář nebo vyčíslení dluhu",
            "Žádosti o odklad exekuce a návrhy související se zastavením exekuce",
            "Využití údajů z podkladového PDF v některých formulářích",
            "Výstup ve formátu DOCX nebo PDF",
        ],
        "summary": "Zjistit více o generátoru",
        "cta": "Zeptat se na generátor",
    },
    {
        "id": "ctecka-vyplatnich-pasek",
        "name": "Čtečka výplatních pásek",
        "icon": "scan",
        "heading": "Výplatní páska dovnitř. Potřebné údaje ven.",
        "intro": "Ruční přepisování údajů z několika výplatních pásek je pomalé a zvyšuje riziko chyby.",
        "description": "Nahrajte výplatnici ve formátu PDF nebo jako obrázek. Aplikace pomocí OCR načte údaje a připraví je ke kontrole. Vybrané výplatnice potom zahrne do společného přehledu příjmů.",
        "features": [
            "Načtení údajů z PDF nebo obrázku pomocí OCR",
            "Práce s hrubou i čistou mzdou",
            "Automatický součet a průměrná čistá mzda",
            "Ruční doplnění údajů z hůře čitelných dokumentů",
        ],
        "summary": "Zjistit více o čtečce",
        "cta": "Zeptat se na čtečku",
    },
    {
        "id": "dluhove-kalkulacky",
        "name": "Dluhové kalkulačky",
        "icon": "calculator",
        "heading": "Složité výpočty bez složitých tabulek",
        "intro": "Praktické kalkulačky pro situace, které se v dluhovém a sociálním poradenství opakují.",
        "description": "Výsledky jsou dostupné okamžitě bez vytváření vlastních vzorců a tabulek.",
        "features": [
            "Srážky ze mzdy, exekuce a oddlužení — výpočty související se srážkami z příjmů a řešením zadlužení",
            "Příjmový potenciál — pomocný nástroj pro práci s příjmovou situací klienta",
            "Chráněné obydlí — výpočet hodnoty chráněného obydlí pro potřeby insolvenčního řízení",
        ],
        "summary": "Prohlédnout přehled kalkulaček",
        "cta": "Zeptat se na kalkulačky",
    },
]

BUDGET_BENEFITS = [
    ("Schválené čerpání", "Přehled částek skutečně uznaných v žádostech o platbu."),
    ("Aktuální zůstatky", "Informace o tom, kolik prostředků zbývá v jednotlivých částech rozpočtu."),
    ("Paušální nárok", "Výpočet nároku na paušální nepřímé náklady podle skutečně schválených přímých výdajů."),
    ("Návrhy přesunů", "Podklady pro rozhodování, kde se prostředky nečerpají a kde mohou naopak chybět."),
    ("Závěrečné vypořádání", "Orientační pohled na stav projektu před jeho finančním ukončením."),
]

SOCIAL_WORK_AREAS = [
    ("Klientská evidence", ["Základní a monitorovací údaje klienta, stav spolupráce, klíčový pracovník, historie podpory a další informace potřebné pro vedení případu."]),
    ("Individuální plánování", ["Popis výchozí situace, cíle klienta, konkrétní kroky, termíny a průběžné vyhodnocování.", "Jednotlivé výkony sociální práce lze navázat na konkrétní cíl, takže je zpětně vidět, co se s klientem řešilo a kam spolupráce směřuje."]),
    ("Evidence sociální práce", ["Záznamy individuální podpory včetně délky výkonu, formy kontaktu, oblasti podpory, výsledku a dalšího navazujícího kroku.", "Systém tak nevytváří pouze statistiku výkonů, ale průběžnou dokumentaci práce s klientem."]),
    ("Case management", ["Pokud situace klienta vyžaduje spolupráci více subjektů, lze samostatně evidovat case management.", "Záznam propojuje klienta, jeho cíl, zapojené aktéry a dohodnutý další postup. Sociální pracovník tak získává přehled o tom, kdo je do řešení situace zapojen a jak jednotlivé kroky na sebe navazují."]),
    ("Síť spolupracujících organizací", ["Evidence institucí a odborníků, se kterými obec při řešení situací klientů spolupracuje.", "Součástí může být také evidence síťovacích aktivit a rozvoje místní spolupráce."]),
    ("Přehled výkonu sociální práce", ["Dashboard a analytické přehledy pro orientaci v evidované sociální práci."]),
]


def product_screenshot(filename, title, width, height, *, uploaded=False):
    path = '/assets/product-screens/' + filename
    crop = ' product-screenshot-opz' if uploaded else ''
    note = 'Skutečné rozhraní aplikace' if uploaded else 'Skutečné rozhraní · ukázkové údaje'
    return f'''<figure class="product-screenshot{crop}"><a class="product-screenshot-image" href="{path}" target="_blank" rel="noopener" aria-label="Zvětšit ukázku: {escape(title)}"><span class="product-screenshot-viewport"><img src="{path}" alt="{escape(title)}" width="{width}" height="{height}" loading="lazy" decoding="async"></span></a><figcaption><span>{note}</span><a href="{path}" target="_blank" rel="noopener">Zvětšit ukázku<span class="sr-only"> — {escape(title)} (nová karta)</span></a></figcaption></figure>'''


def build_digital_tools(icon, email: str) -> str:
    def enquiry(subject: str) -> str:
        return escape("mailto:" + email + "?" + urlencode({"subject": subject}, quote_via=quote), quote=True)

    cards = []
    for tool in TOOLS:
        features = "".join(f"<li>{escape(feature)}</li>" for feature in tool["features"])
        cards.append(f'''<article class="digital-tool" id="{tool['id']}" aria-labelledby="{tool['id']}-title">
<div class="digital-tool-heading">{icon(tool['icon'], 'digital-tool-icon')}<h3 id="{tool['id']}-title">{escape(tool['name'])}</h3></div>
<p class="digital-tool-promise">{escape(tool['heading'])}</p>
<p class="digital-tool-intro">{escape(tool['intro'])}</p>
<details class="digital-tool-details"><summary>{escape(tool['summary'])}<span aria-hidden="true">+</span></summary>
<div><p>{escape(tool['description'])}</p><h4>Co aplikace umí</h4><ul>{features}</ul></div></details>
<a class="digital-enquiry" href="{enquiry('Digitální nástroje – ' + tool['name'])}">{escape(tool['cta'])} <span aria-hidden="true">→</span></a>
</article>''')
    benefits = "".join(f'<div><dt>{escape(title)}</dt><dd>{escape(description)}</dd></div>' for title, description in BUDGET_BENEFITS)
    social_areas = "".join(
        f'<details class="digital-social-area"><summary><h4>{escape(title)}</h4><span aria-hidden="true">+</span></summary><div>'
        + "".join(f'<p>{escape(paragraph)}</p>' for paragraph in paragraphs)
        + '</div></details>'
        for title, paragraphs in SOCIAL_WORK_AREAS
    )
    return f'''<div class="digital-page">
<section class="digital-hero"><div class="wrap">
<div class="breadcrumbs"><a href="/">Úvod</a> / Digitální nástroje</div>
<span class="eyebrow">Digitální nástroje</span>
<h1>Méně rutiny.<br><em>Více času na skutečnou práci.</em></h1>
<p class="digital-lead">Webové aplikace pro sociální práci, dluhové poradenství, projekty OPZ+ a řízení organizací.</p>
<div class="digital-intro"><p>Nástroje vznikají z konkrétních potřeb každodenní praxe. Pomáhají omezit ruční přepisování údajů, zjednodušit opakované výpočty, pracovat s dokumenty a udržet důležité informace přehledně na jednom místě.</p><p>Jednotlivé aplikace lze používat samostatně. Pro organizace i firmy je možné připravit také rozsáhlejší informační systém podle jejich vlastních procesů.</p></div>
<div class="contact-actions"><a class="button dark" href="#prakticke-nastroje">Prohlédnout aplikace <span aria-hidden="true">↓</span></a><a class="button contact-email" href="{enquiry('Dotaz na digitální nástroje SRSS')}">Nezávazně se zeptat</a></div>
<nav class="digital-jumps digital-portfolio-nav" aria-label="Oblasti digitálních nástrojů"><a href="#prakticke-nastroje"><span>01</span> Sociální a dluhové poradenství</a><a href="#projektove-nastroje"><span>02</span> Nástroje pro OPZ+</a><a href="#socialni-prace-a-tym"><span>03</span> Sociální práce a řízení týmu</a><a href="#ai-nastroje"><span>04</span> AI nástroje pro odbornou praxi</a><a href="#systemy-na-miru"><span>05</span> Informační systémy na míru</a></nav>
</div></section>

<section class="section digital-practical" id="prakticke-nastroje"><div class="wrap">
<div class="digital-section-heading"><span class="eyebrow">01 / Praktické nástroje</span><h2>Nástroje pro sociální a dluhové poradenství</h2><p>Čtyři samostatné aplikace pro práci s řízeními, dokumenty, příjmy a výpočty.</p></div>
<div class="digital-tool-grid">{''.join(cards)}</div>
</div></section>

<section class="digital-portfolio-area" id="projektove-nastroje"><div class="wrap digital-area-heading"><span class="eyebrow">02 / Nástroje pro projekty OPZ+</span><h2>Od čerpání rozpočtu po doložené výsledky.</h2><p>Generátor importů do IS ESF, Sledovač čerpání rozpočtu a projektová evidence s evaluací.</p><a class="digital-category-link" href="/digitalni-nastroje/nastroje-pro-opz/">Prohlédnout nástroje pro OPZ+ →</a></div>
<div class="wrap esf-overview"><article class="esf-compact-offer" id="generator-importu-esf"><div><span class="eyebrow">Malý praktický nástroj</span><div class="esf-title-row"><h3>Generátor importů IS ESF 21+</h3><span class="digital-free-badge">Zdarma</span></div><p>Z Excelu do IS ESF bez ručního skládání CSV. Podpořené osoby, klientské podpory, kontrola údajů a adres, importní CSV i kontrolní XLSX.</p></div><div class="esf-compact-actions"><a class="button dark" href="{enquiry('Zájem o ukázku generátoru importů IS ESF 21+')}">Domluvit ukázku →</a><a class="digital-enquiry" href="/digitalni-nastroje/generator-importu-esf/">Jak generátor funguje →</a></div></article></div>
<section class="section digital-budget" id="rozpocet-opz"><div class="wrap">
<div class="digital-budget-layout"><div class="digital-budget-copy">
<h3 class="digital-product-title">Sledovač čerpání rozpočtu OPZ+</h3>
<p class="digital-budget-promise">Víte, kolik jste skutečně vyčerpali.<br>A kolik ještě zbývá.</p>
<p>Rozpočet projektu není jen tabulka schválených částek. V průběhu realizace je potřeba sledovat skutečné čerpání, schválené žádosti o platbu, nepřímé náklady, zůstatky a případné přesuny.</p>
<p>Sledovač čerpání rozpočtu OPZ+ tyto údaje spojuje do jednoho přehledu. Pracuje s exportem rozpočtu XLSX a s PDF žádostí o platbu. Z podkladů vypočítává skutečné schválené čerpání projektu a aktuální stav jednotlivých položek.</p>
<p>Místo několika souborů a ručně propojených tabulek získáte jeden aktuální pohled na finanční stav projektu.</p>
<a class="button dark" href="{enquiry('Zájem o Sledovač čerpání rozpočtu OPZ+')}">Zjistit více o rozpočtu OPZ+ <span aria-hidden="true">→</span></a>
</div><aside class="digital-budget-preview" aria-label="Ukázka a přínosy Sledovače OPZ+">
{product_screenshot('opz-budget.png', 'Sledovač OPZ+ — souhrn rozpočtu a čerpání po položkách', 1920, 1080, uploaded=True)}
<details class="digital-preview-benefits"><summary>Co získáte <span aria-hidden="true">+</span></summary><dl>{benefits}</dl></details>
</aside></div></div></section>

<section class="section digital-nno" id="evidence-evaluace-nno"><div class="wrap"><div class="digital-nno-layout">
<div><span class="eyebrow">Pro neziskové organizace</span><h3 class="digital-product-title">Projektová evidence a evaluace pro NNO</h3><p class="digital-nno-lead">Od práce s klientem až po závěrečnou evaluační zprávu.</p><p>Plánování práce s rodinou, koordinace odborníků, evidence podpory, řízení týmu, projektové indikátory a doložení skutečné změny v jedné navazující evidenci.</p><p class="digital-nno-key">Nestačí vykázat, co se udělalo. Potřebujete doložit, co se změnilo.</p><div class="contact-actions"><a class="button dark" href="/digitalni-nastroje/projektova-evidence-a-evaluace/">Prohlédnout možnosti systému <span aria-hidden="true">→</span></a><a class="digital-enquiry" href="{enquiry('Žádost o ukázku – projektová evidence a evaluace pro NNO')}">Domluvit ukázku →</a></div></div>
<div class="digital-product-proof">{product_screenshot('nno.jpg', 'Projektová evidence — cíle, výsledky a indikátory', 1348, 763)}<div class="digital-nno-areas"><div><h4>Klienti, rodiny a case management</h4><p>Cíle podpory, konkrétní kroky a záznamy práce s klienty ve vzájemných souvislostech.</p></div><div><h4>Řízení projektu</h4><p>Průběžné indikátory, pracovní výkazy, porady a úkoly.</p></div><div><h4>Evaluace projektu</h4><p>Hodnocení T0–T2, výsledky R1 a R2, více zdrojů podkladů a verzované evaluační zprávy.</p></div></div></div>
</div></div></section>

</section>
<section class="digital-portfolio-area" id="socialni-prace-a-tym"><div class="wrap digital-area-heading"><span class="eyebrow">03 / Sociální práce a řízení týmu</span><h2>Podpora klientů. Rozvoj pracovníků.</h2><p>Dva samostatné systémy pro vedení sociální práce a pro fungování týmu.</p></div>
<section class="section digital-social" id="socialni-prace-na-obci"><div class="wrap">
<h3 class="digital-product-title">Systém pro sociální práci na obci</h3>
<p class="digital-social-lead">Klient, jeho cíle, poskytnutá podpora i spolupráce dalších služeb na jednom místě.</p>
<div class="digital-social-layout"><div class="digital-social-copy"><p>Sociální práce není jen evidence kontaktů. U jednoho klienta se v čase propojuje jeho životní situace, individuální cíle, konkrétní podpora sociálního pracovníka, spolupráce dalších institucí i vyhodnocování dalšího postupu.</p><p class="digital-social-purpose">Aplikace pomáhá tuto práci vést jako jeden navazující proces.</p><a class="button dark" href="{enquiry('Zájem o systém pro sociální práci na obci')}">Zeptat se na systém pro obec <span aria-hidden="true">→</span></a>{product_screenshot('municipal.jpg', 'Sociální práce na obci — individuální plán a cíle klienta', 1363, 751)}</div>
<div class="digital-social-areas">{social_areas}</div></div>
</div></section>

<section class="section digital-team" id="tymovy-portal"><div class="wrap digital-nno-layout"><div><span class="eyebrow">Pro sociální služby, NNO a projektové týmy</span><h3 class="digital-product-title">Týmový portál</h3><p class="digital-nno-lead">Řiďte práci. Rozvíjejte lidi.</p><p>Výkazy, hodnocení, vzdělávací plány, absolvované vzdělávání, supervize, porady a úkoly v jednom prostředí.</p><p class="digital-nno-key">Výkon práce a rozvoj lidí nemusí být dva oddělené světy.</p><a class="button dark" href="/digitalni-nastroje/tymovy-portal/">Prohlédnout týmový portál <span aria-hidden="true">→</span></a></div><div class="digital-product-proof">{product_screenshot('team.jpg', 'Týmový portál — souhrn týmu a přehled pracovníků', 1363, 593)}<div class="digital-nno-areas"><div><h4>Hodnocení, které pokračuje vzděláváním</h4><p>Zpětná vazba se promítá do rozvojových cílů, vzdělávacího plánu a vyhodnocení skutečného posunu.</p></div><div><h4>Přehled o týmu</h4><p>Stav výkazů, vzdělávání, supervizí a úkolů na jednom místě.</p></div><div><h4>Metodický spořič</h4><p>Krátké metodické otázky při nečinnosti aplikace, se správným řešením a vysvětlením.</p></div></div></div></div></section>
</section>
<section class="section digital-ai" id="ai-nastroje"><div class="wrap"><div class="digital-section-heading"><span class="eyebrow">04 / AI nástroje pro odbornou praxi</span><h2>Odborný zápis s metodickou oporou</h2></div><div class="digital-nno-layout"><div><h3 class="digital-product-title">E.L.A.I.</h3><p class="digital-nno-lead">Ze syrových poznámek profesionální zápis.</p><p>AI asistent pro dluhové poradce převede pracovní poznámky do strukturovaného textu a nabídne metodickou kontrolu. Pracuje s pravidly, terminologií a fázemi dluhového poradenství.</p><a class="button dark" href="/digitalni-nastroje/elai/">Prohlédnout E.L.A.I. <span aria-hidden="true">→</span></a></div><div class="digital-nno-areas"><div><h4>Čistopis</h4><p>Jazyková úprava a sjednocení pracovních poznámek.</p></div><div><h4>Kazuistika</h4><p>Souvislý odborný obraz případu a jeho vývoje.</p></div><div><h4>Kontrola</h4><p>Druhý pohled na návaznost, zdroje informací a možné nedostatky zápisu.</p></div><p class="digital-ai-note">Výstup kontroluje poradce. Podmínky zpracování klientských údajů je nutné vyjasnit před nasazením.</p></div></div></div></section>

<section class="digital-practice"><div class="wrap"><h2>Nástroje vycházející z praxe</h2><p>Jednotlivé aplikace řeší konkrétní situace, které vznikají při sociální práci, dluhovém poradenství a realizaci projektů. Důraz klademe na jednoduché ovládání, srozumitelné výstupy a úsporu práce tam, kde dnes vzniká zbytečná administrativa.</p></div></section>

<section class="digital-custom" id="systemy-na-miru"><div class="wrap">
<div class="digital-custom-layout"><div><span class="eyebrow">05 / Informační systémy na míru</span><h2>Když jedna aplikace nestačí</h2>
<p class="digital-custom-lead">Propojíme procesy vaší služby, projektu, organizace nebo firmy do jednoho systému.</p>
<p>Samostatný nástroj může vyřešit konkrétní problém. Organizace a firmy ale často potřebují propojit více procesů. Je možné vytvořit informační systém přizpůsobený tomu, jak skutečně pracujete.</p>
<p class="digital-custom-purpose">Cílem je odstranit práci, která se nemusí dělat ručně.</p>
<a class="button" href="{enquiry('Zájem o informační systém na míru')}">Chci řešení na míru <span aria-hidden="true">→</span></a></div>
<div class="digital-custom-areas digital-business-proof"><span class="eyebrow">Ukázkové řešení · ThermoVan</span><h3>Firemní informační systémy na míru</h3><p>Od zákazníka a nabídky přes zakázku, sklad a realizaci až po fakturu, platbu a servis.</p><ul><li>Zákazníci, kalkulace, nabídky a realizace</li><li>Sklad, nákup, doklady a finance</li><li>Komunikace, předání a servis</li></ul><p>Ukázkové řešení pro obchodně-realizační firmu propojuje více než dvacet provozních oblastí.</p><a class="digital-contact-link" href="/digitalni-nastroje/firemni-systemy/">Prohlédnout firemní řešení →</a></div></div>
<div class="digital-custom-contact"><div><h3>Máte podobný problém ve své organizaci nebo firmě?</h3><p>Nemusíte přesně vědět, jak má výsledná aplikace vypadat. Stačí popsat činnost, která zabírá zbytečně mnoho času, opakuje se nebo při ní pracujete s několika tabulkami, dokumenty či informačními systémy.</p><p>Společně posoudíme, zda už některý z nástrojů řešení nabízí, zda jej lze upravit, nebo zda dává smysl vytvořit samostatnou aplikaci.</p></div><a href="{enquiry('Digitální nástroje – potřeby naší organizace')}" class="digital-contact-link">Kontaktujte nás <span aria-hidden="true">→</span></a></div>
</div></section></div>'''


NNO_SECTIONS = [
    ("klientska-prace", "Klienti, rodiny a spolupráce služeb", [
        ("Klienti, rodiny a case management", [
            "Evidence rodin a jednotlivých osob není oddělena od samotné práce s klientem.",
            "U rodiny lze vést cíle podpory, konkrétní kroky, odpovědnosti, termíny a jejich plnění. Jednotlivé záznamy podpory se vážou ke konkrétním aktivním cílům.",
            "Je tak zpětně dohledatelné nejen to, že kontakt proběhl, ale také proč proběhl a k jaké změně měl směřovat.",
        ]),
        ("Plán podpory a koordinace", [
            "Každý cíl může obsahovat konkrétní kroky, odpovědné osoby, termíny a stav plnění.",
            "Do řešení situace lze zapojit další služby a odborníky a sledovat koordinaci podpory dítěte a rodiny.",
            "Systém tak podporuje skutečný case management, nikoli pouze evidenci jednotlivých kontaktů.",
        ]),
        ("Záznamy přímé podpory", [
            "U každého výkonu lze evidovat datum, obsah podpory, pracovníka, zapojené osoby, individuální čas jednotlivých klientů a vazbu na konkrétní část projektu.",
            "Díky tomu lze oddělit pracovní čas zaměstnance od skutečné délky podpory jednotlivých osob a vytvářet přesnější projektové souhrny.",
        ]),
        ("Síť aktérů", [
            "Samostatná evidence organizací a odborníků zapojených do podpory klientů umožňuje sledovat, kdo se na řešení situace podílí a jak je spolupráce nastavena.",
            "Síť aktérů se tak stává součástí case managementu i podkladem pro vyhodnocení projektu.",
        ]),
    ]),
    ("rizeni-projektu", "Řízení projektu", [
        ("Cíle, výstupy a indikátory", [
            "Systém průběžně počítá plnění projektových cílů, výstupů a indikátorů z evidovaných skutečností.",
            "Vedoucí projektu tak nemusí čekat na konec monitorovacího období, aby zjistil, zda se projekt blíží plánovaným hodnotám.",
            "Součástí jsou také podklady k jednotlivým indikátorům a možnost exportovat projektové souhrny.",
        ]),
        ("Pracovní výkazy", [
            "Pracovníci vedou měsíční výkazy podle svých pozic a pracovních vztahů.",
            "Systém pracuje s fondem pracovní doby, úvazky, nepřítomnostmi a skutečnými projektovými činnostmi. Výkaz prochází kontrolou a schválením a lze jej připravit pro tisk nebo podpis.",
        ]),
        ("Porady a úkoly", [
            "Zápisy z porad, odpovědné osoby, termíny a navazující úkoly jsou součástí stejného systému.",
            "Nesplněný úkol se může automaticky přenést do další porady bez vytváření duplicit. Pracovník zároveň vidí své vlastní úkoly a další povinnosti na jednom místě.",
        ]),
    ]),
    ("evaluace-projektu", "Evaluace projektu", [
        ("T0, T1 a T2", [
            "Systém umožňuje vést vstupní, výstupní a následné hodnocení klienta a porovnávat vývoj sledovaných oblastí v čase.",
            "Nejde pouze o uložení konečného skóre. Uchovávají se také podklady a informace potřebné k doložení výsledku.",
        ]),
        ("Výsledky R1 a R2", [
            "Aplikace pracuje s výsledkovými ukazateli klientské změny i s výsledky koordinované podpory rodiny.",
            "Výsledek je vyhodnocován z evidovaných podkladů podle nastavené metodiky, nikoli pouze subjektivním označením pracovníka.",
        ]),
        ("Dotazníky, rozhovory a případové studie", [
            "Evaluace může kombinovat více metod a více zdrojů důkazů.",
            "Systém umožňuje evidovat dotazníková šetření, rozhovory s klienty, členy týmu i externími aktéry, případové studie, zpětnou vazbu dětí a průběh sběru i kvalitu dat.",
        ]),
        ("Evaluační výstupy", [
            "Z dostupných podkladů lze vytvářet průběžné i závěrečné evaluační zprávy.",
            "Jednotlivé verze zprávy mají vlastní stav, autora, kontrolu a schválení. Schválený výstup se uzamkne a jeho další úprava probíhá vytvořením nové verze.",
            "Součástí výstupu mohou být také automaticky vytvořené souhrny projektových výsledků a vizualizace.",
        ]),
    ]),
]


def build_nno_system(email: str) -> str:
    def enquiry(subject: str) -> str:
        return escape("mailto:" + email + "?" + urlencode({"subject": subject}, quote_via=quote), quote=True)

    demo = enquiry("Žádost o ukázku – projektová evidence a evaluace pro NNO")
    project = enquiry("Projektová evidence a evaluace – náš projekt")
    sections = []
    for anchor, heading, topics in NNO_SECTIONS:
        articles = "".join(
            f'<article class="nno-topic"><h3>{escape(title)}</h3><div>'
            + "".join(f'<p>{escape(paragraph)}</p>' for paragraph in paragraphs)
            + '</div></article>'
            for title, paragraphs in topics
        )
        sections.append(f'<section class="section nno-section" id="{anchor}"><div class="wrap"><h2>{escape(heading)}</h2><div class="nno-topics">{articles}</div></div></section>')
    return f'''<div class="nno-page">
<section class="nno-hero"><div class="wrap">
<div class="breadcrumbs"><a href="/">Úvod</a> / <a href="/digitalni-nastroje/">Digitální nástroje</a> / Evidence a evaluace pro NNO</div>
<span class="eyebrow">Pro neziskové organizace</span><h1>Projektová evidence a evaluace pro NNO</h1>
<p class="nno-lead">Od práce s klientem až po závěrečnou evaluační zprávu.</p>
<p>Sociální projekt není jen evidence klientů a uskutečněných aktivit. Je potřeba plánovat práci s rodinou, koordinovat zapojené odborníky, evidovat skutečně poskytnutou podporu, řídit práci týmu, sledovat indikátory projektu a nakonec také doložit, zda podpora vedla ke skutečné změně.</p>
<p>Informační systém propojuje tyto části do jedné navazující evidence.</p>
<p class="nno-key">Nestačí vykázat, co se udělalo. Potřebujete doložit, co se změnilo.</p>
<div class="contact-actions"><a class="button dark" href="{demo}">Chci vidět ukázku <span aria-hidden="true">→</span></a><a class="button contact-email" href="{project}">Probrat náš projekt</a></div>
<nav class="digital-jumps" aria-label="Možnosti systému pro NNO"><a href="#klientska-prace">Klientská práce</a><a href="#rizeni-projektu">Řízení projektu</a><a href="#evaluace-projektu">Evaluace</a><a href="#navrh-s-ai">Pracovní návrh s AI</a><a href="#metodika-projektu">Přizpůsobení projektu</a></nav>
</div></section>
{''.join(sections)}
<section class="nno-ai" id="navrh-s-ai"><div class="wrap"><h2>Pracovní návrh s využitím AI</h2><div><p>Pro přípravu rozsáhlejšího textového výstupu lze využít AI jako pomocný nástroj.</p><p>Před odesláním jsou zobrazeny podklady, které mají být použity. Návrh následně prochází odbornou kontrolou pracovníka.</p><p><strong>Výpočty indikátorů a výsledků nejsou ponechány na AI, ale provádí je samotná aplikace podle nastavených pravidel.</strong></p></div></div></section>
<section class="section nno-integration"><div class="wrap"><h2>Jedna evidence místo několika oddělených světů</h2><p>Klientská práce, projektové řízení a evaluace často vznikají ve třech různých prostředích. Údaje o klientovi jsou v jedné evidenci, výkony a indikátory v tabulkách a evaluace vzniká později znovu skládáním podkladů z dokumentů, formulářů a zápisů.</p><p>Tento systém je propojuje. Údaj, který vznikne při skutečné práci s klientem, může následně sloužit pro řízení projektu, monitoring i evaluaci — bez dalšího ručního přepisování.</p></div></section>
<section class="digital-custom nno-tailored" id="metodika-projektu"><div class="wrap"><span class="eyebrow">Podle potřeb vaší organizace</span><h2>Přizpůsobení metodice konkrétního projektu</h2><p>Každý sociální projekt má jiné cíle, aktivity, indikátory a způsob evaluace. Systém proto může být přizpůsoben konkrétní projektové metodice, požadovaným výstupům a způsobu práce organizace.</p><p>Výchozím řešením je rozsáhlá aplikace vytvořená pro projekt zaměřený na bezpečí dětí a podporu rodin, ve které je propojen case management, projektové řízení a komplexní evaluace.</p><div class="contact-actions"><a class="button" href="{demo}">Chci vidět ukázku <span aria-hidden="true">→</span></a><a class="digital-contact-link" href="{project}">Probrat náš projekt</a></div><a class="nno-back" href="/digitalni-nastroje/">← Všechny digitální nástroje</a></div></section>
</div>'''
