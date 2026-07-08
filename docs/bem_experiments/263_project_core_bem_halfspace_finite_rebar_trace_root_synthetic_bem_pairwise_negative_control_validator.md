# BEM Experiment 263: Half-Space Finite-Rebar Trace-Root Synthetic BEM Pairwise Negative-Control Validator

Date: 2026-06-28

## Purpose

Validate run `262` from a consumer perspective.

Run `262` showed that the synthetic trace-root frequency bins pair cleanly with
the BEM scattered-spectrum keys, but the paired values strongly disagree. This
validator checks whether that no-go decision is internally consistent and
properly bounded.

It does not run real FDTD, ingest real trace files, claim BEM/FDTD agreement,
launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/263_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validation_checks.csv
data/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_TRACE_ROOT_SYNTHETIC_BEM_PAIRWISE_NEGATIVE_CONTROL_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validator.py
```

## Result

```text
validation checks:                    5
validation passes:                    5
blocking failures:                    0
validation ready:                     true
source paired keys:                   117
source frequency rows:                9
source normalized L2 error:           1.0000000672667073
source max scattered relative error:  1.000208702121816
synthetic BEM/FDTD agreement ready:   false
real BEM/FDTD comparison ready:       false
```

The validator checks:

| Check | Result |
| --- | --- |
| Source audit readiness flags are valid | pass |
| Pairwise keys are complete, unique, and finite | pass |
| Frequency summary matches pairwise rows | pass |
| Negative-control mismatch is recomputed | pass |
| Agreement and downstream claims remain blocked | pass |

## Interpretation

The run `262` negative-control comparison is internally consistent. All 117
receiver-frequency pairs are complete and finite, the nine frequency summaries
reproduce the pairwise rows, and the recomputed mismatch remains a no-go for
agreement.

The important result is not that BEM and FDTD agree. They do not. The result is
that the synthetic trace-root table is correctly prevented from becoming
agreement evidence.

## Decision

Use run `263` as the consumer-side validator for the negative-control boundary.
Synthetic trace-root bins remain plumbing evidence only until real FDTD traces
and a real paired BEM/FDTD comparison are available.

Sensitivity coverage remains required before treating this negative-control
boundary as fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validator.py
6 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_validator.png
2573x840, dynamic range=255
```
