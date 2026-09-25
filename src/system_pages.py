"""Product detail pages based on the owner's supplied descriptions."""

from html import escape
from urllib.parse import quote, urlencode


def enquiry(email, subject):
    return escape("mailto:" + email + "?" + urlencode({"subject": subject}, quote_via=quote), quote=True)


def topics(items):
    return "".join(
        f'<article class="system-topic"><h3>{escape(title)}</h3><div>'
        + "".join(f'<p>{escape(p)}</p>' for p in paragraphs)
        + '</div></article>'
        for title, paragraphs in items
    )


BUSINESS_OPERATIONS = [
    ("Od zákazníka k zakázce", [
        "Evidence zákazníků, poptávek a zakázek může být propojena s kalkulací, cenovou nabídkou, smlouvou, termíny i odpovědností konkrétních pracovníků.",
        "Uživatel tak vidí nejen údaje o zákazníkovi, ale především aktuální stav zakázky a další krok, který je potřeba provést.",
    ]),
    ("Kalkulace, nabídky a smlouvy", [
        "Interní kalkulace může pracovat s aktuálními cenami materiálu a technologickými postupy.",
        "Po schválení lze připravit nabídku, smlouvu a následné dokumenty bez opakovaného přepisování stejných údajů.",
    ]),
    ("Realizace a zakázkové listy", [
        "Zakázkový list může obsahovat rozsah realizace, technologické údaje, plánovanou spotřebu materiálu, fotografie i skutečnou spotřebu.",
        "Potřebný materiál lze současně rezervovat ve skladu a zahrnout do nákupního plánu.",
    ]),
    ("Sklad a nákup", [
        "Evidence skladových položek, rezervací a aktuálních nákupních cen může být přímo propojena s rozpracovanými zakázkami.",
        "Systém tak dokáže ukázat nejen stav skladu, ale také co bude potřeba nakoupit vzhledem k plánovaným termínům realizace.",
    ]),
]

BUSINESS_FINANCE = [
    ("Předání a fakturace", [
        "Z dokončené zakázky lze vytvořit předávací protokol včetně skutečně provedených prací, spotřeby, víceprací, fotodokumentace a potvrzení zákazníka.",
        "Po potvrzeném předání může systém připravit konečnou fakturu a zohlednit již uhrazené zálohy. Faktury mohou obsahovat QR platbu a být odesílány přímo z aplikace.",
    ]),
    ("Banka a finanční přehled", [
        "Bankovní pohyby lze automaticky načítat a párovat s vydanými i přijatými doklady.",
        "Cashflow potom nevychází pouze z účetní historie, ale také z otevřených faktur, plánovaných nákupů a rozpracovaných zakázek.",
    ]),
    ("Přijaté doklady bez ručního přepisování", [
        "Přijatou fakturu nebo účtenku lze nahrát přímo do systému.",
        "OCR připraví dodavatele, číslo dokladu, data a částky ke kontrole a originální dokument se bezpečně uloží do firemního archivu.",
    ]),
]

BUSINESS_RELATIONS = [
    ("E-mail jako součást zakázky", [
        "Firemní schránka nemusí být oddělený svět. E-mail lze rozpoznat podle zákazníka nebo kódu zakázky a jeho přílohy automaticky uložit ke správnému případu.",
        "Komunikace, dokumenty a zakázka tak zůstávají propojené.",
    ]),
    ("Reklamace a servis", [
        "Po dokončení zakázky práce systému nekončí.",
        "Reklamace a servisní případy mohou mít vlastní odpovědnost, termín, náklady, dokumentaci a historii řešení.",
    ]),
]


