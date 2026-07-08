# Experiment 1507: Fine Transition Crossing Estimate Audit

Date: 2026-06-28

## Purpose

Estimate the zero-margin crossing inside the guarded 44-45 mm acquisition-layout
transition using saved 2D artifacts.

This run uses the transition margin rows from run `1501` and the guarded
post-margin claim-boundary sensitivity from run `1506`. It does not run FDTD,
launch GPU work, promote physical transfer, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1507_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_audit_crossing_rows.csv
data/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_audit_summary.json
figures/local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_FINE_TRANSITION_CROSSING_ESTIMATE_AUDIT.md
scripts/
```

## Result

```text
stress curves:                       4
all crossings found:                 true
mean crossing offset:                44.620737 mm
crossing offset range:               0.000000 mm
minimum clearance from 45 mm:        0.379263 mm
all margin curves identical:         true
all failure curves identical:        true
crossing estimate audit ready:       true
near-45 mm clearance only:           true
broad radius tolerance promoted:     false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved fine-transition margins place the zero-margin crossing at about
`44.621 mm`. The `45 mm` layout is therefore just beyond the tested stress
threshold, with less than `0.5 mm` clearance. The four stress curves are
identical in the saved artifact, so this audit strengthens the local
acquisition-offset mechanism but does not justify broad physical or
GPU/field/3D promotion.

## Decision

Use run `1507` as the fine-transition crossing estimate. Treat `45 mm` as a
narrow local clearance in the tested synthetic setup, not as a broad acquisition
rule.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_audit.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_audit.py: pass
tests/test_local_2d_state_consistent_objective_revision_fine_transition_crossing_estimate_audit.py: pass
```

Figure validation:

```text
3616x916, dynamic range=255
```
