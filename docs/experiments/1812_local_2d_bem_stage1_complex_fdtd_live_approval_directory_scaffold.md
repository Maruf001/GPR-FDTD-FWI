# Experiment 1812: BEM Stage-1 Complex FDTD Live Approval Directory Scaffold

Date: 2026-07-01

## Purpose

Create the empty live-approval drop directory for the BEM stage-1 FDTD return.

This run creates the directory only. It does not create a live approval JSON,
create a BEM partial-return CSV, authorize FDTD, execute FDTD, run BEM/FDTD
comparison, transfer to field data, or start 3D/HPC work.

## Output

```text
outputs/experiments/1812_local_2d_bem_stage1_complex_fdtd_live_approval_directory_scaffold
```

## Result

```text
scaffold rows:                    1
approval directory present:       true
approval directory present before true
live approval file present:       false
accepted live approvals:          0
FDTD producer authorized now:     false
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
field transfer ready:             false
3D/HPC ready:                     false
```

The empty approval drop directory is:

```text
outputs/experiments/_external_2d_returns/bem_stage1_complex_fdtd_pending
```

The live approval JSON is still absent:

```text
outputs/experiments/_external_2d_returns/bem_stage1_complex_fdtd_pending/APPROVED_BEM_STAGE1_COMPLEX_FDTD_RETURN.json
```

## Interpretation

The BEM-specific 2D approval drop directory exists, but the live approval JSON
is still absent.

## Decision

Use this empty directory as the live approval drop location. Keep FDTD execution
and BEM/FDTD comparison blocked until a real approval JSON and real partial
return pass intake.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_directory_scaffold.py
2 passed
```

Figure check:

```text
1925x847, dynamic range=255
```
