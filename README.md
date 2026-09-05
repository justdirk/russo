# Russo 23 — sito

Sito statico del salone **Russo 23** (Belli Capelli by Russo), Via Giuseppe Meda 23, Milano.

- `index.html` — la pagina (italiano, con interruttore inglese)
- `img/` — le fotografie ottimizzate. Al primo run il workflow le ricostruisce dalle fonti pubbliche elencate in `tools/sources.json` (Wayback Machine del vecchio sito, archivio Turli, copertina del libro, Instagram del salone) e le committa qui.
- `robots.txt`, `sitemap.xml`
- `.github/workflows/pages.yml` — pubblica su GitHub Pages a ogni push su `main`

## Indirizzo
GitHub Pages: `https://justdirk.github.io/russo/`

Quando il dominio definitivo è deciso: aggiungere un file `CNAME` con il dominio e sostituire `https://www.bellicapellibyrussomilano.it/` in `index.html`, `robots.txt` e `sitemap.xml`.

## Cosa manca
- Un ritratto di Raffaele Russo (nessuna fonte ne ha uno).
- Conferma del listino con il titolare (sezione `#listino` e blocco JSON-LD `hasOfferCatalog`).
