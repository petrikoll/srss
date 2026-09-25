# Web SRSS Jeseník — GitHub a Render

Samostatný export prezentačního webu Střediska rozvoje sociálních služeb, o.p.s. ze dne 25. 9. 2026.

## Co balíček obsahuje

- Celý prezentační web: úvod, informace o organizaci, služby, poradna, projekty, dokumenty, kontakty a produktové stránky digitálních nástrojů.
- Texty, logo, fotografie, ilustrace, čtyři ukázky rozhraní a responzivní styly.
- Upravitelný zdroj stránek v Pythonu a hotové HTML ve složce `dist`.
- `render.yaml` pro nasazení na Render.

**Samotné nabízené aplikace nejsou součástí balíčku.** Generátor IS ESF, ISIR, Sledovač OPZ+, E.L.A.I. a ostatní nástroje mají na webu prezentační obsah. Funkční generátor ani zdrojové kódy těchto aplikací se neexportují. Jeho původní spouštěcí tlačítka jsou v tomto exportu nahrazena tlačítkem „Domluvit ukázku“, které otevře e-mail na `srssjesenik@gmail.com`.

Web nepotřebuje databázi, přihlášení návštěvníka ani vlastní aplikační server. Kontaktní tlačítka používají telefonní a e-mailové odkazy. Ke správě webu slouží soubory v GitHubu; administrace/CMS není součástí.

## 1. Nahrání do GitHubu

1. Rozbalte ZIP do složky v počítači.
2. V GitHubu vytvořte nový prázdný repozitář, například `srss-jesenik-web`. Může být soukromý.
3. Zvolte **Add file → Upload files** a nahrajte **obsah rozbalené složky**, včetně podsložek a souboru `.python-version`. Nenahrávejte pouze samotný ZIP.
4. Potvrďte nahrání pomocí **Commit changes**.

V kořeni repozitáře musí být přímo `render.yaml`, `README.md`, `.python-version`, `src/` a `dist/`. Nevkládejte je ještě do další nadřazené složky.

Nepřenášejí se přístupové údaje k původnímu hostingu, původní Git historie ani jeho interní nastavení.

## 2. Nasazení na Render — doporučený postup

V Renderu zvolte **New → Blueprint**, připojte GitHub a vyberte tento repozitář. Render načte připravený `render.yaml`. Zkontrolujte službu `srss-jesenik-web` a potvrďte vytvoření.

Alternativně lze použít **New → Static Site** a zadat:

| Nastavení | Hodnota |
| --- | --- |
| Repository | Váš repozitář `srss-jesenik-web` |
| Branch | Větev obsahující soubory, obvykle `main` |
| Root Directory | Nechte prázdné |
| Build Command | `python3 src/build.py` |
| Publish Directory | `dist` |

Soubor `.python-version` nastavuje Python 3.12. Nejsou potřeba další Python balíčky, Node.js, npm, databáze ani tajné klíče. Pro Static Site se nezadává Start Command.

Po dokončení nasazení dostanete adresu na `onrender.com`. Návštěvníci se nemusí přihlašovat do Renderu ani GitHubu. Vlastní doménu lze připojit později v nastavení služby.

**Nenastavujte pravidlo přepisující všechny adresy na `/index.html`.** Tento web má samostatné HTML soubory pro jednotlivé podstránky; nejde o jednostránkovou React aplikaci.

## 3. Jak web upravovat

| Co upravujete | Soubor nebo složka |
| --- | --- |
| Hlavní stránky, společná hlavička a patička, kontakty | `src/build.py` |
| Přehled digitálních nástrojů a projektová evidence | `src/digital_tools.py` |
| Firemní systém, týmový portál a E.L.A.I. | `src/system_pages.py` |
| Prezentační stránky IS ESF, nástrojů OPZ+ a BIO Registry | `src/portfolio_extensions.py` |
| Archivní podklady | `src/catalog.json` |
| Vzhled | `dist/assets/site.css` |
| Obrázky a ukázky | `dist/assets/` |

Po změně zdrojového textu odešlete změnu do GitHubu. Při zapnutém automatickém nasazování Render sestaví a zveřejní novou verzi.

HTML v `dist/` je hotový výstup, ale při sestavení se obnovuje ze `src/`. Trvalé změny textů proto dělejte ve zdrojových souborech. `dist/assets/site.css` a obrázky se při sestavení zachovávají; tuto složku nemažte ani nevyřazujte z Gitu. `site.js` se generuje v `src/build.py`.

### Lokální náhled ve Windows

Pokud máte nainstalovaný Python 3.12 nebo novější, otevřete terminál v kořeni rozbalené složky:

```powershell
py -3 src/build.py
py -3 -m http.server 8000 --directory dist
```

Otevřete `http://localhost:8000`. Server ukončíte `Ctrl+C`. Náhled spouštějte přes tento server, ne dvojklikem na HTML — navigace používá adresy od kořene webu.

Na Linuxu/macOS použijte stejné příkazy s `python3` místo `py -3`.

## Zachované vlastnosti

- Dosavadní zákaz indexace `noindex,nofollow` zůstává zachován. Nebrání běžnému veřejnému otevření stránky; pokud má být web dohledatelný ve vyhledávačích, upravte tento meta tag v `src/build.py` a web znovu sestavte.
- Historické dokumenty a články zůstávají odkazované na původní externí zdroje. Jejich plné texty a přílohy nejsou součástí exportu.
- Mapy, fonty a další existující externí zdroje používají původní adresy. Samotná navigace a hlavní obrázky nejsou závislé na původní adrese ChatGPT Site.
- BIO Registry zůstává jako již existující samostatná produktová stránka; není vráceno do hlavního přehledu digitálních nástrojů.

## Dokumentace hostingu

Postup ověřen 25. 9. 2026 podle dokumentace Render:

- https://render.com/docs/static-sites
- https://render.com/docs/blueprint-spec
- https://render.com/docs/python-version

Balíček je připraven k nahrání. Nasazení do vašeho účtu GitHub/Render ještě nebylo provedeno.
