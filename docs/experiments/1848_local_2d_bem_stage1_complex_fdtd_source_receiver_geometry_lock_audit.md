# Experiment 1848: BEM Stage-1 FDTD Source/Receiver Geometry Lock Audit

Date: 2026-07-02

## Purpose

Convert the guarded BEM acquisition-geometry sensitivity result into 2D-side
requirements for the pending BEM stage-1 FDTD partial return.

The current BEM stage-1 FDTD return path still has no live approval JSON and
no partial-return CSV. This run records the geometry fields that must accompany
any future FDTD return before a real BEM/FDTD comparison is allowed.

This is a CPU-only 2D control audit. It does not authorize FDTD, execute FDTD,
compare BEM against FDTD, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1848_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit
```

## Result

```text
source authorization decision ready:        true
source BEM geometry ready:                  true
geometry lock rows:                         6
required geometry locks:                    6
currently satisfied geometry locks:         0
blocking FDTD authorization locks:          6
blocking BEM/FDTD comparison locks:         6
live files:                                 0
missing files:                              2
FDTD producer authorized now:               false
FDTD executed now:                          false
real BEM/FDTD comparison ready:             false
BEM peak offset span at z=0:                2.6214537950832346 dB
BEM max relative L2 across offset:          0.7099232724148534
BEM max relative L2 across antenna z:       0.4171376953084501
BEM max relative L2 across full grid:       0.9115427115447009
geometry locks ready for FDTD authorization:false
geometry locks ready for BEM/FDTD comparison:false
field transfer ready:                       false
3D/HPC ready:                               false
gpu priority:                               none
```

Geometry locks:

| Priority | Lock | Required return field | BEM metric | Value |
| ---: | --- | --- | --- | ---: |
| 1 | Tx/Rx offset | `tx_rx_offset_m` | max relative L2 across offset | 0.7099232724148534 |
| 2 | antenna z | `antenna_z_m` | max relative L2 across antenna z | 0.4171376953084501 |
| 3 | source/receiver coordinates | `source_x_m;source_z_m;receiver_x_m;receiver_z_m` | peak span across offset | 2.6214537950832346 |
| 4 | phase-center reference | `phase_center_reference` | peak-time span across offset | 0.13190034196385092 |
| 5 | BEM geometry case identity | `bem_geometry_case_id` | full-grid max relative L2 | 0.9115427115447009 |
| 6 | geometry sidecar or columns | `geometry_sidecar_path_or_geometry_columns` | missing file count | 2 |

## Interpretation

The pending FDTD partial return cannot be treated as a fair BEM/FDTD comparison
unless it carries source/receiver geometry. Receiver index and frequency are
not enough. The future return must state Tx/Rx spacing, antenna z-position,
source and receiver coordinates, phase-center reference, and the BEM geometry
case it is intended to match.

## Decision

Keep FDTD authorization, FDTD execution, and BEM/FDTD comparison blocked until
the live approval JSON and partial-return CSV are present and include the
required geometry information.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
4 passed
```

Python compile check:

```text
run_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
pass
```

Figure check:

```text
3293x871, dynamic range=255
```
