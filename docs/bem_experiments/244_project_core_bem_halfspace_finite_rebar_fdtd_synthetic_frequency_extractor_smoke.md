# BEM Experiment 244: Half-Space Finite-Rebar FDTD Synthetic Frequency Extractor Smoke

Date: 2026-06-28

## Purpose

Smoke-test the scalar frequency-extraction mechanics on synthetic
target/background time traces generated from the BEM spectra.

Runs `241`-`243` guarded the FDTD-side input contract. This run checks whether
the intended sine/cosine least-squares extractor can recover selected complex
frequency bins from synthetic scalar time traces. The target trace is generated
from the BEM total spectrum, the background trace is generated from the BEM
background spectrum, and the recovered scattered spectrum is compared with the
BEM scattered spectrum.

This is a CPU-only synthetic smoke. It does not run real FDTD, compare real
paired files, implement full 3D Maxwell BEM, run inversion, launch GPU/HPC work,
run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/244_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_trace_arrays.npz
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_bins.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_receiver_errors.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_smoke_summary.json
figures/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_FDTD_SYNTHETIC_FREQUENCY_EXTRACTOR_SMOKE.md
scripts/script_snapshot_manifest.json
```

## Result

```text
receivers:                         13
frequencies:                       9
time samples:                      4096
dt:                                1e-11 s
trace duration:                    4.096e-08 s
extracted rows:                    117
receiver error rows:               13
design condition number:           1.050778890483821
max absolute error:                7.105427357601002e-13
max relative error:                2.1699084408491636e-13
synthetic extractor smoke ready:   true
real FDTD extraction ready:        false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU ready:                         false
field FWI ready:                   false
```

## Interpretation

The scalar frequency-extraction mechanics work on synthetic traces. Target and
background traces generated from the BEM spectra recover the scattered
frequency bins with near machine-precision error.

This validates extraction mechanics only. It does not validate real FDTD data,
full 3D electromagnetic modeling, or measured-field transfer.

## Decision

Use run `244` as a synthetic extractor smoke. The next BEM task can validate and
stress-test this smoke before any real FDTD extraction. Real FDTD extraction,
real BEM/FDTD comparison, 3D validation, inversion, field transfer, GPU/HPC
readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_smoke.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_smoke.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_smoke.py: pass
```

Figure check:

```text
2463x828, dynamic range=255
```
