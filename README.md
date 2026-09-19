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
- [Recasting American Power in Latin America](https://carnegieendowment.org/research/2026/09/recasting-american-power-in-latin-america)
- [Kopalnia, która zbudowała Libiąż - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMijAFBVV95cUxNbGFTQUJOTE1oVDQzT3B4TDNQQlYwblNLZnNIa2dOUTlDMV9YTUdkeThmSTlTWjRnaFZySERoSjZPeVF2eVVxb0drNl8yQmdPeWRDazVRUnRwYV9seVRoVUotN3FIbklfZVd5NjNxMTMzMEtlOTlYb3BPTmRybkZITTljZXZNVUtacWVDYQ?oc=5)
- [Co łączy salezjanów w Oświęcimiu z Juliuszem Słowackim? Niezwykła historia - Gazeta Krakowska](https://news.google.com/atom/articles/CBMiuAFBVV95cUxNd3VELWw1UkxOeG1VOHMtbF82R0N3OVp6amp2Mnd0Mi0wMGxQNGtEaUtNekhvdjltR2lWYUxKQW4yNGpoaFhxNk5oamIzMlNlM1VycXRZTkN3c1NsZktVdjVqTXExamc0LXpId3QwYU5hOENCbWg5MFA5ZUJ6cE5ocWNmeTVhN0xpNm9tMWNhNUpUQVpDVGoxWGgxbTI0WkpIcGRBVTY4MVRiakFXaS0tSWF4RmQ4MTdE?oc=5)
- [Janina znów trzęsie powiatem. Gdzie teraz trwa wydobycie? - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMirgFBVV95cUxPSnhkRndIdkFSNmdMeXVyRFJoS19tWDFfekFEN1k4TXBpQ1hyTTUwb09rRFZBVjdhbVBfLU9lUmU5UnprUWtYZExYeVJUVFZZUHFKdl9LMWhHaUdaWWxwbDQwakppZWNSTlNMQnB1WHZQWTA1RTBva1p6N092alk2NE51dmMtUmh3UkE3aHg4cEQxeXc0YXZGQjN2TXNOM0RuQjhOSnlmcWJHODlzT3c?oc=5)
- [Turkey says it could help meet Saudi military needs under defence pact](https://www.reuters.com/business/aerospace-defense/turkey-says-it-could-help-meet-saudi-military-needs-under-defence-pact-2026-09-19/)
- [Slovak PM Fico says some in West seek war between Russia and NATO](https://www.reuters.com/world/slovak-pm-fico-says-some-west-seek-war-between-russia-nato-2026-09-19/)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝My passion has been to build an enduring company where people were motivated to make great products; the products, not the profits, were the motivation. Sculley flipped these priorities to where the goal was to make money. It's a subtle difference, but it ends up meaning everything. — Steve Jobs❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
