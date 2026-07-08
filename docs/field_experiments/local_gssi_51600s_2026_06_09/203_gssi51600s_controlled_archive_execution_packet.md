# Field Experiment 203: Controlled Archive Execution Packet

Date: 2026-06-28

## Purpose

Join the integrated archive acceptance contract with the nine required DZT
intake slots into one collection-day execution packet.

Runs `200`-`202` validated the controlled archive acceptance contract. Run
`193` defined the nine concrete real-file slots. This run combines those into
one packet that can be used when a real controlled archive arrives.

This run does not ingest real field files, modify the pending archive, run field
FWI, launch GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/203_gssi51600s_controlled_archive_execution_packet
```

Key artifacts:

```text
data/field_controlled_archive_execution_packet_steps.csv
data/field_controlled_archive_execution_packet_file_slots.csv
data/field_controlled_archive_execution_packet_summary.json
figures/field_controlled_archive_execution_packet.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_PACKET.md
scripts/run_gssi_field_controlled_archive_execution_packet.py
scripts/test_gssi_field_controlled_archive_execution_packet.py
```

## Result

```text
execution stages:                   10
design-ready stages:                9
real-accepted stages:               0
blocking stages:                    10
metadata values required:           11
real files required:                9
DZT signature slots:                9
profile repeat slots:               3
time-zero reference slots:          3
amplitude reference slots:          3
DZT size floor bytes:               65536
GSSI header prefix hex:             ff07
execution packet template ready:    true
real files present:                 false
integrated archive ready:           false
field FWI ready:                    false
```

## Required DZT Slots

| Slot | Role | Target file | Archive path | Current status |
| ---: | --- | --- | --- | --- |
| 1 | controlled_profile_repeat | controlled_profile_repeat_01.DZT | raw/profiles/controlled_profile_repeat_01.DZT | pending_real_file |
| 2 | controlled_profile_repeat | controlled_profile_repeat_02.DZT | raw/profiles/controlled_profile_repeat_02.DZT | pending_real_file |
| 3 | controlled_profile_repeat | controlled_profile_repeat_03.DZT | raw/profiles/controlled_profile_repeat_03.DZT | pending_real_file |
| 4 | time_zero_reference | time_zero_reference_01.DZT | raw/references/time_zero/time_zero_reference_01.DZT | pending_real_file |
| 5 | time_zero_reference | time_zero_reference_02.DZT | raw/references/time_zero/time_zero_reference_02.DZT | pending_real_file |
| 6 | time_zero_reference | time_zero_reference_03.DZT | raw/references/time_zero/time_zero_reference_03.DZT | pending_real_file |
| 7 | amplitude_reference | amplitude_reference_01.DZT | raw/references/amplitude/amplitude_reference_01.DZT | pending_real_file |
| 8 | amplitude_reference | amplitude_reference_02.DZT | raw/references/amplitude/amplitude_reference_02.DZT | pending_real_file |
| 9 | amplitude_reference | amplitude_reference_03.DZT | raw/references/amplitude/amplitude_reference_03.DZT | pending_real_file |

Each required file slot carries the integrated DZT guard:

```text
minimum size:   65536 bytes
header prefix:  ff07
checksum:       required
```

## Interpretation

The controlled archive intake path is now executable as a template: the
10-stage acceptance contract and nine DZT file slots are joined with DZT
size/header guard requirements. This removes ambiguity about what a future real
archive must contain and how it should be preflighted.

No real files are present, so this is an execution packet, not real archive
acceptance.

## Decision

Use this packet for real controlled archive intake.

Keep checksum/intake, controlled evidence, real archive acceptance, field FWI,
GPU work, and field 3D/HPC blocked until the nine real DZT files and required
metadata pass the integrated gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_packet.py
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_sensitivity.py
7 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_execution_packet.py: pass
tests/test_gssi_field_controlled_archive_execution_packet.py: pass
```

Figure check:

```text
3040x877, dynamic range=255
```
