# Experiment 1521: Acquisition-Layout High-Side Stability Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1520` high-side validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `1519` artifact and
rejects damaged variants covering policy drift, offset drift, label collision,
row-count drift, taxonomy drift, removed `45.0 mm` suppression, removed or
shifted `45.125 mm` failure reappearance, downstream promotion, figure drift,
and script-snapshot drift.

It does not rerun the CPU probe, launch GPU work, transfer to field evidence,
run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1521_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validation_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_OFFSET_TRANSITION_HIGH_SIDE_STABILITY_PROBE_CPU_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                          15
expected pass:                      1
observed pass:                      1
expected failures:                  14
observed failures:                  14
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 1519:             true
rejects damaged variants:           true
first reappeared far -0.8 offset:   45.125 mm
first reappeared far -1.6 offset:   45.125 mm
larger-offset safety claim ready:   false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The run `1520` validator accepts the exact run `1519` high-side probe and
rejects controlled damaged variants. This hardens the non-monotonic result:
the sampled `45.0 mm` suppression point is real in the saved artifact, but the
failure reappearance at `45.125 mm` is also real and must not be hidden.

## Decision

Use runs `1519-1521` as the guarded high-side correction block. Keep a
monotonic larger-offset safety claim, broad physical claim, GPU work, field
transfer, field FWI, and 3D/HPC work blocked. The next useful 2D step is a
claim-boundary refresh that integrates the high-side correction.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_validation_sensitivity.py: pass
```

Figure validation:

```text
3491x913, dynamic range=255
```
