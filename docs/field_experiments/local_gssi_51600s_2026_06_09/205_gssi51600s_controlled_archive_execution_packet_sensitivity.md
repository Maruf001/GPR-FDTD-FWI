# Field Experiment 205: Controlled Archive Execution Packet Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `204` execution packet validator with damaged packet
variants.

Run `204` showed that the exact run `203` packet is consumer-ready. This run
checks the negative-control side: damaged packets should fail.

This run does not ingest real field files, modify the pending archive, run field
FWI, launch GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/205_gssi51600s_controlled_archive_execution_packet_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_execution_packet_sensitivity_scenarios.csv
data/field_controlled_archive_execution_packet_sensitivity_summary.json
figures/field_controlled_archive_execution_packet_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_PACKET_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_execution_packet_sensitivity.py
scripts/test_gssi_field_controlled_archive_execution_packet_sensitivity.py
```

## Result

```text
scenarios:                         10
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        9
observed failure scenarios:        9
unexpected outcomes:               0
sensitivity ready:                 true
real archive acceptance ready:     false
field FWI ready:                   false
3D/HPC ready:                      false
```

| Scenario | Expected pass | Observed pass | Failed checks |
| --- | --- | --- | --- |
| exact_execution_packet | true | true | none |
| missing_file_slot | false | false | file_slot_count_matches_summary; role_counts_match_expected_three_each; all_slots_require_dzt_signature; all_slots_carry_matching_dzt_guard; all_slots_pending_real_files |
| wrong_role_count | false | false | role_counts_match_expected_three_each |
| missing_dzt_signature_requirement | false | false | all_slots_require_dzt_signature |
| wrong_dzt_header_guard | false | false | all_slots_carry_matching_dzt_guard |
| slot_not_pending_real_file | false | false | all_slots_pending_real_files |
| packet_template_not_ready | false | false | execution_packet_template_ready |
| real_archive_marked_ready | false | false | downstream_states_remain_blocked |
| field_fwi_marked_ready | false | false | downstream_states_remain_blocked |
| stage_count_mismatch | false | false | execution_stage_count_matches_summary |

## Interpretation

The execution packet validator accepts the exact packet and rejects all damaged
variants: missing file slot, wrong role count, missing DZT signature
requirement, wrong DZT header guard, non-pending slot status, not-ready packet
flag, premature real-archive/field-FWI readiness, and stage-count mismatch.

This gives the field execution-packet package both positive and negative-control
coverage.

## Decision

Use runs `203`-`205` as the current controlled archive execution-packet guard
package.

Keep real archive acceptance, checksum/intake, field FWI, GPU work, and field
3D/HPC blocked until real files and metadata pass the integrated gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_packet_validator.py
tests/test_gssi_field_controlled_archive_execution_packet_sensitivity.py
8 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_execution_packet_sensitivity.py: pass
tests/test_gssi_field_controlled_archive_execution_packet_sensitivity.py: pass
```

Figure check:

```text
2717x842, dynamic range=255
```
