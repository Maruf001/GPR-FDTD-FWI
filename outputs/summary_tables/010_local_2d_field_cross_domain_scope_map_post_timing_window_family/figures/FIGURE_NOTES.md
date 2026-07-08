# Figure Notes

## `local_2d_field_cross_domain_scope_map.png`

This is a CPU-only manuscript scope map. It combines current
synthetic 2D known-truth policy summaries with measured-field
spacing and timing QC summaries.

Policy label: `local_2d_field_cross_domain_scope_map_ready_no_gpu`.
Scope rows: `7`.
Field/synthetic spacing ratio: `1.933`.
Field resolution benchmark ready: `False`.
Field FWI ready: `False`.
GPU priority: `none`.

Inputs and outputs:

- Scope rows: `local_2d_field_cross_domain_scope_rows.csv`.
- Summary: `local_2d_field_cross_domain_scope_summary.json`.
- Figure validation: `figure_validation.csv`.

Scope boundary:

The figure does not merge synthetic known-truth resolution claims
with measured-field QC. It explicitly blocks field resolution
benchmark, absolute time-zero, 3D, cover-depth, radius, and field
FWI claims from the current measured GSSI dataset.

