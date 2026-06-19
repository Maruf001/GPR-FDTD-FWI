# Figure Notes

## `local_2d_detector_blind_envelope_reliability_gate.png`

This CPU-only figure builds a truth-free reliability gate from
policy-grid x-slot drift across blind-envelope detector selections.

Policy label: `local_2d_detector_blind_envelope_reliability_gate_cpu_no_fwi`.
Stable slot-range threshold: `5.0` mm.
Stable assignments: `10`.
Review assignments: `2`.
Tuning-sensitive cases detected: `2`.
Ready for reliability claim: `True`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case reliability rows: `local_2d_detector_blind_envelope_reliability_gate_cases.csv`.
- Branch reliability rows: `local_2d_detector_blind_envelope_reliability_gate_branches.csv`.

Scope boundary:

This audit reads saved CPU detector-policy rows only. The gate itself
uses no truth labels, while the success fractions are used only for
post-hoc evaluation. It does not run FDTD, FWI, GPU kernels, field
FWI, 3D/HPC jobs, or neural-network training.

