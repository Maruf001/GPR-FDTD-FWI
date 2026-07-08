# Local 2D Source/Time-Zero Matched Factorization Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records output `159`, a matched-pair audit of the local 2D
source/time-zero sensitivity branch.

The run reuses cached diagnostics from run `146` and performs no new FDTD, GPU
work, field transfer, field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/159_local_2d_source_time_zero_matched_factorization
```

Tracked note:

```text
docs/experiments/879_local_2d_source_time_zero_matched_factorization.md
```

## Result

```text
selected cases:                         5
matched pairs:                          20
matched geometry-changed cases:         2
matched geometry-stable cases:          3
changed without time-shift cases:       2
prior max unmatched geometry span mm:   126.12394697280925
max matched geometry delta mm:          5.0
max radius delta mm:                    2.5
max time-shift delta ps:                50.0
max amplitude delta percent:            15.474560561251682
time-zero-only explanation ready:       false
new FDTD ready:                         false
GPU work ready:                         false
field transfer ready:                   false
```

## Interpretation

The previous source/time-zero selected replay overstated geometry movement if
read naively, because its largest spans mixed different target indices. The
matched audit is stricter: within the same target/pass/objective, the largest
movement is 5 mm.

The robustness boundary still does not disappear. Two variable-radius cases
show matched geometry changes, while the close10/close14/control cases remain
stable. A time-zero-only explanation is blocked because geometry changes are
observed without a time-shift delta when amplitude/frequency perturbations are
present.

## Decision

Tighten the local 2D claim language:

```text
Stable and fixed-radius-like cases pass matched source/time-zero robustness.
Broad variable-radius robustness remains blocked, and the driver is not
time-zero alone.
```

Do not launch new FDTD, GPU work, field transfer, or field FWI from this result
alone.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_time_zero_matched_factorization.py
sha256: bd3c8ae7a4e4ea885875659b2f2a5d4d4d85d2b990d39bad8052ed4575d513cd

test_local_2d_source_time_zero_matched_factorization.py
sha256: 64aee1bc6c9ecfeb242e7ac746f1b4203910f951a62b34cae0219682a3bd1bc3
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_matched_factorization.py
4 passed
```

Figure check:

```text
local_2d_source_time_zero_matched_factorization.png
2428x778, dynamic range=255
```

Marathon status: active. The next defensible branch is to refresh the source
robustness gate/presentation pack with the matched-factorization correction or
add this milestone to the snapshot audit.
