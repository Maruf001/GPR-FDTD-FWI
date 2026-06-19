# Figure Notes

## `local_2d_detector_selector_feature_family_audit.png`

This figure compares leave-one-case detector selector policies over saved
feature-rank outputs. It does not run FDTD, FWI, detector scoring, GPU
kernels, field FWI, 3D/HPC work, or neural-network training.

Policy label: `local_2d_detector_selector_feature_family_audit_cpu_no_fwi`.
Best policy: `component_only` / `branch`.
Best top50 cases: `10`.
Best top200 cases: `12`.
Top200 gain over all-feature global selector: `3`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Restricting detector selector features to component/waveform scores removes the span-target overfit that caused the close50 source-mismatch deeper-than-top200 failures. The best selector reaches all cases within top200 and improves top50 coverage over the all-feature global selector, but top1 all-truth recovery remains 0 cases, so detector-seeded FWI is still blocked.

