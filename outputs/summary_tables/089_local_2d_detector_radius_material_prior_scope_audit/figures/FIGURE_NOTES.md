# Figure Notes

## `local_2d_detector_radius_material_prior_scope_audit.png`

This CPU-only figure separates controlled synthetic radius/material priors
from detector-inferred radius/material seeds.

Policy label: `local_2d_detector_radius_material_prior_scope_audit_cpu_no_fwi`.
Stable controlled-prior cases: `10`.
Review cases excluded: `2`.
Radius patterns: `5,6,8`.
Detector radius seeds: `0`.
Detector material seeds: `0`.
GPU priority: `none`.

Scope boundary:

The radius/material values are controlled synthetic design priors from the command
plan and config, not detector-inferred seeds. This audit does not run refinement,
FWI, GPU kernels, 3D/HPC jobs, or neural-network training.

