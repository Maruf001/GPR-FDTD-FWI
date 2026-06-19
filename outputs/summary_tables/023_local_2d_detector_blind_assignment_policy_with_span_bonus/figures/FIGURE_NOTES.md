# Figure Notes

## `local_2d_detector_blind_assignment_policy.png`

This figure summarizes blind score/diversity assignment policies over saved
detector B-scans. It does not rerun FDTD, FWI, GPU kernels, field FWI,
or 3D/HPC work.

Policy label: `local_2d_detector_blind_assignment_policy_saved_bscan_cpu`.
Case/policy rows: `46656`.
Best config: `none_top20_moderate12_baseline`.
Best assignment policy: `top20_minx8_span0p5`.
Best all-truth cases: `2`.
GPU used: `False`.

No blind score/diversity assignment policy recovers all cases. The detector still supplies useful candidate lists, but detector-to-FWI should be framed as rank-gated or oracle/upper-bound unless a stronger assignment rule is introduced.

