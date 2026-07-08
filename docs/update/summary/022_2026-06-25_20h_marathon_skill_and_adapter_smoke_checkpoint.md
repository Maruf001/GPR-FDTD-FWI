# 20h Marathon Skill And Adapter Smoke Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records two things:

1. The new execution-discipline skill requested by the user.
2. The next BEM adapter branch after run `037`.

This is a progress checkpoint, not a marathon stop condition.

## Skill

Created a separate personal Codex skill:

```text
/home/lam002/.codex/skills/gpr-20h-marathon
```

Purpose:

```text
Do not stop at clean checkpoints during a requested 20-hour autonomous
marathon. Treat checkpoints as progress artifacts, then continue to the next
defensible branch unless the user pauses, the requested window elapses, or a
real blocker/resource limit applies.
```

Validation:

```text
python /home/lam002/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /home/lam002/.codex/skills/gpr-20h-marathon

Skill is valid.
```

## BEM Run Added

```text
038_project_core_bem_scattering_adapter_smoke
```

Tracked note:

```text
docs/bem_experiments/038_project_core_bem_scattering_adapter_smoke.md
```

## Result

Run `038` converts the run `037` BEM/project-grid adapter contract into an
executable smoke test over the run `036` cases.

```text
contract run:                       outputs/bem_experiments/037_project_core_bem_scattering_adapter_contract
source run:                         outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
cases checked:                      3
interface items checked:            7
missing interface items:            0
worst selected adapter L2:          0.44601690298659386
adapter smoke ready:                true
```

Selected adapter metrics:

| epsr | Selected variant | Selected L2 |
| ---: | --- | ---: |
| 1.25 | product_div_source | 0.0989465314024021 |
| 2.0 | product_div_source | 0.23018542478328735 |
| 4.0 | receiver_conjugate_div_source | 0.44601690298659386 |

## Interpretation

The BEM/project-core scattering adapter is now an executable harness, not only
a design contract. It still uses project-core generated target-cell fields, but
it defines the exact interface and acceptance gate that BEM-compatible fields
must satisfy next.

## Next Branch

Continue immediately to:

```text
Replace project-core-generated target-cell fields in the run 038 adapter
harness with BEM-derived or BEM-compatible field inputs, while preserving the
same interface and gates.
```

Field and synthetic 2D guardrails remain unchanged:

```text
field FWI ready:        false
field GPU/HPC ready:    false
new fixed-radius GPU:   false
```

## Validation

```text
python -m py_compile run_project_core_bem_scattering_adapter_smoke.py
python run_project_core_bem_scattering_adapter_smoke.py
```

Figure check:

```text
outputs/bem_experiments/038_project_core_bem_scattering_adapter_smoke/figures/project_core_bem_scattering_adapter_smoke.png
1708x769, dynamic range=255
```
