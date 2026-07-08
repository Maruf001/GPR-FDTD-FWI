# Experiment 1539: Two-Sided Edge Suppression Window Width Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1538` validator for the saved run `1537`
suppression-window width audit.

This run checks that the validator accepts the exact run `1537` artifacts and
rejects controlled damaged variants for source identity drift, row drift, gap
drift, false wide-window promotion, downstream promotion, figure drift, and
script-snapshot drift.

## Output

```text
outputs/experiments/1539_local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validation_sensitivity.png
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
accepts exact run 1537:             true
rejects damaged variants:           true
lower failure-to-suppression gap:   0.007812 mm
suppression-to-upper-failure gap:   0.015625 mm
failure-to-failure bracket span:    0.023437 mm
narrow sampled window ready:        true
wide suppression-window ready:      false
broad acquisition safety ready:     false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

## Interpretation

The run `1538` validator accepts the exact run `1537` width audit and rejects
controlled damaged variants. This guards the narrow sampled suppression-window
result and blocks wider acquisition-safety claims.

## Decision

Use runs `1537-1539` as the guarded suppression-window width-audit block. Keep
wide-window, monotonic acquisition, physical, GPU, field, and 3D claims
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3617x904, dynamic range=255
```
