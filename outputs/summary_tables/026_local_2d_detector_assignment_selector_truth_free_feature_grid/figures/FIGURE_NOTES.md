# Figure Notes

## `local_2d_detector_assignment_selector.png`

This figure compares truth-free selector heuristics against the fixed
shared blind-assignment policy and the per-case policy oracle. It reads
saved assignment rows only and does not rerun FDTD, FWI, GPU kernels,
field FWI, or 3D/HPC work.

Policy label: `local_2d_detector_assignment_selector_truth_free_feature_grid`.
Selector candidates: `220`.
Best in-sample selector: `span_target70_w1_rank_lite_center0.06_gap0`.
Best in-sample all-truth cases: `1`.
Leave-one-case all-truth cases: `0`.
Shared-policy all-truth cases: `2`.
Per-case oracle all-truth cases: `7`.
GPU used: `False`.

The truth-free selector grid does not improve on the fixed shared policy under leave-one-case validation. The policy-oracle gap should be treated as evidence for missing selector features or the need for downstream objective gating, not as a ready detector-to-FWI initializer.

