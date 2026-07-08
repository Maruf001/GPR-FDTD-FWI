# BEM Experiment Trackers

This folder tracks the boundary element method research stream.

It is intentionally separate from the synthetic FDTD/FWI tracker stream:

```text
docs/experiments/
outputs/experiments/
```

and from the measured field-data tracker stream:

```text
docs/field_experiments/
outputs/field_experiments/
```

The matching output convention is:

```text
outputs/bem_experiments/NNN_run_name
```

Use this track for:

- BEM repository and library evaluations.
- Reproduction of provided 2D GPR-BEM cases.
- 2D BEM versus 2D FDTD cross-checks.
- Minimal 3D BEM forward-model prototypes.
- BEM/FDTD validation matrices.
- BEM readiness or blocker reports.

Do not use this stream for current synthetic FDTD/FWI runs or measured GSSI
field-QC runs. Keep those in their existing tracker families.

The BEM output tree may contain shallow external repository snapshots, build
directories, generated meshes, and solver outputs. It is therefore ignored by
Git except for the top-level README.
