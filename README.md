# .ai

Portable building blocks for AI-assisted projects: communication profiles, private overlays, instruction and style libraries, conservative provider defaults, reusable skills, and small tools that keep configuration understandable.

The repository is intentionally a **public core**, not a personal configuration dump. Project-specific preferences, identities, credentials, paths, and workflow rules belong in downstream private overlays.

## Why this exists

AI configuration tends to drift into copied prompts, provider-specific files, and slightly different versions of the same rule. `.ai` keeps the reusable layer in one place and makes private customization explicit.

The basic model is simple:

```text
public core + private overlay -> effective local configuration
```

Later layers win. No reverse synchronization is needed.

## Layout

```text
.ai/
├── profiles/              portable base profiles
├── examples/              small overlay examples
├── schema/                profile schema
├── tools/                 merge and rendering helpers
├── instructions/          paste-ready portable instructions
├── styles/                style vocabulary and guidance
├── templates/             small project starting points
├── skills/                reusable opt-in skills
├── .claude/               conservative Claude Code reference defaults
└── .codex/                conservative Codex reference defaults
```

Files in this repository do not magically become provider instructions just because they exist. Treat them as inputs or templates and wire them into the provider or project that should use them.

## Install as a submodule

For most repositories, the cleanest setup is to pin this public core as `.ai/core` and keep only your own overlay beside it:

```bash
git submodule add https://github.com/trvny/.ai.git .ai/core
mkdir -p .ai/generated
cp .ai/core/examples/profile.overlay.yaml .ai/profile.yaml
python -m pip install pyyaml jsonschema
```

After cloning a repository that already uses the submodule:

```bash
git submodule update --init --recursive
```

The full walkthrough covers cloning, overlays, rendering, updates, CI checkout and what belongs upstream vs. downstream:

**[Submodule setup guide →](docs/submodule.md)**

Keep `.ai/core` untouched. Put private values next to it:

```text
consumer-repo/
└── .ai/
    ├── core/              git submodule -> trvny/.ai
    ├── profile.yaml       private partial overlay
    ├── private/           other local-only material
    └── generated/         optional composed output
```

### Compose the effective profile

```bash
python .ai/core/tools/merge_profile.py \
  .ai/core/profiles/default.yaml \
  .ai/profile.yaml \
  --schema .ai/core/schema/style-profile.schema.json \
  --output .ai/generated/profile.yaml
```

Mappings are merged recursively. Scalars and lists from later files replace earlier values. An overlay can therefore contain only the fields it actually changes. The schema applies to the final composed profile, not to each partial overlay by itself.

### Render ready-to-use instructions

The renderer accepts the same ordered profile stack, so a consumer does not need a duplicated helper:

```bash
python .ai/core/tools/render_profile.py \
  .ai/core/profiles/default.yaml \
  .ai/profile.yaml \
  --schema .ai/core/schema/style-profile.schema.json \
  --output .ai/generated/instructions.txt
```

Language defaults to the composed profile's locale and can be overridden with `--language en` or `--language pl`.

Example overlay:

```yaml
id: my-private-profile
locale: pl-PL
personality:
  modifiers:
    concise: 2
    warm: 2
```

The rest still comes from the public base profile.

### Updating the core

```bash
git -C .ai/core fetch origin
git -C .ai/core checkout main
git -C .ai/core pull --ff-only
git add .ai/core
```

The direction stays obvious:

- reusable change -> this public repository
- personal or project-specific change -> the downstream overlay

## Portable library

`instructions/instructions.md` provides compact ready-to-adapt instruction blocks. `styles/styles.md` documents the portable style vocabulary used by the profile schema. `templates/` contains deliberately small starters rather than a full application framework.

## Provider defaults

`.claude/settings.json` and `.codex/config.toml` are conservative reference defaults. They intentionally avoid credentials, personal paths, model preferences, and project identities.

If a provider expects configuration at the consumer repository root, copy or adapt the relevant file there. A config nested inside a submodule is not automatically discovered by the provider.

## Skills

`skills/` contains portable opt-in bundles that are useful outside any single project. The initial bundle is `english-polish.skill`, focused on natural English <-> Polish translation and localization.

Project-specific and archival skills should stay in downstream private storage until they are intentionally cleaned up for public use.

## Security boundary

Public files must not contain:

