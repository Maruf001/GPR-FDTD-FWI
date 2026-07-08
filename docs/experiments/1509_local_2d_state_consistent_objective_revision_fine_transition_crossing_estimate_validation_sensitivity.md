# Experiment 1509: Fine Transition Crossing Estimate Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1508` crossing-estimate validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `1507` crossing
estimate and rejects damaged variants covering identity, counts, crossing
values, curve identity, guarded state, downstream promotion, figure validation,
and script snapshots.

It does not run FDTD, launch GPU work, promote physical transfer, run field FWI,
or start 3D/HPC work.

## Output

```text
outputs/experiments/1509_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validation_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_FINE_TRANSITION_CROSSING_ESTIMATE_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                  20
expected pass:              1
observed pass:              1
expected failures:          19
observed failures:          19
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1507:     true
rejects damaged variants:   true
physical claim ready:       false
GPU work ready:             false
field transfer ready:       false
field FWI ready:            false
3D/HPC ready:               false
```

## Interpretation

The validator accepts the exact run `1507` crossing estimate and rejects damaged
variants covering identity, counts, crossing values, curve identity, guarded
state, downstream promotion, figure validation, and script snapshots.

## Decision

Use runs `1507-1509` as the guarded fine-transition crossing estimate block.
The result remains local mechanism evidence and does not promote physical, GPU,
field, or 3D claims.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validation_sensitivity.py: pass
```

Figure validation:

```text
3581x903, dynamic range=255
```
