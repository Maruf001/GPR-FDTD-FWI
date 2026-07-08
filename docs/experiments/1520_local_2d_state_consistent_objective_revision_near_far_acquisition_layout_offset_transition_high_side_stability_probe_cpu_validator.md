# Experiment 1520: Acquisition-Layout High-Side Stability Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1519` high-side Tx/Rx offset probe from artifacts.

The validator checks that the `45.0 mm` sampled far-error suppression is
preserved and that the failures above `45.0 mm` are also preserved. This keeps
the result from being simplified into an unsupported monotonic rule.

This run does not execute FDTD, launch GPU work, transfer to field evidence,
run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1520_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator_validation_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_OFFSET_TRANSITION_HIGH_SIDE_STABILITY_PROBE_CPU_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:                    9
passed checks:                        9
failed checks:                        0
high-side validation ready:           true
grid models validated:                75
objective rows validated:             450
candidate rows validated:             1800
first suppressed far -0.8 offset:     45.0 mm
first suppressed far -1.6 offset:     45.0 mm
first reappeared far -0.8 offset:     45.125 mm
first reappeared far -1.6 offset:     45.125 mm
high-side suppression stable -0.8:    false
high-side suppression stable -1.6:    false
larger-offset safety claim ready:     false
physical claim ready:                 false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

## Interpretation

The validator accepts the exact high-side result from run `1519`. The local
synthetic acquisition-layout effect is non-monotonic in this tested grid:
`45.0 mm` suppresses the negative far-radius failures, while `45.125 mm` and
higher offsets bring those failures back for near-radius errors of `+1.5 mm`
and `+1.9 mm`.

## Decision

Use runs `1519-1520` as the guarded high-side correction block. Keep the
larger-offset safety claim, broad physical claim, GPU work, field transfer,
field FWI, and 3D/HPC work blocked. Sensitivity hardening remains required
before integrating this into the local 2D claim boundary.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator.py
4 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validator.py: pass
```

Figure validation:

```text
3617x932, dynamic range=255
```
