# BEM Experiment 236: Half-Space Finite-Rebar BEM/FDTD Comparison Contract Validator

Date: 2026-06-28

## Purpose

Validate the matched scalar BEM/FDTD comparison contract from run `235`.

Run `235` defined the schema and requirements for a future comparison. This run
checks that the contract is internally consistent and still keeps execution and
claim states blocked.

This is a CPU-only validator. It does not run FDTD, compare real paired files,
implement full 3D Maxwell BEM, run inversion, launch GPU/HPC work, run field
FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/236_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_comparison_contract_validation_checks.csv
data/project_core_bem_halfspace_finite_rebar_comparison_contract_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_FDTD_COMPARISON_CONTRACT_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
validation passes:                  7
blocking failures:                  0
validation ready:                   true
source requirements:                14
source schema columns:              31
source metrics:                     6
BEM exporter ready:                 false
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The seven checks confirm:

| Check | Outcome |
| --- | --- |
| Contract counts match the run `235` summary | Pass |
| Requirement status counts are guarded | Pass |
| Schema columns are complete and required | Pass |
| Acceptance metric readiness is explicit | Pass |
| Source shape and one-candidate cost floor are preserved | Pass |
| Contract is ready while execution remains blocked | Pass |
| Inversion, field transfer, GPU, and field FWI remain blocked | Pass |

## Interpretation

The matched scalar BEM/FDTD comparison contract is internally consistent.
Counts, schema columns, acceptance-metric readiness, source shape, and blocked
execution states agree with the run `235` summary.

## Decision

Use run `236` as the consumer validator for the comparison contract. The next
BEM step is a negative-control sensitivity run against this validator. Do not
claim real BEM/FDTD agreement, 3D validation, inversion, field transfer,
GPU/HPC readiness, or field FWI from the validator alone.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_validator.py
6 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_validator.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_validator.py: pass
```

Figure check:

```text
2465x840, dynamic range=255
```
