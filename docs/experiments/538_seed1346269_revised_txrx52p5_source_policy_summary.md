# Experiment 538: Seed1346269 Revised Tx/Rx=52.5 Source-Policy Summary

## Purpose

Run 1005 summarizes the revised seed1346269 policy after experiments
1000-1003 refined the older 973-978 branch.

## 1005: Seed1346269 Revised Tx/Rx=52.5 Source-Policy Summary

Output:

```text
outputs/experiments/1005_seed1346269_revised_txrx52p5_source_policy_summary
```

Source runs:

```text
973, 974, 975, 976, 977, 978, 1000, 1001, 1002, 1003
```

## Result

Revised target-specific policy:

```text
target0: run 1000, 8 sources, Tx/Rx=52.5, base accepted, late-window caveats
target2: run 1002, 7 sources, Tx/Rx=60, base accepted, early_high caveat
target1: run 1003, 5 sources, Tx/Rx=52.5, clean accepted
```

## Interpretation

The revised seed1346269 branch reduces source-density cost without hiding
caveats. Target0 improves from an 11-source accepted rescue to an 8-source
Tx/Rx=52.5 base-accepted row, but late-window diagnostics still fail. Target2
does not transfer to 5-source Tx/Rx=52.5, but 7-source Tx/Rx=60 is enough for
base acceptance with an early_high caveat. Target1 is clean at 5-source
Tx/Rx=52.5.

## Validation

```text
JSON parse: run_manifest.json and seed1346269_revised_policy_summary.json pass
CSV rows: policy rows=10, objective diagnostics=60
figure validation: four PNG figures are nonblank with nonzero dynamic range
visual inspection: policy bar chart, target0 trend, target2 trend, and objective heatmap are readable
figure notes: figures/FIGURE_NOTES.md present
resources: CPU-only summary while experiment 1004 kept the GPU active
```

## Next Decision

Continue with seed3524578 target0 at 8 sources and Tx/Rx=60.
