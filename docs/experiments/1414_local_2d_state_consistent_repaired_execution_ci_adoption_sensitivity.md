# Local 2D Experiment 1414: Repaired Execution CI Adoption Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1413` CI adoption validator against controlled damage
cases.

This run checks whether the validator accepts only the exact adoption checklist
and rejects common source-readiness, route-count, dry-run-resolution,
fast/full-authority, blocked-route, and downstream-promotion failures.

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1414_local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity_scenarios.csv
data/local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ADOPTION_SENSITIVITY.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity.py
```

## Result

```text
scenarios:                                  21
expected pass scenarios:                    1
expected failure scenarios:                 20
observed pass scenarios:                    1
observed failure scenarios:                 20
unexpected outcomes:                        0
sensitivity ready:                          true
full pack remains authoritative:            true
sentinel replaces full pack:                false
physical claim ready:                       false
GPU work ready:                             false
field transfer ready:                       false
field FWI ready:                            false
ready for 3D/HPC:                           false
```

The exact checklist passes. The 20 damaged variants fail as expected:

| Damage family | Examples |
| --- | --- |
| Source readiness drift | dry run not ready, claim guard not ready, checklist not ready |
| Route-count drift | route count drift, missing route, wrong adoption tier |
| Dry-run resolution drift | dry-run failure, expected/observed row mismatch |
| Fast/full authority drift | fast route requires full pack, full route does not require full pack |
| Blocked route drift | blocked route becomes executable or no longer requires new design |
| Claim-boundary drift | sentinel replaces full pack, physical/GPU/field/FWI/3D readiness |

## Interpretation

The CI adoption checklist now has guarded sensitivity coverage. It accepts the
exact checklist and rejects controlled corruption of the route split, table
resolution, fast/full-pack authority, blocked-route behavior, and claim
boundary.

## Decision

Use runs `1412-1414` as the guarded local 2D CI adoption checklist package.
Keep the full 88-row core table authoritative, keep the 11-row sentinel
fast-smoke-only, and keep physical claims, GPU work, field transfer, field FWI,
and 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity.py
6 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_adoption_sensitivity.png
3257x894, dynamic range=255
```
