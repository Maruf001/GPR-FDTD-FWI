# Figure Notes

## `local_2d_detector_blind_envelope_robustness_audit.png`

This CPU-only figure audits held-out split robustness and
truth-versus-wrong score margins for the blind component-envelope
detector assignment policy.

Policy label: `local_2d_detector_blind_envelope_robustness_audit_cpu_no_fwi`.
Full-success variants: `117`.
Leave-one-seed all-slot cases: `12`.
Leave-one-branch all-slot cases: `11`.
Leave-one-condition all-slot cases: `12`.
Minimum truth-versus-wrong score margin: `0.08362755681394554`.
Robustness boundary: `seed_and_condition_robust_but_not_branch_independent`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Held-out split rows: `local_2d_detector_blind_envelope_robustness_split_rows.csv`.
- Margin rows: `local_2d_detector_blind_envelope_robustness_margin_rows.csv`.

Scope boundary:

This audit reads saved detector component rows and saved blind-envelope
policy rows only. It does not run FDTD, FWI, GPU kernels, field FWI,
3D/HPC jobs, or neural-network training.

