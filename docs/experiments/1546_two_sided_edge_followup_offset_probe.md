# Experiment 1546: Two-Sided Edge Follow-Up Offset Probe

Date: 2026-06-29

## Purpose

Execute the five-offset follow-up plan from run `1543` as a bounded CPU probe.

The run uses the planned offsets:

```text
44.996094, 44.998047, 45.003906, 45.007812, 45.011719 mm
```

and the planned near/far radius-error combinations:

```text
far deltas:  -0.8, -1.6 mm
near deltas: +1.5, +1.9 mm
```

This creates 20 planned model cases. It does not promote a physical claim, run
GPU work, transfer to field data, run field FWI, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1546_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_cpu_result_rows.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_cpu_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_cpu_edge_summary_rows.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_cpu_summary.json
figures/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_cpu.png
```

## Result

```text
planned cases:                         20
grid models executed:                  20
objective selection rows:              120
candidate rows:                        480
all-objectives-truth models:           0
any-failure models:                    20
all-objective-failure models:          0
below-45 offsets tested:               2
above-45 offsets tested:               3
below-45 all far cases suppressed:     false
above-45 all far cases suppressed:     false
follow-up probe ready:                 true
new physical claim ready:              false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
elapsed seconds:                       780.104
```

Edge summary:

| Offset mm | Far -0.8 first failure near delta | Far -1.6 first failure near delta | Both far cases suppressed |
| ---: | ---: | ---: | --- |
| 44.996094 | 1.5 | 1.5 | false |
| 44.998047 | 1.5 | 1.5 | false |
| 45.003906 | 1.5 | 1.5 | false |
| 45.007812 | 1.5 | 1.5 | false |
| 45.011719 | 1.5 | 1.5 | false |

## Interpretation

The follow-up offsets did not find a broader suppression window around the
sampled 45.0 mm point. In the planned 20-case matrix, every offset still has
some objective failure for both far-radius error settings. The failures are
partial rather than all-objective failures, but the result does not support a
wide, monotonic, or physical acquisition-layout rule.

## Decision

Use run `1546` as the executed follow-up offset probe. Keep physical, GPU,
field-transfer, field-FWI, and 3D/HPC claims blocked until validation and
sensitivity checks close this block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_cpu.py
3 passed
```

Figure check:

```text
2430x1495, dynamic range=255
```
