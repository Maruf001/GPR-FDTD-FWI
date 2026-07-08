# Figure Notes

## `local_2d_detector_physics_ambiguity_link.png`

This CPU-only figure links truth-free detector review cases to the
saved close50 29.5 mm synthetic ambiguity evidence.

Policy label: `local_2d_detector_physics_ambiguity_link_cpu_no_fwi`.
Detector review cases: `2`.
Review near-boundary nominal count: `2`.
Review cases with synthetic x ambiguity: `1`.
Ready for branch-localization claim: `True`.
Ready for per-seed physics-equivalence claim: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case link rows: `local_2d_detector_physics_ambiguity_link_cases.csv`.
- Group rows: `local_2d_detector_physics_ambiguity_link_groups.csv`.

Scope boundary:

This audit reads saved detector reliability rows and saved close50
coordinate-confidence summaries. It does not run FDTD, FWI, GPU
kernels, field FWI, 3D/HPC jobs, or neural-network training.

