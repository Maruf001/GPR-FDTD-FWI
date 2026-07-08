# BEM Experiment 081: 3D FDTD Frequency-Bin Extractor Smoke

Date: 2026-06-25

## Purpose

Implement a direct-DFT receiver-trace extractor and prove it on synthetic
target/background traces shaped by the run `080` contract.

This is CPU-only extractor smoke. It does not launch 3D FDTD, field FWI,
GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/081_project_core_bem_3d_fdtd_frequency_bin_extractor_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_frequency_bin_extractor_smoke_traces.csv
data/project_core_bem_3d_fdtd_frequency_bin_extractor_smoke_target_bins.csv
data/project_core_bem_3d_fdtd_frequency_bin_extractor_smoke_background_bins.csv
data/project_core_bem_3d_fdtd_frequency_bin_extractor_smoke_checks.csv
data/project_core_bem_3d_fdtd_frequency_bin_extractor_smoke_summary.json
figures/project_core_bem_3d_fdtd_frequency_bin_extractor_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_FREQUENCY_BIN_EXTRACTOR_SMOKE.md
```

## Result

```text
synthetic trace rows:                 7936
extracted target rows:                124
extracted background rows:            124
comparator checks:                    22
comparator failed checks:             0
extractor smoke pass:                 true
extractor implemented for contract:   true
real FDTD data ready:                 false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

## Interpretation

The run `080` trace-to-frequency-bin contract now has a working direct-DFT
implementation and synthetic pass-case. Synthetic target/background traces are
converted into run `077` frequency-bin rows, and the run `075` comparator
accepts them with zero failed checks.

This is still not real BEM/FDTD validation. Real 3D FDTD target/background
traces are absent.

## Decision

Use this extractor path for future imported 3D FDTD receiver traces. Keep real
comparison, 3D validation, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training blocked until target/background traces come from a real
3D FDTD engine and pass the same comparator.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_frequency_bin_extractor_smoke.py
2 passed
```

Figure check:

```text
1924x810, dynamic range=255
```
