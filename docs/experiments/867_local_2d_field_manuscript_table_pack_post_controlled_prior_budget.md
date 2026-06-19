# Experiment 867: Local 2D Field Manuscript Table Pack Post Controlled Prior Budget

Date: 2026-06-19

## Purpose

Refresh the combined local 2D and field manuscript table pack after adding the
detector radius/material prior-scope audit (`089`) and controlled-prior
refinement budget (`090`).

This is CPU-only manuscript synthesis. It does not run FDTD/FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/124_local_2d_field_manuscript_table_pack_post_controlled_prior_budget
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
policy label:                             local_2d_field_manuscript_table_pack_ready_no_gpu
claim table rows:                         32
figure inventory rows:                    31
metric rows:                              290
auxiliary evidence metrics:               274
detector radius/material prior included:  true
controlled prior ready:                   true
detector-inferred radius/material ready:  false
fixed-radius fine budget points:          29936602
fixed-radius coarse budget points:        156250
known-radius permutation multiplier:      6.0
independent-radius multiplier:            27.0
refinement launch ready:                  false
detector-seeded FWI ready:                false
gpu priority:                             none
ready for manuscript table use:           true
```

## Interpretation

Run `124` updates the manuscript table pack from "radius/material missing" to a
more precise detector-refinement state:

```text
controlled synthetic radius/material priors are scoped for stable saved cases,
but detector-inferred radius/material seeds are still absent.
```

The fixed-radius controlled-prior budget is useful for design sizing only. A
known-radius permutation search would multiply the fine budget by `6`, and an
independent known-radius search by `27`. The table pack keeps refinement launch,
detector-seeded FWI, GPU work, field transfer, and field 3D/HPC blocked.

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
