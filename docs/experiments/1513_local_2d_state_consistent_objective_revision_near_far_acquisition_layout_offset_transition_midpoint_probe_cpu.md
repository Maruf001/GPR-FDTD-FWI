# Experiment 1513: Near/Far Acquisition-Layout Offset Transition Midpoint Probe

Date: 2026-06-29

## Purpose

Run an actual CPU probe at fractional Tx/Rx offsets around the zero-margin
crossing estimated in run `1507`.

Run `1507` estimated a crossing near `44.621 mm` from saved margin values. This
run checks that estimate with direct synthetic evaluations at:

```text
44.00, 44.25, 44.50, 44.625, 44.75, and 45.00 mm
```

The run uses fractional acquisition labels so that `44.25`, `44.5`, and
`44.625` mm cases do not collide with integer-rounded output labels.

This is CPU-only synthetic evidence. It does not launch GPU work, transfer to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1513_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_summary.json
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu_candidate_rows.csv
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_OFFSET_TRANSITION_MIDPOINT_PROBE_CPU.md
scripts/
```

## Result

```text
Tx/Rx offsets tested:                 6
grid models:                          90
objective selection rows:             540
candidate rows:                       2160
all-objectives-truth models:          58
any-failure models:                   32
all-objective failure models:         12
first suppressed far -0.8 offset:     45.0 mm
first suppressed far -1.6 offset:     45.0 mm
midpoint probe ready:                 true
physical claim ready:                 false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
elapsed time:                         3397.043 s
```

Failure still appears at the fractional offsets below 45 mm:

| Tx/Rx offset | Far radius delta 0.0 mm | Far radius delta -0.8 mm | Far radius delta -1.6 mm |
| ---: | ---: | ---: | ---: |
| 44.00 mm | 1.5 mm | 1.5 mm | 1.5 mm |
| 44.25 mm | 1.5 mm | 1.5 mm | 1.5 mm |
| 44.50 mm | 1.5 mm | 1.5 mm | 1.5 mm |
| 44.625 mm | 1.5 mm | 1.5 mm | 1.5 mm |
| 44.75 mm | 1.5 mm | 1.5 mm | 1.5 mm |
| 45.00 mm | 1.5 mm | none | none |

## Interpretation

The direct midpoint probe is stronger evidence than the earlier linear
crossing estimate. It shows that the simple margin interpolation from run
`1507` does not by itself predict the discrete pass/fail behavior of the full
selection pipeline.

The tested far-error failures remain present at `44.625 mm` and `44.75 mm`.
Suppression of the `-0.8 mm` and `-1.6 mm` far-radius failure cases first
appears at the already-tested `45.0 mm` offset.

## Decision

Treat the `44.621 mm` crossing from run `1507` as a margin-only estimate, not as
a promoted operating threshold. Use this run as the current higher-priority
evidence for the local 2D acquisition-layout transition: the discrete tested
transition remains at `45.0 mm` for the far-error suppression cases.

This remains synthetic mechanism evidence only. Do not promote broad physical,
GPU, field-transfer, field-FWI, or 3D/HPC claims from this run.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_midpoint_probe_cpu.py
3 passed
```

Figure validation:

```text
2430x1495, dynamic range=255
```
