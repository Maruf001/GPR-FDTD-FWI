# Figure Notes

## `local_2d_manuscript_contribution_matrix.png`

This CPU-only matrix maps the current synthetic 2D, field QC,
literature-positioning, neural-network triage, and compute-policy
evidence into manuscript contribution roles.

Policy label: `local_2d_manuscript_contribution_matrix_ready_no_gpu`.
Contribution rows: `11`.
Ready rows: `10`.
Deferred rows: `1`.
Synthetic immediate GPU candidates: `0`.
Synthetic conditional GPU candidates: `0`.
Field ready for FWI: `False`.
Field ready for 3D/HPC: `False`.

Outputs:

- Contribution rows: `local_2d_manuscript_contribution_rows.csv`.
- Summary: `local_2d_manuscript_contribution_summary.json`.
- Figure validation: `figure_validation.csv`.

Scope boundary:

The matrix supports manuscript planning and claim discipline. It
does not launch or justify broad GPU runs, field FWI, 3D/HPC,
or neural-network training from the current local data.

