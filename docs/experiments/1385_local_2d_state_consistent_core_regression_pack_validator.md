# Experiment 1385: Local 2D Core Regression Pack Validator

Date: 2026-06-27

## Purpose

Validate the run `1384` core regression pack from a consumer perspective.

This run does not rerun the optimizer, launch broad batches, run GPU work, use
field data, run field FWI, perform 3D/HPC work, or train neural networks.

## Output

```text
outputs/experiments/1385_local_2d_state_consistent_core_regression_pack_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_core_regression_pack_validation_checks.csv
data/local_2d_state_consistent_core_regression_pack_validator_summary.json
figures/local_2d_state_consistent_core_regression_pack_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_CORE_REGRESSION_PACK_VALIDATOR.md
scripts/run_local_2d_state_consistent_core_regression_pack_validator.py
scripts/test_local_2d_state_consistent_core_regression_pack_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
case rows:                       116
validation checks:               9
validation passes:               9
blocking failures:               0
core objective labels:           base, highband
core regression rows:            88
core positive acceptance rows:   8
core negative rejection rows:    20
core hold/uncertain rows:        2
core observation-only rows:      58
core regression pack valid:      true
broad radius tolerance promoted: false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| case_file_nonempty | pass | 116 case rows |
| core_objectives_match_summary | pass | base;highband |
| expanded_objectives_excluded | pass | 0 expanded rows included |
| positive_acceptance_rows_consistent | pass | 8 positive rows |
| negative_rejection_rows_consistent | pass | 20 rejection rows |
| hold_rows_consistent | pass | 2 hold rows |
| observation_rows_consistent | pass | 58 observation rows |
| core_row_count_matches_summary | pass | 88 observed / 88 summary |
| no_gpu_or_field_promotion | pass | GPU, field transfer, and field FWI remain blocked |

## Interpretation

The run `1384` core regression pack is internally consistent and usable as a
consumer-facing regression boundary for the local 2D branch.

## Decision

Use this validator before future scripts consume or extend the core regression
pack. Keep broad radius tolerance, GPU work, field transfer, field FWI, and
3D/HPC blocked by this evidence.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_core_regression_pack_validator.py
sha256: a67410cec686fd3ba2aa85101ebbd45a3a05ece1617ddd0ec2b00fcd148ef43f

test_local_2d_state_consistent_core_regression_pack_validator.py
sha256: 99843a48f8c11c6b440a04c56db78563f64208cae646a75fe11a55c1e7ccca56
```

Subsequent related local 2D state-consistency experiments should start from a
duplicated run-specific script.

## Validation

Focused 2D tests:

```text
tests/test_local_2d_state_consistent_core_regression_pack.py
tests/test_local_2d_state_consistent_core_regression_pack_validator.py
9 passed
```

Figure check:

```text
local_2d_state_consistent_core_regression_pack_validator.png
1960x772, dynamic range=255
```
