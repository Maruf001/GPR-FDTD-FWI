# BEM Experiment 392: 35-Field Real-Return Preflight Closure Plan

Date: 2026-06-29

## Purpose

Collapse the 35-field aperture-aware BEM/FDTD real-return preflight failures
from run `386` into a concrete closure checklist.

This run does not stage external FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, launch GPU work, transfer to field evidence, or start 3D
validation.

## Output

```text
outputs/bem_experiments/392_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan_action_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
closure plan ready:                 true
action groups:                      4
required external files:            3
required frequency files:           2
required metadata file:             1
required blocking metadata fields:  34
full metadata fields:               35
receiver-aperture addendum fields:  5
preflight checks:                   10
blocking failures:                  10
grouped blocking failures:          10
target file present:                false
background file present:            false
metadata file present:              false
real comparison ready:              false
3D validation ready:                false
GPU/HPC ready:                      false
```

## Interpretation

The run `386` preflight failure is concrete. Three external return files are
absent: target frequency bins, background frequency bins, and the metadata
ledger. The metadata ledger must contain 34 blocking fields, including the
receiver-aperture convention fields added after the aperture sensitivity audit.

| Priority | Closure action | Blocking checks | Files required |
| ---: | --- | ---: | ---: |
| 1 | Target frequency-bin export | 3 | 1 |
| 2 | Background frequency-bin export | 3 | 1 |
| 3 | Aperture-aware metadata ledger | 3 | 1 |
| 4 | Rerun 35-field preflight | 1 | 0 |

## Decision

Use this closure plan as the external BEM/FDTD return checklist. Keep real
comparison, 3D validation, field transfer, GPU/HPC, and field FWI blocked until
the three return files pass the 35-field preflight.

## Validation

Focused source test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan.py
3 passed
```

Figure validation:

```text
3652x931, dynamic range=255
```
