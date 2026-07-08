# Experiment 879: Local 2D Source/Time-Zero Matched Factorization

Date: 2026-06-25

## Purpose

Refine the run `146` source/time-zero selected replay by comparing only matched
nominal/source-mismatch rows within the same target, pass, step, and objective.

This corrects the case-level geometry span interpretation: the previous
120-126 mm spans mixed different target indices. The matched audit asks a
cleaner question:

```text
When the target/objective context is held fixed, how much does the geometry
decision move under the source/time-zero/source-amplitude perturbation?
```

This is cached analysis only. It does not run new FDTD, GPU work, field
transfer, field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/159_local_2d_source_time_zero_matched_factorization
```

Key artifacts:

```text
data/local_2d_source_time_zero_matched_pair_deltas.csv
data/local_2d_source_time_zero_matched_factorization_cases.csv
data/local_2d_source_time_zero_matched_factorization_summary.json
docs/LOCAL_2D_SOURCE_TIME_ZERO_MATCHED_FACTORIZATION.md
figures/local_2d_source_time_zero_matched_factorization.png
scripts/run_local_2d_source_time_zero_matched_factorization.py
scripts/test_local_2d_source_time_zero_matched_factorization.py
scripts/script_snapshot_manifest.json
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
max frequency-scale delta percent:      10.000000000000009
time-zero-only explanation ready:       false
new FDTD ready:                         false
GPU work ready:                         false
field transfer ready:                   false
```

## Case Findings

| Category | Matched pairs | Changed pairs | Max geometry delta mm | Driver assessment |
| --- | ---: | ---: | ---: | --- |
| max amplitude stress | 6 | 2 | 5.0 | amplitude/frequency effect without time-shift observed |
| max geometry instability | 10 | 6 | 3.3541019662496847 | amplitude/frequency effect without time-shift observed |
| stable high time shift | 2 | 0 | 0.0 | matched geometry stable |
| fixed-radius-like close14 | 2 | 0 | 0.0 | matched geometry stable |
| low source-effect control | 0 | 0 | 0.0 | matched geometry stable |

## Interpretation

The matched audit tightens the local 2D source/time-zero result:

```text
The earlier 126 mm case span should not be read as direct source/time-zero
geometry movement; it mixed different targets.
```

After matching target/objective context, the largest observed movement is 5 mm,
and the close10/close14/control cases remain geometry-stable. However, two
variable-radius cases still move under matched source perturbations.

Because both changed cases include geometry changes where the time-shift delta
is zero but amplitude/frequency changes are present, a time-zero-only
explanation is not supported.

## Decision

Use this matched audit to tighten claim language. The current defensible
statement is:

```text
Fixed-radius-like and stable cases are robust under matched source/time-zero
rows, but broad variable-radius robustness remains blocked. The driver is not
time-zero alone; source amplitude/frequency perturbations are implicated.
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

Subsequent local 2D source-robustness experiments should start from a
duplicated run-specific script.

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
