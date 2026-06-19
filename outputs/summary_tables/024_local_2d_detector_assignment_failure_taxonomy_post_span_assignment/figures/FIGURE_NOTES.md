# Figure Notes

## `local_2d_detector_assignment_failure_taxonomy.png`

This figure summarizes the best blind assignment row for each saved
close14/close50 detector case. It reads saved assignment rows only and
does not rerun FDTD, FWI, GPU kernels, field FWI, or 3D/HPC work.

Policy label: `local_2d_detector_assignment_failure_taxonomy_saved_rows`.
Cases: `12`.
All-truth cases: `7`.
Dominant failure: `all_truth`.
GPU used: `False`.

The best blind assignment rows still fail most cases. Use this taxonomy to design a stronger assignment model before any detector-to-FWI handoff, or label detector-seeded FWI as an oracle/rank-gated upper-bound.

