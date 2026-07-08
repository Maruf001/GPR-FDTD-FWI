# Figure Notes

## `local_2d_detector_lateral_slot_neighborhood_budget.png`

This CPU-only figure sizes lateral x-slot neighborhoods from saved detector seed errors.

Policy label: `local_2d_detector_lateral_slot_neighborhood_budget_cpu_no_fwi`.
Stable seed cases: `10`.
Review cases: `2`.
Min lateral x-slot half-width for all stable cases: `10.0` mm.
Per-case lateral x-only h10 step2 grid points: `1331.0`.
Hypothetical per-case x/z h10 step2 tensor points: `1771561.0`.
Z coverage validated: `False`.
Ready for x/z neighborhood design: `False`.
Ready for narrow refinement contract: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Half-width rows: `local_2d_detector_lateral_slot_half_width_rows.csv`.
- Grid budget rows: `local_2d_detector_lateral_slot_grid_budget_rows.csv`.

Scope boundary:

This audit reads saved detector contract and seed-export artifacts only. The contract validates
lateral x-slot error, not z error. It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC
jobs, or neural-network training.

