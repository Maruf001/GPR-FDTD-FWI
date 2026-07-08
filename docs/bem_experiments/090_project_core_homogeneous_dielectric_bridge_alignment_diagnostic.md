# BEM Experiment 090: Project-Core Homogeneous Dielectric Bridge Alignment Diagnostic

Date: 2026-06-25

## Purpose

Replay the frozen arrays from run `089` and test whether the failed homogeneous
dielectric bridge is only a trivial alignment problem.

This run does not rerun FDTD or BEM. It tests simple transformations of the
calibrated analytic scattered response against project-core FDTD:

```text
global real scale
sign flip
global time shift
global time shift plus real scale
tracewise real scale
tracewise time shift plus real scale
global complex residual scale
per-frequency complex scale
```

This is CPU-only replay. It does not run GPU kernels, field FWI, 3D/HPC work,
or neural-network training.

## Output

```text
outputs/bem_experiments/090_project_core_homogeneous_dielectric_bridge_alignment_diagnostic
```

Key artifacts:

```text
data/project_core_homogeneous_dielectric_alignment_candidates.csv
data/project_core_homogeneous_dielectric_per_frequency_scales.csv
data/project_core_homogeneous_dielectric_alignment_arrays.npz
data/project_core_homogeneous_dielectric_bridge_alignment_diagnostic_summary.json
figures/project_core_homogeneous_dielectric_alignment_summary.png
figures/project_core_homogeneous_dielectric_best_mid_trace.png
docs/PROJECT_CORE_HOMOGENEOUS_DIELECTRIC_BRIDGE_ALIGNMENT_DIAGNOSTIC.md
scripts/run_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py
scripts/test_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py
scripts/script_snapshot_manifest.json
```

## Result

```text
alignment candidates:                  9
direct calibrated symmetric L2:         1.5075838091082052
best candidate:                         per_frequency_complex_scale
best candidate symmetric L2:            1.0629842444792676
best simple candidate:                  global_time_shift
best simple symmetric L2:               1.4749859059106778
closed by global/simple alignment:      false
closed by per-frequency scale:          false
homogeneous bridge promotable:          false
half-space rung ready:                  false
outputs/experiments promotion ready:    false
GPU work ready:                         false
field transfer ready:                   false
```

Alignment ranking:

| Rank | Candidate | Family | Symmetric L2 |
| ---: | --- | --- | ---: |
| 1 | per_frequency_complex_scale | complex_scale | 1.0629842444792676 |
| 2 | global_time_shift | global_simple | 1.4749859059106778 |
| 3 | direct_calibrated | baseline | 1.5075838091082052 |
| 4 | sign_flip | global_simple | 1.523832229258722 |
| 5 | tracewise_time_shift_real_scale | tracewise_simple | 1.7163968540350487 |
| 6 | global_complex_residual_scale | complex_scale | 1.8051886745925085 |
| 7 | tracewise_real_scale | tracewise_simple | 1.8180164563790593 |
| 8 | global_time_shift_real_scale | global_simple | 1.8502101997140405 |
| 9 | global_real_scale | global_simple | 1.9712759130210395 |

## Interpretation

The run `089` bridge failure is not explained by sign, scalar amplitude,
global delay, tracewise delay, or tracewise amplitude. Even per-frequency
complex scaling only improves the symmetric time-domain L2 to about `1.063`,
which remains above the `0.75` gate.

This points to frequency/spatial scattered-field structure, not only source
spectrum or timing. The next useful BEM/project-core work should target
grid-aware scattering and finite-domain source/field conventions, not
half-space promotion.

## Decision

Do not advance the project-core bridge to the half-space rung. Treat run `090`
as evidence that simple replay alignment cannot close the homogeneous
dielectric bridge. The next branch should be a narrow grid-aware scattering
diagnostic.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test used
for this result:

```text
scripts/run_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py
scripts/test_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py
```

The snapshot manifest SHA-256 entries match the frozen files.

## Validation

Focused tests:

```text
tests/test_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py
3 passed
```

Figure checks:

```text
project_core_homogeneous_dielectric_alignment_summary.png   2050x851, dynamic range=255
project_core_homogeneous_dielectric_best_mid_trace.png      1312x718, dynamic range=255
```
