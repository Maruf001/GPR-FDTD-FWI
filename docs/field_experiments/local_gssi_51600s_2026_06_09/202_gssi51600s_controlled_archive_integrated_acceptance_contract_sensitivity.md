# Field Experiment 202: Integrated Archive Acceptance Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `201` integrated archive acceptance contract validator with
damaged contract scenarios.

Run `201` validated the refreshed contract from run `200`. This run checks that
the validator fails when important contract pieces are damaged or when field FWI
is incorrectly marked ready.

This run does not ingest real field files, modify the pending archive, run field
FWI, launch GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/202_gssi51600s_controlled_archive_integrated_acceptance_contract_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_integrated_acceptance_contract_sensitivity_rows.csv
data/field_controlled_archive_integrated_acceptance_contract_sensitivity_summary.json
figures/field_controlled_archive_integrated_acceptance_contract_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_INTEGRATED_ACCEPTANCE_CONTRACT_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_integrated_acceptance_contract_sensitivity.py
scripts/test_gssi_field_controlled_archive_integrated_acceptance_contract_sensitivity.py
```

## Result

```text
scenarios:                          7
expected passes:                    1
observed passes:                    1
expected failures:                  6
observed failures:                  6
unexpected outcomes:                0
contract sensitivity ready:         true
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

| Scenario | Expected pass | Observed pass | Unexpected |
| --- | --- | --- | --- |
| exact_refreshed_contract | true | true | false |
| missing_dzt_signature_stage | false | false | false |
| wrong_dzt_slot_count | false | false | false |
| integrated_stage_marked_ready | false | false | false |
| missing_integrated_archive_stage | false | false | false |
| field_fwi_marked_ready | false | false | false |
| stage_count_mismatch | false | false | false |

## Interpretation

The integrated contract validator is sensitive to the important failure modes:
missing DZT signature stage, missing integrated archive stage, wrong DZT slot
count, false archive readiness, false field-FWI readiness, and summary/row count
drift.

The exact refreshed contract is still accepted.

## Decision

Keep run `200` as the current archive acceptance contract and run `201`/`202` as
its guards.

Real archive acceptance and field FWI remain blocked until real files pass the
integrated gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_validator.py
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_sensitivity.py
6 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_integrated_acceptance_contract_sensitivity.py: pass
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_sensitivity.py: pass
```

Figure check:

```text
2645x842, dynamic range=255
```
