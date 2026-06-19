# Figure Notes

## `local_2d_detector_separability_blocker_triage.png`

This figure triages saved detector feature-separability outputs. It
does not run FDTD, FWI, detector scoring, GPU kernels, field FWI,
3D/HPC work, or neural-network training.

Policy label: `local_2d_detector_separability_blocker_triage_cpu_no_fwi`.
Cases: `12`.
Best top-50 cases: `11`.
Leave-one top-50 cases: `7`.
Leave-one top-200 cases: `9`.
Feature-generalization failures: `3`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

The detector candidate space is sufficient for a rank-gated upper-bound, but the truth-free feature choice does not generalize. The hardest blockers are close50 source-mismatch cases where per-case features rank truth within top-10/top-50, but leave-one-case feature choice pushes truth deeper than top-200. Do not launch detector-seeded FWI from this selector state.

