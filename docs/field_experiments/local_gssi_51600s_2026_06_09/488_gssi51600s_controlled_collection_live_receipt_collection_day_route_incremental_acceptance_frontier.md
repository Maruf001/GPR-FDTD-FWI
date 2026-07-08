# Field Experiment 488: Controlled Collection Live Receipt Collection-Day Route Incremental Acceptance Frontier

Date: 2026-06-30

## Purpose

Simulate the collection-day receipt frontier after the post-sandbox live-path
guard in runs `485-487`.

The field route has five required file families. This run enumerates all 32
possible family-completion scenarios and asks which scenarios satisfy the
conservative live receipt and parser/provenance/archive gate.

This run does not create live files, parse DZT data, promote measured evidence,
run provenance acceptance, build an archive, launch field FWI, launch GPU work,
or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/488_gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_family_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_frontier_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier.png
scripts/
```

## Result

```text
source guard ready:                         true
source validation ready:                    true
source sensitivity ready:                   true
file families:                              5
family-completion scenarios:                32
current-state scenarios:                    1
partial scenarios:                          30
receipt-complete scenarios:                 1
partial receipt-complete scenarios:         0
total required files:                       33
total required receipt checks:              183
minimum families for receipt completion:    5
current live files present:                 0
current live receipt-ready files:           0
parser ready:                               false
provenance ready:                           false
archive ready:                              false
controlled field evidence ready:            false
field FWI ready:                            false
field 3D/HPC ready:                         false
gpu priority:                               none
```

Required families:

| Family | File type | Files | Receipt checks |
| --- | --- | ---: | ---: |
| controlled_profile_repeat | dzt | 3 | 18 |
| time_zero_reference | dzt | 3 | 18 |
| amplitude_reference | dzt | 3 | 18 |
| global_metadata | metadata_json | 15 | 75 |
| per_file_metadata | metadata_json | 9 | 54 |

## Interpretation

No partial delivery completes the conservative receipt gate. Even scenarios
with four of five families complete still leave either DZT files or metadata
files missing, so parser, provenance, archive, and controlled field evidence
promotion remain blocked.

The only receipt-complete scenario is the all-family case: three controlled
profile repeat DZT files, three time-zero reference DZT files, three
amplitude-reference DZT files, fifteen global metadata JSON files, and nine
per-file metadata JSON files.

## Decision

Use run `488` as the collection-day family-completion frontier. Partial
delivery may be inspected, but parser/provenance/archive promotion stays
blocked until all 33 live files pass receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier.py

3 passed
```

Figure validation:

```text
2428x845, dynamic range=255
```
