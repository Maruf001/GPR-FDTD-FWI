# Figure Notes

## `local_2d_detector_blind_assignment_policy.png`

This figure summarizes blind score-based assignment policies over saved
detector B-scans. It does not rerun FDTD, FWI, GPU kernels, field FWI,
or 3D/HPC work.

Policy label: `local_2d_detector_blind_assignment_policy_saved_bscan_cpu`.
Case/policy rows: `11664`.
Best config: `median_top40_dense4_baseline`.
Best assignment policy: `top40_minx20`.
Best all-truth cases: `1`.
GPU used: `False`.

No blind score-based assignment policy recovers all cases. The detector still supplies useful candidate lists, but detector-to-FWI should be framed as rank-gated or oracle/upper-bound unless a stronger assignment rule is introduced.

