# Experiment 1443: Objective-Revision Execution Manifest

Date: 2026-06-28

## Purpose

Turn the guarded objective-revision adoption checklist from runs `1440-1442`
into a concrete local execution manifest.

This run defines which objective set can drive primary local selection, which
route is only a cross-check, which objective remains diagnostic-only, and which
routes remain blocked.

It does not run new FDTD simulations, launch GPU work, transfer to field data,
run field FWI, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1443_local_2d_state_consistent_objective_revision_execution_manifest
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_execution_manifest_rows.csv
data/local_2d_state_consistent_objective_revision_execution_manifest_objectives.csv
data/local_2d_state_consistent_objective_revision_execution_manifest_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_execution_manifest.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_EXECUTION_MANIFEST.md
scripts/run_local_2d_state_consistent_objective_revision_execution_manifest.py
scripts/test_local_2d_state_consistent_objective_revision_execution_manifest.py
scripts/script_snapshot_manifest.json
```

## Result

```text
manifest routes:                    6
runnable-now routes:                 3
local policy routes:                 2
diagnostic-only routes:              1
new-design-required routes:          1
blocked-current-evidence routes:     2
primary objectives:                  5
majority cross-check objectives:     6
diagnostic objectives:               1
execution manifest ready:            true
drop-veryhigh primary ready:         true
majority vote cross-check ready:     true
veryhigh decision objective blocked: true
broad radius promoted:               false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The local primary objective set is:

```text
base; highband; late; late_high; early_high
```

The `veryhigh` objective is excluded from primary selection. It remains in the
majority-vote cross-check and in diagnostic reporting only.

## Interpretation

The local 2D objective-revision policy is now executable as a manifest:
primary selection uses five non-`veryhigh` objectives, majority vote remains a
local cross-check across all six objectives, and `veryhigh` is diagnostic only.
Broad-radius, physical, GPU, field, FWI, and 3D/HPC routes remain blocked.

## Decision

Use run `1443` as the local 2D objective-revision execution manifest. Do not
use `veryhigh` as the deciding primary objective and do not promote broad,
physical, GPU, field-transfer, field-FWI, or 3D/HPC claims from this branch.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_execution_manifest.py
3 passed
```

Figure validation:

```text
3221x869, dynamic range=255
```
