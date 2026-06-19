# Experiment 866: Local 2D Field Manuscript Table Pack Post Current Handoff

Date: 2026-06-19

## Purpose

Refresh the combined local 2D and field manuscript table pack after the current
synthetic next-question matrix (`1356`) and controlled field handoff (`155`).

This is CPU-only manuscript synthesis. It does not run FDTD/FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/123_local_2d_field_manuscript_table_pack_post_current_handoff
```

Key artifacts:

```text
data/local_2d_field_manuscript_claim_table.csv
data/local_2d_field_manuscript_figure_inventory.csv
data/local_2d_field_manuscript_result_metrics.csv
data/local_2d_field_manuscript_table_pack_summary.json
figures/local_2d_field_manuscript_table_pack.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_field_manuscript_table_pack_ready_no_gpu
claim table rows:                     32
figure inventory rows:                31
metric rows:                          270
synthetic claims:                     11
field claims:                         21
synthetic figures:                    9
field figures:                        22
field collection handoff included:    true
field handoff ready collection day:   true
field handoff ready packet acceptance: false
field handoff ready field FWI:        false
field handoff ready 3D/HPC:           false
gpu priority:                         none
ready for manuscript table use:       true
```

Current field-handoff metrics added to the table pack:

```text
handoff actions:                 7
critical new-data actions:       5
packet rows needing entry:       12
failed acceptance gates:         7
reference uncertainty gate:      0.02 ns
```

## Interpretation

Run `123` is the current compact manuscript table pack. It now ties the
paper-facing synthetic table pack to the current synthetic no-GPU queue and
records the field collection handoff as a guardrail: the run sheet is ready
for controlled 2D field collection, but the packet is not accepted and field
FWI/heavy field work/3D-HPC remain blocked.

This keeps the synthetic and field scopes separate while making the current
field next step visible in the cross-domain manuscript metrics.

## Validation

Focused tests:

```text
tests/test_local_2d_field_manuscript_table_pack.py
6 passed
```

Figure validation:

```text
local_2d_field_manuscript_table_pack.png: 1587x835,
nonwhite=0.3032, dynamic range=255
```
