# Experiment 789: Close50 Tx/Rx 28.75 mm Seed21 Threshold Pilot

Date: 2026-06-17

## Purpose

Narrow GPU pilot for the close50 target2 acquisition threshold. Experiment 787
showed that Tx/Rx 27.5 mm was exact for seed21 but non-clean; replicated
aggregate evidence already showed Tx/Rx 30 mm clean. This run tests the
midpoint between those two offsets:

```text
Tx/Rx offset = 28.75 mm
seed = 21
sources = 4
target = 2
```

This was a single bounded GPU probe, not a broad sweep.

## Output

```text
outputs/experiments/1267_coordinate_optimizer_close50_seed21_sources4_txrx28p75_objectives
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
elapsed time: 1528.1 s
monitored GPU utilization: 84-86%, below the requested 90% ceiling
monitored RAM use: 11.3-11.7%, below the requested 80% ceiling
```

## Interpretation

Tx/Rx 28.75 mm is materially stronger than Tx/Rx 27.5 mm: the base confidence
rows are strong and the highband diagnostic no longer selects the nearby wrong
radius branch.

Because this run used `receiver_sampling=nearest` on a 1 mm grid, the requested
28.75 mm offset maps to an effective receiver-index offset of 29 mm at all four
source positions.

It is still not a clean threshold under the strict policy because both rows
retain a one-grid-cell x ambiguity. The result refines the bracket below 30 mm,
but it does not replace the replicated clean Tx/Rx 30 mm threshold.

Current close50 target2 threshold interpretation:

```text
Tx/Rx 25 mm: ambiguous replicated aggregate.
Tx/Rx 27.5 mm: exact seed21 midpoint, but weak/radius-ambiguous and non-clean.
Tx/Rx 28.75 mm: strong seed21 midpoint, but x-ambiguous and non-clean.
Tx/Rx 30 mm: first clean replicated offset.
```

Do not run additional midpoint seeds unless the paper needs a replicated
non-clean bracket immediately below the clean threshold.

## Validation

Pre-run validation:

```text
Full suite before this GPU run: 431 passed
```

The run was wrapped with a resource monitor and completed without crossing the
requested utilization limits.
