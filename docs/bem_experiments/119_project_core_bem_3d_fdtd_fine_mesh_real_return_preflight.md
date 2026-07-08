# BEM Experiment 119: Fine-Mesh Real-Return Preflight

Date: 2026-06-27

## Purpose

Preflight the preferred nine-bin external FDTD return path for comparison
against the run `117` fine-mesh BEM reference.

This run does not launch FDTD, install real returned files, perform real
BEM/FDTD comparison, make a 3D validation claim, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/119_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_real_return_expected_files.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_REAL_RETURN_PREFLIGHT.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.py
scripts/script_snapshot_manifest.json
```

## Result

```text
expected frequencies:              9
expected receivers:                31
expected rows per frequency file:  279
combined metadata fields:          25
blocking required metadata fields: 24
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

Expected pending return files:

| Role | File |
| --- | --- |
| target frequency bins | `project_core_bem_3d_fdtd_fine_mesh_target_frequency_bins.csv` |
| background frequency bins | `project_core_bem_3d_fdtd_fine_mesh_background_frequency_bins.csv` |
| metadata ledger | `project_core_bem_3d_fdtd_external_return_metadata.csv` |

## Interpretation

The BEM-side reference and synthetic comparator smoke are ready, but the
preferred real external FDTD return is not present in the pending return root.
The target frequency-bin file, background frequency-bin file, and combined
25-field metadata ledger are still required. The current metadata gate treats
24 of those fields as blocking-required.

## Decision

Use this preflight before accepting a preferred nine-bin external FDTD return.
Keep real BEM/FDTD comparison, 3D validation, layered 3D GPR claims, field FWI,
heavy GPU work, field 3D/HPC, and neural-network training blocked until target,
background, and metadata files pass this gate.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.py
sha256: cf0014bf85bf31f9a4174b79a99d3bc2463315840a4fe046c3f11b12a3aa4ed8

test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.py
sha256: bbcf3092c95235adb894cda486daf6273c09564096a625e681dc386ba1d9262d
```

Subsequent related BEM/FDTD return experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.py
5 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_real_return_preflight.png
2680x846, dynamic range=255
```
