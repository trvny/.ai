# .ai

Portable building blocks for AI-assisted projects: communication profiles, private overlays, conservative provider defaults, reusable skills, and small tools that keep configuration understandable.

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
├── tools/                 merge and maintenance helpers
├── skills/                reusable opt-in skills
├── .claude/               conservative Claude Code reference defaults
└── .codex/                conservative Codex reference defaults
```

Files in this repository do not magically become provider instructions just because they exist. Treat them as inputs or templates and wire them into the provider or project that should use them.

## Use it with a private overlay

A clean way to consume the public core from another repository is a Git submodule:

```bash
git submodule add https://github.com/trvny/.ai.git .ai/core
mkdir -p .ai/generated
cp .ai/core/examples/profile.overlay.yaml .ai/profile.yaml
python -m pip install pyyaml jsonschema
```

Keep `.ai/core` untouched. Put private values next to it:

```text
consumer-repo/
└── .ai/
    ├── core/              git submodule -> trvny/.ai
    ├── profile.yaml       private partial overlay
    ├── private/           other local-only material
    └── generated/         optional composed output
```

Merge and validate the public profile with one or more overlays:

```bash
python .ai/core/tools/merge_profile.py \
  .ai/core/profiles/default.yaml \
  .ai/profile.yaml \
  --schema .ai/core/schema/style-profile.schema.json \
  --output .ai/generated/profile.yaml
```

Mappings are merged recursively. Scalars and lists from later files replace earlier values. An overlay can therefore contain only the fields it actually changes. The schema applies to the final composed profile, not to each partial overlay by itself.

Example:

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

## License

ISC. Use it, fork it, reshape it, and keep the copyright and license notice.
