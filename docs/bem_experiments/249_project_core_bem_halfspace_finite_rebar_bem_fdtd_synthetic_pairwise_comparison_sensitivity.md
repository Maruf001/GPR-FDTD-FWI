# BEM Experiment 249: Half-Space Finite-Rebar BEM/FDTD Synthetic Pairwise Comparison Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `248` synthetic pairwise comparison validator against
controlled damage cases.

This run checks whether the validator accepts only the exact synthetic
comparison and rejects common key, residual, peak-location, metric-readiness,
and downstream-promotion failures.

This is CPU-only sensitivity validation. It does not run real FDTD, compare
real paired FDTD files, implement full 3D Maxwell BEM, launch GPU/HPC work, run
field FWI, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/249_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_FDTD_SYNTHETIC_PAIRWISE_COMPARISON_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity.py
```

## Result

```text
scenarios:                                  31
expected pass scenarios:                    1
expected failure scenarios:                 30
observed pass scenarios:                    1
observed failure scenarios:                 30
unexpected outcomes:                        0
sensitivity ready:                          true
synthetic pairwise comparison ready:         true
real FDTD frequency extraction ready:        false
real BEM/FDTD comparison ready:             false
ready for 3D validation:                    false
inversion-scale half-space ready:           false
field transfer ready:                       false
ready for GPU work:                         false
field FWI ready:                            false
```

The exact synthetic comparison passes. The 30 damaged variants fail as
expected:

| Damage family | Examples |
| --- | --- |
| Source readiness drift | BEM exporter or synthetic extractor marked not ready |
| Key drift | paired-key count drift, missing keys, duplicate BEM/FDTD keys |
| Residual drift | nonfinite pairwise residual, high max relative error, high normalized L2 error |
| Metric-readiness drift | complex residual not ready, normalized L2 not reported, phase reference marked ready |
| Peak-location drift | peak row count drift, missing peak row, wrong receiver count, nonzero peak x/index error |
| Downstream promotion | real FDTD extraction, real comparison, 3D, inversion, field transfer, GPU, or field FWI marked ready |

## Interpretation

The synthetic pairwise comparison validator now has guarded sensitivity
coverage. It accepts the exact comparison and rejects controlled corruption of
the key mapping, residual metrics, scan peak-location metrics, metric boundary,
and claim boundary.

This completes a guarded synthetic comparison package. It still does not prove
real BEM/FDTD agreement because no real FDTD traces have been used.

## Decision

Use runs `247-249` as the guarded synthetic BEM/FDTD pairwise comparison
package. Real FDTD extraction, real BEM/FDTD comparison, 3D validation,
inversion-scale use, field transfer, GPU/HPC readiness, and field FWI remain
blocked until real paired FDTD traces are available and pass the same guarded
checks.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity.py
7 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_sensitivity.png
3617x890, dynamic range=255
```