- API keys, tokens, cookies, private endpoints, or secret values
- personal filesystem paths or machine-specific configuration
- private repository details that are not intentionally documented
- personal behavioral profiles presented as generic defaults

Secrets belong in environment variables, provider secret storage, or ignored local files.

## Design rules

- one maintained source of truth per concern
- public core, private overlays
- provider adapters stay thin
- generated output stays separate from maintained input
- simple files before frameworks
- explicit behavior before hidden magic

## 📰 Mininews

<!--README_FEED:START-->
- [Confronting the Barriers to AI Diffusion in the U.S. Military](https://carnegieendowment.org/research/2026/08/confronting-the-barriers-to-ai-diffusion-in-the-us-military)
- [US judges allow Trump to end protections for migrants from South Sudan, Myanmar](https://news.google.com/rss/articles/CBMisAFBVV95cUxOS0R4Q05HNGkyM2Zzaml1b0lTTDJBeFpJWUx6YXZIOVM2RmJ1b0Nidk1qamJmQ2oyUFVVWW0wNWVCV0ZGRkx0c2gzdkh2c2F1TEZPR0lHRlUyNFJHdVhQYm1Ja2gwVjVCTkY5b2hHbWFtbFlBTlZDUTVFRDFERGEwSXhac3dXTHpRbFRxb1NYWHd6VWV6Qjl5bjFlZXVrMkZKOTdJWEZzcTRNSThsdEt1Vw?oc=5)
- [Spain's government announces immediate border controls with Italy in migration spat](https://news.google.com/rss/articles/CBMixwFBVV95cUxPTTcwY21xTGlrcmc5ZmE2cmRUMFpvSExKMTRoZWVubE9PbWpEbGl2dEo1U1BLNDViRDdpbVRmUUhvQmpzUWU4S3k4RnpfeFp0YVFQanRveFJpdkhtcUdlZFVGSTQ1bU5zRWNiQXdWX2ZILW5GeVMtRUJxbFQxTzR0dEN2VEYwandzR3BZb0MyZ0VjNVBXejlBU2UxUHg3YzNsNGdIbzVMaWd1UllZZDlGR2R1RkduWUNPdE9yNGFmVW5Ca19OQmlR?oc=5)
- [US official: We expect a deal soon between Iran and Oman on Strait of Hormuz](https://news.google.com/rss/articles/CBMiuAFBVV95cUxPMkZHc1FWRXNSWG5BdjNhZ0dqOEdNUFUtUl80NTNFYkFrM2RrLVBiSXlOOFdaek5hcEhIMl84OVJLZnVDMzNodFBScmliaFdNYUpaN21uQ3V3VmQ2V1p3MGZ0QUozdTJQb09EcTJ1VERWc3E0d1Z5dkNvalFEcEVSQzRQejkwZmdybVJTVDJPbk4wMS1hWFBOaXJKaTE4MUxHNS1STUFxTzN4S0ZDSmtZOXFhdUZaa0d1?oc=5)
- [EXCLUSIVE: Trump administration to back three mineral projects with $58 million in financing](https://news.google.com/rss/articles/CBMiuwFBVV95cUxPdVZodXZtRWQ1dzdvLWxpTi1jTFNKUlF4RnYxc2JSTnZDdXE3S0gtQ1R5MENuMFlUU1M2S1pMX3pMVFBqZGh6NjhlOUNybmd3MU5WR2RVOG91Wml5WGFNS0w1OVhSWDFiWmJsRzBoRzlJZHNnUG5LeEN3M3RaNW9mNkVvMkYzazRRZF85ek5aYk5kOExBNERwTlN5dGNVdjl4MnZGRXRCZnB0NGNJaHRVWERQU2gzd3pqRVpr?oc=5)
- [Przegląd AI: 7 sierpnia 2026](https://promptowy.com/przeglad-ai-2026-08-07/)
<!--README_FEED:END-->

## 💬 Cytat z szuflady

<!-- markdownlint-disable MD033 -->
<!--STARTS_HERE_QUOTE_README-->
<i>❝Conquer anger with non-anger. Conquer badness with goodness. Conquer meanness with generosity. Conquer dishonesty with truth. — Buddha❞</i>
<!--ENDS_HERE_QUOTE_README-->
<!-- markdownlint-enable MD033 -->

## License

ISC. Use it, fork it, reshape it, and keep the copyright and license notice.
