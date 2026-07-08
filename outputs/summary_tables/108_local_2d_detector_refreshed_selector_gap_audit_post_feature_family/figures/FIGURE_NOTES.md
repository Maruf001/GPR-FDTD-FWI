# Figure Notes

## `local_2d_detector_refreshed_selector_gap_audit.png`

This CPU-only audit explains residual rank gaps after the refreshed detector
selector feature-family audit. It reads saved rank/separability outputs only.

Policy label: `local_2d_detector_refreshed_selector_gap_audit_cpu_no_fwi`.
Selected policy: `component_only` / `branch`.
Dominant feature: `score_component_balanced`.
Selected top50 cases: `10` / `12`.
Selected top200 cases: `12` / `12`.
Dominant top missing targets: `target0,target1`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

The refreshed component-only selector is useful as a rank-gated candidate-list result, but it remains a top-1 failure across all cases. Use this audit to explain residual false-vs-truth dominance and missing-target signatures; do not launch detector-seeded FWI.

Scope boundary: no FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or
neural-network training is performed by this audit.

