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
- [Powiatowi społecznicy spotkają się w Libiążu - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMilgFBVV95cUxQcEhKWlVWS1hZNE9yNGtrTVhmU29Jd2pxTEk2SFlIb2xybWxDVW9ybi1FLUVRanVjZERONVl5V2Y5WEhuZkVKRlM5V0FyVmI5aDNyYlZoSTJHZFNMemlWczZIRExSQnF2amNPVENBemo4UGRMekVKUUlCODVwWjBSRmE4MHI2dDljZGtGTHNsRVEtZ2hMWGc?oc=5)
- [W Puszczy Dulowskiej powstanie rezerwat? Jest oficjalny wniosek - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMiuwFBVV95cUxNVmFGeGRzUF9JWjVoSVFpREs3cmY0U2ZZQ1VLc05VSlI2NUs2X05kM292YnVNdGpGR3VmVktDaHhodDVLd1k4eHNkOU9DdVRxbllhcV9YSzU3ZVk0VXlOVm1Fang5a0dMNEE5b29ZY0ZwUzQ4a3ZudEtlLXd0dGZKVDlSWmEwVXhGSHo5a2cxQVlELWdtSjI3R2hkTHdUMW42TWtYS0pzQUNsbS1TTENNdEdqV3UydzlJb1kw?oc=5)
- [To będzie wyjątkowy dzień dla psów i ich właścicieli. Krzeszowice szykują akcję - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMiwgFBVV95cUxPMUFWanRpTDdQeU8tWE9KeXhEWDg5ZlN2eGtnczAzb1RkQXphbXJuLTZianZubnZoYS1DdUxfTW1VNkp0NjA2VVNQSGFWTTRVbTAwTlVrZFg4bkFnWWY3TmNvdlAwSHFEUk1qakcyODJCcF92RDNDejdxTk4wOTdFZkw3M0FGRTFUd3lweGxySjhfckFodUhzTmR5X3B0Y0kxQzRuZEJ5QTJHT2c1RWhhRl9sZGZuMDlOQ1NTYnhQYzdDUQ?oc=5)
- [Uwaga! Zamknięta droga w Libiążu - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMihAFBVV95cUxOMnRqekw1a1owUDVVZjVVSXpMRXhVSUtwUnNMUzB0SG5acDVzZDVINW1kWlIydTBHTDRyWTFBazd5R295VXVKQnlsZWljVTJ1Rkt6TUxGenpoV3F3TnQxMFM2eWt1X0h2bE51czBwSVdldER6S3kwNHdrSTllbWt2RnJoTDc?oc=5)
- [To oni będą ratować mieszkańców! Czterech nowych strażaków w Chrzanowie - Przelom.pl - portal ziemi chrzanowskiej](https://news.google.com/atom/articles/CBMiuAFBVV95cUxOcHRLczZTTTNJeEtjSDhuUDJFRWNqM0k2Ym9uSFhMcVBxSGFEX00waHM0NF9nbmczcDRFbFpXOGdzcjg5eWpHUjVnYlJBV2RVdnZ1ZEoxODZfN3dJbkJBQnU2NXZuejI0ZVRxQkwweGVRZzR1VmhpMkItV3E0a3VSQzRwWTAzY29MbkVuM3EyX29zdktXV2JMaVctNGVGMUpTb3Y5ZV9SM3lLSmFycU1Za1B3akZJYnd3?oc=5)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝“Code generation, like drinking alcohol, is good in moderation.”— Alex Lowe❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->
