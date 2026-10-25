<div align="center">

# `.ai`

**Portable AI core for profiles, overlays, provider adapters, reusable instructions and skills.**

[![validate](https://img.shields.io/github/actions/workflow/status/trvny/.ai/validate.yml?branch=main&label=validate&logo=githubactions&logoColor=white&style=flat-square)](https://github.com/trvny/.ai/actions/workflows/validate.yml)
[![code license](https://img.shields.io/github/license/trvny/.ai?label=code&logo=opensourceinitiative&logoColor=white&color=6f42c1&style=flat-square)](https://spdx.org/licenses/ISC)
<a href="https://deepwiki.com/trvny/.ai"><img src="https://deepwiki.com/badge.svg" alt="DeepWiki"></a>

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
- [Star History Monthly October 2026 | Execution](https://www.star-history.com/blog/execution)
- [Time for Saudi Clarity on Normalization with Israel](https://carnegieendowment.org/research/2026/10/time-for-saudi-clarity-on-normalization-with-israel)
- [Pożar pociągu w Balinie. Iskry zapaliły benzynę w 1909 r. - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMioAFBVV95cUxPV1JPdk93VlQtRjY4bVoxQ0ljXzcxX3cwWXhvM2ZHSUE0VDdjNlhTR0xQSzlMa0tnYXItbHBieXBmUkVyajN6R1BWamRHU19sTC02Q3oxRXpRcWphS3V1LU1fcWJCN0FVMDg0Qm12Nk0tWTdMRVhRU0ZEWVM1ZGxRd3ZXQm1pdEJsRWhNZWtFSVMyOUdXTVRqdWVDc1czX3NB?oc=5)
- [Serbia's Vucic concedes defeat to student led movement in parliamentary election](https://www.reuters.com/world/europe/serbias-vucic-concedes-defeat-student-led-movement-parliamentary-election-2026-10-25/)
- [Będzie duży przełom w polityce Serbii? Zamknięto lokale wyborcze - Radio Zet](https://news.google.com/atom/articles/CBMiogFBVV95cUxPUXJYdUlWWGtzZnhBRTcwOTA0Sy1wRjBhYnVpRmxjWUhYbGNHS0hsOGNDMnl6RUdxZTNwY2dUWjhYc2MyanBNa2RxS09xQm5hT3JvSXk0OGZ0VHNYb3F0SUdNX1N4ZWdBdEZ5Z0ppVnB5U2FnNU10Z2ZLXzdYNVdOcnF5Wk1VczFzM2RwNE05Q0ttWk96VnFkLUxSWTJFakc1LXc?oc=5)
- [Komisje bez kamer. Czego obawiają się krzeszowiccy radni? - krzeszowiceone.pl](https://news.google.com/atom/articles/CBMiqAFBVV95cUxQMWZFUDVHWkNUVXU2V3NyUGZwcnVUZGF2MEFXRllQcldzd0dBeWY3WkhnQ3R2UGFhVzRXUmkyMWNRQ1VxZXFmVWhOS2c3MnhjcEJsdWpsUkVmemE5anFzUFlDMy16Wk02OTVQM0ppd0NOT2dTb1g5MmdUb090dXZuWGtJdFdoV19yS1o0X3hmcTNVX294Rl9fT3VPVFhGTGVxVnVKQlczcULSAa4BQVVfeXFMT0p4SHVfX2VsRmxFdzdFRmtkU19UVVFxcENYN0VSUTAtVUNoMWo1ZjJ5Q2owbkNxc1VncDhhVWpwUFdNd1Y5WTFYNTNDbDJDdGxxWFZDMDFmR1VweTBLbXhtSkc1eGkwdVpmM3V3VUVrN0tIZzRueFBfSnB6MXgwZ3hzb2gxMjRvUDZVUGI2SDc0UDN2cUVsaUIzU1N4WHV5c0V1ZW9RcW1ZVi1SOVJB?oc=5)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝All the domain names such as Google, Log In or Sign Up were free until 1995, but now everyone has to pay for every new domain name.❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->

## Field Guide (early preview)

The [Starlight wiki source](wiki/) adds a technical and editorial tour of the portable core. Source files in `profiles/`, `tools/`, `schema/` and `docs/` remain canonical. See [wiki roadmap](wiki/README.md).
