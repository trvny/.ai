# Travny Lean

Opt-in, spec-driven development. Intent and evidence over ceremony.
Based on [Spec Kit](https://github.github.io/spec-kit/), not a fork.
Local repo instructions and user intent take precedence. No new permissions.

## Start here

- Tiny fix, obvious change: just do it. No spec files.
- Exploration: spike, compare, prototype. No invented requirements; capture useful
  findings if the work survives. Change course freely.
- Larger change, ambiguous behavior, cross-agent handoff or risky contract:
  write just enough intent, approach, tasks and evidence to resume safely.
- Explicit request for a Spec Kit phase: run that phase. No mandatory phase
  gates or separate approval turns unless repo policy or risk requires them.

Read target repo instructions, live branch, recent changes, open PRs and
existing docs/specs first. Extend an existing home. No duplicate backlog,
constitution, architecture manual or task tracker.

## Chat / MCP (no CLI)

Tell the agent: "Use Travny Lean for this change" or "Continue Travny Lean in
<repo/branch/PR>". Read this guide via repository tools:
`trvny/.ai/templates/spec-kit/travny-lean/README.md` at the agreed ref (prefer
the project's pinned `.ai/core` ref; otherwise an explicitly chosen reviewed
commit). GitHub file reads/writes work without a checkout. Slash commands
are optional; no pretend shell access.

Use existing PR body or existing feature document for a short change. For
long-lived work, prefer existing spec location; fallback
`specs/<slug>/spec.md` (add plan/tasks only when useful). Keep paths discoverable
in the PR description. Resume from that PR's live head, not stale chat memory.
One logical change per PR. No GitHub Issues or project boards required;
use an existing transport issue only as authorized by local repo workflow.
Do not start a parallel tracker.

If the repo already uses Spec Kit, reuse its feature directory and artifacts.
No forced initialization, generated config, branch numbering, or tool installs
for chat-only work. Read/write through available approved tools; report
unavailable tests or writes, not fictional results.

## Native Spec Kit (optional)

For an already initialized project, using Spec Kit 1.4.4 or newer:

```sh
specify preset add --dev .ai/core/templates/spec-kit/travny-lean
specify preset list
specify preset resolve speckit.implement
```

Check resolution for all six phases (`speckit.<phase>`); Travny Lean must win.
Inspect the generated integration commands/skills for the guide reference.
If another preset wins, choose precedence explicitly (lower priority number
wins); do not silently override a project's other presets.

Adjust the path if the core is checked out elsewhere. Initialize only when
the project actually wants native Spec Kit; inspect existing integrations
and preserve their config. Install copies preset files; update intentionally
from the chosen core revision. Generic integration does not register command
overrides: use the chat path above. This preset replaces six core commands;
not a new workflow engine. Unreplaced native commands retain their own
behavior. Preserve configured extension hooks as described below.

Native commands read this installed README
(`.specify/presets/travny-lean/README.md`), not a moving remote source.
If absent, stop that command and repair the preset installation rather than
guessing policy. Keep the existing feature directory if continuing.
For a new feature choose a meaningful repo-relative path, default
`specs/<slug>`; inspect collisions. Set `.specify/feature.json` with
`{"feature_directory":"specs/<slug>"}` only for the selected feature. Never
overwrite another active feature silently. Before selecting, inspect
`SPECIFY_FEATURE_DIRECTORY` if available; if it conflicts, require the
operator to unset or align it before writing the pointer or artifacts.
Existing branch/PR rules win; no automatic branch creation in these commands.

### Native extension hooks

For each replaced phase, inspect `.specify/extensions.yml` if present.
Before phase work, handle `hooks.before_<phase>`; after successful phase
work, handle `hooks.after_<phase>`. Preserve order. Skip explicitly disabled
hooks and defer nonempty conditions to Spec Kit's HookExecutor; do not
interpret conditions yourself. For enabled unconditional hooks, offer
optional hooks without auto-running them; invoke mandatory (`optional: false`)
hooks via the actual integration and await results. Never merely print a
command and claim it ran. If config cannot be parsed, report the error and
that no hooks were checked, including mandatory ones. Do not claim successful
completion if mandatory hooks are blocked, unavailable or fail. Report policy
conflicts (e.g. automatic branch creation) rather than bypassing a hook or
repo authorization. No new hooks or gates required for adoption.

## Phases (scale to the change)

- Constitution: existing AGENTS.md/local policy is canonical. Native only:
  create/update `.specify/memory/constitution.md` as a short index of applicable
  local guidance (paths + scope), plus genuinely new governance explicitly
  requested. Put lasting policy in its existing canonical home, not two copies.
  Governance only; defer implementation. Chat does not need this file.
- Specify: goal, scope/non-goals, observable acceptance criteria, important
  constraints/assumptions. User-visible outcomes, not premature architecture.
  Native: `spec.md`, testable FR/SC IDs if useful. Update when evidence changes.
- Plan: likely touchpoints, meaningful design choices/tradeoffs, validation,
  migration/rollback only when relevant. Native: `plan.md`. Explore alternatives
  freely within actual contracts; do not freeze a weak first idea.
- Tasks: actionable ordered checkboxes, stable IDs for handoffs, relevant
  file paths/criteria; no exhaustive microtasks. Native: `tasks.md`. Mark only
  verified completions, keep blockers and next action explicit.
- Implement: inspect actual code, build, test, adapt plan/spec as needed.
  Work around independent blockers; stop unsafe or unauthorized steps.
  Preserve local PR/review/CI policy. Record deviations and rationale briefly.
- Converge / verify: compare actual behavior with current agreed intent,
  inspect tests/diff and missing cases; record evidence and remaining work.
  Native converge: append only missing actionable checkboxes to `tasks.md`,
  no app code edits, no duplicate tasks. Leave clean task file unchanged.
  Chat: use the existing artifact or PR for evidence; continue safe fixes
  if implementation is authorized. Pending checks are not a completed change.

For native plan/tasks/implement/converge, resolve `SPECIFY_FEATURE_DIRECTORY`
when nonempty, otherwise `.specify/feature.json`. Resolve relative paths from
the repo root; reject paths outside the repo. Keep this resolution read-only;
do not rewrite the saved pointer. If environment access is unavailable and
an override cannot be ruled out, disclose the limitation and avoid ambiguous
writes. Read the constitution if present, local guidance and selected artifacts.
If a required phase artifact is absent, name the missing file; do not invent
prior work. Native specify/plan/tasks write only their designated artifact
(and specify's feature pointer); implementation may update intent with a
brief rationale. Native implement reads spec/plan/tasks and tracks progress.
Never use a preset to bypass approval, release, migration or security policy.

## Minimal handoff

For chat, combine into one existing artifact when enough:

```md
# <goal>
Scope:
Acceptance:
Approach / assumptions:
- [ ] Next meaningful task
Evidence / blockers:
```

English, fragments, no filler. Omit empty sections. Record meaningful changes
to intent and verification. Keep completed history only if useful; do not
maintain the same checklist in two places.

## Pilot candidates

In a monorepo, choose scope at the subsystem boundary, not the whole repo.
For example: a cross-component contract or risky transport change. Do not
add runtime code, gates, folders or automation merely to adopt this guide.
