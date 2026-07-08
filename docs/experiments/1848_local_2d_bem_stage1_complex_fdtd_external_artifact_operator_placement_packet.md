# Experiment 1848: BEM Stage-1 Complex FDTD External Artifact Operator Placement Packet

Date: 2026-07-02

## Purpose

Package the exact live artifact paths and receipt fields required before the
BEM stage-1 complex FDTD producer can be reconsidered for authorization.

This run does not create, fake, or accept the missing artifacts. It converts
the no-authorization decision from runs `1845-1847` into an operator-facing
placement packet.

## Output

```text
outputs/experiments/1848_local_2d_bem_stage1_complex_fdtd_external_artifact_operator_placement_packet
```

## Result

```text
operator packet rows:                  2
parent directories ready:              2
source templates ready:                1
live files:                            0
missing files:                         2
observed SHA-256 values:               0
observed file sizes:                   0
parse/schema checks passed:            0
ready for acceptance recheck rows:     0
blocking decisions:                    2
FDTD producer authorized now:          false
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

Required live artifacts:

```text
outputs/experiments/_external_2d_returns/bem_stage1_complex_fdtd_pending/APPROVED_BEM_STAGE1_COMPLEX_FDTD_RETURN.json
outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_partial.csv
```

## Decision

Place the live approval JSON and BEM stage-1 partial-return CSV, then populate
observed SHA-256, file size, and parse/schema receipt fields before rerunning
any guarded acceptance gate or FDTD producer authorization. Until then,
Project-FDTD execution, real BEM/FDTD comparison, field transfer, GPU
escalation, and 3D/HPC remain blocked.

## Validation

```text
3 focused tests passed
py_compile passed
figure: 2645x829, dynamic range=255
script snapshots: 2
```
