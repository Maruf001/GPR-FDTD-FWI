# Experiment 528: Seed2178309 Tx/Rx=52.5 Acquisition-Policy Summary

## Purpose

Run 994 consolidates the seed2178309 target1 Tx/Rx offset bracket and the
all-target Tx/Rx=52.5 validation. It is an infrastructure/reporting summary
over completed production runs 982 and 987-993.

## 994: Seed2178309 Tx/Rx=52.5 Acquisition-Policy Summary

Output:

```text
outputs/experiments/994_seed2178309_txrx52p5_acquisition_policy_summary
```

Source runs:

```text
target1 offset sweep: 982, 987, 988, 989, 990, 991
all-target Tx/Rx=52.5 validation: 992, 991, 993
```

Generated artifacts:

```text
data/seed2178309_txrx52p5_policy_summary.json
data/seed2178309_txrx_policy_rows.csv
data/seed2178309_txrx_policy_objective_diagnostics.csv
figures/seed2178309_target1_txrx_offset_sweep.png
figures/seed2178309_txrx52p5_all_target_margins.png
figures/seed2178309_txrx52p5_objective_heatmap.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

Target1 offset policy:

```text
accepted_offsets_mm: [50.0, 52.5, 55.0]
rejected_offsets_mm: [45.0, 57.5, 60.0]
best_tested_offset_mm: 52.5
best_tested_run_id: 991
best_tested_margin: 5.111159e-04
```

All-target Tx/Rx=52.5 policy:

```text
target0: run 992, 8 sources, base margin 5.058533e-04
target1: run 991, 5 sources, base margin 5.111159e-04
target2: run 993, 5 sources, base margin 5.993183e-04
status: base_accepted_all_targets_with_target0_late_window_caveat_and_target1_early_high_caveat
```

Diagnostic caveats:

```text
target0 late:      3.338621e-04
target0 late_high: 4.289770e-04
target1 early_high: 4.645839e-04
target2: all diagnostic objective margins above cutoff
```

## Interpretation

Seed2178309 target1 was not rescued by source-density escalation at Tx/Rx=60,
but it was rescued by acquisition offset. The accepted band among tested
offsets is 50-55 mm, with Tx/Rx=52.5 the strongest sampled point. The same
Tx/Rx=52.5 setting is base-accepted for target0, target1, and target2, so the
branch should move to cross-seed transfer instead of adding more seed2178309
source-density runs.

## Validation

```text
JSON parse: run_manifest.json and seed2178309_txrx52p5_policy_summary.json pass
CSV rows: policy rows=8, objective diagnostics=48
summary integrity: row_count=8 and diagnostic_row_count=48 in summary JSON
figure validation:
  seed2178309_target1_txrx_offset_sweep.png is 1600x960 RGBA with nonwhite_fraction=0.031337 and nonzero dynamic range
  seed2178309_txrx52p5_all_target_margins.png is 1440x880 RGBA with nonwhite_fraction=0.543216 and nonzero dynamic range
  seed2178309_txrx52p5_objective_heatmap.png is 1440x928 RGBA with nonwhite_fraction=0.683794 and nonzero dynamic range
visual inspection: all three figures are readable; the heatmap clearly marks target0 late-window deficits, target1 early_high deficit, and clean target2 reserves
figure notes: figures/FIGURE_NOTES.md present and explains all three figures
resources: summary generation used CPU only; the next production GPU run was launched immediately afterward to keep hardware utilization high
```

## Next Decision

Run seed832040 target1 at Tx/Rx=52.5 with 5 sources. That branch is useful
because seed832040 target1 was weak at the Tx/Rx=60 5-source control and
accepted only after a 9-source rescue.
