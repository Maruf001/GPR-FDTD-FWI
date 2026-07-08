# Experiment 1508: Fine Transition Crossing Estimate Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1507` crossing-estimate audit from artifacts.

This run checks the source identity, crossing estimates, crossing rows, curve
identity, guarded narrow-clearance state, downstream blocked states, figure
output, and script snapshots.

It does not run FDTD, launch GPU work, promote physical transfer, run field FWI,
or start 3D/HPC work.

## Output

```text
outputs/experiments/1508_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validator_checks.csv
data/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validator_summary.json
figures/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_FINE_TRANSITION_CROSSING_ESTIMATE_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:               8
passed checks:                   8
failed checks:                   0
validation ready:                true
stress curves:                   4
mean crossing offset:            44.620737 mm
crossing offset range:           0.000000 mm
minimum clearance from 45 mm:    0.379263 mm
all margin curves identical:     true
near-45 mm clearance only:       true
physical claim ready:            false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
```

## Interpretation

The saved crossing estimate is internally consistent: all four stress curves
cross at the same `44.621 mm` estimate, the `45 mm` layout has less than
`0.5 mm` clearance, and downstream physical, GPU, field, and 3D claims remain
blocked.

## Decision

Use run `1508` as the validator for the run `1507` crossing estimate. Treat the
estimate as a local saved-artifact mechanism measurement, not a broad
acquisition rule.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validator.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_validator.py: pass
```

Figure validation:

```text
3509x891, dynamic range=255
```
