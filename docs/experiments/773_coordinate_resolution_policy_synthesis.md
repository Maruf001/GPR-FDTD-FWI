# Experiment 773: Coordinate Resolution Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only synthesis of the existing close-spacing acquisition-resolution
aggregates. This ties together the older 270/280-era close50 branch, the later
close50 Tx/Rx25 completion in experiment 760, and the tighter close30/28/25/20/15/14
spacing aggregates.

No FDTD, FWI, optimizer, or GPU command was run.

## Output

```text
outputs/experiments/1239_coordinate_resolution_policy_synthesis
```

Primary artifacts:

```text
data/coordinate_resolution_policy_groups.csv
data/coordinate_resolution_policy_by_txrx.csv
data/coordinate_resolution_policy_by_spacing.csv
data/coordinate_resolution_policy_summary.json
figures/coordinate_resolution_policy.png
```

## Result

The synthesis classifies 15 acquisition/spacing groups:

| Policy label | Groups |
| --- | ---: |
| `clean_replicated` | 12 |
| `truth_selected_interval` | 2 |
| `mixed_or_failed` | 1 |

Key policy rows:

| Tx/Rx offset | Tested spacings | Clean spacings | Interval spacings | Mixed/failed spacings | Closest clean spacing |
| ---: | --- | --- | --- | --- | ---: |
| 25 mm | 50 | none | none | 50 | none |
| 30 mm | 50 | 50 | none | none | 50 mm |
| 35 mm | 50, 45, 40, 35, 30, 28 | 50, 45, 40, 35, 30 | 28 | none | 30 mm |
| 40 mm | 50, 25 | 50 | 25 | none | 50 mm |
| 45 mm | 28, 25, 20, 15, 14 | 28, 25, 20, 15, 14 | none | none | 14 mm |

The branch-level decision from the generated summary is:

```text
Existing aggregate evidence keeps 35 mm Tx/Rx at close30 as the standard
clean replicated limit, while 45 mm Tx/Rx extends clean replication to close14
in the tested branch. Close50 at Tx/Rx25 is mixed/ambiguous, and close28 at
Tx/Rx35 remains interval-supported.
```

## Interpretation

This resolves the concern around the old output experiments 270 and 280:
those were not weak points by themselves. The real decision was the surrounding
acquisition-resolution envelope. The archive now supports a clearer paper
statement:

```text
For the tested target2 close-spacing branch with 4 sources, the clean spacing
limit depends strongly on Tx/Rx offset. The 35 mm acquisition is clean down to
close30 but not close28. The 45 mm acquisition is clean through close14 in the
tested branch. Truth selection alone is not enough; interval-supported rows
must stay separate from clean replicated rows.
```

This complements the current target1 confidence-policy work. It should not
trigger more close50 Tx/Rx25 GPU work unless the paper specifically needs a
finer 25-30 mm acquisition threshold.

## Validation

```text
tests/test_coordinate_resolution_policy_synthesis.py: 6 passed
coordinate_resolution_policy.png: nonwhite=0.0799, dynamic range=255
```
