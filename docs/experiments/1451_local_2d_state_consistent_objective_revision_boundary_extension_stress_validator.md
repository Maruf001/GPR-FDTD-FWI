# Experiment 1451: Objective Revision Boundary Extension Stress Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1450` boundary-extension stress result from a
consumer perspective.

This run uses saved artifacts only. It does not execute new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1451_local_2d_state_consistent_objective_revision_boundary_extension_stress_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_boundary_extension_case_outcomes.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_stress_validator_checks.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_stress_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_boundary_extension_stress_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_BOUNDARY_EXTENSION_STRESS_VALIDATOR.md
scripts/run_local_2d_state_consistent_objective_revision_boundary_extension_stress_validator.py
scripts/test_local_2d_state_consistent_objective_revision_boundary_extension_stress_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              7
passed checks:                       7
failed checks:                       0
all-objectives truth cases:          3
veryhigh-only failure cases:         2
all-objectives failure cases:        2
mixed failure cases:                 0
drop-veryhigh recovered cases:       5
majority-vote recovered cases:       5
validation ready:                    true
source stress ready:                 false
promote revised objective now:       false
broad radius promoted:               false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

Validated case taxonomy:

| Outcome | Count | Perturbations |
| --- | ---: | --- |
| all objectives select truth | 3 | correct state; near radius +1.80 mm; near radius +1.90 mm |
| only `veryhigh` fails | 2 | far radius -1.60 mm; near radius +2.10 mm |
| all objectives fail | 2 | far radius -1.80 mm; near +1.90 mm plus far -1.60 mm |
| mixed failure | 0 | none |

## Interpretation

The saved stress result is internally consistent. The revised local policy is
not a general boundary-extension repair: drop-`veryhigh` and majority vote each
recover five of seven stress cases, but both fail when every objective selects
the wrong x=187 mm candidate.

This validator protects the decision boundary by making the failed stress
result explicit and non-promoted.

## Decision

Use run `1451` as the guarded validation checkpoint for run `1450`. Treat the
revised objective policy as narrow and failed under harder boundary-extension
stress.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_boundary_extension_stress_validator.py
3 passed
```

Figure validation:

```text
3257x873, dynamic range=255
```
