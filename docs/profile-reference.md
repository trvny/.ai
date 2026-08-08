# Profile reference

`profile.yaml` describes communication and collaboration preferences. It does not grant tools, permissions, credentials, network access, or authority to change external state.

The JSON Schema is the machine-readable source of truth for accepted fields and values. This document explains their intended meaning and the current renderer behavior.

## Layering

Profiles are composed from left to right; later layers win.

- omit a field to inherit it from an earlier layer
- use an explicit value to replace the earlier value
- `null` is an explicit value, not shorthand for "inherit"

Mappings merge recursively. Scalars and lists replace earlier values.

## Personality

### Base voice

`personality.base` selects one base voice:

- `default` — neutral and content-first
- `professional` — precise and low on ceremony
- `friendly` — warm and collaborative
- `honest` — direct about evidence, uncertainty, limits, and completed actions
- `whimsical` — light imagery or humor when useful
- `concise` — result-first with minimal framing
- `cynical` — dry skepticism toward claims and needless complexity, never toward the user

The base voice is always rendered. `personality.intensity` controls extra emphasis on that selected voice; it does not switch the base voice on or off.

Current renderer behavior:

| intensity | effect |
|---|---|
| omitted / `null` | render the selected base voice with no extra emphasis |
| `0` | currently the same rendered output as omitted / `null` |
| `1` | baseline; currently the same rendered output as `0` |
| `2` | add an instruction to make the base voice clearly visible |
| `3` | currently the same rendered output as `2` |

The portable default profile uses `base: friendly` with `intensity: 1`. The `default` base voice itself has no separate built-in intensity.

### Modifiers

Available modifiers are:

`honest`, `warm`, `enthusiastic`, `concise`, `technical`, `educational`, `critical`, `headingsAndLists`, `emoji`, `quickReplies`, `whimsical`, and `cynical`.

Modifier levels accept `0..3` or `null`.

- omitted — inherit the earlier layer
- `null` — explicitly clear the inherited modifier value; no modifier instruction is rendered
- `0` — disable the extra modifier instruction
- `1..3` — enable the modifier

A disabled modifier is not a negative instruction. For example, `honest: 0` means "do not add the extra honesty modifier", not "be dishonest". Platform rules, factual accuracy, and any other active profile instructions still apply.

Current renderer behavior for active modifiers is intentionally simple: levels `1..3` use the same wording. The numeric level currently affects ordering, with stronger modifiers rendered before weaker ones.

Base voice and modifiers are additive. For example, `base: cynical` plus `modifiers.cynical: 3` renders both the cynical base voice and the cynical modifier, so the same tendency is reinforced rather than one value overriding the other.

## Adaptation

All adaptation fields are booleans:

- `followUserRegister`
- `preserveRequestedArtifactStyle`
- `reduceHumorInSeriousContexts`
- `mirrorLanguage`
- `allowCasualProfanity`

Only `true` adds the corresponding instruction to rendered output.

## Collaboration

### `preamble`

- `off` — do not announce work before answering
- `multiStepOnly` — preamble only for multi-step or state-changing work
- `always` — briefly state the plan before acting

### `initiative`

- `conservative` — stay within the requested scope unless another step is necessary
- `balanced` — take obvious useful steps independently without needless scope expansion
- `proactive` — actively surface related problems and useful improvements while respecting scope

### `verification`

- `light` — basic consistency and visible-error checks
- `normal` — verify important claims and results in proportion to risk
- `strict` — require strong evidence and thorough validation before firm conclusions

### `questionPolicy`

- `blockingOnly` — ask only when missing information blocks useful or safe progress
- `materialAmbiguity` — ask when ambiguity could materially change the result
- `earlyAlignment` — for larger tasks, align early on goal, scope, and success criteria

### `assumptionPolicy`

- `cautious` — avoid outcome-changing assumptions; label and confirm them
- `balanced` — make reasonable reversible assumptions and state material ones
- `decisive` — make reasonable decisions independently unless risk is material

The remaining collaboration options are booleans:

- `answerFirst`
- `plainChatIsDefault`
- `respectExplicitTurnInstructions`
- `avoidRoutinePraise`
- `avoidRoutineFollowUpOffer`
- `announceOnlyMaterialActions`
- `reportPartialFailures`
- `preferResultOverProcess`

Only `true` adds the corresponding instruction to rendered output.

## Practical examples

A strong cynical voice with an additional cynical modifier:

```yaml
personality:
  base: cynical
  intensity: 3
  modifiers:
    cynical: 3
```

A neutral base with selected accents:

```yaml
personality:
  base: default
  intensity: 1
  modifiers:
    concise: 2
    technical: 2
    warm: 1
```

An overlay that changes only initiative while inheriting everything else:

```yaml
collaboration:
  initiative: proactive
```

To remove an inherited modifier, set it to `0` or `null`. Prefer `0` when the intent is explicitly "off"; reserve `null` for overlays that intentionally clear a prior value.
