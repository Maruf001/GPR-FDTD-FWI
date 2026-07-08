# Figure Notes

## `local_2d_detector_component_waveform_gate.png`

This CPU-only pilot scores detector candidate triples with component-wise
hyperbola waveform-mask support on saved B-scans.

Policy label: `local_2d_detector_component_waveform_gate_cpu_no_fwi`.
Cases: `12`.
Candidate-triple rows: `12180`.
Component candidates scored: `230`.
Best top-10 objective: `component_balanced` with `3` cases.
Best top-50 objective: `component_balanced` with `10` cases.
Best top-1 all-truth cases: `0`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Scored triples: `local_2d_detector_component_waveform_gate_rows.csv`.
- Case/objective rows: `local_2d_detector_component_waveform_gate_case_objective_summary.csv`.
- Objective summary: `local_2d_detector_component_waveform_gate_objective_summary.csv`.
- Budget curve: `local_2d_detector_component_waveform_gate_budget_curve.csv`.
- Summary: `local_2d_detector_component_waveform_gate_summary.json`.

Scope boundary:

This pilot reads saved B-scans and runs CPU image scoring only. It does not
run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

