# Experiment 1514: Near/Far Acquisition-Layout Midpoint Probe Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1513` fractional-offset midpoint probe from artifacts.

This run checks that the run `1513` CPU result is internally stable: counts,
fractional Tx/Rx labels, failure-threshold maps, below-45 mm failure
persistence, 45 mm suppression, downstream guardrails, figure validation, and
script snapshots.

It does not rerun the expensive CPU probe, launch GPU work, transfer to field
evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1514_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator_validation_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_OFFSET_TRANSITION_MIDPOINT_PROBE_CPU_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:                    8
passed checks:                        8
failed checks:                        0
midpoint probe validation ready:      true
Tx/Rx offsets validated:              6
grid models:                          90
objective selection rows:             540
candidate rows:                       2160
first suppressed far -0.8 offset:     45.0 mm
first suppressed far -1.6 offset:     45.0 mm
linear crossing promoted:             false
discrete transition offset:           45.0 mm
physical claim ready:                 false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

The validator confirms that run `1513` preserved unique fractional labels:

```text
tx_rx_offset_44mm
tx_rx_offset_44p25mm
tx_rx_offset_44p5mm
tx_rx_offset_44p625mm
tx_rx_offset_44p75mm
tx_rx_offset_45mm
```

## Interpretation

Run `1514` validates the corrected local 2D interpretation from run `1513`.
The direct midpoint probe supersedes the simple threshold interpretation of the
run `1507` margin interpolation.

Failures remain present at `44.625 mm` and `44.75 mm` for the far-error cases.
The first tested offset that suppresses the `-0.8 mm` and `-1.6 mm` far-radius
failure cases remains `45.0 mm`.

## Decision

Use runs `1513-1514` as the current guarded midpoint-probe block. The
`44.621 mm` value remains a margin-only estimate, while the discrete tested
transition remains `45.0 mm` for the far-error suppression cases.

Do not promote broad physical, GPU, field-transfer, field-FWI, or 3D/HPC claims
from this block.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator.py
4 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_validator.py: pass
```

Figure validation:

```text
3581x934, dynamic range=255
```
