# Local 2D Experiment 1413: Repaired Execution CI Adoption Validator

Date: 2026-06-28

## Purpose

Validate the run `1412` CI adoption checklist from a consumer perspective.

This run checks whether the adoption checklist can be safely used as the local
2D regression handoff while keeping the full pack authoritative and blocking
physical, GPU, field, and 3D claims.

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1413_local_2d_state_consistent_repaired_execution_ci_adoption_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_adoption_validation_checks.csv
data/local_2d_state_consistent_repaired_execution_ci_adoption_validator_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_adoption_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ADOPTION_VALIDATOR.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_adoption_validator.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_adoption_validator.py
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
validation ready:                          true
source adoption routes:                    6
source fast-smoke routes:                  2
source full-pack routes:                   2
full pack remains authoritative:           true
sentinel replaces full pack:               false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
field FWI ready:                           false
ready for 3D/HPC:                          false
```

The six checks validate:

| Check group | Outcome |
| --- | --- |
| Source readiness | repaired dry run, claim guard, and checklist are ready |
| Route counts | 2 fast-smoke, 2 full-pack, 1 new-design, 1 blocked-current-evidence |
| Table resolution | all dry-run rows pass and expected/observed row counts match |
| Fast/full authority | fast routes use 11 rows; full routes use 88 rows |
| Blocked routes | physical and GPU/field/3D routes remain blocked or require new design |
| Claim boundary | full pack authoritative; sentinel does not replace it |

## Interpretation

The CI adoption checklist is internally consistent. It gives a clean local 2D
regression rule: use the reduced sentinel only for narrow consumer smoke, use
the repaired full core table for boundary-sensitive local 2D changes, and do
not use this evidence to promote physical, GPU, field, field FWI, or 3D/HPC
claims.

## Decision

Use run `1413` as the positive validator for the local 2D CI adoption
checklist. Sensitivity remains required before treating the checklist as fully
guarded.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_adoption_validator.py
7 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_adoption_validator.png
2573x838, dynamic range=255
```
