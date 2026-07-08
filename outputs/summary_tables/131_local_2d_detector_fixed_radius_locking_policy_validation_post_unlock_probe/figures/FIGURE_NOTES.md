# Figure Notes

## `local_2d_detector_fixed_radius_locking_policy_validation.png`

This CPU-only figure summarizes the guarded validation probe for the
fixed-radius near-tie downstream-clearance locking design.

Policy label: `local_2d_detector_fixed_radius_locking_policy_validation_cpu_synthesis`.
Exact geometry recovered: `True`.
Truth selected but ambiguous count: `1`.
Guard max GPU utilization: `88.0` percent.
Guard max RAM used: `14.687683727827094` percent.
GPU priority: `none`.

Scope boundary:

This validates one fixed-radius mechanism branch. It does not authorize
a broad detector queue, detector-seeded FWI, field transfer, 3D/HPC work,
or neural-network training.