def build_business_system(email):
    demo = enquiry(email, "Žádost o ukázku – firemní informační systém")
    process = enquiry(email, "Firemní informační systém – náš proces")
    return f'''<div class="system-page business-system">
<section class="system-hero"><div class="wrap">
<div class="breadcrumbs"><a href="/">Úvod</a> / <a href="/digitalni-nastroje/">Digitální nástroje</a> / Firemní systémy</div>
<span class="eyebrow">Firemní informační systémy na míru</span><h1>Vaše firma už proces má.<br><em>Software se mu může přizpůsobit.</em></h1>
<p class="system-lead">Jeden proces. Jeden systém. Od prvního kontaktu až po zaplacenou zakázku.</p>
<p>Ve firmách často vzniká stejný problém: zákazníci jsou v jedné evidenci, nabídky v dokumentech, zakázky v tabulce, faktury v dalším programu, materiál někde jinde a důležitá komunikace zůstává v e-mailu.</p>
<p>Výsledkem je příliš mnoho míst, kde je potřeba údaje hledat. Informační systém lze vytvořit podle skutečného procesu konkrétní firmy a propojit jednotlivé kroky tak, aby na sebe navazovaly.</p>
<div class="contact-actions"><a class="button dark" href="{demo}">Ukázat firemní řešení <span aria-hidden="true">→</span></a><a class="button contact-email" href="{process}">Probrat náš proces</a></div>
<nav class="digital-jumps" aria-label="Oblasti firemního systému"><a href="#zakazky-realizace">Zakázky a realizace</a><a href="#finance-doklady">Finance a doklady</a><a href="#komunikace-servis">Komunikace a servis</a><a href="#reseni-thermovan">Ukázkové řešení ThermoVan</a></nav>
</div></section>
<section class="section system-section" id="zakazky-realizace"><div class="wrap"><span class="eyebrow">Od poptávky k předání</span><h2>Zakázka má jasný další krok.</h2><div class="system-topics">{topics(BUSINESS_OPERATIONS)}</div></div></section>
<section class="section system-section system-wash" id="finance-doklady"><div class="wrap"><h2>Doklady a finance v souvislostech</h2><div class="system-topics system-rows">{topics(BUSINESS_FINANCE)}</div></div></section>
<section class="section system-section" id="komunikace-servis"><div class="wrap"><h2>Komunikace zůstává u správné zakázky.</h2><div class="system-topics">{topics(BUSINESS_RELATIONS)}</div></div></section>
<section class="digital-custom system-tailored" id="reseni-thermovan"><div class="wrap"><span class="eyebrow">Ukázkové řešení · ThermoVan</span><h2>Software se přizpůsobí procesu firmy. Ne obráceně.</h2>
<p>Ukázkové řešení bylo vytvořeno pro konkrétní obchodně-realizační firmu a propojuje více než dvacet provozních oblastí do jednoho systému.</p>
<p>Jiná firma ale nepotřebuje stejné obrazovky ani stejné procesy. Nejprve se popíše skutečný tok práce a teprve podle něj se určí, které části má smysl digitalizovat a propojit.</p>
<p class="digital-custom-purpose">Cílem je odstranit zbytečné přepisování, hledání a kontrolování mezi několika systémy.</p>
<div class="contact-actions"><a class="button" href="{demo}">Ukázat firemní řešení <span aria-hidden="true">→</span></a><a class="digital-contact-link" href="{process}">Probrat náš proces</a></div><a class="nno-back" href="/digitalni-nastroje/">← Všechny digitální nástroje</a>
</div></section></div>'''


