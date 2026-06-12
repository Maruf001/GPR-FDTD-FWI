# Experiment 513: Seed1346269 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 979 summarizes the seed1346269 full-ringdown target-specific branch after
target0 and target2 needed source-density rescues while target1 passed at
5 sources.

## 979: Seed1346269 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/979_seed1346269_ringdown050_target_specific_rescue_summary
```

Source runs:

```text
973: target0, sources=8, ringdown050, weak control
974: target0, sources=9, ringdown050, weak rescue
975: target0, sources=11, ringdown050, accepted rescue
976: target2, sources=5, ringdown050, weak control
977: target2, sources=9, ringdown050, accepted rescue
978: target1, sources=5, ringdown050, accepted control
```

This is an aggregation run. It does not launch a new FDTD scene; it parses
completed optimizer outputs into branch-level CSV/JSON tables and summary
figures.

## Results

Seed1346269 is accepted after target-specific source-density rescue:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 975 | 11 | 5.043091e-04 | +4.309e-06 | accepted 11-source rescue with late caveat |
| target2 | 977 | 9 | 5.640543e-04 | +6.405e-05 | accepted 9-source rescue |
| target1 | 978 | 5 | 5.202575e-04 | +2.026e-05 | accepted 5-source control |

Rejected truth-preserving rows:

```text
973: target0 8-source weak control
974: target0 9-source weak rescue
976: target2 5-source weak control
```

## Interpretation

The seed1346269 branch is truth-preserving across all tested rows, but the
source-density requirement is target-dependent. Target0 is the fragile case: it
needs 11 sources and retains late-window caveats even after acceptance. Target2
is rescued cleanly at 9 sources. Target1 passes without escalation.

## Artifacts

```text
data/seed1346269_branch_summary.csv
data/seed1346269_branch_summary.json
data/seed1346269_objective_diagnostics.csv
figures/seed1346269_base_margins_by_run.png
figures/seed1346269_objective_margin_heatmap.png
figures/seed1346269_target0_rescue_trend.png
figures/seed1346269_target2_rescue_trend.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Validation

```text
summary JSON: parsed; row_count=6; diagnostic_row_count=36
accepted runs: 975, 977, 978
rejected truth-preserving runs: 973, 974, 976
branch summary CSV rows: 6
objective diagnostics CSV rows: 36
figure validation: seed1346269_base_margins_by_run.png=1920x960 RGBA nonwhite_fraction=0.513159; seed1346269_objective_margin_heatmap.png=1920x1008 RGBA nonwhite_fraction=0.598542; seed1346269_target0_rescue_trend.png=1536x960 RGBA nonwhite_fraction=0.041249; seed1346269_target2_rescue_trend.png=1536x960 RGBA nonwhite_fraction=0.040291
visual inspection: base-margin overview, objective heatmap, target0 rescue trend, and target2 rescue trend are readable with cutoff lines and labels in useful positions
figure notes: figures/FIGURE_NOTES.md present
resources: no new FDTD scene; GPU can move to seed2178309 target0
```

## Next Decision

Continue full-ringdown target-specific replication with seed2178309 target0 at
8 sources. That run is underway as experiment 980.
