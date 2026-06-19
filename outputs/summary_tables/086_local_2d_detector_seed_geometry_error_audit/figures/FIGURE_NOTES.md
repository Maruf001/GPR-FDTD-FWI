# Figure Notes

## `local_2d_detector_seed_geometry_error_audit.png`

This CPU-only figure joins the baseline detector truth plan with the saved detector launch-contract rows,
then computes matched x/z component seed errors for the stable exported detector cases.

Policy label: `local_2d_detector_seed_geometry_error_audit_cpu_no_fwi`.
Stable seed cases: `10`.
Review cases: `2`.
Max stable x error: `10.0` mm.
Max stable z error: `12.0` mm.
Minimum x/z half-width for all stable cases: `12.0` mm.
Per-case h12/step2 x/z tensor points: `4826809.0`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case rows: `local_2d_detector_seed_geometry_error_cases.csv`.
- Component rows: `local_2d_detector_seed_geometry_error_components.csv`.

Scope boundary:

This audit reads saved CSV/JSON tables only. It does not run FDTD, FWI, GPU kernels, field FWI,
3D/HPC jobs, or neural-network training.

