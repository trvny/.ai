<div align="center">

# `.ai`

**Portable AI core for profiles, overlays, provider adapters, reusable instructions and skills.**

[![validate](https://img.shields.io/github/actions/workflow/status/trvny/.ai/validate.yml?branch=main&label=validate&logo=githubactions&logoColor=white&style=flat-square)](https://github.com/trvny/.ai/actions/workflows/validate.yml)
[![code license](https://img.shields.io/github/license/trvny/.ai?label=code&logo=opensourceinitiative&logoColor=white&color=6f42c1&style=flat-square)](https://spdx.org/licenses/ISC)
<a href="https://deepwiki.com/trvny/.ai"><picture><source srcset="https://img.shields.io/badge/DeepWiki-trvny%2F.ai-blue.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAyCAYAAAAnWDnqAAAAAXNSR0IArs4c6QAAA05JREFUaEPtmUtyEzEQhtWTQyQLHNak2AB7ZnyXZMEjXMGeK/AIi+QuHrMnbChYY7MIh8g01fJoopFb0uhhEqqcbWTp06/uv1saEDv4O3n3dV60RfP947Mm9/SQc0ICFQgzfc4CYZoTPAswgSJCCUJUnAAoRHOAUOcATwbmVLWdGoH//PB8mnKqScAhsD0kYP3j/Yt5LPQe2KvcXmGvRHcDnpxfL2zOYJ1mFwrryWTz0advv1Ut4CJgf5uhDuDj5eUcAUoahrdY/56ebRWeraTjMt/00Sh3UDtjgHtQNHwcRGOC98BJEAEymycmYcWwOprTgcB6VZ5JK5TAJ+fXGLBm3FDAmn6oPPjR4rKCAoJCal2eAiQp2x0vxTPB3ALO2CRkwmDy5WohzBDwSEFKRwPbknEggCPB/imwrycgxX2NzoMCHhPkDwqYMr9tRcP5qNrMZHkVnOjRMWwLCcr8ohBVb1OMjxLwGCvjTikrsBOiA6fNyCrm8V1rP93iVPpwaE+gO0SsWmPiXB+jikdf6SizrT5qKasx5j8ABbHpFTx+vFXp9EnYQmLx02h1QTTrl6eDqxLnGjporxl3NL3agEvXdT0WmEost648sQOYAeJS9Q7bfUVoMGnjo4AZdUMQku50McDcMWcBPvr0SzbTAFDfvJqwLzgxwATnCgnp4wDl6Aa+Ax283gghmj+vj7feE2KBBRMW3FzOpLOADl0Isb5587h/U4gGvkt5v60Z1VLG8BhYjbzRwyQZemwAd6cCR5/XFWLYZRIMpX39AR0tjaGGiGzLVyhse5C9RKC6ai42ppWPKiBagOvaYk8lO7DajerabOZP46Lby5wKjw1HCRx7p9sVMOWGzb/vA1hwiWc6jm3MvQDTogQkiqIhJV0nBQBTU+3okKCFDy9WwferkHjtxib7t3xIUQtHxnIwtx4mpg26/HfwVNVDb4oI9RHmx5WGelRVlrtiw43zboCLaxv46AZeB3IlTkwouebTr1y2NjSpHz68WNFjHvupy3q8TFn3Hos2IAk4Ju5dCo8B3wP7VPr/FGaKiG+T+v+TQqIrOqMTL1VdWV1DdmcbO8KXBz6esmYWYKPwDL5b5FA1a0hwapHiom0r/cKaoqr+27/XcrS5UwSMbQAAAABJRU5ErkJggg==" type="image/svg+xml"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></picture></a>

[**Submodule guide**](docs/submodule.md) · [**Example overlay**](examples/profile.overlay.yaml) · [**Schema**](schema/style-profile.schema.json)

</div>

---

## Public core, private overlay

`.ai` keeps reusable AI configuration in one public place while downstream repositories keep their own private or project-specific differences.

```mermaid
flowchart LR
    C[Public .ai core] --> M[Compose]
    O[Private overlay] --> M
    M --> E[Effective profile / instructions]
```

Later layers win. Reusable changes go upstream; local differences stay downstream. No reverse synchronization is needed.

## Layout

```text
.ai/
├── AGENTS.md      canonical repository guidance
├── CLAUDE.md      symlink -> AGENTS.md
├── GEMINI.md      symlink -> AGENTS.md
├── profiles/      base profiles
├── examples/      overlay examples
├── schema/        profile schema
├── tools/         composition helpers
├── tests/         core and repository contract tests
├── instructions/  reusable instructions
├── styles/        style guidance
├── templates/     project starters
└── skills/        portable opt-in skills
```

`CLAUDE.md` and `GEMINI.md` are symlinks to the canonical `AGENTS.md`, keeping one maintained source of repository guidance.

Files here are building blocks. Providers do not automatically discover or apply everything in the repository.

## Use it in another repository

The usual setup is a pinned submodule plus a local overlay:

```bash
git submodule add https://github.com/trvny/.ai.git .ai/core
cp .ai/core/examples/profile.overlay.yaml .ai/profile.yaml
```

For repositories that already use it:

```bash
git submodule update --init --recursive
```

See **[docs/submodule.md](docs/submodule.md)** for cloning, profile composition, rendering, updates and CI checkout.

## Composition

```bash
python .ai/core/tools/merge_profile.py \
  .ai/core/profiles/default.yaml \
  .ai/profile.yaml \
  --schema .ai/core/schema/style-profile.schema.json \
  --output .ai/generated/profile.yaml
```

The final composed profile is validated against the schema. Partial overlays only need to contain the values they change.

Provider-specific files remain reference defaults. Adapt or expose them where the consuming tool expects them rather than duplicating the whole core.

## Security boundary

Keep credentials, tokens, personal paths, private endpoints and machine-specific configuration out of the public core. Use environment variables, secret storage or ignored local files instead.

## Design rules

- one maintained source of truth per concern
- public core, downstream overlays
- thin provider adapters
- generated output separate from maintained input
- simple files before frameworks
- explicit behavior before hidden magic

## License

[ISC](LICENSE)

---

## 📰 Mininews

<!--README_FEED:START-->
- [Trust but Verify: Implementing Frontier AI Policy in California and Beyond](https://carnegieendowment.org/research/2026/11/trust-but-verify-implementing-frontier-ai-policy-in-california-and-beyond)
- [Promises Made, Promises Unmet: The NPP’s Struggle to Reform Sri Lanka](https://carnegieendowment.org/research/2026/11/promises-made-promises-unmet-the-npps-struggle-to-reform-sri-lanka)
- [Ma go wiele telefonów. Mało kto wie, do czego służy ten otwór](https://antyweb.pl/maly-otwor-obok-gniazda-ladowania-telefonu-do-czego-sluzy)
- [Tchibo Esperto Mini: mały ekspres BEZ kapsułek, który skradł me serce](https://antyweb.pl/tchibo-esperto-mini-maly-ekspres-bez-kapsulek-ktory-skradl-me-serce)
- [O północy w Porębie Wielkiej samochód wypadł z drogi, uderzył w drzewo i dachował - Gazeta Krakowska](https://news.google.com/atom/articles/CBMiwgFBVV95cUxPSGEwTVpFRU5NQ2diQUVWVUtQVjJUUW85LU9KZXBCTEtFQnlPWk1TOW1xSl9FQUgyd1pvVWxYRjRpbXhJY3d1NXl1UXQtcVp6aHAwS1VtaTg3SEVZZXpPUHVKZmJjRXgzV1ZhR3JELUs5UUFYWktPbmRMek9PSW9TUlFtaGx4TUh5SWk3MnZIYW5sdzFlZ2R6Ry1DbG1fbGZ5SDh2R0U0WGE4aXUwaVpvTTBqQzZLT1FNQWpteGNBU08yUQ?oc=5)
- [Nocny wypadek w Rudzach k. Zatora. Pijana 17-latka Zatorzanka wypadła z jadącego samochodu - Gazeta Krakowska](https://news.google.com/atom/articles/CBMizgFBVV95cUxOQ3pZTlQ4dng5aUtJSENUMEFndnUzcGJCcUVwRVg5RXhsMjZha2o1WjZmZy0zQnB6QVNzaV9TZWFGOG05b0VDUTI3LWVveTVGdl9PNzRpbkktbHBrMGQ1ZXF5R01sbkhxblhoQkwzVnF4RUVTOTNEUFVjY2cybGY3NEhHbHQ0WkRHMUR6Z1djeEVzZDE1TVI5Y1FoNHpkTllLcndVc0pYUVVrNlFXQjJOQW1Idlg3SXJpRDdFMDdocVJEckwyR2NjMWJnR0Zvdw?oc=5)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝Lenovo stands for ‘new legend’. ‘Le’ for legend, and ‘novo’ stands for new.❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->

## Field Guide (early preview)

The [Starlight wiki source](wiki/) adds a technical and editorial tour of the portable core. Source files in `profiles/`, `tools/`, `schema/` and `docs/` remain canonical. See [wiki roadmap](wiki/README.md).
