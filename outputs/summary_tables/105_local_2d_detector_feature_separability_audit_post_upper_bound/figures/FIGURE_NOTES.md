# Figure Notes

## `local_2d_detector_feature_separability_audit.png`

This figure audits saved detector/component-gate candidate triples. It
does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or
neural-network training.

Policy label: `local_2d_detector_feature_separability_audit_cpu_no_fwi`.
Cases: `12`.
Candidate triples: `12180`.
All-truth triples: `49`.
Best top-1 feature: `score_component_balanced`.
Best top-1 all-truth cases: `0`.
Minimal all-case rank-gated budget: `200`.
Leave-one-case top-1 all-truth cases: `0`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Truth triples are present but rare, and no cross-validated top-1 truth-free feature selector is ready. Treat detector evidence as rank-gated upper-bound/context evidence; do not launch detector-seeded FWI from this selector state.

