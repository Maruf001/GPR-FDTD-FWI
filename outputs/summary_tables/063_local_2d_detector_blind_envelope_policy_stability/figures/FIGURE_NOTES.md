# Figure Notes

## `local_2d_detector_blind_envelope_policy_stability.png`

This CPU-only figure audits how stable the blind-envelope detector
assignment is across the saved 288-policy grid.

Policy label: `local_2d_detector_blind_envelope_policy_stability_cpu_no_fwi`.
All-variant success cases: `10`.
Partial-success cases: `2`.
Tuning-sensitive cases: `2`.
Minimum success fraction: `0.53125`.
Tuning-sensitive case labels: `target2_close50_linear29p5|seed13|nominal;target2_close50_linear29p5|seed34|nominal`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case stability rows: `local_2d_detector_blind_envelope_policy_stability_cases.csv`.
- Branch stability rows: `local_2d_detector_blind_envelope_policy_stability_branches.csv`.

Scope boundary:

This audit reads saved blind-envelope selected-case rows only. It does
not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or
neural-network training.

