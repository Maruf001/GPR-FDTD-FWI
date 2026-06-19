# Figure Notes

## `local_2d_detector_image_objective_gate.png`

This figure compares saved-row detector assignment gates. The image
objective scores assigned triples against saved detector B-scans with
Gaussian hyperbola masks and time-offset families. It does not rerun
FDTD, FWI, GPU kernels, field FWI, or 3D/HPC work.

Policy label: `local_2d_detector_image_objective_gate_saved_bscan_cpu`.
Primary objective: `row_background_sigma60`.
Primary objective all-truth cases: `0`.
Shared-policy all-truth cases: `2`.
Rank/span selector all-truth cases: `0`.
Policy-oracle all-truth cases: `7`.
GPU used: `False`.

The saved-B-scan image objective gate does not improve on the fixed shared policy. Treat the policy-oracle gap as requiring a stronger waveform/objective gate or an explicitly bounded oracle/rank-gated upper-bound, not as a ready automatic detector handoff.

