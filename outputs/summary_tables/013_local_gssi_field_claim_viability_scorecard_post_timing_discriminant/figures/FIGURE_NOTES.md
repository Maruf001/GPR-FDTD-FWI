# Figure Notes

## `local_gssi_field_claim_viability_scorecard.png`

This CPU-only scorecard consolidates existing local GSSI field
evidence into supported, scope-limited, context-only, rejected
control, and blocked manuscript claim classes.

Policy label: `local_gssi_field_claim_viability_scorecard_ready_no_field_fwi`.
Claim rows: `13`.
Supported rows: `3`.
Scope-limited rows: `5`.
Blocked rows: `3`.
Ready for 2D field QC: `True`.
Ready for field FWI: `False`.
Ready for 3D/HPC: `False`.
GPU priority: `none`.

Outputs:

- Claim rows: `local_gssi_field_claim_viability_rows.csv`.
- Summary: `local_gssi_field_claim_viability_summary.json`.
- Figure validation: `figure_validation.csv`.

Scope boundary:

The scorecard supports manuscript wording discipline. It does
not promote field data to absolute time-zero, cover-depth,
radius, field FWI, 3D, HPC, or synthetic-resolution validation.

