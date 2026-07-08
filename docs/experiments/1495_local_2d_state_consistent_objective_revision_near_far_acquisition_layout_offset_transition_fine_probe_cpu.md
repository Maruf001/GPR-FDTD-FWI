# Experiment 1495: Near/Far Acquisition-Layout Offset Transition Fine Probe

Date: 2026-06-29

## Purpose

Refine the acquisition-layout transition found in run `1489`.

Run `1489` showed that any-objective far-error failures persisted through a
40 mm Tx/Rx offset and disappeared at 45 mm. This run tests the intermediate
offsets:

```text
40, 41, 42, 43, 44, and 45 mm
```

This is a CPU-only synthetic 2D probe. It does not launch GPU work, transfer to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1495_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_probe_cpu_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_probe_cpu_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_probe_cpu_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_probe_cpu.png
scripts/script_snapshot_manifest.json
```

## Result

```text
Tx/Rx offsets mm:                    [40, 41, 42, 43, 44, 45]
Tx/Rx offset count:                  6
grid models:                         90
objective selection rows:            540
candidate rows:                      2160
all-objectives-truth models:         58
any-failure models:                  32
all-objective failure models:        12
first suppressed far -0.8 offset mm: 45.0
first suppressed far -1.6 offset mm: 45.0
fine transition probe ready:         true
elapsed seconds:                     3326.549
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
figure size:                         2430x1495
figure dynamic range:                255
```

The first any-objective failure thresholds are:

| Tx/Rx offset | Far 0.0 mm | Far -0.8 mm | Far -1.6 mm |
| ---: | ---: | ---: | ---: |
| 40 mm | 1.5 | 1.5 | 1.5 |
| 41 mm | 1.5 | 1.5 | 1.5 |
| 42 mm | 1.5 | 1.5 | 1.5 |
| 43 mm | 1.5 | 1.5 | 1.5 |
| 44 mm | 1.5 | 1.5 | 1.5 |
| 45 mm | 1.5 | none | none |

The first all-objective failure thresholds are:

| Tx/Rx offset | Far 0.0 mm | Far -0.8 mm | Far -1.6 mm |
| ---: | ---: | ---: | ---: |
| 40 mm | 1.5 | none | none |
| 41 mm | 1.5 | none | none |
| 42 mm | 1.5 | none | none |
| 43 mm | 1.5 | none | none |
| 44 mm | 1.5 | none | none |
| 45 mm | 1.5 | none | none |

## Interpretation

The refined transition remains sharp in this tested grid. Far-error
any-objective failures persist at 40, 41, 42, 43, and 44 mm, then disappear at
45 mm for both far-neighbor error settings. All-objective far-error failures
are already absent throughout the 40-45 mm fine sweep.

This strengthens the local acquisition-layout story but still does not promote
a broad physical rule. The result is synthetic, local to this geometry and
objective setup, and still needs validation before claim-boundary integration.

## Decision

Use run `1495` as the fine offset-transition map for the 2D near/far
acquisition-layout branch. Keep broad-radius, physical-transfer, GPU,
field-FWI, and 3D/HPC claims blocked pending validation.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_probe_cpu.py
3 passed
```
