# Experiment 765: Target0 Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only aggregation of the target0 exact-geometry confidence branches after
the close-spacing coordinate optimizer campaign. This synthesis checks whether
target0 has a repeatable acquisition policy or whether its apparent rescues are
seed- and branch-dependent.

No FDTD, FWI, or GPU command was run for this synthesis.

## Output

```text
outputs/experiments/1228_coordinate_confidence_target0_policy_synthesis
```

Artifacts:

```text
data/coordinate_confidence_aggregate.csv
data/coordinate_confidence_aggregate.json
figures/coordinate_confidence_aggregate.png
figures/coordinate_ambiguity_widths.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Inputs

The aggregation reads 18 coordinate-optimizer summary JSON files:

```text
seed121393:       runs 949, 950, 951
seed1346269:      runs 973, 974, 975, 1000
seed14930352:     runs 1023, 1024, 1025, 1026
seed7778742049:   runs 1079, 1080, 1081
seed365435296162: runs 1120, 1121, 1122, 1123
```

## Result

Aggregate counts:

```text
rows:                 18
truth-geometry rows:  18
weak rows:            13
moderate rows:         5
x-ambiguity rows:      0
max ambiguity widths:  x=0 mm, z=0 mm, radius=0 mm
```

Per-seed summary:

| Seed | Rows | Exact geometry | Weak | Moderate | Mean margin | Max margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 121393 | 3 | 3 | 3 | 0 | 4.649196e-4 | 4.911751e-4 |
| 1346269 | 4 | 4 | 2 | 2 | 5.032654e-4 | 5.368229e-4 |
| 14930352 | 4 | 4 | 4 | 0 | 4.764917e-4 | 4.932234e-4 |
| 365435296162 | 4 | 4 | 2 | 2 | 4.974589e-4 | 5.281512e-4 |
| 7778742049 | 3 | 3 | 2 | 1 | 4.884401e-4 | 5.583698e-4 |

Acquisition summary:

| Acquisition | Rows | Exact geometry | Weak | Moderate | Mean margin | Max margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 sources, Tx/Rx 45 mm | 1 | 1 | 0 | 1 | 5.281512e-4 | 5.281512e-4 |
| 8 sources, Tx/Rx 50 mm | 1 | 1 | 0 | 1 | 5.049557e-4 | 5.049557e-4 |
| 8 sources, Tx/Rx 52.5 mm | 4 | 4 | 3 | 1 | 4.897574e-4 | 5.368229e-4 |
| 8 sources, Tx/Rx 60 mm | 5 | 5 | 5 | 0 | 4.766500e-4 | 4.991587e-4 |
| 9 sources, Tx/Rx 60 mm | 4 | 4 | 3 | 1 | 5.001938e-4 | 5.583698e-4 |
| 11 sources, Tx/Rx 60 mm | 3 | 3 | 2 | 1 | 4.642603e-4 | 5.043091e-4 |

Best row per seed:

| Seed | Best acquisition | Margin | Confidence |
| --- | --- | ---: | --- |
| 121393 | 9 sources, Tx/Rx 60 mm | 4.911751e-4 | weak |
| 1346269 | 8 sources, Tx/Rx 52.5 mm | 5.368229e-4 | moderate |
| 14930352 | 8 sources, Tx/Rx 60 mm | 4.932234e-4 | weak |
| 365435296162 | 8 sources, Tx/Rx 45 mm | 5.281512e-4 | moderate |
| 7778742049 | 9 sources, Tx/Rx 60 mm | 5.583698e-4 | moderate |

## Interpretation

Target0 is exact in every audited row, but the confidence reserve is still
branch-dependent. The strongest row is seed7778742049 at 9 sources and Tx/Rx
60 mm, while seed365435296162 prefers a lower 45 mm offset and seed1346269
prefers 52.5 mm. Two seeds, 121393 and 14930352, remain weak across the
available target0 branches.

This supports the same manuscript policy used for target1 and target2:
truth-geometry recovery and strict confidence should be reported separately.
For target0, the unresolved part is not point recovery or x/z/r ambiguity
width; it is the radius-margin reserve against a near-best competitor.

## Resource-Cap Decision

The natural next synthetic probe would be another target0 acquisition branch
for the two all-weak seeds. I did not launch it here because the relevant
8/9/11-source coordinate optimizer runs have historically used GPU levels near
or above the current 90% cap. Until a resource-safe limiter or a narrower CPU
reducer is available, target0 follow-up should stay in CPU-side synthesis and
planning rather than broad GPU execution.

## Validation

Both aggregate figures were validated as nonblank:

```text
coordinate_confidence_aggregate.png nonwhite=0.1470
coordinate_ambiguity_widths.png nonwhite=0.0942
```