TEAM_DEVELOPMENT = [
    ("Hodnocení zaměstnanců", [
        "Hodnocení, které nekončí uloženým formulářem.",
        "Vedoucí pracovník může provést pravidelné hodnocení zaměstnance, zachytit jeho silné stránky, profesní cíle a oblasti, ve kterých se potřebuje dále rozvíjet. Výsledek hodnocení se následně promítá do další části systému.",
    ]),
    ("Individuální vzdělávací plán", [
        "Z hodnocení pracovníka mohou vzniknout konkrétní rozvojové potřeby a vzdělávací cíle.",
        "U každého pracovníka lze vést vzdělávací plán, určit, z čeho potřeba rozvoje vychází, naplánovat konkrétní vzdělávací aktivity a na konci období celý plán vyhodnotit.",
    ]),
    ("Skutečně absolvované vzdělávání", [
        "Naplánované vzdělávání a skutečné vzdělávání jsou propojené. Pracovník má vlastní vzdělávací kartu s kurzy, termíny, rozsahem vzdělávání a osvědčeními.",
        "Je tak vidět nejen to, co se mělo uskutečnit, ale také které rozvojové cíle byly skutečně naplněny.",
    ]),
    ("Supervize", [
        "Evidence individuálních a týmových supervizí je součástí stejného prostředí.",
        "Vedoucí tak získává přehled o využití supervize společně s ostatními údaji o profesním rozvoji týmu.",
    ]),
]


def build_team_portal(email):
    demo = enquiry(email, "Žádost o ukázku – Týmový portál")
    team = enquiry(email, "Týmový portál – použití v našem týmu")
    dashboard = "".join(f'<li>{item}</li>' for item in ["Stav pracovních výkazů", "Vzdělávání jednotlivých pracovníků", "Stav vzdělávacích plánů", "Absolvované supervize", "Otevřené úkoly", "Plnění povinností v jednotlivých obdobích"])
    cycle = "".join(f'<li><span>{number:02d}</span>{title}</li>' for number, title in enumerate(["Pracuji a vykazuji", "Dostávám zpětnou vazbu", "Stanovujeme rozvojové cíle", "Vzdělávám se", "Vyhodnocujeme posun"], 1))
    return f'''<div class="system-page team-system">
<section class="system-hero"><div class="wrap">
<div class="breadcrumbs"><a href="/">Úvod</a> / <a href="/digitalni-nastroje/">Digitální nástroje</a> / Týmový portál</div>
<span class="eyebrow">Týmový portál pro sociální služby a projekty</span><h1>Řiďte práci.<br><em>Rozvíjejte lidi.</em></h1>
<p class="system-lead">Výkon práce a rozvoj lidí nemusí být dva oddělené světy.</p>
<p>Jednoduchý personální a projektový portál pro týmy v sociálních službách, neziskových organizacích a projektech. Spojuje pracovní výkazy, hodnocení pracovníků, vzdělávací plány, absolvované vzdělávání, supervize, porady a úkoly do jednoho přehledného prostředí.</p>
<div class="contact-actions"><a class="button dark" href="{demo}">Chci vidět týmový portál <span aria-hidden="true">→</span></a><a class="button contact-email" href="{team}">Probrat použití v našem týmu</a></div>
<nav class="digital-jumps" aria-label="Možnosti Týmového portálu"><a href="#pracovni-vykazy">Pracovní výkazy</a><a href="#rozvoj-pracovniku">Hodnocení a rozvoj</a><a href="#prehled-tymu">Porady a tým</a><a href="#metodicky-sporic">Metodický spořič</a></nav>
</div></section>
<section class="section system-section" id="pracovni-vykazy"><div class="wrap system-split"><div><span class="eyebrow">Pracovní výkazy</span><h2>Každý pracovník vidí svůj výkaz. Vedoucí vidí, co potřebuje zkontrolovat.</h2></div><div><p>Pracovník průběžně eviduje svou práci a připravuje měsíční výkaz. Systém pracuje s pracovními pozicemi, úvazkem, fondem pracovní doby a pravidly konkrétního projektu.</p><p>Výkaz lze elektronicky předat nadřízenému ke kontrole a následně stáhnout v podobě připravené k podpisu. Podepsané výkazy lze znovu nahrát a archivovat.</p></div></div></section>
<section class="section system-section system-wash" id="rozvoj-pracovniku"><div class="wrap"><span class="eyebrow">Od zpětné vazby ke skutečnému posunu</span><h2>Hodnocení navazuje na vzdělávání.</h2><div class="system-topics">{topics(TEAM_DEVELOPMENT)}</div></div></section>
<section class="section system-section" id="prehled-tymu"><div class="wrap system-split"><div><h2>Porady a úkoly</h2><p>Porada nemusí skončit zápisem uloženým ve složce. Z jednání lze vytvořit zápis, přiřadit odpovědnost a termíny a sledovat navazující úkoly.</p><p>Tím se propojuje týmová komunikace s konkrétní odpovědností za další postup.</p></div><div class="team-dashboard"><h2>Dashboard týmu</h2><p>Vedoucí získává na jednom místě přehled o týmu. Může sledovat například:</p><ul>{dashboard}</ul><p>Nemusí proto otevírat několik tabulek a kontrolovat každého pracovníka zvlášť.</p></div></div></section>
<section class="team-method" id="metodicky-sporic"><div class="wrap system-split"><div><span class="eyebrow">Průběžný rozvoj odbornosti</span><h2>Metodický spořič</h2><p class="system-lead">I několik minut během pracovního dne lze využít pro rozvoj odbornosti.</p></div><div><p>Při delší nečinnosti může aplikace nabídnout pracovníkovi krátkou metodickou otázku.</p><p>Pracovník si zvolí jednu nebo několik otázek, odpoví a okamžitě získá správné řešení s vysvětlením.</p><p>Z běžného čekání tak vzniká drobná příležitost průběžně si upevňovat odborné znalosti. Bez samostatného e-learningového systému a bez povinného dlouhého školení.</p></div></div></section>
<section class="section system-section team-cycle"><div class="wrap"><h2>Jeden jednoduchý cyklus</h2><ol>{cycle}</ol><p>Právě propojení těchto kroků je hlavním rozdílem oproti samostatné aplikaci na pracovní výkazy nebo běžné personální evidenci.</p></div></section>
<section class="digital-custom system-tailored"><div class="wrap"><span class="eyebrow">Pro sociální služby, NNO a projektové týmy</span><h2>Lehký systém pro práci i rozvoj vašeho týmu.</h2><p>Výchozí systém vznikl pro konkrétní sociální projekt, jeho princip je ale možné přizpůsobit dalším organizacím.</p><p>Lze upravit role pracovníků, pracovní pozice, strukturu výkazů, pravidla schvalování, způsob hodnocení, vzdělávací proces i metodický obsah.</p><p class="digital-custom-purpose">Lehký systém pro organizace, které chtějí řídit nejen práci, ale také rozvoj lidí, kteří ji vykonávají.</p><div class="contact-actions"><a class="button" href="{demo}">Chci vidět týmový portál <span aria-hidden="true">→</span></a><a class="digital-contact-link" href="{team}">Probrat použití v našem týmu</a></div><a class="nno-back" href="/digitalni-nastroje/">← Všechny digitální nástroje</a></div></section>
</div>'''


