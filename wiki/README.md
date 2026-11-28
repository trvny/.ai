# .ai Wiki

Astro / Starlight. Public repository reference, generated from canonical sources at build time. No parallel docs.

```sh
cd wiki
npm ci
npm run dev
npm run build
```

Requires Node and Python 3 (stdlib only). Generator: `scripts/generate.py`. Source edits trigger Pages rebuilds. While the local dev server runs, use `npm run generate` after canonical source edits. Starlight search, navigation, per-page metadata and breadcrumbs; generated `sitemap.xml`, `llms.txt`, `llms-full.txt`. Hub crawler policy in `public/robots.txt`.

Published at https://ai.bartek.lol/ via GitHub Pages Actions. Custom domain: DNS-only CNAME to `trvny.github.io`; GitHub Pages manages HTTPS. Root `robots.txt` and sitemap apply to this host.
