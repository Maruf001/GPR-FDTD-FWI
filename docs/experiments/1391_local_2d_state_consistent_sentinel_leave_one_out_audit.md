# Local 2D Experiment 1391: Sentinel Leave-One-Out Audit

Date: 2026-06-27

## Purpose

Audit whether each row in the 13-row risk-augmented sentinel suite is
mandatory under coverage-token and margin-risk criteria.

Runs `1384`-`1390` built the 88-row core regression pack, selected a compact
sentinel suite, added two margin-risk rows, and validated the 13-row suite from
a consumer perspective. This run asks whether that 13-row suite is minimal.

This is a CPU-only table audit. It does not run FDTD, FWI, GPU work, field
transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1391_local_2d_state_consistent_sentinel_leave_one_out_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_sentinel_leave_one_out_rows.csv
data/local_2d_state_consistent_sentinel_leave_one_out_audit_summary.json
figures/local_2d_state_consistent_sentinel_leave_one_out_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_SENTINEL_LEAVE_ONE_OUT_AUDIT.md
scripts/run_local_2d_state_consistent_sentinel_leave_one_out_audit.py
scripts/test_local_2d_state_consistent_sentinel_leave_one_out_audit.py
```

## Result

```text
source core regression rows:        88
source sentinel rows:               13
required coverage tokens:           32
uncovered coverage tokens:          0
coverage-mandatory rows:            9
risk-add-on mandatory rows:         2
overall mandatory rows:             11
individually redundant rows:        2
risk-augmented suite covers tokens: true
strictly minimal:                   false
full pack remains authoritative:    true
GPU ready:                          false
field FWI ready:                    false
```

Leave-one-out result:

| Sentinel | Run | Role | Source | Lost tokens if removed | Coverage mandatory | Risk mandatory | Redundant |
| ---: | ---: | --- | --- | ---: | --- | --- | --- |
| 1 | 1376 | core_positive_acceptance | category_coverage_sentinel | 3 | true | false | false |
| 2 | 1375 | core_negative_rejection | category_coverage_sentinel | 0 | false | false | true |
| 3 | 1377 | core_observation_only | category_coverage_sentinel | 1 | true | false | false |
| 4 | 1375 | core_hold_uncertain | category_coverage_sentinel | 3 | true | false | false |
| 5 | 1378 | core_negative_rejection | category_coverage_sentinel | 0 | false | false | true |
| 6 | 1379 | core_negative_rejection | category_coverage_sentinel | 1 | true | false | false |
| 7 | 1376 | core_observation_only | category_coverage_sentinel | 1 | true | false | false |
| 8 | 1376 | core_observation_only | category_coverage_sentinel | 1 | true | false | false |
| 9 | 1376 | core_observation_only | category_coverage_sentinel | 1 | true | false | false |
| 10 | 1376 | core_observation_only | category_coverage_sentinel | 1 | true | false | false |
| 11 | 1376 | core_observation_only | category_coverage_sentinel | 1 | true | false | false |
| 12 | 1377 | core_negative_rejection | margin_risk_addon | 0 | false | true | false |
| 13 | 1378 | core_observation_only | margin_risk_addon | 0 | false | true | false |

## Interpretation

The 13-row sentinel suite covers all required coverage tokens, but it is not
strictly minimal. Nine rows are mandatory because removing them loses required
coverage tokens. The two margin-risk add-ons do not add unique coverage tokens,
but they remain mandatory for the margin-risk purpose that motivated run
`1388`. Two category rows are individually redundant under the current token
definition.

This does not invalidate the 13-row suite. It clarifies that it is an optional
fast smoke layer, not a minimal proof set and not a replacement for the full
88-row pack.

## Decision

Keep the 13-row suite as the optional fast smoke layer for now. Do not treat it
as minimal or authoritative. The full 88-row core pack remains authoritative,
and broad radius tolerance, GPU work, field transfer, field FWI, and 3D/HPC
remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_sentinel_leave_one_out_audit.py
4 passed
```

Figure validation:

```text
local_2d_state_consistent_sentinel_leave_one_out_audit.png
2860x845, dynamic range=255
```
