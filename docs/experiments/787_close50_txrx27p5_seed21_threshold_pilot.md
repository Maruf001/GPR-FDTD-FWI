# Experiment 787: Close50 Tx/Rx 27.5 mm Seed21 Threshold Pilot

Date: 2026-06-17

## Purpose

Narrow GPU pilot for the close50 target2 acquisition threshold after the CPU
audit in experiment 786. Existing evidence showed Tx/Rx 25 mm ambiguous and
Tx/Rx 30 mm clean for the tested sources4 target2 branch. This run tests the
midpoint, Tx/Rx 27.5 mm, for seed21 only.

This is not a broad sweep. It was run as a single bounded GPU probe and
monitored for the requested utilization limits.

## Output

```text
outputs/experiments/1265_coordinate_optimizer_close50_seed21_sources4_txrx27p5_objectives
```

Artifacts:

```text
data/multi_rebar_coordinate_optimizer_summary.json
data/coordinate_confidence_report.csv
data/coordinate_objective_diagnostics.csv
data/coordinate_objective_top_candidates.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_2_candidates.csv
data/coordinate_step_02_revisit_target_2_candidates.csv
figures/coordinate_confidence_margins.png
figures/coordinate_radius_decision_panel.png
figures/coordinate_objective_radius_candidates.png
figures/system_scene_geometry.png
run_manifest.json
```

## Command Shape

The command matched the existing close50 sources4 target2 Tx/Rx 25/30 branch,
with only these changes:

```text
--tx-rx-offset-mm 27.5
--replication-cases noise10_seed21 ... source_mismatch_noise10_seed21
--run-name coordinate_optimizer_close50_seed21_sources4_txrx27p5_objectives
```

## Result

Final state:

```text
x = [190, 250, 300] mm
z = [90, 90, 90] mm
r = [6, 6, 8] mm
```

Confidence rows:

| Case | Step | Best x/z/r | Margin | Confidence | Ambiguity |
| --- | --- | --- | ---: | --- | --- |
| nominal seed21 | main | 300 / 90 / 8.0 | 4.7846e-04 | `weak` | x = 300-301 mm, r = 7.5-8.0 mm |
| source-mismatch seed21 | main | 300 / 90 / 8.0 | 6.5201e-04 | `moderate` | x = 300-301 mm, r = 7.5-8.0 mm |
| nominal seed21 | revisit | 300 / 90 / 8.0 | 4.7846e-04 | `weak` | x = 300-301 mm, r = 7.5-8.0 mm |
| source-mismatch seed21 | revisit | 300 / 90 / 8.0 | 6.5201e-04 | `moderate` | x = 300-301 mm, r = 7.5-8.0 mm |

Objective diagnostics:

```text
Base objective: exact but weak/moderate.
Highband objective: selects the nearby wrong branch x=301 mm, r=7.5 mm.
```

Runtime:

```text
elapsed time: 1945.8 s
monitored GPU utilization: 85-86%, below the requested 90% ceiling
RAM use: about 13 GiB, below the requested 80% ceiling
```

## Interpretation

This midpoint pilot is enough to keep 27.5 mm out of the clean threshold bucket.
Although the base objective picks the truth, it has a weak nominal row and a
nonzero ambiguity interval. The high-band diagnostic selects the nearby wrong
branch. Under the current policy, a clean replicated threshold requires exact
rows without ambiguity and with sufficient margin.

Current close50 target2 threshold interpretation:

```text
Tx/Rx 25 mm: ambiguous.
Tx/Rx 27.5 mm: exact base pick for seed21, but not clean.
Tx/Rx 30 mm: first tested clean replicated offset.
```

Do not spend GPU on seed13/34 at Tx/Rx 27.5 mm unless the paper specifically
needs a three-seed non-clean bracket. The single seed21 counterexample is
already enough to prevent 27.5 mm from replacing 30 mm as the clean threshold.

## Validation

Focused pre-run audit tests:

```text
tests/test_close50_legacy_policy_audit.py: 3 passed
```

Full suite before this GPU run:

```text
425 passed
```
