# Figure Notes

## `local_2d_detector_target_failure_taxonomy.png`

This CPU-only figure summarizes which target locations are dropped by
the current truth-free detector selector when the selected triple is wrong.

Policy label: `local_2d_detector_target_failure_taxonomy_cpu_no_fwi`.
Failed selector cases: `9` of `12`.
Dominant missing target: `target1`.
Target1 missing cases: `7`.
Multi-target failure cases: `5`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case taxonomy: `local_2d_detector_target_failure_taxonomy_cases.csv`.
- Branch taxonomy: `local_2d_detector_target_failure_taxonomy_branch_summary.csv`.

Scope boundary:

This audit reads existing selector gap rows only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

