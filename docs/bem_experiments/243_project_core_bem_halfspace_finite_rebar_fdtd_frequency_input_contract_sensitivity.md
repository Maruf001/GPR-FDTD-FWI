# BEM Experiment 243: Half-Space Finite-Rebar FDTD Frequency Input Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the FDTD-side input-contract validator from run `242`.

Run `242` validated the run `241` input contract. This run checks whether the
validator rejects controlled damage to schema columns, receiver/frequency keys,
requirements, source BEM shape, extraction readiness, and downstream decision
flags.

This is a CPU-only sensitivity run. It does not run FDTD, extract frequency
bins, compare real paired files, implement full 3D Maxwell BEM, run inversion,
launch GPU/HPC work, run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/243_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_FDTD_FREQUENCY_INPUT_CONTRACT_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         25
expected pass scenarios:           1
expected failure scenarios:        24
observed pass scenarios:           1
observed failure scenarios:        24
unexpected outcomes:               0
sensitivity ready:                 true
input contract guarded:            true
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The exact run `241` input contract passes. The damaged scenarios fail as
expected for:

| Damage family | Validator response |
| --- | --- |
| Time-trace schema count, required flag, or column-name drift | Rejected |
| Receiver or frequency key count/required drift | Rejected |
| Requirement count/status drift | Rejected |
| Extraction-blocker accounting drift | Rejected |
| Source BEM export shape drift | Rejected |
| False input-contract, projection, extractor, trace-file, FDTD-extraction, real-comparison, 3D, inversion, field, GPU, or field-FWI promotion | Rejected |

## Interpretation

The FDTD input-contract validator accepts the exact run `241` contract and
rejects controlled damage to schema columns, receiver/frequency keys,
requirement counts, status counts, extraction-blocker accounting, source BEM
shape, input-contract readiness, extraction readiness, and downstream promotion
flags.

## Decision

Use runs `241`-`243` as the guarded FDTD input-contract package for the scalar
comparison path. The next BEM task can define the scalar projection convention
or implement a synthetic extractor smoke. Real FDTD extraction, real comparison,
3D validation, inversion, field transfer, GPU/HPC readiness, and field FWI
remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_sensitivity.py
7 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_sensitivity.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_sensitivity.py: pass
```

Figure check:

```text
3419x890, dynamic range=255
```
