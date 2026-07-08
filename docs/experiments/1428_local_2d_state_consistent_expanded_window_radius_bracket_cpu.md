# Experiment 1428: Local 2D State-Consistent Expanded-Window Radius Bracket

Date: 2026-06-28

## Purpose

Execute the first CPU follow-up from the run `1427` design matrix: smaller
near-neighbor and far-neighbor radius perturbations under the expanded target
x-window and six-objective audit.

This run does not launch GPU work, transfer to field data, run field FWI, or
promote 3D/HPC work.

## Output

```text
outputs/experiments/1428_local_2d_state_consistent_expanded_window_radius_bracket_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_expanded_window_radius_bracket_results.csv
data/local_2d_state_consistent_expanded_window_radius_bracket_candidates.csv
data/local_2d_state_consistent_expanded_window_radius_bracket_summary.json
figures/local_2d_state_consistent_expanded_window_radius_bracket.png
docs/LOCAL_2D_STATE_CONSISTENT_EXPANDED_WINDOW_RADIUS_BRACKET.md
scripts/run_local_2d_state_consistent_expanded_window_radius_bracket_cpu.py
scripts/test_local_2d_state_consistent_expanded_window_radius_bracket_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
perturbations:                         10
objectives:                            6
result rows:                           60
candidate rows:                        1080
correct state all objectives truth:    true
perturbed truth rows:                  52
perturbed failure rows:                2
minimum wrong-minus-truth misfit:      -0.0035579159181040702
expanded bracket all passed:           false
tolerance boundary detected:           true
near +radius last all-objectives pass: 1.75 mm
near +radius first any-objective fail: none in tested bracket
far -radius last all-objectives pass:  0.75 mm
far -radius first any-objective fail:  1.00 mm
elapsed:                               520.109 seconds
```

The two failures are both `veryhigh` objective failures:

| Perturbation | Objective | Selected x | Wrong-minus-truth misfit |
| --- | --- | ---: | ---: |
| far neighbor radius -1.00 mm | veryhigh | 187.0 mm | -0.0035579159181040702 |
| far neighbor radius -1.25 mm | veryhigh | 187.0 mm | -0.0035579159181040702 |

## Interpretation

The run `1427` design matrix produced useful new evidence. Near-neighbor radius
increase is less fragile than the earlier expanded-window audit suggested: the
tested near-radius bracket passes through +1.75 mm across all six objectives.

Far-neighbor radius decrease remains fragile under the `veryhigh` objective.
The first tested failure occurs at -1.00 mm, while -0.75 mm still passes across
all six objectives.

This narrows the next 2D question to the far-neighbor/veryhigh interaction. It
does not justify a broad radius-tolerance claim, GPU work, field transfer,
field FWI, or 3D/HPC escalation.

## Decision

Use run `1428` as the first actual expanded-window CPU bracket result. The next
2D follow-up should diagnose the far-neighbor `veryhigh` objective failure,
not start a broad GPU batch.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_expanded_window_radius_bracket_cpu.py
2 passed
```

Figure validation:

```text
2460x1456, dynamic range=255
```
