# Experiment 501: Seed514229 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 967 aggregates the seed514229 target-specific branch after target2 needed
a 9-source rescue and target1 passed by a razor base margin.

## 967: Seed514229 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/967_seed514229_ringdown050_target_specific_rescue_summary
```

Source runs:

| Run | Target | Sources | Role | Base margin | Status |
| ---: | --- | ---: | --- | ---: | --- |
| 963 | target0 | 8 | control | 5.335991e-04 | accepted with late caveat |
| 964 | target2 | 5 | control | 4.482192e-04 | rejected weak control |
| 965 | target2 | 9 | rescue | 5.346563e-04 | accepted rescue |
| 966 | target1 | 5 | control | 5.006472e-04 | accepted razor |

## Results

Seed514229 is accepted after the target2 9-source rescue. The accepted branch
rows are 963, 965, and 966; rejected truth-preserving row 964 records the
failed target2 5-source control.

The branch remains low-reserve:

```text
target0: accepted at 8 sources; late margin below cutoff
target2: rejected at 5 sources, accepted at 9 sources; early_high still below cutoff
target1: accepted at 5 sources by +6.472349e-07; early_high below cutoff
```

## Artifacts

```text
data/seed514229_branch_summary.csv
data/seed514229_branch_summary.json
data/seed514229_objective_diagnostics.csv
figures/seed514229_base_margins_by_run.png
figures/seed514229_objective_margin_heatmap.png
figures/seed514229_target2_rescue_trend.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Validation

```text
summary JSON: parsed; row_count=4; diagnostic_row_count=24
accepted runs: 963, 965, 966
rejected truth-preserving runs: 964
branch summary CSV rows: 4
objective diagnostics CSV rows: 24
figure validation: base_margins=1824x960 RGBA nonwhite_fraction=0.574508; objective_heatmap=1824x936 RGBA nonwhite_fraction=0.647185; target2_rescue_trend=1536x960 RGBA nonwhite_fraction=0.026945
visual inspection: base-margin chart, objective heatmap, and source-density rescue trend are readable and decision-grade
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was free to continue with seed832040 target0
```

## Interpretation

The seed514229 branch is accepted, but the evidence is not as strong as the
seed196418 branch: target2 needed extra source density, target2 early_high
remained below cutoff after rescue, and target1 cleared the base cutoff by a
razor margin. Continue the Fibonacci replication chain to test whether this
low-reserve behavior repeats.

## Next Decision

Continue full-ringdown target-specific replication with seed832040 target0 at
8 sources.
