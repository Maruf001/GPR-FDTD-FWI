# Experiment 791: Close50 Tx/Rx 29.375 mm Effective-Offset Duplicate

Date: 2026-06-17

## Purpose

Narrow GPU bisection probe between the non-clean requested Tx/Rx 28.75 mm pilot
and the clean replicated requested Tx/Rx 30 mm aggregate. The intent was to test
whether the one-grid-cell x ambiguity cleared before the 30 mm point.

This was a single bounded GPU probe, not a broad sweep.

## Output

```text
outputs/experiments/1269_coordinate_optimizer_close50_seed21_sources4_txrx29p375_objectives
```

Artifacts:

```text
data/multi_rebar_coordinate_optimizer_summary.json
data/coordinate_confidence_report.csv
data/coordinate_objective_diagnostics.csv
data/coordinate_objective_top_candidates.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_2_candidates.csv
figures/coordinate_confidence_margins.png
figures/coordinate_radius_decision_panel.png
figures/coordinate_objective_radius_candidates.png
figures/system_scene_geometry.png
run_manifest.json
```

## Result

Final state:

```text
x = [190, 250, 300] mm
z = [90, 90, 90] mm
r = [6, 6, 8] mm
```

Confidence rows:

| Case | Best x/z/r | Margin | Confidence | Ambiguity |
| --- | --- | ---: | --- | --- |
| nominal seed21 | 300 / 90 / 8.0 | 1.2481e-03 | `strong` | x = 300-301 mm, r = 8.0-8.0 mm |
| source-mismatch seed21 | 300 / 90 / 8.0 | 1.5828e-03 | `strong` | x = 300-301 mm, r = 8.0-8.0 mm |

Objective diagnostics:

```text
Base objective: selects truth for both cases.
Highband diagnostic: selects truth for both cases.
No radius-ambiguity revisit targets were triggered.
```

Runtime and resource envelope:

```text
elapsed time: 1515.9 s
monitored GPU utilization: 81-86%, below the requested 90% ceiling
monitored RAM use: 11.3-11.6%, below the requested 80% ceiling
```

## Effective-Offset Check

With 1 mm grid spacing and `receiver_sampling=nearest`, requested Tx/Rx
28.75 mm and 29.375 mm both map to the same receiver indices:

| Requested Tx/Rx | Receiver indices | Effective offsets |
| ---: | --- | --- |
| 28.75 mm | `[109, 237, 373, 509]` | `[29, 29, 29, 29]` mm |
| 29.375 mm | `[109, 237, 373, 509]` | `[29, 29, 29, 29]` mm |
| 30.0 mm | `[110, 238, 374, 510]` | `[30, 30, 30, 30]` mm |

The confidence and objective rows for 29.375 mm are numerically identical to
the 28.75 mm run, so this is not independent threshold evidence.

## Interpretation

Do not add more requested-offset bisection runs between 28.75 mm and 30 mm
under the current nearest-sampled 1 mm grid. They will either duplicate the
effective 29 mm receiver geometry or jump to the effective 30 mm geometry.

The useful conclusion is methodological: the close50 threshold is currently
resolved at the effective receiver-index level, not at arbitrary sub-millimeter
requested Tx/Rx offsets. To study the transition inside the 29-30 mm effective
gap, use linear receiver interpolation or a finer grid, then rerun a deliberately
small pilot.

The policy table from experiment 790 should remain the active close50 threshold
policy; experiment 791 is a duplicate-effective-geometry check.
