# 3D Experiment Trackers

This directory is the tracker root for future 3D GPR FDTD/FWI work.

It is intentionally separate from `docs/experiments`, which is the mature 2D
synthetic experiment tracker stream. Do not place 3D planning notes, NERSC/HPC
readiness notes, 3D solver validation notes, or neural-network 3D scout notes in
the 2D tracker sequence.

Suggested structure:

```text
docs/3d_experiments/
  README.md
  initial_plan/
  001_hpc_readiness.md
  002_budget_cfl_smoke.md
  nn_000_3dinvnet_audit.md
```

Large run products should stay under a separate output root such as
`outputs/3d_experiments` and should not be mixed with `outputs/experiments` or
`outputs/field_experiments`.
