# Experiment 496: Seed317811 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 962 closes the seed317811 branch after target2 required a 9-source rescue.
It aggregates completed coordinate-optimizer outputs into branch-level
CSV/JSON tables and decision figures; it does not launch a new FDTD scene.

## 962: Seed317811 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/962_seed317811_ringdown050_target_specific_rescue_summary
```

Source runs:

```text
958: target0, sources=8, ringdown050
959: target2, sources=5, ringdown050, weak control
960: target2, sources=9, ringdown050, rescue
961: target1, sources=5, ringdown050
```

## Results

Seed317811 is accepted after a target2 9-source rescue:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 958 | 8 | 5.875666e-04 | +8.757e-05 | accepted with late caveat |
| target2 | 960 | 9 | 5.095658e-04 | +9.566e-06 | accepted rescue |
| target1 | 961 | 5 | 6.017320e-04 | +1.017e-04 | accepted |

Rejected rows: 959.

The branch is truth-preserving on all rows, but it is not high-reserve:
target0 carries late/late_high caveats and target2 rescue clears base by only
9.57e-06 with early_high still below cutoff.

## Artifacts

```text
data/seed317811_branch_summary.csv
data/seed317811_branch_summary.json
data/seed317811_objective_diagnostics.csv
figures/seed317811_base_margins_by_run.png
figures/seed317811_objective_margin_heatmap.png
figures/seed317811_target2_rescue_trend.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Validation

```text
summary JSON: parsed; row_count=4; diagnostic_row_count=24
accepted runs: 958, 960, 961
rejected truth-preserving runs: 959
branch summary CSV rows: 4
objective diagnostics CSV rows: 24
base margins figure: 1824x960 RGBA, nonwhite_fraction=0.557173
objective heatmap: 1824x936 RGBA, nonwhite_fraction=0.647197
target2 rescue trend: 1536x960 RGBA, nonwhite_fraction=0.032054
visual inspection: all three figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present
resources: no new FDTD scene; GPU moved to seed514229 target0
```

## Next Decision

Continue full-ringdown target-specific replication with seed514229 target0 at
8 sources. That run is underway as experiment 963.
