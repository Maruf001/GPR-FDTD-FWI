# BEM Experiment 109: 3D Comparison Metadata Contract Addendum

Date: 2026-06-27

## Purpose

Convert the latest BEM-side mesh, source, and receiver sensitivity findings into
a strict metadata addendum for future paired 3D FDTD returns.

Runs `106`-`108` showed that the 3D comparison setup is sensitive to mesh,
source, and receiver conventions. This run asks the handoff question:

```text
Can the existing external-return metadata template prove that a returned FDTD
bundle used the exact BEM comparison conventions?
```

This run does not modify older request artifacts, install returned data, run
3D FDTD, or claim BEM/FDTD validation.

## Output

```text
outputs/bem_experiments/109_project_core_bem_3d_comparison_metadata_contract_addendum
```

Key artifacts:

```text
data/project_core_bem_3d_comparison_strict_metadata_addendum.csv
data/project_core_bem_3d_comparison_metadata_gap_audit.csv
data/project_core_bem_3d_comparison_sensitivity_basis.csv
data/project_core_bem_3d_comparison_metadata_contract_addendum_summary.json
figures/project_core_bem_3d_comparison_metadata_contract_addendum.png
docs/PROJECT_CORE_BEM_3D_COMPARISON_METADATA_CONTRACT_ADDENDUM.md
scripts/run_project_core_bem_3d_comparison_metadata_contract_addendum.py
scripts/test_project_core_bem_3d_comparison_metadata_contract_addendum.py
scripts/script_snapshot_manifest.json
```

## Result

```text
strict metadata fields:              13
existing return metadata fields:      12
fields needing addendum:              13
blocking fields needing addendum:     12
strict metadata contract ready:       true
return metadata template needs addendum: true
real BEM/FDTD comparison ready:       false
3D validation ready:                  false
layered 3D GPR ready:                 false
field FWI ready:                      false
GPU/HPC ready:                        false
```

The strict addendum requires:

| Metadata key | Required value |
| --- | --- |
| `source_model` | `electric_point_dipole_proxy` |
| `source_position_m` | `-0.04,0.0,0.09` |
| `source_dipole_moment` | `0.0,1.0,0.0` |
| `source_normalization` | `match Bempp run 072 arbitrary unit dipole before any amplitude claim` |
| `receiver_positions_sha256` | `b89ab6b166b42349a17a79ec84fd41b963e63c7dc590f39f32fb53838616c4da` |
| `receiver_count` | `31` |
| `receiver_span_y_m` | `0.16` |
| `receiver_height_z_m` | `0.09` |
| `receiver_coordinate_tolerance_m` | `<=1e-9 for returned frequency-bin receiver keys` |
| `frequency_bins_sha256` | `b603640b49c0db482bc6ed8c5b9f71e2ed9486b3bb66a0ef407238b22e7603b7` |
| `surface_mesh_baseline` | `Bempp finite cylinder axial_segments=6 radial_segments=16` |
| `target_geometry` | `PEC finite cylinder; axis=x; length_m=0.12; radius_m=0.01; center_m=0,0,0` |
| `background_epsr` | `6.0` |

## Interpretation

The existing external request artifacts contain much of the needed information:
the manifest has the source position and dipole moment, and the request pack
includes receiver positions and frequency bins. However, the return metadata
template does not require those strict fields as explicit returned metadata.

That is a real acceptance gap. A returned FDTD bundle could be structurally
complete but still fail to prove that source orientation, source position,
receiver height, receiver coordinates, and frequency keys match the BEM-side
comparison convention.

## Decision

Use this addendum as the next return-gate update before accepting real external
FDTD files for BEM comparison.

Do not claim real BEM/FDTD comparison or 3D validation until returned files
provide these metadata and pass the existing frequency-bin gates.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_comparison_metadata_contract_addendum.py
sha256: 87fa5eeb77206c1ad8e13f31aee0928dc019efc28592b93f62e3e3b8127dcfc2

test_project_core_bem_3d_comparison_metadata_contract_addendum.py
sha256: 79793b0de42f172b427f9b59a6c775b670d63705462b9a03ef01a56c37929b02
```

Subsequent external-return gate updates should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_comparison_metadata_contract_addendum.py
3 passed
```

Figure check:

```text
project_core_bem_3d_comparison_metadata_contract_addendum.png
2212x843, dynamic range=255
```
