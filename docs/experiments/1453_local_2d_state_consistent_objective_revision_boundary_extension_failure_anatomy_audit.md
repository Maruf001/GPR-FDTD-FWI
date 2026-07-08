# Experiment 1453: Objective Revision Boundary-Extension Failure Anatomy

Date: 2026-06-28

## Purpose

Audit the saved run `1450` boundary-extension stress result to separate
isolated objective instability from stronger all-objective wrong-x locks.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1453_local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_objective_rows.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_perturbations.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_policy_rows.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_BOUNDARY_EXTENSION_FAILURE_ANATOMY.md
scripts/run_local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_audit.py
scripts/test_local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
perturbations:                       7
objective detail rows:              42
all-objectives-truth cases:          3
veryhigh-isolated failure cases:     2
all-objective wrong-x lock cases:    2
mixed objective failure cases:       0
common wrong-lock x:                 187.0 mm
wrong-lock objective failures:      12
minimum wrong-minus-truth misfit:   -0.023872185127222008
drop-veryhigh recovered cases:       5 / 7
majority-vote recovered cases:       5 / 7
failure anatomy ready:               true
promote revised objective now:       false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

Failure classes:

| Class | Cases | Interpretation |
| --- | ---: | --- |
| all objectives select truth | 3 | corrected-state and smaller near-radius extensions remain inside the narrow validated region |
| veryhigh isolated failure | 2 | drop-`veryhigh` and majority vote still recover truth |
| all-objective wrong-x lock | 2 | all six objectives select x=187 mm; objective filtering cannot repair these cases |
| mixed objective failure | 0 | no partial non-`veryhigh` failure class appears in this block |

## Interpretation

The failed stress result has two distinct failure modes. Two cases are isolated
`veryhigh`-objective failures where drop-`veryhigh` and majority vote recover
truth. Two harder cases are all-objective wrong-x locks where every objective
selects x=187 mm, so objective filtering alone cannot repair the branch.

## Decision

Use run `1453` as the failure-anatomy explanation for runs `1450-1452`.
Preserve the revised objective only inside its narrow validated scope, and
require a new disambiguating design before broad-radius, physical-transfer,
GPU, field-FWI, or 3D/HPC claims.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_boundary_extension_failure_anatomy_audit.py
3 passed
```

Figure validation:

```text
3284x1676, dynamic range=255
```
