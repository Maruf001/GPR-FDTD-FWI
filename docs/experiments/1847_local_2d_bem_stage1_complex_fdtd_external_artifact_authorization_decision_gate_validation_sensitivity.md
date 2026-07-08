# Experiment 1847: BEM Stage-1 Complex FDTD External Artifact Authorization Decision Gate Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `1846` authorization-decision validator.

## Result

```text
source validator ready:                true
scenarios:                             22
expected pass scenarios:               1
expected fail scenarios:               21
observed pass scenarios:               1
observed fail scenarios:               21
unexpected outcomes:                   0
damaged scenarios rejected:            21
live files:                            0
missing files:                         2
FDTD producer authorized now:          false
FDTD executed now:                     false
BEM/FDTD comparison ready:             false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

Rejected damaged states include false live-file, hash, ready-recheck,
authorization, command, accepted-artifact, FDTD execution, BEM/FDTD
comparison, field/3D/GPU, figure, and script-snapshot promotion.

## Decision

Use runs `1845-1847` as the guarded no-authorization decision block for the
BEM stage-1 external artifacts.

Focused validation: `11 passed`.

Figure check: `3365x886`, dynamic range `255`.
