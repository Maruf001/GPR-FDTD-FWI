# Figure Notes

## `local_2d_detector_candidate_rank_policy.png`

This figure summarizes top-N candidate-rank requirements from saved
detector sensitivity rows. It does not rerun FDTD, FWI, GPU kernels,
field FWI, or 3D/HPC work.

Policy label: `local_2d_detector_candidate_rank_policy_saved_bscan_cpu`.
Cases: `12`.
Configurations: `81`.
Minimal rank cap for full recovery: `40`.
Best config: `none_top40_moderate12_baseline`.
Best-config mean max assigned rank: `21.333333333333332`.
Best-config worst max assigned rank: `32.0`.
GPU used: `False`.

All cases are recoverable only with a deeper candidate budget. Use the detector as a truth-containing candidate generator, and gate any detector-to-FWI pilot by rank/cost.

