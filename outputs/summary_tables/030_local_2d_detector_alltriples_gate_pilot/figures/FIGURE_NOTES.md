# Figure Notes

## `local_2d_detector_alltriples_gate_pilot.png`

This CPU-only pilot scores all detector candidate triples from the
branch-specific top-20 saved-B-scan detector configurations.

Policy label: `local_2d_detector_alltriples_gate_pilot_cpu_no_fwi`.
Cases: `12`.
Candidate-triple rows: `12180`.
Best top1 all-truth case count: `0`.
Best top10 objective: `span_bonus` with `2` cases.
Best top50 objective: `span_bonus` with `8` cases.
Ready for detector-seeded FWI: `False`.

Outputs:

- Combo scores: `local_2d_detector_alltriples_gate_rows.csv`.
- Case/objective summary: `local_2d_detector_alltriples_gate_case_objective_summary.csv`.
- Objective summary: `local_2d_detector_alltriples_gate_objective_summary.csv`.
- Summary: `local_2d_detector_alltriples_gate_summary.json`.

Scope boundary:

The pilot reads saved B-scans and reruns detector candidate scoring on CPU.
It does not run FDTD, FWI, GPU kernels, 3D/HPC jobs, field FWI, or neural-network training.

