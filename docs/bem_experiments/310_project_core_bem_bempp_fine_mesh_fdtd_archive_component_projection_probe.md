# BEM Experiment 310: Bempp Fine-Mesh FDTD Archive Component Projection Probe

Date: 2026-06-28

## Purpose

Test whether projecting the 3D Bempp reference onto individual field
components repairs the run `309` proxy-comparator mismatch.

This run uses saved artifacts only. It does not run FDTD, run a new BEM solve,
calibrate amplitude agreement, accept run `293` evidence, validate 3D physics,
transfer to field evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/310_project_core_bem_bempp_fine_mesh_fdtd_archive_component_projection_probe
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_component_projection_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_component_projection_model_summary.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_component_projection_probe_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_component_projection_probe.png
scripts/script_snapshot_manifest.json
```

## Result

```text
projection models:                    7
frequency-model rows:                 63
baseline model:                       vector_norm_amplitude
baseline pass count:                  7 / 9
baseline mean fit L2:                 0.138495
best model:                           vector_norm_amplitude
best model pass count:                7 / 9
best model mean fit L2:               0.138495
best component model:                 ey_magnitude
best component pass count:            5 / 9
best component mean fit L2:           0.156554
best complex-model pass count:        0 / 9
component projection improves base:   false
component projection repair ready:    false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
field FWI ready:                      false
```

Model summary:

| Rank | Model | Pass count | Mean fit L2 | Max fit L2 | Failure frequencies GHz |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | vector_norm_amplitude | 7 | 0.1385 | 0.3700 | 0.4; 3 |
| 2 | ey_magnitude | 5 | 0.1566 | 0.3622 | 0.4; 1.25; 1.5; 2 |
| 3 | ez_magnitude | 0 | 0.5060 | 0.6124 | all |
| 4 | ex_magnitude | 0 | 0.5430 | 0.6501 | all |
| 5 | ey_complex | 0 | 0.8230 | 0.9705 | all |
| 6 | ez_complex | 0 | 0.9887 | 0.9996 | all |
| 7 | ex_complex | 0 | 0.9890 | 0.9999 | all |

## Interpretation

The individual-component projection does not repair the proxy-comparator
mismatch. The existing vector-norm amplitude comparison remains the best
projection with seven of nine frequencies under the diagnostic marker. The
closest component-only model is `Ey` magnitude with five of nine frequencies
under the marker. Complex component fits do not pass any frequency, which
points away from a simple phase-aware component-selection fix.

## Decision

Keep the component-projection repair blocked. The next useful BEM branch is a
source/operator diagnostic, not a calibrated BEM/FDTD agreement claim. Real
BEM/FDTD comparison, 3D validation, field transfer, GPU/HPC readiness, and
field FWI remain blocked.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_component_projection_probe.py
3 passed
```

Figure validation:

```text
2951x1486, dynamic range=255
```
