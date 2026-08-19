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
- [US debt crosses $40 trillion threshold after doubling under Trump and Biden](https://www.reuters.com/world/us-debt-crosses-40-trillion-threshold-after-doubling-under-trump-biden-2026-08-19/)
- [Dwa miasta, dwie trasy i setki rowerów. „Zakręceni sąsiedzi” wracają! - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMivAFBVV95cUxNdV9rWVhja3MybWdTV2pLeEFhcVUxUHRtbTFreFJIUXZLcGxfMEpqNkdBQ1gwTjRqWVpKb1BMT3dWYmVBX1N0Y1RFako2ZlJRbGJLQjQyTGxnOGJ4ZHJjTVlBNktWSXNLMFFiTkl4SHRKSWpXZzV6UFVKVVJRcXAyMDBTdDllbVI1bWtaR3RndVBwejYzVmRvbjJCZUt1MlJnemxmTXloNlpZdDlpY0dLdkhrUjVFS2JvMy1TcA?oc=5)
- [Liberia's former vice president charged in probe of transnational drug ring, government says](https://www.reuters.com/world/africa/liberias-former-vice-president-charged-transnational-narcotics-investigation-2026-08-19/)
- [Garmin Fenix 8 na dużej przecenie. Czyszczenie magazynów](https://antyweb.pl/garmin-fenix-8-na-duzej-przecenie-czyszczenie-magazynow)
- [Google dodaje quizy, symulacje i nowe funkcje Lens do wyszukiwarki na nowy rok szkolny](https://promptowy.com/google-quizy-symulacje-lens-wyszukiwarka-rok-szkolny/)
- [UN's Guterres seriously concerned by US sanctions on ICC](https://www.reuters.com/world/uns-guterres-seriously-concerned-by-us-sanctions-icc-2026-08-19/)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝I alone cannot change the world, but I can cast a stone across the waters to create many ripples. — Mother Teresa❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
