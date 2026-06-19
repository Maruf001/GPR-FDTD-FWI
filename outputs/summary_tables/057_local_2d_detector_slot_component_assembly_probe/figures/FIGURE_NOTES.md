# Figure Notes

## `local_2d_detector_slot_component_assembly_probe.png`

This CPU-only figure tests whether saved detector components can recover
the known branch target slots when assembled slot-by-slot.

Policy label: `local_2d_detector_slot_component_assembly_probe_cpu_no_fwi`.
Current triple selector all-truth cases: `3`.
Depth/slot prior best all-truth cases: `5`.
Slot assembly all-target cases: `12`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Variant grid: `local_2d_detector_slot_component_assembly_variants.csv`.
- Selected case rows: `local_2d_detector_slot_component_assembly_selected_cases.csv`.

Scope boundary:

This is a branch-slot upper-bound/contract probe. It uses the known
synthetic branch slot locations and is not a deployable detector selector.
It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or
neural-network training.

