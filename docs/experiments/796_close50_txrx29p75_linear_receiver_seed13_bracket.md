# Experiment 796: Close50 Tx/Rx 29.75 mm Linear Receiver Seed13 Bracket

Date: 2026-06-17

## Purpose

Bounded GPU bracket after experiments 793-795. Seed13 at linear 29.5 mm was
exact and strong but retained a one-grid-cell x ambiguity in the nominal row.
This run tests whether increasing the linearly interpolated Tx/Rx offset to
29.75 mm clears that known seed13 ambiguity before the nearest-sampled 30 mm
threshold.

```text
requested Tx/Rx offset: 29.75 mm
receiver sampling: linear
seed: 13
sources: 4
target: 2
```

This was a single bracket point, not a sweep.

## Output

```text
outputs/experiments/1274_coordinate_optimizer_close50_seed13_sources4_txrx29p75_linear_receiver_objectives
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
| nominal seed13 | 300 / 90 / 8.0 | 2.1984e-03 | `strong` | x = 300-301 mm, r = 8.0-8.0 mm |
| source-mismatch seed13 | 300 / 90 / 8.0 | 2.1334e-03 | `strong` | x = 300-300 mm, r = 8.0-8.0 mm |

Objective diagnostics:

```text
Base objective: selects truth for both cases.
Highband diagnostic: selects truth for both cases.
Highband margins: 1.3150e-03 and 1.5305e-03.
No radius-ambiguity revisit targets were triggered.
```

Runtime and resource envelope:

```text
elapsed time: 1510.1 s
monitored GPU utilization: peak 86%, below the requested 90% ceiling
monitored RAM use: peak 11.7%, below the requested 80% ceiling
```

## Interpretation

The seed13 bracket at 29.75 mm remains exact and strong, but it does not clear
the known nominal x ambiguity. Therefore, the sub-30 linear branch should not
be promoted to a clean below-30 threshold from this evidence.

The current paper-safe statement is:

```text
Linear-sampled close50 target2 seed13 remains x-ambiguous at both 29.5 and
29.75 mm. Nearest-sampled close50 target2 still has first clean replicated
support at 30 mm.
```

## Validation

Figure sanity:

```text
coordinate_confidence_margins.png: 1804x665 RGBA
coordinate_radius_decision_panel.png: 2126x1583 RGBA
coordinate_objective_radius_candidates.png: 2025x835 RGBA
system_scene_geometry.png: 1634x1028 RGBA
```
