# Experiment 1386: Local 2D State-Consistent Core Regression Sentinel Suite

Date: 2026-06-27

## Purpose

Select a small coverage-preserving sentinel suite from the run `1384` local 2D
core regression pack.

The full run `1384` pack remains the authoritative 88-row regression boundary.
This run asks whether a smaller subset can cover the observed source runs,
core objectives, decision roles, status labels, truth/margin states, and
perturbation-sign tokens for fast smoke checks and presentation-scale examples.

This is a CPU-only selection audit. It does not rerun the optimizer, launch
broad batches, run GPU work, use field data, run field FWI, perform 3D/HPC
work, or train neural networks.

## Output

```text
outputs/experiments/1386_local_2d_state_consistent_core_regression_sentinel_suite
```

Key artifacts:

```text
data/local_2d_state_consistent_core_regression_sentinel_rows.csv
data/local_2d_state_consistent_core_regression_sentinel_coverage.csv
data/local_2d_state_consistent_core_regression_sentinel_role_summary.csv
data/local_2d_state_consistent_core_regression_sentinel_suite_summary.json
figures/local_2d_state_consistent_core_regression_sentinel_suite.png
docs/LOCAL_2D_STATE_CONSISTENT_CORE_REGRESSION_SENTINEL_SUITE.md
scripts/script_snapshot_manifest.json
```

## Result

```text
source core regression rows:       88
sentinel rows:                     11
coverage tokens:                   32
covered tokens:                    32
uncovered tokens:                  0
compression ratio:                 0.125
source run count:                  5
sentinel run count:                5
source role count:                 4
sentinel role count:               4
sentinel suite ready:              true
sentinel replaces full pack:       false
broad radius tolerance promoted:   false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

Role summary:

| Role | Full core rows | Sentinel rows | Full source runs | Sentinel source runs |
| --- | ---: | ---: | ---: | ---: |
| core_hold_uncertain | 2 | 1 | 1 | 1 |
| core_negative_rejection | 20 | 3 | 4 | 3 |
| core_observation_only | 58 | 6 | 4 | 2 |
| core_positive_acceptance | 8 | 1 | 4 | 1 |

## Interpretation

The full 88-row core pack can be accompanied by an 11-row sentinel suite that
covers every observed coverage token in the core evidence: source runs, core
objectives, regression roles, decisions, status labels, truth/margin states,
and perturbation-sign tokens.

The sentinel suite is therefore useful for fast smoke checks and compact
examples, but it is deliberately not a replacement for the full regression
pack. It does not widen the physical claim boundary.

## Decision

Use run `1386` as a fast sentinel layer on top of run `1384`. Keep run `1384`
as the authoritative full core regression pack. Do not use the sentinel suite
to promote broad radius tolerance, broad batches, GPU work, field transfer,
field FWI, or 3D/HPC work.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_core_regression_sentinel_suite.py
5 passed
```

Figure validation:

```text
local_2d_state_consistent_core_regression_sentinel_suite.png
2770x848, dynamic range=255
```

Script snapshots:

```text
run_local_2d_state_consistent_core_regression_sentinel_suite.py
sha256=b7a8167b36e7fe6e8b696ea293809a728f354fa3577700b7f2f899cc41a39def

tests/test_local_2d_state_consistent_core_regression_sentinel_suite.py
sha256=23a0cfc600b355f52ef3391ef0f02c0031247a55a03ed1c44b4edd73d41216bb
```
