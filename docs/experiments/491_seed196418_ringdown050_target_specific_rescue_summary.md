# Experiment 491: Seed196418 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 957 closes the seed196418 branch after target1 required a 9-source rescue.
It aggregates completed coordinate-optimizer outputs into branch-level
CSV/JSON tables and decision figures; it does not launch a new FDTD scene.

## 957: Seed196418 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/957_seed196418_ringdown050_target_specific_rescue_summary
```

Source runs:

```text
953: target0, sources=8, ringdown050
954: target2, sources=5, ringdown050
955: target1, sources=5, ringdown050, weak control
956: target1, sources=9, ringdown050, rescue
```

## Results

Seed196418 is accepted after a target1 9-source rescue:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 953 | 8 | 6.119611e-04 | +1.120e-04 | accepted |
| target2 | 954 | 5 | 6.784989e-04 | +1.785e-04 | accepted |
| target1 | 956 | 9 | 5.895553e-04 | +8.956e-05 | accepted rescue |

Rejected rows: 955.

The target1 rescue trend is the key branch result: target1 increases from
4.809369e-04 at 5 sources to 5.895553e-04 at 9 sources, and all six objective
variants are above cutoff in the rescue row.

## Artifacts

```text
data/seed196418_branch_summary.csv
data/seed196418_branch_summary.json
data/seed196418_objective_diagnostics.csv
figures/seed196418_base_margins_by_run.png
figures/seed196418_objective_margin_heatmap.png
figures/seed196418_target1_rescue_trend.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Validation

```text
summary JSON: parsed; row_count=4; diagnostic_row_count=24
accepted runs: 953, 954, 956
rejected truth-preserving runs: 955
branch summary CSV rows: 4
objective diagnostics CSV rows: 24
base margins figure: 1824x960 RGBA, nonwhite_fraction=0.533219
objective heatmap: 1824x936 RGBA, nonwhite_fraction=0.647597
target1 rescue trend: 1536x960 RGBA, nonwhite_fraction=0.029429
visual inspection: all three figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present
resources: no new FDTD scene; GPU moved to seed317811 target0
```

## Next Decision

Continue full-ringdown target-specific replication with seed317811 target0 at
8 sources. That run is underway as experiment 958.
