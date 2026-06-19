# Figure Notes

## `local_2d_baseline_readiness_audit.png`

This CPU-only audit summarizes existing synthetic detector,
detector-seeded refinement, multi-rebar assignment, and field
hyperbola-template evidence for manuscript baseline planning.

Policy label: `local_2d_baseline_readiness_cpu_first_no_gpu`.
Baseline rows: `6`.
Ready baseline rows: `2`.
Single-detector scenarios: `96`.
Single-detector hit rate: `1.000`.
Two-stage exact fraction: `1.000`.
Immediate GPU candidates: `0`.
Conditional GPU candidates: `0`.

Outputs:

- Baseline rows: `local_2d_baseline_readiness_rows.csv`.
- Summary: `local_2d_baseline_readiness_summary.json`.
- Figure validation: `figure_validation.csv`.

Scope boundary:

The audit plans baseline comparisons; it does not run detector,
FDTD, FWI, GPU, field FWI, 3D/HPC, or neural-network jobs.

