# Field Experiment 492: Controlled Collection Live Receipt Collection-Day Route Work-Split Policy Validator

Date: 2026-06-30

## Purpose

Validate the run `491` work-split policy from its generated artifacts.

The validator checks that the policy still represents the same conservative
field route: 15 global metadata files can be prepared before measurement, 18
files remain measurement-dependent, and no partial delivery can promote parser,
provenance, archive, field FWI, or field 3D/HPC readiness.

This is a CPU-only artifact validation. It does not create live files, parse
DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/492_gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validator.png
scripts/
```

## Result

```text
checks:                                 5
passed checks:                          5
failed checks:                          0
work stages:                            4
total required files:                   33
total required receipt checks:          183
pre-fill files:                         15
pre-fill receipt checks:                75
measurement-dependent files:            18
measurement-dependent receipt checks:   108
all files required for promotion:       true
partial delivery promotes parser:       false
field FWI ready:                        false
field 3D/HPC ready:                     false
gpu priority:                           none
validation ready:                       true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source work-split policy ready | pass |
| 2 | stage rows match conservative field route | pass |
| 3 | prefill and measurement-dependent counts match | pass |
| 4 | partial delivery keeps parser and field FWI blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `491` is internally consistent and still has the intended acceptance
boundary. The pre-collection work block is useful for planning, but it does not
weaken the receipt gate. All 33 required files remain necessary before the
field packet can be promoted.

## Decision

Use this validator as the artifact guard for run `491`. Keep field FWI, GPU
work, and field 3D/HPC blocked until the measured collection packet is complete
and passes the later receipt, parser, provenance, and archive gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_work_split_policy_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_work_split_policy_validation_sensitivity.py

6 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
