# Field Experiment 491: Controlled Collection Live Receipt Collection-Day Route Work-Split Policy

Date: 2026-06-30

## Purpose

Split the run `488-490` collection-day frontier into preparation and
measurement work blocks.

The goal is to identify what can be prepared before field collection and what
must wait for measured DZT files, without changing the all-files-required
promotion gate.

This run does not create live files, parse DZT data, promote measured evidence,
run provenance acceptance, build an archive, launch field FWI, launch GPU work,
or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/491_gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy.png
scripts/
```

## Result

```text
source frontier ready:                 true
source validation ready:               true
source sensitivity ready:              true
work stages:                           4
total required files:                  33
total required receipt checks:         183
pre-fill files:                        15
pre-fill receipt checks:               75
pre-fill file fraction:                0.45454545454545453
pre-fill check fraction:               0.4098360655737705
measurement-dependent files:           18
measurement-dependent receipt checks:  108
all files required for promotion:      true
partial delivery promotes parser:      false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

Work split:

| Stage | Families | Files | Receipt checks | Before measurement |
| --- | --- | ---: | ---: | --- |
| pre_collection_prefill | global_metadata | 15 | 75 | true |
| collection_day_measured_dzt | controlled_profile_repeat; time_zero_reference; amplitude_reference | 9 | 54 | false |
| post_measurement_per_file_metadata | per_file_metadata | 9 | 54 | false |
| final_receipt_parser_provenance_archive | all_families | 0 | 0 | false |

## Interpretation

About 45% of the required files and 41% of the receipt checks are global
metadata that can be prepared before collection. The measurement-dependent
part is still substantial: nine measured DZT files plus nine per-file metadata
records.

This work split improves collection preparation, but it does not weaken the
acceptance gate. Parser, provenance, archive, controlled field evidence, field
FWI, and field 3D/HPC remain blocked until all 33 files pass receipt.

## Decision

Prepare the 15 global metadata files before field collection. Keep
parser/provenance/archive promotion blocked until all 33 files pass receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_work_split_policy.py

3 passed
```

Figure validation:

```text
2284x847, dynamic range=255
```
