# Figure Notes

## `local_2d_detector_controlled_prior_refinement_budget.png`

This CPU-only figure budgets detector handoff scopes after the x/z
neighborhood and controlled radius/material prior audits.

Policy label: `local_2d_detector_controlled_prior_refinement_budget_cpu_no_fwi`.
Radius pattern: `5,6,8` mm.
Fixed-radius fine stable points: `29936602`.
Known-radius permutation multiplier: `6.0`.
Independent known-radius multiplier: `27.0`.
GPU priority: `none`.

Scope boundary:

Fixed slot radii are controlled synthetic priors, not detector-inferred
radius/material estimates. This audit does not run refinement, FWI,
GPU kernels, 3D/HPC jobs, field transfer, or neural-network training.

