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
- [How to Engage with New Media: A Strategic Guide for Nonprofit Organizations](https://carnegieendowment.org/research/2026/08/how-to-engage-with-new-media-a-strategic-guide-for-nonprofit-organizations)
- [How the U.S. Export-Import Bank Can Finally Join the Fight Against Climate Change](https://carnegieendowment.org/research/2026/09/renewable-energy-investment-united-states-exim-export-import-bank)
- [Darmowa telewizja na YouTube: ponad 210 oficjalnych kanałów na żywo z Polski i świata, sprawdzanych codziennie](https://promptowy.com/darmowa-telewizja-na-youtube-lista-kanalow-na-zywo/)
- [Przegląd AI: 5 września 2026](https://promptowy.com/przeglad-ai-2026-09-05/)
- [Zamknięcie dnia: Kto traci, gdy AI robi wszystko za nas](https://promptowy.com/zamkniecie-dnia-kto-traci-gdy-ai-robi-wszystko-za-nas/)
- [Putin says US-Russia contacts beneficial as talks begin with Witkoff and Kushner](https://www.reuters.com/world/europe/putin-says-us-russia-contacts-beneficial-talks-begin-with-witkoff-kushner-2026-09-05/)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝IMDb is one of the oldest websites on the internet, and began on Usenet in 1990 as a list of “actresses with beautiful eyes.”❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
