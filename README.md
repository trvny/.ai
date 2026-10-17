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
- [Nawet 2500 zł miesięcznie na pomoc dla seniorów. Trzeba się pośpieszyć - Przelom.pl](https://news.google.com/atom/articles/CBMiswFBVV95cUxPaU5xTTlhMXA3R0lNeUkzT1JSYjdNck45emw2cTVBR2kwcTBvaTRtbGJLbm8yX2VhMnFYNHVyTFBpaVNwbi1XZFJGbGQ0RzJkVE5vU3pZT0twckk4TVMwOGhCTEc3bm90QW1BRWFCaEhrcE0wWk54c0NkLVdLSW9QNVR4Y2xTMWNPN0MyRzZib0NNZVVSVGFrZ2I4MzRUWVVPenoyVzh3aGxSQkQ2ejNTSTYzaw?oc=5)
- [Mówiąca AI influencerka lokalnie: Kandinsky 6 i Wan 2.2](https://promptowy.com/ai-influencerka-wideo-lokalnie/)
- [Ukrainian foreign minister says Russian-held town is a 'death trap' with starving residents](https://www.reuters.com/world/ukrainian-foreign-minister-says-russian-held-town-is-death-trap-with-starving-2026-10-17/)
- [github-advanced-security created review 5560129998 on PR #399 in travnie/aistee](https://github.com/travnie/aistee/pull/399?feedseek_event=17499601129#pullrequestreview-5560129998)
- [github-advanced-security commented on PR #399 in travnie/aistee · comment 4304538333](https://github.com/travnie/aistee/pull/399?feedseek_event=17499600796#discussion_r4304538333)
- [github-actions published release aistee-latest in travnie/aistee](https://github.com/travnie/aistee/releases/tag/aistee-latest#feedseek-event-17499576281)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝“Without a systematic way to start and keep data clean, bad data will happen.”— Donato Diorio❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
