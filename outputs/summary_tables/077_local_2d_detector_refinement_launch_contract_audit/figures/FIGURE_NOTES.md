# Figure Notes

## `local_2d_detector_refinement_launch_contract_audit.png`

This CPU-only figure audits whether the saved blind-envelope detector
assignments define a refinement launch contract.

Policy label: `local_2d_detector_refinement_launch_contract_audit_cpu_no_fwi`.
Candidate component seed table cases: `10` / `12`.
Review cases: `2`.
Active blocker count: `6`.
Active blockers: `radius_material_contract_missing;policy_grid_selected_on_saved_corpus;deployable_top1_selector_not_validated;branch_independent_transfer_not_robust;review_cases_present;per_seed_physics_equivalence_not_ready`.
Ready for component seed table: `True`.
Ready for narrow refinement contract: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Contract rows: `local_2d_detector_refinement_launch_contract_cases.csv`.
- Blocker rows: `local_2d_detector_refinement_launch_contract_blockers.csv`.

Scope boundary:

This audit reads saved detector policy rows only. It does not run FDTD,
FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

