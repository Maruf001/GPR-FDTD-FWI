# Figure Notes

## `local_2d_detector_component_selector_audit.png`

This CPU-only audit evaluates truth-free selectors over saved component
waveform-gated detector triples.

Policy label: `local_2d_detector_component_selector_audit_cpu_no_fwi`.
Selector candidates: `975`.
Best in-sample selector: `cb0.4_min0.4_span0.25_target70.0_tw0.25_rank0.08`.
Best in-sample all-truth cases: `1`.
Leave-one-case all-truth cases: `0`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Selector summary: `local_2d_detector_component_selector_summary.csv`.
- Best selected cases: `local_2d_detector_component_selector_best_cases.csv`.
- Cross-validation cases: `local_2d_detector_component_selector_cv_cases.csv`.

Scope boundary:

This audit reads saved CPU rows only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

