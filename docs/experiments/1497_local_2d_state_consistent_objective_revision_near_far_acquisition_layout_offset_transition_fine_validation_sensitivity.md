# Experiment 1497: Near/Far Acquisition-Layout Offset Transition Fine Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1496` fine offset-transition validator with controlled
damaged variants.

The exact run `1495` artifact set should pass. Damaged variants should fail
when they change the offset list, offset counts, row counts, failure taxonomy,
threshold maps, suppressed-offset value, downstream guardrails, figure
validation, or script snapshots.

This is CPU-only validation hardening. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, promote a physical
claim, or start 3D/HPC work.

## Output

```text
outputs/experiments/1497_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validation_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    13
expected pass:                1
observed pass:                1
expected failures:            12
observed failures:            12
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 1495:       true
rejects damaged variants:     true
broad radius promoted:        false
physical claim ready:         false
GPU work ready:               false
field transfer ready:         false
field FWI ready:              false
3D/HPC ready:                 false
figure size:                  3329x895
figure dynamic range:         255
```

The validator rejects all damaged variants:

| Scenario | Expected | Observed |
| --- | --- | --- |
| exact run 1495 inputs | pass | pass |
| policy label drift | fail | fail |
| Tx/Rx offset count drift | fail | fail |
| Tx/Rx offset list drift | fail | fail |
| grid model count drift | fail | fail |
| result row count drift | fail | fail |
| failure taxonomy drift | fail | fail |
| first any-threshold drift | fail | fail |
| first all-threshold drift | fail | fail |
| suppressed-offset drift | fail | fail |
| downstream promotion | fail | fail |
| figure validation drift | fail | fail |
| script snapshot drift | fail | fail |

## Interpretation

The run `1496` validator accepts the exact run `1495` fine offset-transition
result and rejects controlled damaged variants for offset-list drift,
offset/count drift, row-count drift, taxonomy drift, threshold drift,
suppression-threshold drift, downstream promotion, figure validation drift, and
script-snapshot drift.

## Decision

Use runs `1495-1497` as the guarded 2D acquisition-layout fine
offset-transition block. The transition map refines the acquisition-layout
claim boundary, but broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC
claims remain blocked pending claim-boundary integration.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validation_sensitivity.py
3 passed
```
