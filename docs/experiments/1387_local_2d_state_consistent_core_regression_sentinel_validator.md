# Experiment 1387: Local 2D State-Consistent Core Regression Sentinel Validator

Date: 2026-06-27

## Purpose

Validate the run `1386` sentinel suite from a consumer perspective.

This run checks that the sentinel rows are a true subset of the full run `1384`
core regression pack, that all declared coverage tokens are covered, and that
the sentinel layer is still marked as a smoke layer rather than a replacement
for the full pack.

This is a CPU-only validation audit. It does not rerun the optimizer, launch
broad batches, run GPU work, use field data, run field FWI, perform 3D/HPC
work, or train neural networks.

## Output

```text
outputs/experiments/1387_local_2d_state_consistent_core_regression_sentinel_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_core_regression_sentinel_validation_checks.csv
data/local_2d_state_consistent_core_regression_sentinel_validator_summary.json
figures/local_2d_state_consistent_core_regression_sentinel_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_CORE_REGRESSION_SENTINEL_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
source core regression rows:      88
sentinel rows:                    11
coverage rows:                    32
validation checks:                9
validation passes:                9
blocking failures:                0
compression ratio:                0.125
sentinel suite valid:             true
sentinel replaces full pack:      false
authoritative full pack rows:     88
broad radius tolerance promoted:  false
GPU work ready:                   false
field transfer ready:             false
field FWI ready:                  false
3D/HPC ready:                     false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| sentinel_file_nonempty | pass | 11 sentinel rows |
| coverage_file_nonempty | pass | 32 coverage rows |
| sentinels_are_subset_of_source_core_pack | pass | 0 sentinel keys absent from full core pack |
| all_declared_coverage_tokens_covered | pass | 0 uncovered declared tokens |
| sentinel_tokens_cover_source_tokens | pass | 0 source tokens absent from sentinels |
| sentinel_row_count_matches_summary | pass | 11 observed / 11 summary |
| compression_is_strict | pass | 11 sentinel / 88 full core rows |
| sentinel_does_not_replace_full_pack | pass | sentinel is marked as smoke layer only |
| no_gpu_or_field_promotion | pass | GPU, field transfer, and field FWI remain blocked |

## Interpretation

The sentinel suite is valid as a compact coverage layer for the run `1384`
core pack. It can support fast smoke checks and compact examples, but the full
88-row core regression pack remains authoritative.

## Decision

Use run `1387` as the consumer-side validator for the sentinel suite. Keep
the full 88-row core pack authoritative and keep broad radius tolerance, GPU
work, field transfer, field FWI, and 3D/HPC blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_core_regression_sentinel_validator.py
5 passed
```

Figure validation:

```text
local_2d_state_consistent_core_regression_sentinel_validator.png
1960x772, dynamic range=255
```

Script snapshots:

```text
run_local_2d_state_consistent_core_regression_sentinel_validator.py
sha256=8be40936e201adc6c42205501502cffb8e681d6dae6da0f194e65545a12be1fb

tests/test_local_2d_state_consistent_core_regression_sentinel_validator.py
sha256=2f0adee1bdb7a3eac3ff5e7d0218536ef27ef4391712a1f81f8abc104fa333ca
```
