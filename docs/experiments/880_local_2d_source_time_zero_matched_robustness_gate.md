# Experiment 880: Local 2D Matched Source/Time-Zero Robustness Gate

Date: 2026-06-25

## Purpose

Promote the matched-factorization result from run `159` into a pass/block
claim gate.

This supersedes the coarser run `147` gate for source/time-zero claim language
because it uses matched nominal/source-mismatch pairs within the same target,
pass, step, and objective.

This is cached analysis only. It does not run new FDTD, GPU work, field
transfer, field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/160_local_2d_source_time_zero_matched_robustness_gate
```

Key artifacts:

```text
data/local_2d_source_time_zero_matched_robustness_gate.csv
data/local_2d_source_time_zero_matched_robustness_gate_summary.json
docs/LOCAL_2D_SOURCE_TIME_ZERO_MATCHED_ROBUSTNESS_GATE.md
figures/local_2d_source_time_zero_matched_robustness_gate.png
scripts/run_local_2d_source_time_zero_matched_robustness_gate.py
scripts/test_local_2d_source_time_zero_matched_robustness_gate.py
scripts/script_snapshot_manifest.json
```

## Result

```text
cases gated:                         5
robust cases:                        3
blocked sensitive cases:             2
matched geometry-changed cases:      2
matched geometry-stable cases:       3
changed without time-shift cases:    2
prior span refined by matched pairs: true
general source/time-zero claim ready: false
close14-like gate pass:              true
broad variable-radius claim ready:   false
time-zero-only explanation ready:    false
new FDTD run ready:                  false
GPU work ready:                      false
field transfer ready:                false
```

## Gate Rows

| Category | Changed pairs | Max matched delta mm | Driver | Gate |
| --- | ---: | ---: | --- | --- |
| max amplitude stress | 2 | 5.0 | amplitude/frequency effect without time-shift observed | blocked |
| max geometry instability | 6 | 3.3541019662496847 | amplitude/frequency effect without time-shift observed | blocked |
| stable high time shift | 0 | 0.0 | matched geometry stable | pass |
| fixed-radius-like close14 | 0 | 0.0 | matched geometry stable | pass |
| low source-effect control | 0 | 0.0 | matched geometry stable | pass |

## Interpretation

The fixed-radius-like and stable/control cases pass the matched robustness gate.
The two variable-radius cases remain blocked, but the reason is now sharper:
the evidence does not support a time-zero-only explanation because geometry
changes occur without a time-shift delta when amplitude/frequency perturbations
are present.

## Decision

Use this matched gate in local 2D claim language:

```text
Stable and fixed-radius-like cases are robust under matched source/time-zero
rows. Broad variable-radius robustness remains blocked. The driver is not
time-zero alone.
```

Do not launch new FDTD, GPU work, field transfer, or field FWI from this result
alone.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_time_zero_matched_robustness_gate.py
sha256: deb476e798c4b0ae5e0d63bf3a80e6e86e98271ada52681c432865d3185a928f

test_local_2d_source_time_zero_matched_robustness_gate.py
sha256: b8ebd29f199ce25095350a781a73ff00f430e9d6e0877f0ae72002fc94e68c23
```

Subsequent local 2D source-robustness gate refreshes should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_matched_robustness_gate.py
2 passed
```

Figure check:

```text
local_2d_source_time_zero_matched_robustness_gate.png
1925x770, dynamic range=255
```
