# Figure Notes

## `local_2d_detector_rank_budget_diagnostic.png`

This CPU-only diagnostic reads the saved all-triples detector gate rows
and summarizes how many candidate triples per case are needed before
an all-truth detector triple appears under each objective.

Policy label: `local_2d_detector_rank_budget_diagnostic_cpu_no_fwi`.
Cases: `12`.
Candidate-triple rows: `12180`.
Best top-20 objective: `span_bonus` with `6` cases.
Best top-50 objective: `span_bonus` with `8` cases.
Minimal all-case budget: `200` candidate triples per case.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case diagnostics: `local_2d_detector_rank_budget_case_diagnostic.csv`.
- Objective diagnostics: `local_2d_detector_rank_budget_objective_summary.csv`.
- Budget curve: `local_2d_detector_rank_budget_curve.csv`.
- Summary: `local_2d_detector_rank_budget_diagnostic_summary.json`.

Scope boundary:

This diagnostic does not run FDTD, FWI, GPU kernels, field FWI,
3D/HPC jobs, or neural-network training.

