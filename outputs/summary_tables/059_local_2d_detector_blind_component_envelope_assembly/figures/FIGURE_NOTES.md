# Figure Notes

## `local_2d_detector_blind_component_envelope_assembly.png`

This CPU-only figure evaluates a blind component-envelope assembly
policy over saved local 2D detector component rows.

Policy label: `local_2d_detector_blind_component_envelope_assembly_cpu_no_fwi`.
Best all-target-slot cases: `12`.
Leave-one-case all-target-slot cases: `12`.
Known-slot upper bound cases: `12`.
Uses branch slots for selection: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Variant grid: `local_2d_detector_blind_component_envelope_assembly_variants.csv`.
- Selected case rows: `local_2d_detector_blind_component_envelope_assembly_selected_cases.csv`.
- Leave-one-case rows: `local_2d_detector_blind_component_envelope_assembly_leave_one_case.csv`.

Scope boundary:

The selector uses candidate component support envelopes and spacing
structure, not the known branch slot coordinates. Truth is used only
to score the policy grid and report target-slot recovery. This does
not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or
neural-network training.

