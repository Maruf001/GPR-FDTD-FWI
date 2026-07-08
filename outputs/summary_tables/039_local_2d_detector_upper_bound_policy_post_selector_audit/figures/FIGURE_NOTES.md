# Figure Notes

## `local_2d_detector_upper_bound_policy.png`

This CPU-only policy synthesis separates detector rank-gated upper-bound
evidence from deployable detector-seeded FWI readiness.

Policy label: `local_2d_detector_upper_bound_policy_cpu_no_fwi`.
Best rank-gated upper-bound strategy: `component_gate_minimal_all_case_upper_bound`.
Minimal all-case rank-gated triples per case: `200`.
Selector leave-one-case all-truth cases: `0`.
Ready for rank-gated upper-bound claim: `True`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Policy rows: `local_2d_detector_upper_bound_policy_rows.csv`.
- Summary: `local_2d_detector_upper_bound_policy_summary.json`.

Scope boundary:

This synthesis reads saved CPU summaries only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

