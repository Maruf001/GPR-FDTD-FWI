# Experiment 1839: BEM Stage-1 External Artifact Receipt Checklist

Date: 2026-07-01

## Purpose

Create a fillable receipt checklist for the two live external artifacts needed
before the first BEM stage-1 complex FDTD producer can be authorized.

The two required artifacts are:

```text
live approval JSON
BEM stage-1 partial-return CSV
```

This is a CPU-only checklist run. It does not create live artifacts, authorize
FDTD execution, run FDTD, complete a BEM/FDTD comparison, transfer to field
evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1839_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_checklist
```

## Result

```text
source claim boundary ready:           true
source validation ready:               true
source sensitivity ready:              true
receipt rows:                          2
pending receipt rows:                  2
present live files:                    0
accepted artifacts:                    0
parent directories present:            2
source templates present:              1
blank observed SHA-256 values:         2
blank observed file sizes:             2
ready for acceptance recheck:          0
FDTD producer authorized now:          false
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

## Interpretation

The BEM stage-1 external handoff now has a two-row receipt checklist. It
records where the live approval JSON and partial-return CSV must appear, which
artifact-specific parse/schema check applies, and which receipt fields remain
blank until files arrive.

Both live artifacts are still absent. This means the receipt checklist is ready
as a controlled intake aid, but it does not authorize FDTD execution or a
BEM/FDTD comparison.

## Decision

Keep FDTD authorization, FDTD execution, real BEM/FDTD comparison, field
transfer, and 3D/HPC blocked until both live artifacts arrive and pass the
external artifact acceptance gate.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_checklist.py
4 passed
```

Figure check:

```text
1870x790, dynamic range=255
```
