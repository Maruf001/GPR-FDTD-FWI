# Local 2D Experiment 1388: Sentinel Margin-Risk Audit

Date: 2026-06-27

## Purpose

Check whether the 11-row sentinel suite from run `1386` covers the closest
finite decision margins in the full 88-row core regression pack from run `1384`.

Run `1387` validated the sentinel as a category-coverage smoke layer. This run
asks the narrower risk question:

```text
Does the sentinel also include the most fragile finite-margin cases?
```

This is a CPU-only audit of saved tables. It does not run FDTD, FWI, GPU work,
field transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1388_local_2d_state_consistent_sentinel_margin_risk_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_sentinel_margin_role_summary.csv
data/local_2d_state_consistent_sentinel_margin_addons.csv
data/local_2d_state_consistent_sentinel_margin_risk_audit_summary.json
figures/local_2d_state_consistent_sentinel_margin_risk_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_SENTINEL_MARGIN_RISK_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
core regression rows:                 88
sentinel rows:                        11
finite-margin core rows:              84
missing-margin core rows:             4
role count:                           4
finite-margin role count:             3
closest finite roles covered:         1
missing-margin roles covered:         2
suggested margin add-ons:             2
risk-augmented sentinel recommended:  true
sentinel valid as category smoke:      true
sentinel replaces full pack:           false
full pack remains authoritative:       true
broad radius tolerance promoted:       false
gpu work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

Role summary:

| Role | Core rows | Sentinel rows | Full closest abs margin | Sentinel closest abs margin | Covers closest |
| --- | ---: | ---: | ---: | ---: | --- |
| core_hold_uncertain | 2 | 1 |  |  | false |
| core_negative_rejection | 20 | 3 | 3.72744339579012e-05 | 0.00027061154662177955 | false |
| core_observation_only | 58 | 6 | 0.0004147381786346327 | 0.0045159392920220455 | false |
| core_positive_acceptance | 8 | 1 | 0.01994705692712514 | 0.01994705692712514 | true |

Suggested risk add-ons:

| Reason | Run | Perturbation | Objective | Role | Margin |
| --- | ---: | --- | --- | --- | ---: |
| closest_finite_margin_not_in_sentinel | 1377 | far_neighbor_radius_minus_2mm | base | core_negative_rejection | -3.72744339579012e-05 |
| closest_finite_margin_not_in_sentinel | 1378 | near_neighbor_radius_plus_2p50mm | highband | core_observation_only | 0.0004147381786346327 |

## Interpretation

The sentinel suite remains valid as a fast category-coverage smoke layer. It
covers the promoted positive-margin boundary and the missing-margin classes.

It does not include the closest finite-margin negative-rejection row or the
closest finite-margin observation-only row. Those are the most fragile boundary
cases in the full pack. A two-row risk add-on is therefore justified if future
fast smoke checks need to catch boundary-sensitive changes.

## Decision

Keep run `1387` as the category-coverage sentinel validator, but do not let it
replace the full 88-row pack. Add a risk-augmented sentinel layer before relying
on sentinel-only smoke checks for boundary-sensitive changes.

Broad radius tolerance, GPU work, field transfer, field FWI, and 3D/HPC remain
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_sentinel_margin_risk_audit.py
6 passed
```

Figure validation:

```text
local_2d_state_consistent_sentinel_margin_risk_audit.png
2859x847, dynamic range=255
```

Script snapshots:

```text
run_local_2d_state_consistent_sentinel_margin_risk_audit.py
sha256=199dd06c826a92e5a9c2e63ad557e23ec0f62e2bdb2592024fcb76dea55ec000

tests/test_local_2d_state_consistent_sentinel_margin_risk_audit.py
sha256=d3e2c8c0189c11057815aee404ed56eaca396f8d4e059cc7bb5d193c239f44e4
```
