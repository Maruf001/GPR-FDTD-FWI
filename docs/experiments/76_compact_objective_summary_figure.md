# Experiment 76: Compact Objective Summary Figure

## Purpose

Replace the ultra-wide objective diagnostic plot from run 532 with a compact
report-ready summary figure while keeping the row-level CSV/JSON artifacts as
the audit trail.

## 543: Compact Objective Summary Figure

Output:

```text
outputs/experiments/543_compact_objective_summary_figure
```

Command:

```text
CPU-only one-off Python plotting script reading the run 505, 531, and 532
coordinate objective diagnostic JSON files and writing compact CSV and PNG
artifacts under run 543.
```

Inputs:

```text
outputs/experiments/505_variable_depth_radius_all_targets_txrx50_objective_confidence_report/data/coordinate_objective_diagnostic_report.json
outputs/experiments/531_variable_depth_radius_all_targets_three_seed_txrx50_ringdown025_objective_confidence_report/data/coordinate_objective_diagnostic_report.json
outputs/experiments/532_variable_depth_radius_txrx50_all_condition_objective_confidence_report/data/coordinate_objective_diagnostic_report.json
```

Artifacts:

```text
data/compact_objective_summary.csv
figures/compact_objective_summary.png
figures/FIGURE_NOTES.md
run_manifest.json
```

CSV metrics:

```text
Non-ringdown Tx/Rx=50: rows=18, truth=18, geometry_changes=0,
  veryhigh ratio min/mean/max=1.482/1.803/2.563,
  base labels weak/moderate/strong=15/3/0,
  veryhigh labels weak/moderate/strong=5/11/2,
  base max radius ambiguity=0.25 mm, veryhigh max radius ambiguity=0.0 mm.

Fitted ringdown: rows=9, truth=9, geometry_changes=0,
  veryhigh ratio min/mean/max=1.058/1.231/1.403,
  base labels weak/moderate/strong=1/7/1,
  veryhigh labels weak/moderate/strong=0/6/3,
  base max radius ambiguity=0.0 mm, veryhigh max radius ambiguity=0.0 mm.

All condition: rows=27, truth=27, geometry_changes=0,
  veryhigh ratio min/mean/max=1.058/1.612/2.563,
  base labels weak/moderate/strong=16/10/1,
  veryhigh labels weak/moderate/strong=5/17/5,
  base max radius ambiguity=0.25 mm, veryhigh max radius ambiguity=0.0 mm.
```

Plot validation:

```text
compact_objective_summary.png: 2160x864 px, min=0, max=255,
dynamic range=255, pixel std=70.5278.
```

## Interpretation

The compact figure preserves the main run 532 decision: veryhigh improves the
objective margin in every selected non-ringdown, fitted-ringdown, and combined
Tx/Rx=50 mm variable-depth/variable-radius row, improves confidence labels, and
does not change the recovered truth geometry.

Use run 543 for report layout and use run 532 for row-level audit details. Keep
the base objective as the production coordinate update rule; veryhigh remains a
branch-level reporting diagnostic, not a globally promoted optimizer objective.

## Next Decision

Continue reporting/packaging work unless a concrete physics gap appears in the
handoff matrix. No GPU run is queued by this result.
