# BEM Experiment 084: External 3D FDTD Return Preflight

Date: 2026-06-25

## Purpose

Define and run the preflight for returned external 3D FDTD frequency-bin files
before the BEM/FDTD comparator is allowed to run.

Run `083` packaged the request. This run defines the acceptance gate for the
future returned files.

This is a CPU-only preflight. It does not launch 3D FDTD, field FWI, GPU/HPC
work, or neural-network training.

## Output

```text
outputs/bem_experiments/084_project_core_bem_3d_fdtd_external_return_preflight
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_external_return_preflight.csv
data/project_core_bem_3d_fdtd_external_return_preflight_summary.json
figures/project_core_bem_3d_fdtd_external_return_preflight.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXTERNAL_RETURN_PREFLIGHT.md
scripts/run_project_core_bem_3d_fdtd_external_return_preflight.py
scripts/test_project_core_bem_3d_fdtd_external_return_preflight.py
scripts/script_snapshot_manifest.json
```

## Result

```text
preflight checks:                   10
passed checks:                      0
failed checks:                      10
blocking findings:                  10
paired frequency return ready:      false
real external FDTD data present:    false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
local 3D FDTD launch ready:         false
```

The default pending return folder is:

```text
outputs/bem_experiments/external_3d_fdtd_returns/pending_run083
```

It currently contains no returned target/background frequency-bin files, so the
preflight fails as expected.

## Interpretation

The return preflight is now executable. It requires both returned frequency-bin
files to exist, match the 12-column comparator schema, contain 124 rows each,
use the correct run roles, and fill all six complex-field component columns.

This is still not 3D validation. It is the gate that future returned external
FDTD files must pass before the run `075` comparator can be rerun on real
paired data.

## Decision

Do not run the real BEM/FDTD comparator or make any 3D validation claim until
both returned frequency-bin files pass this preflight.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_external_return_preflight.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_external_return_preflight.png
1924x772, dynamic range=255
```
