# suveræn.dk

Kildekode og komplet, versionsstyret backup til hjemmesiden for den danske bog **Kryptosuverænitet – Bitcoins krypterede politiske filosofi** af Erik Cason.

Den publicerede side skal ligge på [suveræn.dk](https://suveræn.dk/) (DNS/HTTP bruger IDN-domænets ASCII-form `xn--suvern-tua.dk`). Køb foregår eksternt hos [SHOP21](https://shop21.dk/vare/kryptosuveraenitet-bitcoins-krypterede-politiske-filosofi/).

## Teknisk overblik

Siden er bevidst almindelig, statisk HTML og CSS:

- ingen database eller serverkode
- ingen JavaScript, tracking, cookies eller eksterne fonte
- ingen obligatoriske pakker eller build-trin
- GitHub Actions publicerer indholdet ved hvert push til `main`
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
| Bogforside | `assets/images/book-cover.webp` |
| Social delingsgrafik | `assets/images/social-card.webp` |
| Favicon | `assets/images/favicon.svg` |
| Titler, descriptions, canonical og Open Graph | `<head>` i hver HTML-fil |
| Søgemaskiners sider | `sitemap.xml` og `robots.txt` |
| Custom domain | `CNAME` |

### Udskift bogforsiden

Den nuværende `assets/images/book-cover.webp` er en original pladsholder, fordi SHOP21-siden ikke viser en eksplicit licens til at genudgive den officielle forside.

Når rettighedshaveren har givet tilladelse:

1. eksportér forsiden som WebP i cirka 900 × 1350 px (samme billedforhold),
2. optimér filen til web,
3. erstat `assets/images/book-cover.webp` uden at ændre filnavnet,
4. ret billedets `alt`-tekst og fjern pladsholderteksten i `index.html`,
5. commit og push ændringen.

Genbrug ikke SHOP21s billedfil alene fordi URL’en er offentlig; indhent brugsret først.

## Test før push

Kør projektets kontrolscript (kun Python-standardbiblioteket kræves):

```bash
python3 scripts/check_site.py
```

Scriptet kontrollerer blandt andet interne links, billeder, canonical URLs, metadata, headingstruktur, sitemap, robots, CNAME og hemmelighedsmønstre. Tilføj `--external` for at kontrollere eksterne links; eksterne servere kan dog afvise automatiske forespørgsler midlertidigt.

Gennemse desuden siden manuelt på smal og bred skærm samt med tastaturet.

## Deploy med GitHub Pages

Workflowet `.github/workflows/pages.yml` kører automatisk ved push til `main` og kan også startes manuelt under **Actions → Deploy static site to GitHub Pages → Run workflow**. Det uploader repositoryets statiske filer og publicerer dem via GitHub Pages.

Repositoryets Pages-indstilling skal have **Source: GitHub Actions**. Første opsætning:

1. Gå til **Settings → Pages**.
2. Vælg **GitHub Actions** under *Build and deployment / Source*.
3. Kontrollér det seneste workflow under **Actions**.
4. Angiv `xn--suvern-tua.dk` som custom domain, hvis GitHub ikke allerede har læst `CNAME`.
5. Slå **Enforce HTTPS** til, når DNS-kontrollen er færdig og certifikatet er udstedt.

Deployment kræver ingen secrets. GitHubs kortlivede `GITHUB_TOKEN` oprettes automatisk til workflowet og gemmes ikke i repositoryet.

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

På en ny maskine klones repositoryet normalt, hvorefter `python3 -m http.server 4000` giver en lokal kopi. Hvis GitHub Pages skal gendannes, aktivér **Settings → Pages → GitHub Actions** og kør workflowet igen.

Siden kan også flyttes til Netlify, Cloudflare Pages, S3 eller en almindelig webserver ved at publicere repositoryets rod. Ved et nyt domæne skal canonical/OG-URLs, `robots.txt`, `sitemap.xml` og `CNAME` opdateres.

## Sikkerhed og privatliv

- Commit aldrig passwords, tokens, API-nøgler, mail-login eller `.env`-filer.
- Brug GitHub OAuth/device login, SSH eller en kortlivet token med mindst mulige rettigheder.
- Siden indlæser ingen tredjepartsscripts og foretager ingen tracking. Derfor er der som udgangspunkt hverken cookies eller behov for cookie-banner.
- Eksterne sider kan have deres egne privatlivs- og cookiepolitikker.

## Kildeprincipper

Tekster fra Crypto Sovereignty er linket og krediteret, ikke kopieret. Årstal og bibliografiske fakta er verificeret, hvor de bruges. Læselisten skelner mellem baggrundsmateriale og den danske bogs dokumenterede beskrivelse.
