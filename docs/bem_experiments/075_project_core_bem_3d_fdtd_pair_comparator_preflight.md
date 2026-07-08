# BEM Experiment 075: 3D FDTD Pair Comparator Preflight

Date: 2026-06-25

## Purpose

Define and preflight the expected FDTD frequency-bin output schema for a future
paired target/background comparison against the run `072` Bempp dipole-source
reference.

This is a no-launch, no-data artifact. It does not run 3D FDTD, field FWI,
GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/075_project_core_bem_3d_fdtd_pair_comparator_preflight
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_frequency_bin_schema.csv
data/project_core_bem_3d_fdtd_target_expected_frequency_bins.csv
data/project_core_bem_3d_fdtd_background_expected_frequency_bins.csv
data/project_core_bem_3d_fdtd_pair_comparator_preflight.csv
data/project_core_bem_3d_fdtd_pair_comparator_preflight_summary.json
figures/project_core_bem_3d_fdtd_pair_comparator_preflight.png
docs/PROJECT_CORE_BEM_3D_FDTD_PAIR_COMPARATOR_PREFLIGHT.md
```

## Result

```text
required schema columns:             12
preflight checks:                    22
passed checks:                       1
failed checks:                       21
target expected frequency rows:      124
background expected frequency rows:  124
target FDTD rows present:            0
background FDTD rows present:        0
comparison ready:                    false
3D validation claim ready:           false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

The one passing check is important: the run `073` manifests already pass the
run `074` manifest validator. The 21 failures are the expected no-data state:
target and background FDTD frequency-bin outputs do not exist yet.

Each future target/background output must provide 124 rows:

```text
31 receivers x 4 frequencies
```

Required frequency-bin columns:

```text
run_role
receiver_index
x_m
y_m
z_m
frequency_hz
field_ex_real
field_ex_imag
field_ey_real
field_ey_imag
field_ez_real
field_ez_imag
```

## Interpretation

The FDTD pair-comparison schema is now explicit. Current comparison remains
blocked because no paired FDTD target/background frequency-bin data exist.

## Decision

Use this preflight before any future BEM/FDTD comparison. Do not claim 3D
validation until both target and background FDTD outputs satisfy the schema and
subtraction gates.

## Validation

Figure check:

```text
2104x844, dynamic range=255
```
