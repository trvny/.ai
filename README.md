<div align="center">

# `.ai`

**Portable AI core for profiles, overlays, provider adapters, reusable instructions and skills.**

[![validate](https://img.shields.io/github/actions/workflow/status/trvny/.ai/validate.yml?branch=main&label=validate&logo=githubactions&logoColor=white&style=flat-square)](https://github.com/trvny/.ai/actions/workflows/validate.yml)
[![license](https://img.shields.io/github/license/trvny/.ai?label=license&logo=opensourceinitiative&logoColor=white&color=6f42c1&style=flat-square)](LICENSE)
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
├── CLAUDE.md      Claude import shim -> AGENTS.md
├── GEMINI.md      Gemini import shim -> AGENTS.md
├── profiles/      base profiles
├── examples/      overlay examples
├── schema/        profile schema
├── tools/         composition helpers
├── tests/         core and repository contract tests
├── instructions/  reusable instructions
├── styles/        style guidance
├── templates/     project starters
├── skills/        portable opt-in skills
├── .claude/       Claude reference defaults
└── .codex/        Codex reference defaults
```

`CLAUDE.md` and `GEMINI.md` are regular text import shims rather than symlinks, so the canonical `AGENTS.md` also works in Windows checkouts without requiring symlink support.

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
- [Urban Word of the Day — grebo](https://www.urbandictionary.com/define.php?term=grebo&defid=1975218)
- [How to Engage with New Media: A Strategic Guide for Nonprofit Organizations](https://carnegieendowment.org/research/2026/08/how-to-engage-with-new-media-a-strategic-guide-for-nonprofit-organizations)
- [Urban Word of the Day — board chow](https://www.urbandictionary.com/define.php?term=board%20chow&defid=2568411)
- [Pasażerowie mogą odetchnąć z ulgą! Koniec tymczasowego przystanku w Chrzanowie - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMixAFBVV95cUxOS3BfMTRsT1NSLWFBRXQwdHpoYU1rOTVKNkJ4T0M2LWRHWFZ1NGVpanVyR2lEQ1pxVXFScDVKUV9janVRNEk0VGJDTkdLYThvU1VPSHBzeDdkM3lqMEpjcHRpU2d6VGVLQjZRZzBybTJvaGw4RHBlX0pnOFdhR3A0VzdIcEVfdG5BRnVwTTRvX3BvUXRkenVBekliN0s0NTdzYWJ6Mk4xVFV1Y0ljMnVsUW82ZmZNT0VMMF9GMFF2WXNhcVZq?oc=5)
- [ZKKM zmienił komunikat. Te autobusy ominą część Libiąża - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMipgFBVV95cUxPQXplaXdNTDRaSWN4bWJ1LWNMN2pTYTZhelVOenZDdlgzUTJEV1hTTGFyRFd1RXlRMldVblNRcFk3Y2hRclQ0UGxVbDQxUy1JaHpaTl9ZSXF1bkZmLXRXZDlFZk0tUmN2WXFwVHpPSV9fOVlsbkRORHBVS2pVdy1aRDV1WGZDVmptQUdBRHhVcVpJUmpUUWk1SmJnZjJFaFhfa1U5cW1B?oc=5)
- [Drugie takie miejsce w Małopolsce. Zaplecze techniczne Kolei Małopolskich rośnie w Oświęcimiu - oswiecimonline.pl](https://news.google.com/atom/articles/CBMiwAFBVV95cUxQb3dBZkZFZ3R4SWgycm1uNC1RR2tMYTdUTUh2X21jQk02X1JJWmpXZUZ4cUNPM1R2TXh0Y0ZDajhuQzJRTDQyWTVYa2RwSlFPdlBTYlZobVhMQzVIQlVWeHBXOW9KZU1RMzVrbEZEbDdtdTA4QUJsMkRSTTVQb0NwU2VsWkZaVjlOVEFVdHFBb2c5ZGVRcGhOU3huZWdjRmtfQ1NkdENTUGMwUFF2WUx4NXV3SEYzbkdNNTR0M0JkTm8?oc=5)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝The Space Shuttle never flew on new year’s day or eve because its computers couldn’t handle a year rollover.❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
