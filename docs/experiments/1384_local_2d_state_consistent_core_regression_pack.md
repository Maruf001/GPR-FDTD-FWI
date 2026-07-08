# Experiment 1384: Local 2D State-Consistent Core Regression Pack

Date: 2026-06-27

## Purpose

Turn the run `1382` acceptance-status table and run `1383` objective-support
map into a concrete core regression pack for the local 2D state-consistency
branch.

This run does not rerun the optimizer, launch broad batches, run GPU work, use
field data, run field FWI, perform 3D/HPC work, or train neural networks.

## Output

```text
outputs/experiments/1384_local_2d_state_consistent_core_regression_pack
```

Key artifacts:

```text
data/local_2d_state_consistent_core_regression_cases.csv
data/local_2d_state_consistent_core_regression_role_summary.csv
data/local_2d_state_consistent_core_regression_by_run.csv
data/local_2d_state_consistent_core_regression_pack_summary.json
figures/local_2d_state_consistent_core_regression_pack.png
docs/LOCAL_2D_STATE_CONSISTENT_CORE_REGRESSION_PACK.md
scripts/run_local_2d_state_consistent_core_regression_pack.py
scripts/test_local_2d_state_consistent_core_regression_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source status rows:                  116
core objective labels:               base, highband
case rows:                           116
core regression rows:                88
expanded observation-only rows:      28
core positive acceptance rows:       8
core negative rejection rows:        20
core hold/uncertain rows:            2
core observation-only rows:          58
core source run count:               5
core regression pack ready:          true
broad radius tolerance promoted:     false
broad batch ready:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
```

Role summary:

| Role | Rows | Core rows | Future-regression rows | Run count | Objectives |
| --- | ---: | ---: | ---: | ---: | --- |
| core_hold_uncertain | 2 | 2 | 2 | 1 | base;highband |
| core_negative_rejection | 20 | 20 | 20 | 4 | base;highband |
| core_observation_only | 58 | 58 | 58 | 4 | base;highband |
| core_positive_acceptance | 8 | 8 | 8 | 4 | base;highband |
| expanded_observation_only | 28 | 0 | 0 | 2 | early_high;late;late_high;veryhigh |

Core rows by run:

| Run | Core rows | Positive | Reject | Hold | Observe |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1375 | 4 | 0 | 2 | 2 | 0 |
| 1376 | 18 | 2 | 0 | 0 | 16 |
| 1377 | 34 | 2 | 6 | 0 | 26 |
| 1378 | 22 | 2 | 9 | 0 | 11 |
| 1379 | 10 | 2 | 3 | 0 | 5 |

## Interpretation

The local 2D branch now has an executable core regression boundary. `base` and
`highband` are the only core objectives. Corrected-state finite-margin rows are
positive cases, wrong-geometry rows are rejection cases, missing-margin rows
remain hold cases, and truth-selected perturbation rows remain observations.

This is a useful regression pack, not a broad-radius tolerance claim.

## Decision

Use this pack for future local 2D state-consistency regression checks. Do not
treat observation-only rows or expanded-only objectives as broad radius
tolerance, GPU readiness, field transfer readiness, field FWI readiness, or
3D/HPC readiness.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_core_regression_pack.py
sha256: f613676b9027bcd41f00f92fabcb324ba4434f6a8b3c9fdc9dff1a7b34e077fb

test_local_2d_state_consistent_core_regression_pack.py
sha256: 7b2c229207eca94d2971eb390783e752c9cd213191229e864b32d658ef4db282
```

Subsequent related local 2D state-consistency experiments should start from a
duplicated run-specific script.

## Validation

Focused state-consistency tests:

```text
tests/test_local_2d_state_consistent_acceptance_status_synthesis.py
tests/test_local_2d_state_consistent_objective_support_map.py
tests/test_local_2d_state_consistent_core_regression_pack.py
13 passed
```

Figure check:

```text
local_2d_state_consistent_core_regression_pack.png
2680x850, dynamic range=255
```
