# Experiment 764: Recent Target1/Target2 Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only aggregation of the recent exact-but-weak target1 and target2 decision
branches after the local 2026-06-17 follow-up probes. This synthesis asks
whether the new target1 Tx/Rx=52.5 and target2 Tx/Rx=50 probes change the
confidence policy.

No FDTD, FWI, or GPU command was run for this synthesis.

## Output

```text
outputs/experiments/1227_coordinate_confidence_recent_target1_target2_policy_synthesis
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

The aggregation reads 17 coordinate-optimizer summary JSON files:

```text
target1 seed5527939710754757: runs 1216, 1217, 1218, 1223
target1 seed610:              runs 897, 899, 898, 1224
target2 seed20365011074:      runs 1090, 1091, 1092, 1093, 1225
target2 seed308061521720129:  runs 1184, 1185, 1186, 1226
```

## Result

Aggregate counts:

```text
rows:                 17
truth-geometry rows:  17
weak rows:            16
moderate rows:         1
x-ambiguity rows:      0
max ambiguity widths:  x=0 mm, z=0 mm, radius=0 mm
```

Per-target summary:

| Target | Rows | Exact geometry | Weak | Moderate | Mean margin | Max margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| target1 | 8 | 8 | 8 | 0 | 4.437210e-4 | 4.962451e-4 |
| target2 | 9 | 9 | 8 | 1 | 4.719057e-4 | 5.181019e-4 |

Acquisition summary for the recent branches:

| Acquisition | Rows | Exact geometry | Mean margin | Max margin |
| --- | ---: | ---: | ---: | ---: |
| 5 sources, Tx/Rx 50 mm | 2 | 2 | 4.944079e-4 | 5.181019e-4 |
| 5 sources, Tx/Rx 52.5 mm | 2 | 2 | 4.697186e-4 | 4.962451e-4 |
| 5 sources, Tx/Rx 60 mm | 4 | 4 | 4.766640e-4 | 4.964072e-4 |
| 7 sources, Tx/Rx 60 mm | 2 | 2 | 4.625907e-4 | 4.743122e-4 |
| 8 sources, Tx/Rx 60 mm | 1 | 1 | 4.205166e-4 | 4.205166e-4 |
| 9 sources, Tx/Rx 60 mm | 4 | 4 | 4.624328e-4 | 4.981292e-4 |
| 11 sources, Tx/Rx 60 mm | 2 | 2 | 3.832907e-4 | 4.033775e-4 |

## Interpretation

The recent probes sharpen the policy:

1. Target1 remains exact-but-unresolved under the strict base-margin rule.
   Tx/Rx=52.5 improves seed610 to a near miss, but neither tested target1
   branch crosses `5.0e-4`.
2. Target2 Tx/Rx=50 is branch-sensitive. It rescues seed20365011074, but it
   fails to rescue seed308061521720129.
3. Source-count escalation is not monotonic. The 11-source rows are both weak
   and worse than the best 5/9-source alternatives.
4. The current ambiguity is radius-confidence reserve, not x/z/r point recovery
   or lateral separability. Every recent row is exact and has zero reported
   x/z/r ambiguity width.

## Policy Update

For manuscript or report language:

```text
Exact geometry and strict confidence should be reported separately.
Target1 weak branches should stay exact-but-unresolved unless the base margin
clears the cutoff.
Target2 Tx/Rx=50 may be tested once on near-miss branches, but successful and
failed replications must both be reported.
Do not treat more sources as a default rescue after a 9-source near miss.
```

## Validation

Both aggregate figures were validated as nonblank:

```text
coordinate_confidence_aggregate.png nonwhite=0.1371
coordinate_ambiguity_widths.png nonwhite=0.0960
```
