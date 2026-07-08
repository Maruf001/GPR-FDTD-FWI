# Experiment 1849: BEM Stage-1 FDTD Source/Receiver Geometry Lock Audit Validator

Date: 2026-07-02

## Purpose

Validate the run `1848` source/receiver geometry lock audit from saved
artifacts.

This run checks the six geometry locks, required geometry-field state,
no-live-artifact state, BEM geometry metric basis, blocked downstream scope,
figure output, and script snapshots.

This is a CPU-only validation run. It does not authorize FDTD, execute FDTD,
compare BEM against FDTD, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1849_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validator
```

## Result

```text
validation checks:                       6
passed checks:                           6
failed checks:                           0
geometry lock rows:                      6
required geometry locks:                 6
currently satisfied geometry locks:      0
blocking FDTD authorization locks:       6
blocking BEM/FDTD comparison locks:      6
live files:                              0
missing files:                           2
FDTD producer authorized now:            false
FDTD executed now:                       false
real BEM/FDTD comparison ready:          false
BEM peak offset span at z=0:             2.6214537950832346 dB
BEM max relative L2 across offset:       0.7099232724148534
BEM max relative L2 across antenna z:    0.4171376953084501
BEM max relative L2 across full grid:    0.9115427115447009
geometry locks ready for authorization:  false
geometry locks ready for comparison:     false
field transfer ready:                    false
3D/HPC ready:                            false
gpu priority:                            none
validation ready:                        true
```

Validation checks:

| Check order | Validation check | Passed |
| ---: | --- | --- |
| 1 | source audit identity and readiness | true |
| 2 | geometry lock shape and required fields | true |
| 3 | no-live-artifact state preserved | true |
| 4 | BEM geometry metric basis | true |
| 5 | downstream claims blocked | true |
| 6 | figure and scripts valid | true |

## Interpretation

The geometry-lock audit validates as the current 2D-side handoff boundary for
the pending BEM stage-1 FDTD return. No FDTD authorization or BEM/FDTD
comparison is allowed while the live approval JSON, partial-return CSV, and
geometry-lock fields are absent.

## Decision

Use runs `1848-1849` as the guarded source/receiver geometry-lock block for
the BEM stage-1 FDTD return.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validator.py
8 passed
```

Python compile check:

```text
run_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
run_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validator.py
pass
```

Figure check:

```text
2717x864, dynamic range=255
```
