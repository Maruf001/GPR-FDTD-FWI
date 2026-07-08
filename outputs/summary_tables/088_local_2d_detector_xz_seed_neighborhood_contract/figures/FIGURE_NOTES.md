# Figure Notes

## `local_2d_detector_xz_seed_neighborhood_contract.png`

This CPU-only figure summarizes the branch-specific x/z seed-neighborhood
contract derived from saved detector seed artifacts.

Policy label: `local_2d_detector_xz_seed_neighborhood_contract_cpu_no_fwi`.
Stable contract cases: `10`.
Review cases excluded: `2`.
Branch half-widths: `target2_close14:10;target2_close50_linear29p5:12`.
Fine-grid reduction fraction: `0.3797848226436969`.
GPU priority: `none`.

Scope boundary:

This contract sizes coordinate-only x/z neighborhoods for saved stable detector
cases. It does not run refinement, FWI, GPU kernels, 3D/HPC jobs, or neural
network training, and it does not provide radius/material seeds.

