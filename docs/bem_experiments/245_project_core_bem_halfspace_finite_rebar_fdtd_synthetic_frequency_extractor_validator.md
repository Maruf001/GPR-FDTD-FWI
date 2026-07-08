# BEM Experiment 245: Half-Space Finite-Rebar FDTD Synthetic Frequency Extractor Validator

Date: 2026-06-28

## Purpose

Validate the synthetic scalar frequency-extractor smoke from run `244`.

Run `244` showed that synthetic target/background time traces generated from
the BEM spectra can recover the selected scattered frequency bins. This run
checks the smoke from a downstream consumer perspective.

This is a CPU-only validator. It does not run real FDTD, compare real paired
files, implement full 3D Maxwell BEM, run inversion, launch GPU/HPC work, run
field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/245_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_validation_checks.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_FDTD_SYNTHETIC_FREQUENCY_EXTRACTOR_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  5
validation passes:                  5
blocking failures:                  0
validation ready:                   true
source extracted rows:              117
source max relative error:          2.1699084408491636e-13
synthetic extractor smoke ready:    true
real FDTD extraction ready:         false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The five checks confirm:

| Check | Outcome |
| --- | --- |
| Extracted shape matches the summary | Pass |
| Extraction error summaries match and stay below threshold | Pass |
| Design matrix is well conditioned | Pass |
| Synthetic smoke is ready while real extraction remains blocked | Pass |
| 3D, inversion, field transfer, GPU, and field FWI remain blocked | Pass |

## Interpretation

The synthetic scalar frequency-extractor smoke is internally consistent. Shape,
receiver error summaries, global error summaries, design conditioning, synthetic
readiness, and blocked real-extraction/downstream states all pass.

## Decision

Use run `245` as the consumer validator for the synthetic extractor smoke. The
next BEM step is a negative-control sensitivity run. Real FDTD extraction, real
comparison, 3D validation, inversion, field transfer, GPU/HPC readiness, and
field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_validator.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_validator.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_synthetic_frequency_extractor_validator.py: pass
```

Figure check:

```text
2357x821, dynamic range=255
```
