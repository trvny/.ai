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
- [RUSI Reflects: The Mecca Agreement: From US Primacy to Regional Agency](https://www.rusi.org/news-and-comment/rusi-reflects/rusi-reflects-mecca-agreement-us-primacy-regional-agency)
- [W Płokach znów tłumy pielgrzymów. Wieczorem niebo rozświetlą fajerwerki \(WIDEO,ZDJĘCIA\) - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMixAFBVV95cUxQaC1GaFhPX2pHZFJfamMxZzF2YmhfQm80Skc0dXpKUjhacjhsVG1zTVJIVlVsZTBCeURHbHVpb1hxcFZQUnp5UFVsRjkzWUNrUnZad19lR25McVM3aUFOejdxR3FyYVhUaFlFZXJBdjFvUXhkQ3RXZVJNVEZabFhNMm1xbE04QnpfeHhVa29ibGFOeS1vaFRTc0hDV2MyM2tYTHFDcDRkbEFOZVAzVy1paHU4OW8tRmJOd0ZJV3lPSHgtMXRt?oc=5)
- [Dokąd trafia drewno z lokalnych lasów? Znamy największego odbiorcę - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMiywFBVV95cUxONzNnUVJJRFJGLUVFWDZZejZTRzM0LV9faTRmSm5sV3hqQWM0OFExRjZwMXk0VW9LUlVreUVjMTFmUTdGQmdKUWNIdDVXTDA2WE82YjhtY2dSWFMtNGhoU1hYNTQtVV9PdEJONTctTno5bHdjN09JTHpVQWl2b21DQm8yclA0U0lET3R3OUhYeUZnXzhUR0VycW5TR3dWMFBySXFvaGF6Ukprb2xZckd4OE1NOE5oRnBGNXg4dXAtZVJaVW8wMzZ1Z2ZfOA?oc=5)
- [Trump says he is removing U.S. tariffs on Irish whiskey](https://www.reuters.com/world/us/trump-says-he-is-lifting-tariffs-irish-whiskey-2026-09-13/)
- [Ahead of Fed meeting, Trump says US should have world's lowest interest rate](https://www.reuters.com/business/ahead-fed-meeting-trump-says-us-should-have-worlds-lowest-interest-rate-2026-09-13/)
- [Trump says he will consider request to release more 9/11 records](https://www.reuters.com/world/us/trump-says-hell-consider-whether-release-more-911-records-2026-09-13/)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝When you don't know what you believe, everything becomes an argument. Everything is debatable. But when you stand for something, decisions are obvious. — Anonymous❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
