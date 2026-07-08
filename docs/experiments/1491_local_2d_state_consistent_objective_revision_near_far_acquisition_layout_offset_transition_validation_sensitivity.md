# Experiment 1491: Near/Far Acquisition-Layout Offset-Transition Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1490` validator with controlled damaged variants.

The exact run `1489` artifact set should pass. Damaged variants should fail
when they change offset lists, counts, row totals, failure taxonomy, threshold
maps, suppression offsets, downstream guardrails, figure validation, or script
snapshots.

This is CPU-only validation hardening. It does not launch GPU work, transfer to
field evidence, run field FWI, promote a physical claim, or start 3D/HPC work.

## Output

```text
outputs/experiments/1491_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validation_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validation_sensitivity.png
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
accepts exact run 1489:       true
rejects damaged variants:     true
figure size:                  3329x895
figure dynamic range:         255
```

## Interpretation

The validator accepts the exact run `1489` transition result and rejects all
controlled corruptions. This means the guarded transition claim depends on the
actual saved five-offset result, not only on a loosely shaped summary file.

## Decision

Use runs `1489-1491` as the guarded 2D acquisition-layout offset-transition
block. The transition map refines the acquisition-layout claim boundary, but
broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims remain
blocked pending claim-boundary integration.
