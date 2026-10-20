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
- [Przejście podziemne w Chrzanowie zamknięte. Trwa wielkie czyszczenie - Przelom.pl](https://news.google.com/atom/articles/CBMiwAFBVV95cUxQNVAwQWVCWmNJWlVKVjNnRXVjQ1J6SzAxdW9LX1prNk1OdFUwb1BpYkhiMmUwQkxWazhQVDFpUlV0MUV5MWFDY1RjbE5KcE1hVHFHclB4MDVyamxMbXV1aU5RRng1blVFZWUwSnVteGJJZTV3dElCU3dPQ1l1MTdWSHM0eVloS0VnNGpELXFTUTV5Z3d2Rk1pSEt1RTlTRjVzaWg5MUVINUI0VXRZRG5Qb3pwaGZGNXNFbVZFZFZkb2o?oc=5)
- [EXCLUSIVE: OpenAI seeks to accelerate fundraising ahead of Anthropic IPO, sources say](https://www.reuters.com/world/openai-seeks-accelerate-fundraising-ahead-anthropic-ipo-sources-say-2026-10-19/)
- [US officials plan to travel to Norway, Russia for Ukraine talks, sources say](https://www.reuters.com/world/europe/us-officials-plan-travel-norway-ukraine-talks-sources-say-2026-10-19/)
- [Nvidia-backed Nscale, Anthropic in talks for new $45 billion AI cloud deal, source says](https://www.reuters.com/technology/nscale-anthropic-talks-45-billion-cloud-computing-deal-bloomberg-news-reports-2026-10-19/)
- [Former Google CEO Schmidt owns 1% stake in Anthropic, Bloomberg reports](https://www.reuters.com/business/former-google-ceo-schmidt-owns-1-stake-anthropic-bloomberg-reports-2026-10-19/)
- [Texas federal judge suspended from hearing cases over mental health concerns](https://www.reuters.com/legal/government/texas-federal-judge-suspended-hearing-cases-over-mental-health-concerns-2026-10-19/)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝“I do not fear computers. I fear lack of them.”— Isaac Asimov❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
