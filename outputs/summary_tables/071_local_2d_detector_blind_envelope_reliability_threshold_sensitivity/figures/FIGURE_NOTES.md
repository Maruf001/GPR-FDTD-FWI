# Figure Notes

## `local_2d_detector_blind_envelope_reliability_threshold_sensitivity.png`

This CPU-only figure tests whether the x-slot drift reliability gate
depends on a brittle threshold choice.

Policy label: `local_2d_detector_blind_envelope_reliability_threshold_sensitivity_cpu_no_fwi`.
Threshold count: `12`.
Clean threshold count: `5`.
Clean threshold range: `5.0` to `19.0` mm.
Default threshold: `5.0` mm.
Default threshold clean: `True`.
Ready for reliability claim: `True`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Threshold rows: `local_2d_detector_blind_envelope_reliability_threshold_sensitivity_rows.csv`.

Scope boundary:

This audit reads saved CPU detector reliability rows only. It does not
run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network
training.

