# Local 2D Matched Source/Time-Zero Robustness Gate Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records output `160`, the matched robustness gate built from
run `159`.

No new FDTD, GPU work, field transfer, field FWI, or neural-network training was
launched.

## Output

```text
outputs/summary_tables/160_local_2d_source_time_zero_matched_robustness_gate
```

Tracked note:

```text
docs/experiments/880_local_2d_source_time_zero_matched_robustness_gate.md
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

## Decision

Use output `160` as the current local 2D source/time-zero claim gate. Stable and
fixed-radius-like cases are robust under matched rows; broad variable-radius
robustness is still blocked, and the driver is not time-zero alone.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_time_zero_matched_robustness_gate.py
sha256: deb476e798c4b0ae5e0d63bf3a80e6e86e98271ada52681c432865d3185a928f

test_local_2d_source_time_zero_matched_robustness_gate.py
sha256: b8ebd29f199ce25095350a781a73ff00f430e9d6e0877f0ae72002fc94e68c23
```

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

Marathon status: active. The next defensible branch is to refresh the
presentation/team evidence with the matched gate and then add outputs `159-160`
to the snapshot audit.
