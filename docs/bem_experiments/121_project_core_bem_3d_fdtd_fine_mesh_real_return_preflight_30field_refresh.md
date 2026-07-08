# BEM Experiment 121: Fine-Mesh Real-Return Preflight 30-Field Refresh

Date: 2026-06-27

## Purpose

Refresh the preferred nine-bin external FDTD return preflight so it requires
the 30-field metadata template from run `120`.

This run does not launch FDTD, install real returned files, perform real
BEM/FDTD comparison, make a 3D validation claim, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/121_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_real_return_30field_expected_files.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_30field_preflight_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_30field_preflight_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_REAL_RETURN_PREFLIGHT_30FIELD_REFRESH.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
expected frequencies:              9
expected receivers:                31
expected rows per frequency file:  279
full metadata fields:              30
blocking metadata fields:          29
fine-mesh addendum fields:         5
preflight checks:                  10
blocking failures:                 10
target file present:               false
background file present:           false
metadata file present:             false
BEM reference export ready:        true
synthetic sensitivity expected:    true
real return preflight ready:       false
real BEM/FDTD comparison ready:    false
3D validation claim ready:         false
```

Current blocking checks:

| Check | Status | Detail |
| --- | --- | --- |
| `fdtd_target_file_exists` | fail | target frequency-bin file missing |
| `fdtd_background_file_exists` | fail | background frequency-bin file missing |
| `metadata_file_exists` | fail | metadata ledger missing |
| `metadata_required_keys_present` | fail | `missing=29` |

## Interpretation

The preferred real-return preflight now matches the 30-field fine-mesh metadata
template from run `120`. The BEM reference export and synthetic sensitivity
smoke remain ready, but real target, background, and metadata files are still
absent.

## Decision

Use this refreshed 30-field preflight as the current preferred nine-bin return
gate. Keep real BEM/FDTD comparison, 3D validation, layered 3D GPR claims,
field FWI, heavy GPU work, field 3D/HPC, and neural-network training blocked
until all target, background, and metadata checks pass.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh.py
sha256: 9c011b748ea7f9c45bcce5cf2da022f5ca9d6db984fda7b5a44c37ac13011e08

test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh.py
sha256: 95c8d326ed525a013c27a7c094ee34e84312db6dbfc17b29fdc45da854e5540f
```

Subsequent related BEM/FDTD return experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh.py
3 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.png
2680x846, dynamic range=255
```
