# BEM Experiment 237: Half-Space Finite-Rebar BEM/FDTD Comparison Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `236` matched scalar BEM/FDTD comparison-contract
validator.

Run `236` validated the comparison contract from run `235`. This run checks
whether the validator rejects controlled damage to the contract.

This is a CPU-only sensitivity run. It does not run FDTD, compare real paired
files, implement full 3D Maxwell BEM, run inversion, launch GPU/HPC work, run
field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/237_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_comparison_contract_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_comparison_contract_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_FDTD_COMPARISON_CONTRACT_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         22
expected pass scenarios:           1
expected failure scenarios:        21
observed pass scenarios:           1
observed failure scenarios:        21
unexpected outcomes:               0
sensitivity ready:                 true
contract guarded:                  true
BEM exporter ready:                 false
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The exact run `235` contract passes. The damaged scenarios fail as expected for:

| Damage family | Validator response |
| --- | --- |
| Requirement-count and requirement-status drift | Rejected |
| Blocking-flag drift | Rejected |
| Schema-count, schema-required, and schema-name drift | Rejected |
| Metric-count and metric-readiness drift | Rejected |
| Source shape or cost-floor drift | Rejected |
| Contract-readiness drift | Rejected |
| False exporter, extractor, real-comparison, 3D, inversion, field, GPU, or field-FWI promotion | Rejected |

## Interpretation

The comparison-contract validator accepts the exact run `235` contract and
rejects controlled damage to requirement counts, status counts, blocking flags,
schema completeness, metric readiness, source shape, cost floor, contract
readiness, and downstream promotion flags.

## Decision

Use runs `235`-`237` as the guarded scalar BEM/FDTD comparison-contract package.
Implementation can proceed toward a BEM exporter. Real comparison, 3D
validation, inversion, field transfer, GPU/HPC readiness, and field FWI remain
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_sensitivity.py
7 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_sensitivity.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_sensitivity.py: pass
```

Figure check:

```text
3347x891, dynamic range=255
```
