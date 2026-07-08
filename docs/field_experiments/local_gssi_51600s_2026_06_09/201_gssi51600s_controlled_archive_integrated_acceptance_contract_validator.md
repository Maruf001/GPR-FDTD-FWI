# Field Experiment 201: Integrated Archive Acceptance Contract Validator

Date: 2026-06-28

## Purpose

Validate the refreshed integrated archive acceptance contract from run `200`.

This run checks that downstream consumers can rely on the new contract: the DZT
signature preflight stage is present, the integrated archive preflight stage is
present, current candidates remain blocked, and field FWI remains blocked.

This run does not ingest real field files, modify the pending archive, run field
FWI, launch GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/201_gssi51600s_controlled_archive_integrated_acceptance_contract_validator
```

Key artifacts:

```text
data/field_controlled_archive_integrated_acceptance_contract_validation_checks.csv
data/field_controlled_archive_integrated_acceptance_contract_validator_summary.json
figures/field_controlled_archive_integrated_acceptance_contract_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_INTEGRATED_ACCEPTANCE_CONTRACT_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_integrated_acceptance_contract_validator.py
scripts/test_gssi_field_controlled_archive_integrated_acceptance_contract_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
source refreshed contract stages:   10
source integrated-ready candidates: 0
contract validation ready:          true
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

| Check | Expected | Observed | Passes |
| --- | --- | --- | --- |
| refreshed_stage_count_matches_summary | 10 | 10 | true |
| dzt_signature_preflight_present | true | true | true |
| integrated_archive_preflight_present | true | true | true |
| dzt_signature_stage_requires_nine_slots | 9 | 9 | true |
| integrated_stage_blocks_current_candidates | false | false | true |
| false_ready_prevention_recorded | 1 | 1 | true |
| no_integrated_ready_candidates | 0 | 0 | true |
| field_fwi_remains_blocked | false | false | true |

## Interpretation

The refreshed contract is internally consistent and ready to use as the current
field archive gate.

The validation does not accept the current or pending archive. It only confirms
that the new gate correctly requires both DZT signature preflight and integrated
archive preflight before checksum/intake can proceed.

## Decision

Use run `200` as the current controlled archive acceptance contract.

Keep checksum/intake, controlled evidence, field FWI, GPU work, and field 3D/HPC
blocked until a real archive passes the integrated gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_refresh.py
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_validator.py
6 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_integrated_acceptance_contract_validator.py: pass
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_validator.py: pass
```

Figure check:

```text
2537x822, dynamic range=255
```
