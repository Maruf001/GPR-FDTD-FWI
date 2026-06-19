# Figure Notes

## `local_2d_detector_handoff_budget.png`

This CPU-only synthesis compares detector candidate-list recall,
blind assignment, per-case oracle assignment, and saved-B-scan
image-objective gating as possible detector-to-FWI handoffs.

Policy label: `local_2d_detector_handoff_budget_cpu_no_fwi`.
Strategies: `7`.
Cheapest full candidate strategy: `branch_top20_candidate_list`.
Cheapest full candidate triples per case: `1140`.
Best deployable all-truth cases: `2`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Strategy rows: `local_2d_detector_handoff_budget_rows.csv`.
- Summary: `local_2d_detector_handoff_budget_summary.json`.
- Figure validation: `figure_validation.csv`.

Scope boundary:

The budget reads saved detector summaries only. It does not run
detectors, FDTD, FWI, GPU kernels, 3D/HPC jobs, or neural-network training.

