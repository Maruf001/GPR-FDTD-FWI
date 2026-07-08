# Experiment 1480: Near/Far Source-Model Generalization Probe

Date: 2026-06-28

## Purpose

Execute the source-model axis from the guarded run `1466` near/far
generalization design.

This CPU-only probe repeats the near/far radius-error interaction grid for
matched negative and positive source time-shift variants. It keeps the geometry,
candidate grid, acquisition layout, objective windows, source frequency, source
amplitude, and noise seed fixed while changing the source time shift from
`-50 ps` to `+50 ps`.

This does not launch GPU work, transfer to field evidence, run field FWI, or
start 3D/HPC work.

## Output

```text
outputs/experiments/1480_local_2d_state_consistent_objective_revision_near_far_source_model_generalization_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_probe.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_SOURCE_MODEL_GENERALIZATION_PROBE.md
```

## Result

```text
source time shifts ps:                [-50.0, 50.0]
source count:                         2
near-radius deltas:                   5
far-radius deltas:                    3
grid models:                          30
objective selection rows:             180
candidate rows:                       720
all-objectives-truth models:          10
any-failure models:                   20
all-objective failure models:         10
first any-failure by source/far:      {'source_time_shift_negative_50ps': {'0.0': 1.5, '-0.8': 0.5, '-1.6': 0.5}, 'source_time_shift_positive_50ps': {'0.0': 1.5, '-0.8': 0.5, '-1.6': 0.5}}
first all-failure by source/far:      {'source_time_shift_negative_50ps': {'0.0': 1.5, '-0.8': 1.5, '-1.6': 1.5}, 'source_time_shift_positive_50ps': {'0.0': None, '-0.8': 1.5, '-1.6': 1.5}}
source probe ready:                   true
promote revised objective now:        false
physical claim ready:                 false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

## Interpretation

The local near/far failure boundary is not an artifact of using only the
previously tested negative source time shift. The first any-objective failure
threshold is identical for the matched `-50 ps` and `+50 ps` source variants.
The positive time-shift case slightly softens the far-error-free all-objective
failure at the largest near-radius errors, but it does not remove the severe
near/far failure boundary when far-neighbor radius error is present.

## Decision

Use this as the executed source-model generalization check. Keep broad-radius,
physical-transfer, GPU, field-FWI, and 3D/HPC claims blocked until the source
result is validated and the acquisition-layout axis is also tested.
