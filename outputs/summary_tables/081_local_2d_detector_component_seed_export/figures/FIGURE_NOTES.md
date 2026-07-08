# Figure Notes

## `local_2d_detector_component_seed_export.png`

This CPU-only figure exports stable detector rows as coordinate-only
component seeds for later design work.

Policy label: `local_2d_detector_component_seed_export_coordinate_only_no_fwi`.
Exported seed cases: `10`.
Exported component rows: `30`.
Excluded review cases: `2`.
Ready for coordinate seed table: `True`.
Ready for radius/material contract: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Component seed rows: `local_2d_detector_component_seed_rows.csv`.
- Excluded case rows: `local_2d_detector_component_seed_excluded_cases.csv`.

Scope boundary:

This export reads saved detector launch-contract rows only. It does not run FDTD, FWI, GPU kernels,
field FWI, 3D/HPC jobs, or neural-network training.

