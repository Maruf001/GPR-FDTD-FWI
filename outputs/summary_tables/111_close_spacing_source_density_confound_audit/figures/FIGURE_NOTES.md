# Figure Notes

## `close_spacing_source_density_confound_audit.png`

This CPU-only figure audits matched controls and confounds in the
close50/close14 source-density comparison.

Matched control factors: `5`.
Acquisition confounds: `1`.
Geometry confounds: `1`.
Context-only factors: `1`.
Spacing-only causal generalization ready: `False`.
Broad GPU queue ready: `False`.

Scope boundary:

This audit reads saved synthetic 2D summaries. It does not run FDTD/FWI,
GPU kernels, detector-seeded FWI, field FWI, 3D/HPC, or neural-network training.

