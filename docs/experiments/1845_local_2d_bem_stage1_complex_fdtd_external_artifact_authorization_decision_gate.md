# Experiment 1845: BEM Stage-1 Complex FDTD External Artifact Authorization Decision Gate

Date: 2026-07-02

## Purpose

Convert the run `1842-1844` no-live-artifact refresh block into an explicit
authorization decision gate for the BEM stage-1 complex FDTD producer.

## Result

```text
artifact rows:                         2
live files:                            0
missing files:                         2
observed hashes / sizes:               0 / 0
approval JSON parseable:               0
partial-return CSV parseable:          0
ready for acceptance recheck:          0
blocking decisions:                    2
FDTD producer authorized now:          false
FDTD executed now:                     false
BEM/FDTD comparison ready:             false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

## Decision

Do not authorize the BEM stage-1 FDTD producer until both live artifacts are
present: the live approval JSON and the BEM stage-1 partial-return CSV.

Figure check: `2753x856`, dynamic range `255`.
