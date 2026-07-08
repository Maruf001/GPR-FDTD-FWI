# BEM 3D External FDTD Return Inbox Preflight

Date: 2026-06-25

## Scope

This checkpoint records BEM run `104`, an executable preflight for the run
`103` external-FDTD return inbox.

No placeholder returned data was created. No BEM/FDTD comparison, 3D
validation, local 3D FDTD launch, GPU/HPC work, field FWI, or neural-network
training was started.

## Output

```text
outputs/bem_experiments/104_project_core_bem_3d_external_fdtd_return_inbox_preflight
docs/bem_experiments/104_project_core_bem_3d_external_fdtd_return_inbox_preflight.md
```

## Result

```text
preflight checks:                   18
passed checks:                      1
failed checks:                      17
blocking findings:                  17
required return files:              2
missing return files:               2
metadata fields required:           12
metadata fields missing/unfilled:   12
return inbox preflight ready:       false
real external FDTD data present:    false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
local 3D FDTD launch ready:         false
GPU/HPC ready:                      false
```

## Decision

Use run `104` as the acceptance preflight before installing returned external
3D FDTD data into the pending return root. The current blocker is concrete:
both target/background frequency-bin files and the completed metadata ledger
are absent.

## Milestone Snapshot

Frozen scripts:

```text
run_project_core_bem_3d_external_fdtd_return_inbox_preflight.py
sha256: 10bc3f2dd783a40bd650e36a88de886f78bd6b554584b8909257f05627473d5f

test_project_core_bem_3d_external_fdtd_return_inbox_preflight.py
sha256: 82223789449d08228892b43b367eb6b097996b8095face934a0f03130efc058b
```

Future BEM 3D return-intake experiments should begin from a duplicated
run-specific script, then be modified for the new question.

## Validation

Focused test:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_project_core_bem_3d_external_fdtd_return_inbox_preflight.py -q
4 passed
```

Figure check:

```text
1924x772, dynamic range=255
```
