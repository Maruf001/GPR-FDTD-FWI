# Experiment 1503: Fine Offset-Transition Margin Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1502` margin-audit validator with controlled damaged
variants.

Run `1502` validates the saved run `1501` margin audit. This run checks that
the validator accepts the exact saved audit and rejects controlled drift in
source identity, guarded-claim state, row counts, taxonomy counts, transition
counts, margin signs, downstream states, figure validation, and script
snapshots.

This run does not run new FDTD simulations, launch GPU work, transfer claims to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1503_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validation_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                  14
expected pass:              1
observed pass:              1
expected failures:          13
observed failures:          13
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1501:     true
rejects damaged variants:   true
GPU work ready:             false
field transfer ready:       false
3D/HPC ready:               false
figure size:                3401x909
figure dynamic range:       255
```

## Interpretation

The run `1502` validator accepts the exact run `1501` margin audit and rejects
controlled damaged variants for source identity drift, guarded-claim drift,
row-count drift, taxonomy drift, transition count drift, margin-sign drift,
downstream promotion, figure-validation drift, and script-snapshot drift.

## Decision

Use runs `1501-1503` as the guarded margin-audit block for the fine
acquisition-layout transition. Broad physical, GPU, field-transfer, field-FWI,
and 3D/HPC claims remain blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validation_sensitivity.py
3 passed
```
