# .ai Field Guide

Starlight / Astro wiki prototype for the existing `.ai` project. Technical and editorial entrypoint; **not** a fork of canonical instructions, profile schemas or the composition engine.

```sh
cd wiki
npm ci
npm run dev
npm run build
```

This builds to `wiki/dist/`. Hosting and custom domain are intentionally not configured yet. A later deployment can use Cloudflare or GitHub Pages, after route and visibility review.

## Next

- Build the Overlay Playground from canonical engine fixtures.
- Document selected case studies rather than copying raw source files.
- Add diagrams and experimental essays in MDX.
- Optional translations when there is substantial stable material.
- Keep links to existing `docs/`, `schema/`, `tools/`, `profiles/` authoritative.
