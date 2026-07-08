# Experiment 794: Close50 Tx/Rx 29.5 mm Linear Receiver Seed13 Replication

Date: 2026-06-17

## Purpose

Second bounded GPU run for the close50 target2 linear-receiver point tested in
experiment 793. The aim was to replicate the 29.5 mm linearly interpolated
receiver offset with an independent noise seed before treating it as a
candidate below-30 mm threshold result.

```text
requested Tx/Rx offset: 29.5 mm
effective receiver offset: [29.5, 29.5, 29.5, 29.5] mm
receiver sampling: linear
seed: 13
sources: 4
target: 2
```

This was a narrow replication run, not a sweep.

## Output

```text
outputs/experiments/1272_coordinate_optimizer_close50_seed13_sources4_txrx29p5_linear_receiver_objectives
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
| nominal seed13 | 300 / 90 / 8.0 | 2.0957e-03 | `strong` | x = 300-301 mm, r = 8.0-8.0 mm |
| source-mismatch seed13 | 300 / 90 / 8.0 | 1.9887e-03 | `strong` | x = 300-300 mm, r = 8.0-8.0 mm |

Objective diagnostics:

```text
Base objective: selects truth for both cases.
Highband diagnostic: selects truth for both cases.
Highband margins: 1.2127e-03 and 1.3798e-03.
No radius-ambiguity revisit targets were triggered.
```

Runtime and resource envelope:

```text
elapsed time: 1527.3 s
monitored GPU utilization: 84-86%, below the requested 90% ceiling
monitored RAM use: about 11.4-11.6%, below the requested 80% ceiling
```

## Interpretation

The seed13 replication keeps the true target2 geometry as the best solution in
both base rows and both highband diagnostics. It is therefore exact and strong
on the radius-margin criterion.

It does not make the linear 29.5 mm point clean under the stricter
no-x-ambiguity policy, because the nominal seed13 row still admits a 300-301 mm
same-radius ambiguity candidate. The paper-safe statement is:

```text
Linear-sampled close50 target2 at 29.5 mm is exact and strong across seeds 21
and 13, but it is not clean-replicated because one nominal row retains a
one-grid-cell x ambiguity.
```

This means seed34 is not necessary to answer the immediate clean-replication
question. A further GPU run should be justified by a sharper question, such as
estimating ambiguity frequency across seeds or bracketing where the seed13
x ambiguity clears under linear receiver sampling.

## Validation

Figure sanity:

```text
coordinate_confidence_margins.png: 1804x665 RGBA
coordinate_radius_decision_panel.png: 2126x1583 RGBA
coordinate_objective_radius_candidates.png: 2025x835 RGBA
system_scene_geometry.png: 1623x1028 RGBA
```
