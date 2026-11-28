# .ai Wiki

Astro / Starlight. Public repository reference, generated from canonical sources at build time. No parallel docs.

```sh
cd wiki
npm ci
npm run dev
npm run build
```

Requires Node and Python 3 (stdlib only). Generator: `scripts/generate.py`. Source edits trigger Pages rebuilds. Starlight search, navigation, per-page metadata and breadcrumbs; generated `sitemap.xml`, `llms.txt`, `llms-full.txt`. Hub crawler policy in `public/robots.txt`.

Published at https://trvny.github.io/.ai/ via GitHub Pages Actions. Project-scoped `/.ai/robots.txt` is not the host's root crawler policy; `https://trvny.github.io/robots.txt` is authoritative. Submit the project sitemap directly if needed.
