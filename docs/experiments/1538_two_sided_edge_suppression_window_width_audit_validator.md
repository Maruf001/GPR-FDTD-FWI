# Experiment 1538: Two-Sided Edge Suppression Window Width Audit Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1537` suppression-window width audit from artifacts.

This run checks source identity, window rows, gap metrics, downstream blocked
states, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1538_local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validator_checks.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validator.png
scripts/
```

## Result

```text
validation checks:                   6
passed checks:                       6
failed checks:                       0
validation ready:                    true
last failed below 45.0 mm:           44.992188 mm
sampled suppression point:           45.0 mm
first reappeared above 45.0 mm:      45.015625 mm
lower failure-to-suppression gap:    0.007812 mm
suppression-to-upper-failure gap:    0.015625 mm
failure-to-failure bracket span:     0.023437 mm
narrow sampled window ready:         true
wide suppression-window claim ready: false
broad acquisition safety ready:      false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved width audit is internally consistent. The sampled suppression point
remains bracketed by nearby failures, and wide-window or monotonic acquisition
claims stay blocked.

## Decision

Use run `1538` as the validator for the run `1537` suppression-window width
audit. Sensitivity hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validator.py
3 passed
```

Figure validation:

```text
3545x927, dynamic range=255
```
