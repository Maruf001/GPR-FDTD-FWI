# Field Experiment 640: First-Return Acceptance Rerun Decision Gate

Date: 2026-07-02

## Purpose

Convert the run `637-639` live-state refresh block into an explicit decision
gate for whether the first-return acceptance gate should be rerun.

This run does not accept measured field evidence. It records whether all
expected files and preliminary receipt observations are present before a
future acceptance-gate rerun is authorized.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/640_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate
```

## Result

```text
source refresh ready:                  true
source validator ready:                true
source sensitivity ready:              true
receipt rows:                          18
unique measured pairs:                 9
DZT receipt rows:                      9
metadata receipt rows:                 9
live files found:                      0
missing files:                         18
observed SHA-256 values:               0
observed file-size values:             0
metadata JSON parseable files:         0
DZT signature candidates:              0
ready for acceptance-gate rerun:       0
accepted field-evidence rows:          0
decision checks:                       6
required decision checks:              5
passed required decision checks:       3
blocking decision checks:              2
blocking decisions:                    all_expected_live_files_observed; receipt_observations_complete
acceptance-gate rerun needed:          false
acceptance-gate rerun authorized now:  false
next required action:                  place_all_18_expected_first_return_files_and_populate_receipt_observations
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The receipt structure is ready, but the actual first-return files and receipt
observations are still absent. The two active blockers are complete live-file
presence and completed preliminary receipt observations.

## Decision

Do not rerun the first-return acceptance gate yet. Keep controlled field
evidence, field FWI, and field 3D/HPC blocked until all 18 expected files are
present and the receipt has hashes, sizes, parseable metadata JSON files, and
DZT signature candidates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh_validation_sensitivity.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validation_sensitivity.py
24 passed
```

Figure check:

```text
3221x874, dynamic range=255
```
