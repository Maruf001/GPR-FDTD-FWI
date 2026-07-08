# BEM Experiment 246: Half-Space Finite-Rebar FDTD Synthetic Frequency Extractor Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the synthetic scalar frequency-extractor validator from run `245`.

Run `245` validated the synthetic extractor smoke from run `244`. This run
checks whether the validator rejects controlled damage to extracted shape, error
summaries, conditioning, readiness flags, and downstream decision flags.

This is a CPU-only sensitivity run. It does not run real FDTD, compare real
paired files, implement full 3D Maxwell BEM, run inversion, launch GPU/HPC work,
run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/246_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_FDTD_SYNTHETIC_FREQUENCY_EXTRACTOR_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected failure scenarios:        17
observed pass scenarios:           1
observed failure scenarios:        17
unexpected outcomes:               0
sensitivity ready:                 true
synthetic extractor guarded:       true
real FDTD extraction ready:        false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU ready:                         false
field FWI ready:                   false
```

The exact run `244` smoke passes. The damaged scenarios fail as expected for:

| Damage family | Validator response |
| --- | --- |
| Extracted row shape drift | Rejected |
| Receiver-error summary drift | Rejected |
| Global error-summary drift | Rejected |
| Excessive extraction error | Rejected |
| Poor design-matrix conditioning | Rejected |
| Source guard or synthetic-readiness drift | Rejected |
| False real FDTD extraction, real-comparison, 3D, inversion, field, GPU, or field-FWI promotion | Rejected |

## Interpretation

The synthetic frequency-extractor validator accepts the exact run `244` smoke
and rejects controlled damage to extracted shape, receiver-error summaries,
global error summaries, conditioning, source guard, synthetic readiness, real
extraction readiness, and downstream promotion flags.

## Decision

Use runs `244`-`246` as the guarded synthetic frequency-extractor package. Real
FDTD extraction, real comparison, 3D validation, inversion, field transfer,
GPU/HPC readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_sensitivity.py
7 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_sensitivity.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_sensitivity.py: pass
```

Figure check:

```text
3041x894, dynamic range=255
```
