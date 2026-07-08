# Experiment 1429: Local 2D Expanded-Window Objective Failure Diagnosis

Date: 2026-06-28

## Purpose

Diagnose the objective-level failure mode from run `1428` using saved result and
candidate tables.

This run does not execute new FDTD simulations, launch GPU work, transfer to
field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1429_local_2d_state_consistent_expanded_window_objective_failure_diagnosis
```

Key artifacts:

```text
data/local_2d_state_consistent_expanded_window_objective_failure_summary.csv
data/local_2d_state_consistent_expanded_window_objective_failure_critical_candidates.csv
data/local_2d_state_consistent_expanded_window_objective_failure_diagnosis_summary.json
figures/local_2d_state_consistent_expanded_window_objective_failure_diagnosis.png
docs/LOCAL_2D_STATE_CONSISTENT_EXPANDED_WINDOW_OBJECTIVE_FAILURE_DIAGNOSIS.md
scripts/run_local_2d_state_consistent_expanded_window_objective_failure_diagnosis.py
scripts/test_local_2d_state_consistent_expanded_window_objective_failure_diagnosis.py
scripts/script_snapshot_manifest.json
```

## Result

```text
objectives:                         6
failure objectives:                 1
failure rows:                       2
critical candidate rows:            8
critical objective:                 veryhigh
minimum wrong-minus-truth misfit:   -0.0035579159181040702
near radius all-objectives pass:    1.75 mm
far radius all-objectives pass:     0.75 mm
far radius first any-objective fail: 1.00 mm
broad radius tolerance promoted:    false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The failure mode is isolated:

| Objective | Failure rows | Minimum margin | Far last pass | Far first fail |
| --- | ---: | ---: | ---: | ---: |
| base | 0 | 0.006343088963540772 | 1.25 mm | none |
| highband | 0 | 0.004106765164174454 | 1.25 mm | none |
| late | 0 | 0.007479438657672907 | 1.25 mm | none |
| late_high | 0 | 0.007058936066005453 | 1.25 mm | none |
| veryhigh | 2 | -0.0035579159181040702 | 0.75 mm | 1.00 mm |
| early_high | 0 | 0.0008886491570309005 | 1.25 mm | none |

For the two failed rows, the top wrong candidates are x=187, 188, and 189 mm,
while the truth reference is x=190 mm. The wrong candidates beat truth by
`0.0035579159181040702` under the `veryhigh` objective.

## Interpretation

The expanded-window radius problem is not broad across all objectives. It is
concentrated in the `veryhigh` objective for far-neighbor radius decreases at
-1.00 mm and -1.25 mm.

## Decision

Use run `1429` to focus the next 2D follow-up on the far-neighbor/`veryhigh`
interaction. Do not promote broad radius, physical, GPU, field-transfer,
field-FWI, or 3D/HPC claims.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_expanded_window_objective_failure_diagnosis.py
4 passed
```

Figure validation:

```text
2933x846, dynamic range=255
```
