# Figure Notes

## `local_2d_detector_fixed_radius_locking_policy_design.png`

This CPU-only figure designs a truth-free near-tie downstream-clearance
lock after the fixed-radius second-pass residual audit.

Policy label: `local_2d_detector_fixed_radius_locking_policy_design_cpu_selector`.
Near-tie relative threshold: `0.05`.
Selected lock target: `1`.
Selected lock coordinate: `[250.0,90.0]` mm.
Ready for one guarded unlock probe: `True`.
GPU priority: `single_guarded_unlock_probe_candidate`.

Scope boundary:

This design can justify at most one guarded validation probe. It does
not authorize a broad GPU queue, detector-seeded FWI, field transfer,
3D/HPC work, or neural-network training.

