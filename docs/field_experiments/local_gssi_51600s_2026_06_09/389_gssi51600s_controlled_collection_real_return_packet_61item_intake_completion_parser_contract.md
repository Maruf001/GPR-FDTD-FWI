# Field Experiment 389: Intake Completion Parser Contract

Date: 2026-06-29

## Purpose

Define how a future filled intake worksheet must be parsed before any returned
field packet can be accepted.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/389_gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_completion_rule_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_status_rule_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_parser_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract.png
```

## Result

```text
source worksheet ready:                   true
parser contract ready:                    true
worksheet rows:                           49
direct real-input rows:                   33
generated follow-up rows:                 16
completion columns:                       6
required completion columns:              5
completion rules:                         6
status rules:                             8
blank completion cells:                   294
parser-accepted current rows:             0
parser-rejected current rows:             49
current measured-evidence rows:           0
current field-FWI input-ready rows:       0
ready to parse future completed worksheet: true
current blank worksheet has real evidence: false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

The parser contract requires five fields for both direct real inputs and
generated follow-up files: returned source path, SHA-256 hash, byte count,
UTC timestamp, and operator initials. The intake note remains optional.

## Decision

Use this parser contract before accepting any filled worksheet. The current
worksheet is still blank and non-evidence; field FWI, GPU work, and field
3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_completion_parser_contract.py
4 passed
```

Figure check:

```text
3221x880, dynamic range=255
```
