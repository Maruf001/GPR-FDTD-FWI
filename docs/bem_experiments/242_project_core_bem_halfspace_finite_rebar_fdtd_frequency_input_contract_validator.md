# BEM Experiment 242: Half-Space Finite-Rebar FDTD Frequency Input Contract Validator

Date: 2026-06-28

## Purpose

Validate the FDTD-side input contract from run `241`.

Run `241` defined the target/background time-trace schema and inherited
receiver/frequency keys needed before future FDTD traces can be converted into
the scalar BEM/FDTD comparison schema. This run checks that the contract is
internally consistent and still keeps extraction and comparison blocked.

This is a CPU-only validator. It does not run FDTD, extract frequency bins,
compare real paired files, implement full 3D Maxwell BEM, run inversion, launch
GPU/HPC work, run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/242_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_validation_checks.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_FDTD_FREQUENCY_INPUT_CONTRACT_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  6
validation passes:                  6
blocking failures:                  0
validation ready:                   true
source schema columns:              13
source receiver keys:               13
source frequency keys:              9
input contract ready:               true
scalar projection convention ready: false
complex extractor ready:            false
paired trace files present:         false
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The six checks confirm:

| Check | Outcome |
| --- | --- |
| Time-trace schema matches the contract | Pass |
| Receiver and frequency keys match the source BEM export | Pass |
| Requirement status counts are guarded | Pass |
| Source BEM export shape is preserved | Pass |
| Input contract is ready while extraction remains blocked | Pass |
| 3D, inversion, field transfer, GPU, and field FWI remain blocked | Pass |

## Interpretation

The FDTD input contract is internally consistent. Schema columns, inherited
receiver/frequency keys, requirement status counts, source BEM export shape, and
blocked extraction/downstream states agree with the run `241` summary.

## Decision

Use run `242` as the consumer validator for the FDTD input contract. The next
BEM step is a negative-control sensitivity run. Frequency extraction, real
comparison, 3D validation, inversion, field transfer, GPU/HPC readiness, and
field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_validator.py
6 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_validator.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_validator.py: pass
```

Figure check:

```text
2375x841, dynamic range=255
```
