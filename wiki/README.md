# .ai Field Guide

Starlight / Astro wiki for the existing `.ai` project. Technical and editorial entrypoint; **not** a fork of canonical instructions, profile schemas or the composition engine.

```sh
cd wiki
npm ci
npm run dev
npm run build
```

The public target is **https://trvny.github.io/.ai/**. The [Wiki Pages workflow](../.github/workflows/wiki-pages.yml) builds only the `wiki/` source and deploys to GitHub Pages. Enable **Settings → Pages → Build and deployment → GitHub Actions** once for this repository. Until that setting is enabled and the deployment succeeds, treat the URL as a target, not a confirmed live website.

The Astro `base` is `/.ai`, matching the repository project URL. Existing source docs remain canonical.

## Next

- Build the Overlay Playground from canonical engine fixtures.
- Document selected case studies rather than copying raw source files.
- Add diagrams and experimental essays in MDX.
- Optional translations when there is substantial stable material.
- Keep links to existing `docs/`, `schema/`, `tools/`, `profiles/` authoritative.
