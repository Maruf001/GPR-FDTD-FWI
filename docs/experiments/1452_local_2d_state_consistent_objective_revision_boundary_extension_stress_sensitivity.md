# Experiment 1452: Objective Revision Boundary Extension Stress Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1451` validator for the saved run `1450`
boundary-extension stress result.

This run uses in-memory mutations of saved artifacts only. It does not execute
new FDTD simulations, launch GPU work, transfer to field evidence, run field
FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1452_local_2d_state_consistent_objective_revision_boundary_extension_stress_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_boundary_extension_stress_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_stress_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_boundary_extension_stress_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_BOUNDARY_EXTENSION_STRESS_SENSITIVITY.md
scripts/run_local_2d_state_consistent_objective_revision_boundary_extension_stress_sensitivity.py
scripts/test_local_2d_state_consistent_objective_revision_boundary_extension_stress_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         15
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        14
observed failure scenarios:        14
unexpected outcomes:               0
sensitivity ready:                 true
exact run 1450 accepted:           true
damaged variants rejected:         true
promote revised objective now:     false
broad radius promoted:             false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

Damaged variants covered:

| Damage family | Outcome |
| --- | --- |
| source objective-row count drift | rejected |
| all-pass, `veryhigh`-only, and all-objective failure taxonomy drift | rejected |
| false drop-`veryhigh` or majority-vote promotion | rejected |
| source stress-ready promotion | rejected |
| GPU or field-transfer readiness promotion | rejected |
| blank figure validation | rejected |
| missing script-snapshot count | rejected |
| policy-row count drift | rejected |

## Interpretation

The run `1451` validator accepts the exact saved run `1450` stress result and
rejects every damaged variant tested here. This guards the failed
boundary-extension result from being accidentally reinterpreted as a successful
policy promotion.

## Decision

Use runs `1450`-`1452` as the guarded failed boundary-extension stress block.
The revised local objective policy remains narrow and should not be promoted
beyond the earlier validated scope.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_boundary_extension_stress_sensitivity.py
3 passed
```

Figure validation:

```text
3437x895, dynamic range=255
```
