# Experiment 1381: Local 2D State-Consistent Margin Guard Audit

Date: 2026-06-27

## Purpose

Audit whether a simple wrong-minus-truth misfit margin guard can flag the
finite-margin failure states from runs `1376`-`1379` without rejecting the
corrected-state mechanism promoted by run `1380`.

This run does not rerun the optimizer, launch broad batches, run GPU work, use
field data, run field FWI, perform 3D/HPC work, or train neural networks.

## Output

```text
outputs/experiments/1381_local_2d_state_consistent_margin_guard_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_margin_guard_rows.csv
data/local_2d_state_consistent_margin_guard_thresholds.csv
data/local_2d_state_consistent_margin_guard_classifications.csv
data/local_2d_state_consistent_margin_guard_audit_summary.json
figures/local_2d_state_consistent_margin_guard_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_MARGIN_GUARD_AUDIT.md
scripts/run_local_2d_state_consistent_margin_guard_audit.py
scripts/test_local_2d_state_consistent_margin_guard_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source rows:                                      116
finite-margin rows:                               104
missing-margin rows:                              12
finite failure rows:                              26
finite correct-state rows:                        12
recommended threshold:                            0.0
recommended threshold captured failures:          26
recommended threshold flagged correct-state rows: 0
captures all finite failures:                     true
leaves corrected state unflagged:                 true
caution threshold:                                0.005
caution threshold flagged truth perturbations:    20
margin guard supported:                           true
finite-margin rows only:                          true
broad batch ready:                                false
GPU work ready:                                   false
field transfer ready:                             false
field FWI ready:                                  false
```

Threshold sweep:

| Threshold | Failure rows captured | Correct-state rows flagged | Truth-perturbation rows flagged | Captures all finite failures |
| ---: | ---: | ---: | ---: | --- |
| 0.0 | 26 | 0 | 0 | true |
| 0.001 | 26 | 0 | 3 | true |
| 0.002 | 26 | 0 | 4 | true |
| 0.005 | 26 | 0 | 20 | true |
| 0.01 | 26 | 1 | 40 | true |

## Interpretation

For rows where the wrong-minus-truth margin exists, the zero-threshold guard is
effective:

```text
if wrong_minus_truth_misfit <= 0, mark the selection uncertain
```

That rule catches all 26 observed finite-margin failures and does not flag the
corrected-state rows. This gives a clean confidence guard for the local 2D
state-consistency branch.

The rule is intentionally limited. It does not cover rows where the margin was
not computed, and it does not promote broad radius tolerance. A more cautious
threshold such as 0.005 catches the same failures but also flags 20
truth-selected perturbation rows, so it is better treated as an ambiguity flag,
not a hard acceptance rule.

## Decision

Add a finite-margin confidence guard to the local 2D state-consistency branch:

```text
For finite-margin audit rows, promote a selected geometry only when
wrong_minus_truth_misfit > 0.
```

If the margin is missing or non-positive, mark the case uncertain instead of
promoting it.

Keep broad local 2D batches, GPU work, field transfer, and field FWI blocked.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_margin_guard_audit.py
sha256: ddd52249a0ec854d1f48b5125aab383d6be8f988110c8700672ee780dd95d6ff

test_local_2d_state_consistent_margin_guard_audit.py
sha256: 0895dde0212c7e2b72f5fec6e83b465d322a1a9f8fdc7c5cb2f28db05453312e
```

Subsequent related local 2D state-consistency experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_margin_guard_audit.py
4 passed
```

Figure check:

```text
local_2d_state_consistent_margin_guard_audit.png
2680x845, dynamic range=255
```
