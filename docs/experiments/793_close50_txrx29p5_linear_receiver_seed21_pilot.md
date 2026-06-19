# Experiment 793: Close50 Tx/Rx 29.5 mm Linear Receiver Seed21 Pilot

Date: 2026-06-17

## Purpose

Single bounded GPU pilot following the effective-offset policy in experiment
792. Nearest receiver sampling cannot resolve requested sub-millimeter offsets
between effective 29 and 30 mm on the 1 mm grid, so this run tests one
linearly interpolated receiver offset inside that gap:

```text
requested Tx/Rx offset: 29.5 mm
effective receiver offset: [29.5, 29.5, 29.5, 29.5] mm
receiver sampling: linear
seed: 21
sources: 4
target: 2
```

This was not a broad sweep or replicated aggregate.

## Output

```text
outputs/experiments/1271_coordinate_optimizer_close50_seed21_sources4_txrx29p5_linear_receiver_objectives
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
| nominal seed21 | 300 / 90 / 8.0 | 1.4692e-03 | `strong` | x = 300-300 mm, r = 8.0-8.0 mm |
| source-mismatch seed21 | 300 / 90 / 8.0 | 1.8459e-03 | `strong` | x = 300-300 mm, r = 8.0-8.0 mm |

Objective diagnostics:

```text
Base objective: selects truth for both cases.
Highband diagnostic: selects truth for both cases.
No radius-ambiguity revisit targets were triggered.
```

Runtime and resource envelope:

```text
elapsed time: 1549.7 s
monitored GPU utilization: 85-86%, below the requested 90% ceiling
monitored RAM use: about 11.4-11.6%, below the requested 80% ceiling
```

## Interpretation

The linear receiver pilot is stronger than the nearest-sampled effective 29 mm
pilot: it removes the one-grid-cell x ambiguity and keeps both base rows in the
strong-confidence bucket. It also keeps the highband diagnostic on the true
branch.

This does not replace the replicated nearest-sampling threshold at 30 mm. It is
a single-seed linear receiver pilot. The paper-safe statement remains:

```text
Nearest-sampled close50 target2: first clean replicated offset is 30 mm.
Linear-sampled close50 target2 seed21: 29.5 mm is clean in this single pilot.
```

Useful next GPU work, only if needed, is a narrow two-seed replication of this
linear 29.5 mm point or a direct linear 29.0/29.25 bracket. Do not resume
nearest-sampled sub-millimeter bisection.

## Validation

Pre-run validation:

```text
full suite before this GPU run: 438 passed
```

Figure sanity:

```text
coordinate_confidence_margins.png: 1804x665 RGBA
coordinate_radius_decision_panel.png: 2126x1583 RGBA
coordinate_objective_radius_candidates.png: 2025x835 RGBA
system_scene_geometry.png: 1623x1028 RGBA
```
