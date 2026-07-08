# Experiment 868: Local 2D Field Cross-Domain Scope Map Post Controlled Prior Budget

Date: 2026-06-19

## Purpose

Refresh the local 2D/field cross-domain scope map against the current
manuscript table pack (`124`) so the field archive, synthetic resolution
claims, and controlled-prior detector-refinement budget stay separated.

This is CPU-only manuscript synthesis. It does not run FDTD/FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/125_local_2d_field_cross_domain_scope_map_post_controlled_prior_budget
```

Key artifacts:

```text
data/local_2d_field_cross_domain_scope_rows.csv
data/local_2d_field_cross_domain_scope_summary.json
figures/local_2d_field_cross_domain_scope_map.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_field_cross_domain_scope_map_ready_no_gpu
scope rows:                           8
field min same-time spacing:          96.657 mm
synthetic close-spacing context max:  50.0 mm
field/synthetic spacing ratio:        1.93314
field resolution benchmark ready:     false
field absolute time-zero ready:       false
field FWI ready:                      false
detector controlled prior ready:      true
detector-inferred radius/material:    false
controlled-prior fixed fine points:   29936602
controlled-prior permutation factor:  6.0
refinement launch ready:              false
detector-seeded FWI ready:            false
gpu priority:                         none
ready for manuscript scope table:     true
```

## Interpretation

Run `125` is the current paper-facing scope boundary:

```text
synthetic known-truth resolution evidence remains synthetic,
measured GSSI field evidence remains 2D QC/context,
controlled-prior detector refinement remains design sizing only.
```

The measured field cue spacing is wider than the synthetic close-spacing stress
regime, so the field archive can contextualize but not validate the synthetic
25-30 mm close-spacing threshold. The controlled-prior detector budget is not
detector-inferred radius/material, not field transfer, and not a launch gate.

## Validation

Focused tests:

```text
tests/test_local_2d_field_cross_domain_scope_map.py
3 passed
```

Figure validation:

```text
local_2d_field_cross_domain_scope_map.png: 2484x801,
nonwhite=0.1703, dynamic range=255
```
