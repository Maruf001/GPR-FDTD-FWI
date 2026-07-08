# Figure Notes

## `close50_branch_preservation_probe_readiness.png`

This CPU-only figure scores the close50 rows from the branch-preservation
actionability table against the saved close50 sampling-boundary and
source-count evidence.

Candidate rows: `3`.
Single bounded GPU replicate ready: `True`.
Recommended case: `274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives`.
Recommended new seed options: `13,21`.
Broad GPU queue ready: `False`.

Scope boundary:

This scorecard reads saved outputs only. It does not launch FDTD/FWI,
detector-seeded FWI, broad close50 sweeps, field FWI, or 3D/HPC jobs.

