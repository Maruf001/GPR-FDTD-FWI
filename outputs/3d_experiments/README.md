# 3D Experiment Outputs

This directory is reserved for future 3D GPR FDTD/FWI run products.

It is intentionally separate from:

- `outputs/experiments`, the mature 2D synthetic experiment archive;
- `outputs/field_experiments`, the field/lab data output stream.

Expected run layout:

```text
outputs/3d_experiments/NNN_run_name/
  README.md
  run_manifest.json
  data/
  figures/
```

Before any A100/NERSC run writes here, create the matching tracker under
`docs/3d_experiments` and save a budget/runtime-memory estimate. Do not write
full 3D fields for all time steps by default; prefer receiver traces, sparse
snapshots, summary tables, and selected figures.
