# Figure Notes

## `local_2d_detector_depth_slot_prior_probe.png`

This CPU-only figure probes broad depth and expected-x-slot priors on the
saved detector component-gate rows.

Policy label: `local_2d_detector_depth_slot_prior_probe_cpu_no_fwi`.
Base all-truth cases: `3`.
Best all-truth cases: `5`.
Best depth weight: `12.0`.
Best slot weight: `1.0`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Variant grid: `local_2d_detector_depth_slot_prior_probe_variants.csv`.
- Selected case rows: `local_2d_detector_depth_slot_prior_probe_selected_cases.csv`.

Scope boundary:

This probe reads existing saved detector rows only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

