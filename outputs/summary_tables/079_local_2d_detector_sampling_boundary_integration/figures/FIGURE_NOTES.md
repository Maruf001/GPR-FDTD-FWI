# Figure Notes

## `local_2d_detector_sampling_boundary_integration.png`

This CPU-only figure integrates detector reliability/stability rows
with the close50 sampling-boundary synthesis. It reads saved tables
only and does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC, or
neural-network training.

Policy label: `local_2d_detector_sampling_boundary_integration_cpu_no_fwi`.
Detector review cases: `2`.
Review cases below clean threshold: `2`.
Close50 nominal review cases: `2`.
Per-seed physics equivalence ready: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case rows: `local_2d_detector_sampling_boundary_integration_cases.csv`.
- Category rows: `local_2d_detector_sampling_boundary_integration_categories.csv`.

