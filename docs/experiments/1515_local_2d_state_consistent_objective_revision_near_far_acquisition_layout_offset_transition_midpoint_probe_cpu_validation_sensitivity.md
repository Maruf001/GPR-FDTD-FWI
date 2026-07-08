# Experiment 1515: Near/Far Acquisition-Layout Midpoint Probe Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1514` midpoint-probe validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `1513` midpoint probe
and rejects damaged variants covering policy drift, offset-list drift,
fractional-label collision, row-count drift, taxonomy drift, below-45 mm
failure removal, 45 mm suppression removal, suppression-offset drift,
downstream promotion, figure validation drift, and script-snapshot drift.

It does not rerun the CPU probe, launch GPU work, transfer to field evidence,
run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1515_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validation_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_OFFSET_TRANSITION_MIDPOINT_PROBE_CPU_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                          14
expected pass:                      1
observed pass:                      1
expected failures:                  13
observed failures:                  13
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 1513:             true
rejects damaged variants:           true
linear crossing promoted:           false
discrete transition offset:         45.0 mm
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The run `1514` validator accepts the exact run `1513` midpoint probe and rejects
the damaged variants. This protects the corrected interpretation: below-45 mm
failure removal, 45 mm suppression removal, and suppression-offset drift are
all caught as validation failures.

## Decision

Use runs `1513-1515` as the guarded midpoint-probe correction block. The
`44.621 mm` crossing remains a margin-only estimate, while the discrete tested
transition for far-error suppression remains `45.0 mm`.

Broad physical, GPU, field-transfer, field-FWI, and 3D/HPC claims remain
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator.py
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validation_sensitivity.py
7 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator.py: pass
run_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validation_sensitivity.py: pass
```

Figure validation:

```text
3401x931, dynamic range=255
```
