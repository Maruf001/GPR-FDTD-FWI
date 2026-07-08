# Field Experiment 238: Controlled Archive Real Return Intake Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `237` real-return intake contract validator.

Run `237` validated the run `236` contract under the exact expected state. This
run checks whether the validator fails closed when counts, file rows,
provenance rows, gate rows, required blockers, or downstream readiness states
are damaged.

It does not contain real measured files, fill real signoff values, accept an
archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/238_gssi51600s_controlled_archive_real_return_intake_contract_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_return_intake_contract_sensitivity_scenarios.csv
data/field_controlled_archive_real_return_intake_contract_sensitivity_summary.json
figures/field_controlled_archive_real_return_intake_contract_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_INTAKE_CONTRACT_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_real_return_intake_contract_sensitivity.py
scripts/test_gssi_field_controlled_archive_real_return_intake_contract_sensitivity.py
```

## Result

```text
scenarios:                         32
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:        31
observed failure scenarios:        31
unexpected outcomes:                0
sensitivity ready:                  true
real files present:                 false
real signoff values present:        false
provenance acceptance ready:        false
checksum intake ready:              false
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

The exact run `236` contract passes. Thirty-one damaged variants fail as
expected, including count drift, missing file/provenance/gate rows, file role
drift, signoff/check drift, DZT guard drift, premature file/provenance
readiness, missing real blockers, and false archive/downstream readiness.

## Interpretation

The real-return intake contract is now guarded from the current consumer side.
It remains an intake shape, not accepted field evidence.

## Decision

Use runs `236-238` as the guarded real-return intake contract. Real measured
files and measured signoff/provenance values remain required before archive
acceptance can be tested.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_return_intake_contract_sensitivity.py
6 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_return_intake_contract_sensitivity.png
3581x888, dynamic range=255
```
