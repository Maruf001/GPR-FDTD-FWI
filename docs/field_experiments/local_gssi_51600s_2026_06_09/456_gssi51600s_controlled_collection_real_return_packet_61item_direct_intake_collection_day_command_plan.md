# Field Experiment 456: Direct-Intake Collection-Day Command Plan

Date: 2026-06-30

## Purpose

Convert the run `455` collection-day checklist into non-executed receipt-check
commands.

The command plan provides one command per expected copied file. DZT files get a
nonempty-file and SHA-256 checksum command. Metadata JSON files get a
nonempty-file, JSON parse, and SHA-256 checksum command.

This run does not execute the commands, copy files, accept parser output,
accept provenance, archive the packet, run field FWI, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/456_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_command_plan
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_command_plan_command_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_command_plan_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_command_plan_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_command_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source checklist ready:                    true
commands:                                  33
DZT checksum commands:                     9
JSON parse/checksum commands:              24
commands executed:                         0
receipt-check ready commands:              0
command actions:                           3
command plan ready:                        true
GPU priority:                              none
```

## Decision

Run these commands only after measured files are copied into the staged return
tree. Then rerun receipt, parser, provenance, and archive gates before any
field FWI or field 3D/HPC work.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_collection_day_command_plan.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
