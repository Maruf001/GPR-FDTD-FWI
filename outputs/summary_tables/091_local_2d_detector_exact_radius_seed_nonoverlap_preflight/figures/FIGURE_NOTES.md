# Figure Notes

## `local_2d_detector_exact_radius_seed_nonoverlap_preflight.png`

This figure checks whether stable detector-exported coordinate seeds
remain physically non-overlapping when the controlled synthetic
`5,6,8` mm radius prior is imposed.

Direct-ready stable seeds: `7`.
Overlap-blocked stable seeds: `3`.
Maximum repair required: `2.000` mm.

Scope boundary:

This is a CPU preflight for future narrow synthetic fixed-radius
pilots. It does not run FDTD/FWI, infer detector radii/materials,
transfer to field data, or authorize broad GPU work.

