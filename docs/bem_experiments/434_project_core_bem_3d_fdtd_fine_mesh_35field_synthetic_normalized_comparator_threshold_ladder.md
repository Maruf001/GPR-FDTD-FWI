# BEM Experiment 434: 35-Field Synthetic Normalized-Comparator Threshold Ladder

Date: 2026-06-29

## Purpose

Stress the guarded run `428` normalized-comparator score with controlled
synthetic perturbations around the configured residual tolerance.

This is a synthetic threshold-response audit. It does not use real returned
FDTD files, and it does not promote real BEM/FDTD comparison, 3D validation,
GPU/HPC work, field transfer, or field FWI.

## Output

```text
outputs/bem_experiments/434_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_perturbed_score_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder.png
```

## Result

```text
source score ready:                true
threshold ladder ready:            true
relative tolerance:                1e-12
scenarios:                         9
pass scenarios:                    5
fail scenarios:                    4
source score rows:                 279
perturbed score rows:              2511
pass rows:                         1395
fail rows:                         1116
max passing relative residual:     9.50339903422461e-13
min failing relative residual:     1.0501746923583452e-12
threshold gap:                     9.983478893588429e-14
first positive failing perturb.:   1.05e-12
first negative failing perturb.:  -1.05e-12
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The score behaves as intended around the threshold: near-tolerance
perturbations pass, while slightly-over-tolerance perturbations fail.

## Decision

Use this ladder as a synthetic comparator threshold contract for future
returned-packet scoring. Do not use it as real BEM/FDTD comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder.py
3 passed as part of the 10-test focused set
```

Figure check:

```text
3580x888, dynamic range=255
```
