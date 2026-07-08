# Local 2D Experiment 1393: Reduced Sentinel Validator

Date: 2026-06-27

## Purpose

Validate the run `1392` reduced sentinel candidate from a consumer
perspective.

Run `1392` removed the two individually redundant category rows identified by
run `1391`, producing an 11-row candidate. This run checks that the reduced
candidate has no duplicate keys, remains inside the full core pack, covers all
required tokens, preserves both margin-risk add-ons, and removes only the
intended redundant rows.

This is a CPU-only table validation. It does not run FDTD, FWI, GPU work,
field transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1393_local_2d_state_consistent_reduced_sentinel_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_reduced_sentinel_validation_checks.csv
data/local_2d_state_consistent_reduced_sentinel_validator_summary.json
figures/local_2d_state_consistent_reduced_sentinel_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REDUCED_SENTINEL_VALIDATOR.md
scripts/run_local_2d_state_consistent_reduced_sentinel_validator.py
scripts/test_local_2d_state_consistent_reduced_sentinel_validator.py
```

## Result

```text
validation checks:             9
validation passes:             9
blocking failures:             0
reduced sentinel rows:         11
removed redundant rows:        2
required tokens:               32
uncovered tokens:              0
reduced sentinel valid:        true
fast smoke ready:              true
sentinel replaces full pack:   false
full pack remains authoritative: true
GPU ready:                     false
field FWI ready:               false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| reduced_rows_nonempty | pass | 11 rows |
| row_count_matches_summary | pass | 11 observed / 11 summary |
| no_duplicate_keys | pass | 0 duplicate keys |
| all_reduced_rows_in_core_pack | pass | 11 / 11 rows in core pack |
| required_tokens_still_covered | pass | 32 / 32 tokens covered |
| margin_addons_preserved | pass | 2 / 2 margin add-ons |
| removed_rows_match_redundant_indices | pass | removed [2, 5] / redundant [2, 5] |
| full_pack_remains_authoritative | pass | full pack authoritative, reduced sentinel does not replace it |
| no_gpu_field_or_3d_promotion | pass | GPU, field transfer, field FWI, and 3D/HPC blocked |

## Interpretation

The reduced 11-row sentinel candidate passes all consumer checks. It can replace
the 13-row risk-augmented sentinel as the preferred optional fast-smoke suite
for local 2D state-consistency changes.

This does not reduce the authoritative evidence base. The full 88-row core
regression pack remains the authoritative check whenever a change affects the
boundary itself.

## Decision

Use the 11-row reduced sentinel as the preferred optional fast-smoke suite for
local 2D state-consistency changes. The full 88-row core pack remains
authoritative, and broad radius tolerance, GPU work, field transfer, field FWI,
and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_reduced_sentinel_validator.py
3 passed
```

Figure validation:

```text
local_2d_state_consistent_reduced_sentinel_validator.png
2249x839, dynamic range=255
```
