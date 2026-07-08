# Figure Notes

## `local_2d_detector_fixed_radius_residual_ambiguity_audit.png`

This CPU-only figure audits why the guarded fixed-radius second-pass
pilot stopped at a 1 mm residual instead of exact recovery.

Policy label: `local_2d_detector_fixed_radius_residual_ambiguity_audit_cpu_no_gpu`.
Final L-infinity residual: `1.0` mm.
Truth selected but ambiguous: `1`.
Truth present but objective prefers neighbor: `1`.
Truth absent after non-overlap filtering: `1`.
GPU priority: `none`.

Scope boundary:

This audit does not authorize another GPU iteration, broad detector
queue, detector-seeded FWI, field transfer, 3D/HPC work, or neural
network training.

