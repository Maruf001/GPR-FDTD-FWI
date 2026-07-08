# Local 2D Experiment 1390: Risk-Augmented Sentinel Validator

Date: 2026-06-27

## Purpose

Validate the run `1389` risk-augmented sentinel suite from a consumer
perspective.

This run checks that the 13-row suite has no duplicate row keys, stays inside
the full core regression pack, preserves the original 11 category sentinels,
and includes the two margin-risk add-ons from run `1388`.

This is a CPU-only validation. It does not run FDTD, FWI, GPU work, field
transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1390_local_2d_state_consistent_risk_augmented_sentinel_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_risk_augmented_sentinel_validation_checks.csv
data/local_2d_state_consistent_risk_augmented_sentinel_validator_summary.json
figures/local_2d_state_consistent_risk_augmented_sentinel_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_RISK_AUGMENTED_SENTINEL_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  9
validation passes:                  9
blocking failures:                  0
source augmented sentinel rows:     13
source margin add-on rows:          2
risk-augmented sentinel valid:      true
sentinel replaces full pack:        false
full pack remains authoritative:    true
broad radius tolerance promoted:    false
gpu work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| augmented_rows_nonempty | pass | 13 rows |
| row_count_matches_summary | pass | 13 observed / 13 summary |
| no_duplicate_keys | pass | 0 duplicate keys |
| all_augmented_rows_in_core_pack | pass | 13 / 13 rows in core pack |
| category_sentinel_count_preserved | pass | 11 category rows |
| margin_addon_count_matches_source | pass | 2 margin add-ons |
| margin_addon_keys_match_run1388 | pass | 2 / 2 add-ons matched |
| full_pack_remains_authoritative | pass | full pack authoritative, sentinel does not replace it |
| no_gpu_field_or_3d_promotion | pass | GPU, field transfer, field FWI, and 3D/HPC blocked |

## Interpretation

The 13-row risk-augmented sentinel suite is internally valid. It preserves the
original 11 category sentinels, adds the two run `1388` margin-risk rows, and
contains no duplicate keys.

The full 88-row core pack remains authoritative. The 13-row suite is an optional
fast smoke layer for boundary-sensitive edits.

## Decision

Use run `1390` as the consumer-side validator for the optional 13-row fast smoke
suite. Keep the 88-row full pack authoritative.

Broad radius tolerance, GPU work, field transfer, field FWI, and 3D/HPC remain
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_risk_augmented_sentinel_validator.py
4 passed
```

Figure validation:

```text
local_2d_state_consistent_risk_augmented_sentinel_validator.png
2231x839, dynamic range=255
```

Script snapshots:

```text
run_local_2d_state_consistent_risk_augmented_sentinel_validator.py
sha256=a790879a0178b3a49fb143d02ca72251ffa9ecb0d140b9362d1aea1db28e722a

tests/test_local_2d_state_consistent_risk_augmented_sentinel_validator.py
sha256=51d9d2d22978ecbf134f6bdf7a28ae3d52282961fe4daccfb764b797f68f056e
```
