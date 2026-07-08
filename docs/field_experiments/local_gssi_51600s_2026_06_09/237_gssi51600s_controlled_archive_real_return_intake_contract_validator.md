# Field Experiment 237: Controlled Archive Real Return Intake Contract Validator

Date: 2026-06-28

## Purpose

Validate the run `236` real-return intake contract from a consumer perspective.

Run `236` joined the operator manifest, signoff contract, provenance closure
actions, and real-acceptance boundary. This validator checks that the file
rows, provenance rows, gate rows, and no-go states preserve the measured-data
requirements.

It does not contain real measured files, fill real signoff values, accept an
archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/237_gssi51600s_controlled_archive_real_return_intake_contract_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_return_intake_contract_validator_checks.csv
data/field_controlled_archive_real_return_intake_contract_validator_summary.json
figures/field_controlled_archive_real_return_intake_contract_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_INTAKE_CONTRACT_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_real_return_intake_contract_validator.py
scripts/test_gssi_field_controlled_archive_real_return_intake_contract_validator.py
```

## Result

```text
validation checks:                  5
validation passes:                  5
blocking failures:                  0
validation ready:                   true
source file rows:                   9
source gates:                       10
real files present:                 false
real signoff values present:        false
provenance acceptance ready:        false
checksum intake ready:              false
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

The validator checks:

| Check | Result |
| --- | --- |
| Contract summary counts are consistent | pass |
| File rows match real-return contract | pass |
| Provenance rows preserve closure actions | pass |
| Gate rows preserve real-acceptance blockers | pass |
| Real archive and downstream states blocked | pass |

## Interpretation

The real-return intake contract is internally consistent. File rows,
provenance closure actions, and gates preserve the measured-data requirements
while keeping real archive acceptance and downstream work blocked.

## Decision

Use run `237` as the positive validator for the real-return intake contract.
Sensitivity remains required before treating the contract as fully guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_return_intake_contract_validator.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_return_intake_contract_validator.png
2609x840, dynamic range=255
```
