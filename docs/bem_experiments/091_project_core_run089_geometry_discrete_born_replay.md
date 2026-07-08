# BEM Experiment 091: Project-Core Run089 Geometry Discrete Born Replay

Date: 2026-06-25

## Purpose

Replay a grid-aware first-order Born-style surrogate on the exact homogeneous
dielectric bridge geometry from run `089`.

Runs `089` and `090` showed that the continuous analytic cylinder reference
does not transfer to project-core FDTD scattering, and that simple alignment
does not repair the gap. This run asks whether the same target scattering is
explained when the surrogate uses project-core background fields at the actual
rasterized target cells.

This is CPU-only. It does not run GPU kernels, field FWI, 3D/HPC work, or
neural-network training.

## Output

```text
outputs/bem_experiments/091_project_core_run089_geometry_discrete_born_replay
```

Key artifacts:

```text
data/project_core_discrete_born_scattering_summary.json
data/project_core_discrete_born_scattering_variants.csv
data/project_core_discrete_born_scattering_frequency.csv
data/project_core_discrete_born_scattering_arrays.npz
figures/project_core_discrete_born_scattering_audit.png
docs/PROJECT_CORE_RUN089_GEOMETRY_DISCRETE_BORN_REPLAY.md
scripts/run_project_core_run089_geometry_discrete_born_replay.py
scripts/test_project_core_run089_geometry_discrete_born_replay.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scan positions:                         7
cylinder epsr:                          4.0
cylinder center:                        x=0.25 m, z=0.15 m
cylinder radius:                        0.03 m
target cell count:                      753
selected frequency bins:                17
legacy analytic-cylinder time L2:       1.5075838091082052
best Born variant:                      receiver_conjugate_div_source
best Born time symmetric L2:            0.5800814918790829
best Born spectral symmetric L2:        0.5800814918790828
best Born improves over legacy:         true
discrete Born scattering ready:         true
GPU required:                           false
field/archive evidence used:            false
```

Variant metrics:

| Variant | Time symmetric L2 | Improves over legacy |
| --- | ---: | --- |
| analytic_cylinder_direct_calibrated | 1.5075838091082052 | false |
| product_div_source | 0.5837605576794438 | true |
| product_no_div | 0.5837605576794438 | true |
| receiver_conjugate_div_source | 0.5800814918790829 | true |

## Interpretation

The run `089` geometry is recoverable when target scattering is represented on
the project grid. This confirms that the failed continuous analytic-cylinder
bridge and failed alignment replay are not evidence that project-core FDTD
target physics is unusable. They show that the continuous analytic/BEM target
representation must be translated into a project-grid-aware scattering
operator before promotion.

## Decision

Use run `091` as the current run-089-geometry positive scattering-operator
checkpoint. The next branch should translate this grid-aware operator into a
reusable BEM/project-core adapter rather than returning to direct-wave or
alignment calibration.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test used
for this result:

```text
scripts/run_project_core_run089_geometry_discrete_born_replay.py
scripts/test_project_core_run089_geometry_discrete_born_replay.py
```

The snapshot manifest SHA-256 entries match the frozen files.

## Validation

Focused tests:

```text
tests/test_project_core_run089_geometry_discrete_born_replay.py
2 passed
```

Figure check:

```text
project_core_discrete_born_scattering_audit.png  2533x716, dynamic range=255
```
