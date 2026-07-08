# Field Experiment 204: Controlled Archive Execution Packet Validator

Date: 2026-06-28

## Purpose

Validate the run `203` controlled archive execution packet from a consumer
perspective.

Run `203` joined the integrated acceptance contract with the nine required DZT
file slots. This run checks that a downstream consumer can read the packet and
confirm the stage count, file-slot count, role counts, DZT guard fields, pending
statuses, and blocked downstream states.

This run does not ingest real field files, modify the pending archive, run field
FWI, launch GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/204_gssi51600s_controlled_archive_execution_packet_validator
```

Key artifacts:

```text
data/field_controlled_archive_execution_packet_validation_checks.csv
data/field_controlled_archive_execution_packet_validator_summary.json
figures/field_controlled_archive_execution_packet_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_PACKET_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_execution_packet_validator.py
scripts/test_gssi_field_controlled_archive_execution_packet_validator.py
```

## Result

```text
validation checks:                  9
validation passes:                  9
blocking failures:                  0
source execution stages:            10
source file slots:                  9
packet validation ready:            true
real archive acceptance ready:      false
checksum intake ready:              false
field FWI ready:                    false
3D/HPC ready:                       false
```

| Check | Expected | Observed | Passes |
| --- | --- | --- | --- |
| execution_stage_count_matches_summary | 10 | 10 | true |
| file_slot_count_matches_summary | 9 | 9 | true |
| role_counts_match_expected_three_each | 3/3/3 | 3/3/3 | true |
| all_slots_require_dzt_signature | 9 | 9 | true |
| all_slots_carry_matching_dzt_guard | 9 | 9 | true |
| all_slots_pending_real_files | 9 | 9 | true |
| execution_packet_template_ready | true | true | true |
| zero_real_accepted_steps | 0 | 0 | true |
| downstream_states_remain_blocked | false | false | true |

## Interpretation

The execution packet is internally consistent and consumer-ready. The stage
count, nine file slots, role counts, DZT guard fields, pending statuses, and
blocked downstream states are all preserved.

This validates the template. It does not accept a real archive.

## Decision

Use run `203` as the controlled archive execution packet and run `204` as its
consumer validator.

Keep real archive acceptance, checksum/intake, field FWI, GPU work, and field
3D/HPC blocked until real files and metadata pass the integrated gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_packet.py
tests/test_gssi_field_controlled_archive_execution_packet_validator.py
8 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_execution_packet_validator.py: pass
tests/test_gssi_field_controlled_archive_execution_packet_validator.py: pass
```

Figure check:

```text
2645x841, dynamic range=255
```
