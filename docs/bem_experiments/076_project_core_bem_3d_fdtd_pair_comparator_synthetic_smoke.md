# BEM Experiment 076: 3D FDTD Pair Comparator Synthetic Smoke

Date: 2026-06-25

## Purpose

Create synthetic target/background frequency-bin rows from the run `072` Bempp
receiver table and feed them through the run `075` comparator schema.

This is a schema smoke test. It is not real 3D FDTD validation and does not run
3D FDTD, field FWI, GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/076_project_core_bem_3d_fdtd_pair_comparator_synthetic_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_synthetic_target_frequency_bins.csv
data/project_core_bem_3d_fdtd_synthetic_background_frequency_bins.csv
data/project_core_bem_3d_fdtd_synthetic_scattered_recovery.csv
data/project_core_bem_3d_fdtd_pair_comparator_synthetic_smoke.csv
data/project_core_bem_3d_fdtd_pair_comparator_synthetic_smoke_summary.json
figures/project_core_bem_3d_fdtd_pair_comparator_synthetic_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_PAIR_COMPARATOR_SYNTHETIC_SMOKE.md
```

## Result

```text
target synthetic rows:               124
background synthetic rows:           124
comparator checks:                   22
comparator failed checks:            0
max scattered recovery error:        3.694567826668716e-12
synthetic comparator pass:           true
real FDTD data ready:                false
3D validation claim ready:           false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

## Interpretation

The comparator schema can pass when target/background rows are complete and
keyed correctly. This is only a synthetic construction from the Bempp table; it
does not create or validate real FDTD data.

## Decision

Keep run `076` as a schema smoke test. Real 3D validation remains blocked until
actual paired FDTD target/background outputs satisfy the same comparator.

## Validation

Figure check:

```text
2104x845, dynamic range=255
```
