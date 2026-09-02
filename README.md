# suveræn.dk

Kildekode og komplet, versionsstyret backup til hjemmesiden for den danske bog **Kryptosuverænitet – Bitcoins krypterede politiske filosofi** af Erik Cason.

Den publicerede side skal ligge på [suveræn.dk](https://suveræn.dk/) (DNS/HTTP bruger IDN-domænets ASCII-form `xn--suvern-tua.dk`). Køb foregår eksternt hos [SHOP21](https://shop21.dk/vare/kryptosuveraenitet-bitcoins-krypterede-politiske-filosofi/).

## Teknisk overblik

Siden er bevidst almindelig, statisk HTML og CSS:

- ingen database eller serverkode
- ingen JavaScript, tracking, cookies eller eksterne fonte
- ingen obligatoriske pakker eller build-trin
- GitHub Pages publicerer direkte fra roden af `main` ved hvert push
- alle produktionsfiler, billeder, metadata og deployment-filer ligger i repositoryet

Det gør siden hurtig, nem at gennemgå og flytbar til enhver statisk webhost. Filen `.nojekyll` sørger for, at GitHub Pages serverer filerne direkte.

## Lokal udvikling

Klon repositoryet og start en simpel lokal webserver fra projektets rod:

```bash
git clone https://github.com/suveraenmand-design/suveraen.dk.git
cd suveraen.dk
python3 -m http.server 4000
```

Åbn derefter <http://localhost:4000/>. Brug ikke kun `file://`, da interne links begynder med `/` og forventer en webserver.

Der skal ikke installeres Ruby, Node.js eller andre dependencies. Stop serveren med `Ctrl+C`.

## Redigering

| Indhold | Fil |
|---|---|
| Forsidetekst og sektioner | `index.html` |
| Om bogen og bogdata | `om-bogen/index.html` |
| Læseliste, noter og kildelinks | `laeseliste/index.html` |
| Ressourcer | `ressourcer/index.html` |
| Farver, typografi og responsivt design | `assets/css/main.css` |
| Bogforside | `assets/images/book-cover.webp` og mobilvariant `book-cover-640.webp` |
| Social delingsgrafik | `assets/images/social-card.webp` |
| Brugerleveret baggrund | `assets/images/background.webp` og `background-mobile.webp` |
| Tidligere Leviathan-afledning | `assets/images/leviathan-bg.webp` |
| Favicon | `assets/images/favicon.svg` |
| Titler, descriptions, canonical og Open Graph | `<head>` i hver HTML-fil |
| Søgemaskiners sider | `sitemap.xml` og `robots.txt` |
| Custom domain | `CNAME` |

### Bogforside og baggrund

De originale, godkendte kildebilleder ligger som `assets/images/9788785340085.jpg` og `assets/images/background.png`. Produktionssiden bruger weboptimerede varianter: `book-cover.webp`/`book-cover-640.webp` og `background.webp`/`background-mobile.webp`. Den tidligere monokrome Leviathan-afledning bevares som et lokalt designasset.

Ved en senere udskiftning:

1. erstat de godkendte kildefiler `9788785340085.jpg` og/eller `background.png`,
2. generér og optimér begge desktop- og mobilvarianter i WebP,
3. opdatér eventuelt socialkortet og `leviathan-bg.webp`,
4. ret filernes mål og billedets `alt`-tekst i `index.html`,
5. commit og push ændringen.

Kildemanuskriptet/PDF’en er ophavsretligt beskyttet og versionsstyres ikke i dette offentlige repository. Webteksterne er korte redaktionelle parafraser, ikke boguddrag.

## Test før push

Kør projektets kontrolscript (kun Python-standardbiblioteket kræves):

```bash
python3 scripts/check_site.py
```

Scriptet kontrollerer blandt andet interne links, billeder, canonical URLs, metadata, headingstruktur, sitemap, robots, CNAME og hemmelighedsmønstre. Tilføj `--external` for at kontrollere eksterne links; eksterne servere kan dog afvise automatiske forespørgsler midlertidigt.

Gennemse desuden siden manuelt på smal og bred skærm samt med tastaturet.

## Deploy med GitHub Pages

Repositoryet bruger GitHub Pages’ indbyggede branch-deployment, som er den simpleste løsning til denne statiske side. Pages er konfigureret med **Deploy from a branch**, branch **`main`** og mappe **`/(root)`**. Ved hvert push til `main` publicerer GitHub automatisk den nye version.

Filen `.nojekyll` sørger for, at indholdet serveres direkte uden Jekyll-behandling. Deployment kræver ingen secrets, tokens i repositoryet eller tredjepartstjenester.

Kontrollér opsætningen under **Settings → Pages → Build and deployment**:

1. *Source* skal være **Deploy from a branch**.
2. *Branch* skal være **main** og **/(root)**.
3. Custom domain skal være **`xn--suvern-tua.dk`**.
4. Slå **Enforce HTTPS** til, når DNS-kontrollen er færdig og certifikatet er udstedt.

Deploymentstatus kan ses under repositoryets **Deployments** eller **Actions**. En almindelig opdatering er:

```bash
git add .
git commit -m "Beskriv ændringen"
git push origin main
```

## Domain og DNS

Custom domain er `suveræn.dk`; den tekniske ASCII/punycode-form i DNS, GitHub og `CNAME` er `xn--suvern-tua.dk`. Canonical URL er apex-domænet uden `www`.

Opret disse records hos DNS-udbyderen (udbyderens rodnavn kan vises som `@` eller `xn--suvern-tua.dk`):

| Type | Hostname | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `suveraenmand-design.github.io.` |

Hvis DNS-udbyderen kræver det fulde IDN-hostname i stedet for `@`, bruges `xn--suvern-tua.dk` for apex og `www.xn--suvern-tua.dk` for `www`.

Fjern modstridende A/AAAA/CNAME-records for `@` og `www`. Bevar naturligvis MX/TXT-records, der bruges til mail eller domæneverifikation. En TTL på 3600 sekunder er passende. GitHub anbefaler både apex-records og `www`-CNAME; når apex er custom domain, omdirigerer Pages normalt `www` til apex.

Efter DNS-propagation:

```bash
dig +short xn--suvern-tua.dk A
dig +short xn--suvern-tua.dk AAAA
dig +short www.xn--suvern-tua.dk CNAME
curl -I https://xn--suvern-tua.dk/
curl -I https://www.xn--suvern-tua.dk/
```

Kontrollér, at apex giver `200`, at `www` omdirigerer til apex, og at browserens certifikat er gyldigt. DNS og certifikatudstedelse kan tage op til 24 timer. Brug ikke wildcard-DNS mod GitHub Pages.

## Backup

Repositoryet er hjemmesidens fulde, versionsstyrede backup. Hver Git-commit indeholder en genskabelig tilstand af HTML, CSS, lokale assets, metadata, domainfil og deployment-konfiguration. Der er ingen data i en ekstern database.

Lav eventuelt en ekstra offline backup med:

```bash
git clone --mirror https://github.com/suveraenmand-design/suveraen.dk.git suveraen.dk.git
```

## Recovery og flytning

På en ny maskine klones repositoryet normalt, hvorefter `python3 -m http.server 4000` giver en lokal kopi. Hvis GitHub Pages skal gendannes, vælg **Settings → Pages → Deploy from a branch**, derefter **main** og **/(root)**.

Siden kan også flyttes til Netlify, Cloudflare Pages, S3 eller en almindelig webserver ved at publicere repositoryets rod. Ved et nyt domæne skal canonical/OG-URLs, `robots.txt`, `sitemap.xml` og `CNAME` opdateres.

## Sikkerhed og privatliv

- Commit aldrig passwords, tokens, API-nøgler, mail-login eller `.env`-filer.
- Brug GitHub OAuth/device login, SSH eller en kortlivet token med mindst mulige rettigheder.
- Siden indlæser ingen tredjepartsscripts og foretager ingen tracking. Derfor er der som udgangspunkt hverken cookies eller behov for cookie-banner.
- Eksterne sider kan have deres egne privatlivs- og cookiepolitikker.

## Kildeprincipper

Tekster fra Crypto Sovereignty er linket og krediteret, ikke kopieret. Årstal og bibliografiske fakta er verificeret, hvor de bruges. Læselisten skelner mellem baggrundsmateriale og den danske bogs dokumenterede beskrivelse.
