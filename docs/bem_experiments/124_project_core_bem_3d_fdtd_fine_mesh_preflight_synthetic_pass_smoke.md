# BEM Experiment 124: Fine-Mesh Preflight Synthetic Pass Smoke

Date: 2026-06-27

## Purpose

Build a complete synthetic target/background/metadata return inside the output
folder and run the preferred 30-field fine-mesh return preflight against it.

This run does not create real external FDTD data, run local 3D FDTD, make a 3D
validation claim, launch GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/124_project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke
```

Key artifacts:

```text
synthetic_return_root/
data/project_core_bem_3d_fdtd_fine_mesh_synthetic_return_preflight_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_synthetic_target_frequency_bins.csv
data/project_core_bem_3d_fdtd_fine_mesh_synthetic_background_frequency_bins.csv
data/project_core_bem_3d_fdtd_fine_mesh_synthetic_metadata.csv
data/project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_PREFLIGHT_SYNTHETIC_PASS_SMOKE.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
expected frequencies:             9
expected receivers:               31
target rows:                      279
background rows:                  279
metadata rows:                    30
preflight checks:                 25
preflight passes:                 25
blocking failures:                0
synthetic preflight ready:        true
real external FDTD data:          false
real BEM/FDTD comparison ready:   false
3D validation claim ready:        false
```

All blocking checks passed in the synthetic return root:

```text
fdtd_target_file_exists
fdtd_target_output_present
fdtd_target_required_columns
fdtd_target_row_count
fdtd_target_expected_key_coverage
fdtd_target_no_extra_keys
fdtd_target_no_duplicate_keys
fdtd_target_run_role
fdtd_target_receiver_positions
fdtd_target_finite_components
fdtd_background_file_exists
fdtd_background_output_present
fdtd_background_required_columns
fdtd_background_row_count
fdtd_background_expected_key_coverage
fdtd_background_no_extra_keys
fdtd_background_no_duplicate_keys
fdtd_background_run_role
fdtd_background_receiver_positions
fdtd_background_finite_components
metadata_file_exists
metadata_schema
metadata_required_keys_present
metadata_required_values_nonblank
fine_mesh_real_return_preflight_ready
```

## Interpretation

The preferred 30-field fine-mesh preflight is achievable. A complete synthetic
target/background/metadata return passes all blocking checks.

This validates the gate mechanics only. It does not change the real-data
blocker because the passing files are synthetic BEM-derived rows, not real
external FDTD target/background returns.

## Decision

Keep run `121` as the real-return gate. Use this synthetic pass smoke only to
confirm that the gate can pass when the required files and metadata are
present. Real BEM/FDTD comparison, 3D validation, local 3D FDTD launch,
GPU/HPC, layered 3D GPR claims, and field FWI remain blocked until real
external FDTD files pass the same gate.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke.py
sha256: 1020c152ebf60d8409b3b93d30bde4fffa13921a1aa054d94966fe92e9ec199b

test_project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke.py
sha256: 0cd7f1d980a405cc67d5185ae7a1c72854c94c72cc0d5fecd28f1628e6b3dcc8
```

Subsequent related BEM/FDTD return experiments should start from a duplicated
run-specific script.

## Validation

Focused fine-mesh preflight tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke.py
7 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_preflight_synthetic_pass_smoke.png
2680x846, dynamic range=255
```
