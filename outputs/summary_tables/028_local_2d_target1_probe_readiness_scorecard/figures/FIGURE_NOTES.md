# Figure Notes

## `local_2d_target1_probe_readiness_scorecard.png`

This CPU-only scorecard consolidates the saved target1 weak-exact,
acquisition-confidence, source-density exception, and next-question
outputs into explicit target1 GPU-probe gates.

Policy label: `local_2d_target1_probe_readiness_requires_new_hypothesis`.
Scorecard rows: `10`.
Triggered gates: `0`.
GPU action count: `0`.
Ready for target1 GPU probe: `False`.
Modern exception series: `0`.

Outputs:

- Scorecard rows: `local_2d_target1_probe_readiness_rows.csv`.
- Summary: `local_2d_target1_probe_readiness_summary.json`.
- Figure validation: `figure_validation.csv`.

Scope boundary:

The scorecard reads existing CSV/JSON artifacts only. It does not run
FDTD, FWI, optimizer, GPU, 3D/HPC, field FWI, or neural-network jobs.

