# BEM Experiment 118: Fine-Mesh Comparator Synthetic Sensitivity

Date: 2026-06-27

## Purpose

Use the run `117` fine-mesh BEM reference export to synthesize target/background
FDTD-style returns and test whether the nine-bin comparison path behaves
sensibly before real external FDTD files arrive.

This run does not launch FDTD, install real returned files, perform real
BEM/FDTD comparison, make a 3D validation claim, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/118_project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_synthetic_target_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_synthetic_background_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_metric_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_frequency_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_scenario_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_validation_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_COMPARATOR_SYNTHETIC_SENSITIVITY.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenario count:                         3
frequency count:                        9
receiver count:                         31
rows per scenario:                      279
synthetic target rows:                  837
synthetic background rows:              837
validation checks:                      54
validation failed checks:               0
scenario pass count:                    2
scenario fail count:                    1
pass threshold relative L2:             0.1
exact reconstruction max relative L2:   8.942279382796571e-15
small-error max relative L2:            0.0500000000000035
bad-error max relative L2:              0.30000000000000254
synthetic sensitivity behaves expected: true
real FDTD data ready:                   false
comparison ready on real data:          false
3D validation claim ready:              false
```

Scenario summary:

| Scenario | Rows | Max relative L2 | Mean relative L2 | Passes threshold |
| --- | ---: | ---: | ---: | --- |
| bad_scattered_scale_error | 279 | 0.30000000000000254 | 0.30000000000000016 | false |
| exact_reconstruction | 279 | 8.942279382796571e-15 | 9.140164716141724e-16 | true |
| small_scattered_scale_error | 279 | 0.0500000000000035 | 0.05000000000000003 | true |

## Interpretation

The current nine-bin comparison path behaves correctly on synthetic
target/background returns generated from the BEM reference:

- exact reconstruction gives effectively zero error,
- a five percent scattered-field scale error remains below the provisional
  ten percent comparison line,
- a thirty percent scattered-field scale error fails.

This verifies comparator sensitivity around the current BEM reference payload.
It is still synthetic and does not validate the BEM model against real 3D FDTD.

## Decision

Use this run as the end-to-end synthetic sensitivity smoke for the preferred
nine-bin BEM/FDTD comparison path.

Keep real comparison, 3D validation, layered 3D GPR claims, field FWI, heavy
GPU work, field 3D/HPC, and neural-network training blocked until external FDTD
target/background files pass the real import, metadata, and comparison gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.py
sha256: 5a85a9b4e7f6f0ee01f2ceb412cfa9daaa05a2bc0e7293d6ca9f8a781297a444

test_project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.py
sha256: e9124e499285b88695c66249505df8226c5ae15cd61e37df6e6ec02d52fe337f
```

Subsequent related BEM/FDTD comparison experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.png
2680x851, dynamic range=255
```
