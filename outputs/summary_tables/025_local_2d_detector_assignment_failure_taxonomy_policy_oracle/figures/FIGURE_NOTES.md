# Figure Notes

## `local_2d_detector_assignment_failure_taxonomy.png`

This figure summarizes a per-case policy-oracle: for each saved
close14/close50 detector case, it picks the best row from the saved
blind-assignment grid. It is not a deployable shared policy result.
It reads saved assignment rows only and does not rerun FDTD, FWI,
GPU kernels, field FWI, or 3D/HPC work.

Policy label: `local_2d_detector_assignment_failure_taxonomy_per_case_policy_oracle`.
Selection scope: `per_case_best_assignment_policy_oracle`.
Cases: `12`.
Per-case oracle all-truth cases: `7`.
Best deployable shared-policy all-truth cases: `2`.
Dominant failure: `all_truth`.
GPU used: `False`.

This is a per-case policy-oracle over saved blind-assignment rows, not a deployable shared policy. It shows exploitable signal in the candidate lists, but the best shared blind policy still fails most cases. Use this taxonomy to design a stronger assignment-policy selector or downstream objective gate before any detector-to-FWI handoff.