ELAI_MODES = [
    ("Čistopis", [
        "Vložte pracovní poznámky ze schůzky. E.L.A.I. opraví jazyk, sjednotí formulace a vytvoří věcný profesionální zápis použitelný jako podklad do klientské dokumentace.",
        "Při úpravě má zachovat význam původních informací a nepřidávat skutečnosti, které ve vstupu nejsou. Výstup před uložením kontroluje poradce.",
    ]),
    ("Kazuistika", [
        "Z jednotlivých informací může vzniknout souvislý odborný obraz případu.",
        "E.L.A.I. propojí vstupní situaci klienta, jeho zakázku, průběh práce, klíčová zjištění, zvolené řešení a další směr podpory.",
        "Výsledkem je čitelná odborná kazuistika zachycující vývoj případu a jeho souvislosti.",
    ]),
    ("Kontrola", [
        "Druhý odborný pohled před uložením zápisu. E.L.A.I. dokáže zápis také pouze zkontrolovat.",
        "Zaměřuje se na nedostatky, které mohou skutečně ovlivnit odbornou použitelnost zápisu nebo bezpečnost dalšího postupu.",
        "Může upozornit na nejasný další krok, nedostatečně popsaný zdroj informace, chybějící důležité riziko, slabou návaznost navrženého řešení na zjištěnou situaci, chybějící podstatnou informaci nebo metodicky problematickou formulaci.",
    ]),
]

