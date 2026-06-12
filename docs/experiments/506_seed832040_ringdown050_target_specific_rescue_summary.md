# Experiment 506: Seed832040 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 972 aggregates the seed832040 target-specific branch after target1 needed
a 9-source rescue.

## 972: Seed832040 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/972_seed832040_ringdown050_target_specific_rescue_summary
```

Source runs:

| Run | Target | Sources | Role | Base margin | Status |
| ---: | --- | ---: | --- | ---: | --- |
| 968 | target0 | 8 | control | 5.090708e-04 | accepted with late caveat |
| 969 | target2 | 5 | control | 5.592987e-04 | accepted clean |
| 970 | target1 | 5 | control | 3.952201e-04 | rejected weak control |
| 971 | target1 | 9 | rescue | 5.167231e-04 | accepted rescue |

## Results

Seed832040 is accepted after the target1 9-source rescue. The accepted branch
rows are 968, 969, and 971; rejected truth-preserving row 970 records the
failed target1 5-source control.

The branch remains low-reserve:

```text
target0: accepted at 8 sources; late margin below cutoff
target2: accepted cleanly at 5 sources
target1: rejected at 5 sources, accepted at 9 sources; all diagnostics clear after rescue
```

## Artifacts

```text
data/seed832040_branch_summary.csv
data/seed832040_branch_summary.json
data/seed832040_objective_diagnostics.csv
figures/seed832040_base_margins_by_run.png
figures/seed832040_objective_margin_heatmap.png
figures/seed832040_target1_rescue_trend.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Validation

```text
summary JSON: parsed; row_count=4; diagnostic_row_count=24
accepted runs: 968, 969, 971
rejected truth-preserving runs: 970
branch summary CSV rows: 4
objective diagnostics CSV rows: 24
figure validation: base_margins=1824x960 RGBA nonwhite_fraction=0.507832; objective_heatmap=1824x936 RGBA nonwhite_fraction=0.588033; target1_rescue_trend=1536x960 RGBA nonwhite_fraction=0.037166
visual inspection: base-margin chart, objective heatmap, and target1 source-density rescue trend are readable and decision-grade
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was free to continue with seed1346269 target0
```

## Interpretation

Seed832040 is accepted, but the evidence is caveated by two low-reserve rows:
target0 clears the base cutoff by only 9.071e-06 with a late-window caveat,
and target1 needs 9 sources to clear the base cutoff by 1.672e-05. Continue
the Fibonacci replication chain to test whether this source-density rescue
pattern persists.

## Next Decision

Continue full-ringdown target-specific replication with seed1346269 target0 at
8 sources.
