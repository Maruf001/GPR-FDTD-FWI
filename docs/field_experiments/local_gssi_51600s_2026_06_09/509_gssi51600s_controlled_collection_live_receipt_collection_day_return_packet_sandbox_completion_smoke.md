# Field Experiment 509: Return-Packet Sandbox Completion Smoke

Date: 2026-06-30

## Purpose

Test the positive receipt path for the run `506` collection-day return-packet
intake contract without touching the live external-return paths.

Run `506` defined the real 33-file contract. This run fills that same contract
inside an output-local sandbox and checks whether the receipt mechanics pass
when every required file family is present.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/509_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_sandbox_manifest.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_sandbox_receipt_report.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_sandbox_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_sandbox_family_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke.png
scripts/
```

## Result

```text
source contract ready:                 true
source contract files:                 33
source receipt checks:                 183
sandbox files written:                 33
sandbox DZT files:                     9
sandbox metadata JSON files:           24
sandbox nonempty files:                33
sandbox receipt-ready files:           33
sandbox receipt checks:                183
sandbox metadata JSON parse-ready:     24
sandbox complete families:             5
metadata templates linked:             24
templates accepted as live receipt:    0
original live files present:           0
synthetic-only files:                  33
measured field evidence files:         0
live receipt ready:                    false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
```

Family completion:

| File family | Contract files | Sandbox receipt-ready | Live receipt-ready |
| --- | ---: | ---: | ---: |
| controlled profile repeat | 3 | 3 | 0 |
| time-zero reference | 3 | 3 | 0 |
| amplitude reference | 3 | 3 | 0 |
| global metadata | 15 | 15 | 0 |
| per-file metadata | 9 | 9 | 0 |

## Interpretation

The receipt mechanics can pass for the complete 33-file packet. This is a
positive-path smoke of the contract, not measured field evidence. The files are
synthetic placeholders written inside the run `509` output folder, and none of
them overlap the live external-return locations.

The real collection-day requirement is unchanged:

```text
3 controlled profile DZT files
3 time-zero reference DZT files
3 amplitude-reference DZT files
15 completed global metadata JSON files
9 completed per-file metadata JSON files
```

## Decision

Use run `509` as the output-local receipt-mechanics pass case for the run `506`
contract. Keep live receipt, parser/provenance/archive promotion, field FWI,
and field 3D/HPC blocked until real files satisfy the same contract at the
locked live paths.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke.py

3 passed
```

Figure check:

```text
2536x869, dynamic range=255
```
