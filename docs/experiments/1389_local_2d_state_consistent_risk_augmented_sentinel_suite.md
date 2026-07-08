# Local 2D Experiment 1389: Risk-Augmented Sentinel Suite

Date: 2026-06-27

## Purpose

Build the risk-augmented sentinel suite recommended by run `1388`.

Run `1387` validated the 11-row sentinel suite as a category-coverage smoke
layer. Run `1388` showed that it missed the closest finite-margin
negative-rejection and observation-only rows. This run adds those two rows.

This is a CPU-only table synthesis. It does not run FDTD, FWI, GPU work, field
transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1389_local_2d_state_consistent_risk_augmented_sentinel_suite
```

Key artifacts:

```text
data/local_2d_state_consistent_risk_augmented_sentinel_rows.csv
data/local_2d_state_consistent_risk_augmented_sentinel_role_summary.csv
data/local_2d_state_consistent_risk_augmented_sentinel_suite_summary.json
figures/local_2d_state_consistent_risk_augmented_sentinel_suite.png
docs/LOCAL_2D_STATE_CONSISTENT_RISK_AUGMENTED_SENTINEL_SUITE.md
scripts/script_snapshot_manifest.json
```

## Result

```text
source category sentinels:       11
source margin add-ons:           2
augmented sentinel rows:         13
duplicate keys:                  0
margin-risk add-on rows:         2
category coverage preserved:     true
risk-augmented sentinel ready:   true
sentinel replaces full pack:     false
full pack remains authoritative: true
broad radius tolerance promoted: false
gpu work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
```

Role summary:

| Role | Augmented rows | Category rows | Margin add-ons |
| --- | ---: | ---: | ---: |
| core_hold_uncertain | 1 | 1 | 0 |
| core_negative_rejection | 4 | 3 | 1 |
| core_observation_only | 7 | 6 | 1 |
| core_positive_acceptance | 1 | 1 | 0 |

Margin add-on rows:

| Run | Perturbation | Objective | Role | Margin |
| ---: | --- | --- | --- | ---: |
| 1377 | far_neighbor_radius_minus_2mm | base | core_negative_rejection | -3.72744339579012e-05 |
| 1378 | near_neighbor_radius_plus_2p50mm | highband | core_observation_only | 0.0004147381786346327 |

## Interpretation

The 13-row suite preserves all 11 category-coverage sentinels and adds the two
closest finite-margin rows from the full 88-row core pack. It is a stronger
fast smoke layer for boundary-sensitive changes.

The full 88-row core pack remains authoritative. The augmented suite is a fast
screen, not a replacement.

## Decision

Use this 13-row suite as an optional fast smoke layer when boundary margins
matter. Do not let it replace the full core pack.

Broad radius tolerance, GPU work, field transfer, field FWI, and 3D/HPC remain
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_risk_augmented_sentinel_suite.py
6 passed
```

Figure validation:

```text
local_2d_state_consistent_risk_augmented_sentinel_suite.png
2230x847, dynamic range=255
```

Script snapshots:

```text
run_local_2d_state_consistent_risk_augmented_sentinel_suite.py
sha256=412429d49a7be4408105c1f25926c1f7e7cfa6384914bda1bb1cba5b01b02efd

tests/test_local_2d_state_consistent_risk_augmented_sentinel_suite.py
sha256=bdf5115ff676b38a50cb1512eeb6a3b101945fd51054f66a3a0dbc3a6a790648
```
