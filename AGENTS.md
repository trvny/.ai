# AGENTS.md

This repository is the reusable public core for portable AI configuration.
Keep it generic, inspectable, and safe to consume from private downstream overlays.

## Boundaries

- Never add credentials, secret values, cookies, private endpoints, or personal filesystem paths.
- Do not encode one user's identity, private repositories, private services, or personal workflow as a generic default.
- Keep reusable behavior here. Keep personal and project-specific behavior in downstream overlays.
- Do not copy a public core file into a private consumer merely to customize it. Prefer a partial overlay.
- Do not import private Git history when promoting material into this repository.

## Structure

- `profiles/` contains complete reusable base profiles.
- `examples/` contains deliberately incomplete overlays and usage examples.
- `schema/` describes complete profile documents, not partial overlays.
- `tools/` contains small deterministic helpers.
- `instructions/` contains portable ready-to-adapt instruction blocks.
- `styles/` documents the portable style vocabulary and guidance.
- `templates/` contains deliberately small project starters.
- `skills/` contains intentionally published opt-in skill bundles.
- `.claude/` and `.codex/` are reference provider defaults. They are not automatically active in repositories that include this project as a submodule.

## Overlay contract

Overlay files are applied from left to right. Later values win.
Mappings merge recursively; lists and scalar values replace earlier values.
An overlay may be partial, but the final composed profile should be a valid complete profile.

Changes to overlay behavior should remain backward compatible unless a versioned migration is explicitly documented.

## Maintenance

- Prefer small, reversible changes.
- Keep one maintained source of truth per concern.
- Keep generated output out of maintained source directories.
- Avoid adding abstractions when a normal file or short script is enough.
- Validate executable helpers and referenced paths after changes.
- Keep comments, pull-request descriptions, and changelogs concise.