ELAI_PHASES = [
    ("Jednání se zájemcem o službu", ["Zakázka klienta, základní situace, prvotní stabilizace a další postup."]),
    ("Mapování závazků a příčin předlužení", ["Zdroje informací, mapování dluhů, příčiny situace a vyhodnocování získaných podkladů."]),
    ("Hledání a realizace řešení", ["Volba dalšího postupu, splátkové dohody, oddlužení a další způsoby řešení dluhové situace."]),
]


def build_elai(email):
    demo = enquiry(email, "Žádost o ukázku – E.L.A.I.")
    advice = enquiry(email, "E.L.A.I. – použití v naší poradně")
    return f'''<div class="system-page elai-system">
<section class="system-hero"><div class="wrap"><div class="breadcrumbs"><a href="/">Úvod</a> / <a href="/digitalni-nastroje/">Digitální nástroje</a> / E.L.A.I.</div>
<span class="eyebrow">E.L.A.I. · AI asistent pro dluhové poradce</span><h1>Ze syrových poznámek<br><em>profesionální zápis.</em></h1><p class="system-lead">Poznámky ze schůzky nemusí být hotovým zápisem.</p>
<p>Stačí zachytit důležité informace tak, jak při jednání skutečně vznikají. E.L.A.I. je následně převede do profesionálního textu a současně kontroluje jeho obsah z pohledu metodiky dluhového poradenství.</p><p>E.L.A.I. pracuje s pravidly, terminologií a logikou odborné práce dluhového poradce.</p>
<div class="contact-actions"><a class="button dark" href="{demo}">Chci vidět E.L.A.I. <span aria-hidden="true">→</span></a><a class="button contact-email" href="{advice}">Zajímá mě použití v naší poradně</a></div>
<nav class="digital-jumps" aria-label="Možnosti E.L.A.I."><a href="#modelova-ukazka">Modelová ukázka</a><a href="#zpusoby-prace">Tři způsoby práce</a><a href="#metodika-poradenstvi">Metodika poradenství</a><a href="#odborna-kontrola">Odborná kontrola a údaje</a></nav></div></section>
<section class="section system-section" id="modelova-ukazka"><div class="wrap"><span class="eyebrow">Modelový příklad se smyšlenými údaji</span><h2>Takto si děláte poznámky.<br>Takto může vypadat zápis.</h2>
<div class="elai-example"><div class="elai-raw"><h3>Pracovní poznámky</h3><p>klient 4 exekuce, výpis nemá, chce insolvenci, čistá mzda 26k, domluveno donese smlouvy…</p><span class="elai-example-label">E.L.A.I. · formulace a kontrola</span></div><div class="elai-output"><h3>Návrh strukturovaného zápisu</h3><dl><div><dt>Zakázka klienta</dt><dd>Klient má zájem o řešení své dluhové situace prostřednictvím oddlužení.</dd></div><div><dt>Dosud zjištěné informace</dt><dd>Klient uvádí čtyři exekuce a čistou mzdu 26 000 Kč. Výpis nemá k dispozici. Počet exekucí ani příjem nejsou v předložených poznámkách doloženy.</dd></div><div><dt>Dohodnutý další krok</dt><dd>Klient přinese smlouvy k dalšímu jednání.</dd></div></dl><div class="elai-quality"><strong>Kontrola kvality</strong><p>V poznámkách chybí termín dalšího jednání. Možnost oddlužení zatím není posouzena.</p></div><div class="elai-quality"><strong>Doporučený další postup ke zvážení poradcem</strong><p>Ověřit zdroje informací a doplnit podklady k posouzení situace.</p></div></div></div>
<p class="elai-example-note">Ilustrační příklad struktury výstupu, nikoli výsledek živého spuštění aplikace. Návrh zápisu i doporučení posuzuje poradce.</p></div></section>
<section class="section system-section system-wash" id="zpusoby-prace"><div class="wrap"><h2>Tři způsoby práce</h2><div class="system-topics system-rows">{topics(ELAI_MODES)}</div></div></section>
<section class="section system-section" id="metodika-poradenstvi"><div class="wrap"><h2>Rozumí procesu dluhového poradenství</h2><p class="system-section-intro">E.L.A.I. pracuje s jednotlivými fázemi odborné podpory. Kontrola se přizpůsobuje předmětu konkrétního kontaktu a nevyžaduje automaticky informace, které do dané fáze práce nepatří.</p><div class="system-topics system-rows">{topics(ELAI_PHASES)}</div></div></section>
<section class="section system-section system-wash"><div class="wrap system-split"><div><h2>Ověřená informace není totéž co tvrzení klienta.</h2></div><div><p>Pro kvalitní dluhové poradenství je důležité vědět, odkud informace pochází.</p><p>E.L.A.I. proto pracuje s rozdílem mezi údajem doloženým například dokumentem, registrem nebo komunikací s institucí a informací, kterou zatím uvedl pouze klient.</p><p>Pomáhá tak vytvářet přesnější a odborně čitelnější dokumentaci.</p></div></div></section>
<section class="section system-section"><div class="wrap system-split"><div><h2>AI s metodikou</h2><p>E.L.A.I. má definovaná pravidla odborného zápisu, používanou terminologii, minimální standard jednotlivých fází podpory a zásady metodické kontroly.</p><p>Cílem je použitelný odborný výstup: srozumitelná formulace, struktura a návaznost informací.</p></div><div><h2>Pravidla lze dále přizpůsobit</h2><p>Do aplikace lze doplnit vlastní metodické pokyny. Organizace tak může určit požadovaný styl zápisů, oblasti, na které má kontrola klást větší důraz, nebo vlastní metodická pravidla.</p><p>Základní princip lze přizpůsobit metodice konkrétní poradny nebo služby.</p></div></div></section>
<section class="elai-review" id="odborna-kontrola"><div class="wrap system-split"><div><h2>Odborné rozhodnutí zůstává na poradci.</h2><p>Výstup E.L.A.I. nenahrazuje odborné rozhodnutí pracovníka. Poradce zná klienta, posuzuje jeho situaci a rozhoduje o dalším postupu.</p><p>AI pomáhá s formulací, strukturou, kontrolou návaznosti a upozorněním na možné nedostatky.</p></div><div><h2>Práce s klientskými údaji</h2><p>Pro ukázku používejte smyšlené údaje bez identifikace skutečných klientů.</p><p>Před nasazením se skutečnými klientskými zápisy je potřeba vyjasnit, jaké údaje lze vkládat, jak je zbavit identifikujících údajů a za jakých podmínek se text ukládá a zpracovává u poskytovatele AI.</p></div></div></section>
<section class="digital-custom system-tailored"><div class="wrap"><span class="eyebrow">Pro vaši poradnu</span><h2>Méně času nad formulací.<br>Více prostoru pro odbornou práci.</h2><p>Probereme způsob použití, metodiku vaší služby i podmínky práce s údaji.</p><div class="contact-actions"><a class="button" href="{demo}">Chci vidět E.L.A.I. <span aria-hidden="true">→</span></a><a class="digital-contact-link" href="{advice}">Zajímá mě použití v naší poradně</a></div><a class="nno-back" href="/digitalni-nastroje/">← Všechny digitální nástroje</a></div></section>
</div>'''
