# BEM Experiment 087: External 3D FDTD Return Metadata Preflight Smoke

Date: 2026-06-25

## Purpose

Prove that the run `086` metadata preflight can pass when the metadata ledger
and SHA-256 file hashes are complete.

This is the synthetic pass-case companion to the real pending-return failure
from run `086`.

This run does not launch 3D FDTD, run the real BEM/FDTD comparator, field FWI,
GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/087_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.csv
data/project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke_summary.json
figures/project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXTERNAL_RETURN_METADATA_PREFLIGHT_SMOKE.md
synthetic_return/project_core_bem_3d_fdtd_target_frequency_bins.csv
synthetic_return/project_core_bem_3d_fdtd_background_frequency_bins.csv
synthetic_return/project_core_bem_3d_fdtd_external_return_metadata.csv
scripts/run_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py
scripts/test_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
synthetic returned files:           2
metadata rows:                      12
preflight checks:                   7
passed checks:                      7
failed checks:                      0
blocking findings:                  0
synthetic metadata smoke pass:      true
synthetic smoke only:               true
real external FDTD data present:    false
ready for return preflight:         false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
```

## Interpretation

The metadata-preflight logic is satisfiable: a complete synthetic ledger with
matching SHA-256 values passes all seven checks.

The real pending external return remains absent. This run is a synthetic smoke,
not returned external FDTD data and not 3D validation.

## Decision

Keep run `086` as the real metadata gate. Use run `087` only to show the gate
logic can pass when the returned metadata and hashes are complete.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py
2 passed
```

Compile check:

```text
run_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py: pass
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py: pass
```

Figure check:

```text
1492x738, dynamic range=255
```
