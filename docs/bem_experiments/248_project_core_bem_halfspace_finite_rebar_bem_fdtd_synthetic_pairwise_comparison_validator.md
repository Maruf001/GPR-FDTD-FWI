# BEM Experiment 248: Half-Space Finite-Rebar BEM/FDTD Synthetic Pairwise Comparison Validator

Date: 2026-06-28

## Purpose

Validate the run `247` synthetic pairwise comparison from a consumer
perspective.

This run checks whether the synthetic comparison artifact can be safely read as
a mechanics validation while still blocking real BEM/FDTD agreement, 3D
validation, inversion-scale use, field transfer, GPU/HPC readiness, and field
FWI.

This is CPU-only validation. It does not run real FDTD, compare real paired
FDTD files, implement full 3D Maxwell BEM, launch GPU/HPC work, run field FWI,
or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/248_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_FDTD_SYNTHETIC_PAIRWISE_COMPARISON_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator.py
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
validation ready:                          true
source paired keys:                        117
source frequency peak rows:                9
source max scattered relative error:       2.1699084408491636e-13
source normalized L2 error:                2.459587752743292e-15
synthetic pairwise comparison ready:        true
real FDTD frequency extraction ready:       false
real BEM/FDTD comparison ready:            false
ready for 3D validation:                   false
inversion-scale half-space ready:          false
field transfer ready:                      false
ready for GPU work:                        false
field FWI ready:                           false
```

The six checks validate:

| Check group | Outcome |
| --- | --- |
| Source readiness | BEM exporter and synthetic extractor are ready |
| Key completeness | 117 paired keys, no missing keys, no duplicate keys |
| Complex residuals | finite values, max relative error and normalized L2 error below `1e-8` |
| Peak locations | 9 frequency rows, 13 receivers each, zero peak-location error |
| Metric boundary | key/residual/peak metrics ready, phase-reference metric still blocked |
| Claim boundary | synthetic comparison ready, real comparison and downstream states false |

## Interpretation

The synthetic pairwise comparison smoke is internally consistent. It confirms
that the comparison plumbing created in run `247` has the expected shape,
residual behavior, peak-location accounting, and claim boundary.

This validation does not change the scientific claim boundary. The comparison
is still synthetic because the FDTD-like bins came from traces generated from
the BEM spectra.

## Decision

Use run `248` as the consumer validator for the synthetic pairwise comparison
smoke. Sensitivity remains required before treating the pairwise comparison
guard as robust.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator.py
7 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_validator.png
2537x841, dynamic range=255
```
