# BEM 3D External FDTD Return Inbox Preflight Smoke

Date: 2026-06-25

## Scope

This checkpoint records BEM run `105`, a synthetic smoke for the run `104`
return-inbox preflight.

The smoke uses an isolated copied inbox under run `105`; it does not modify the
real run `103` inbox and does not install synthetic files into the pending
return root.

No real BEM/FDTD comparison, 3D validation, local 3D FDTD launch, GPU/HPC work,
field FWI, or neural-network training was started.

## Output

```text
outputs/bem_experiments/105_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke
docs/bem_experiments/105_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.md
```

## Result

```text
synthetic required files:             2
synthetic metadata fields:            12
preflight checks:                     18
passed checks:                        18
failed checks:                        0
blocking findings:                    0
synthetic smoke preflight ready:      true
gate can pass on complete synthetic:  true
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
local 3D FDTD launch ready:           false
GPU/HPC ready:                        false
```

## Decision

The run `104` gate can pass on a complete, hash-consistent inbox. This confirms
the current real blocker is missing real returned files and metadata, not an
impossible gate. Keep BEM/FDTD comparison and 3D validation blocked until run
`104` passes on real external FDTD returns in the run `103` inbox.

## Milestone Snapshot

Frozen scripts:

```text
run_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py
sha256: abbe16b093d5f81db4826e9f83c4745c7de710e93b9debab547ff34cc427e31d

test_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py
sha256: 6d8aa7d6202f9e9683cf89199c6e01b052c80f51c877e3fd9cf26648a668b53c
```

## Validation

Focused test:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py -q
3 passed
```

Figure check:

```text
1924x772, dynamic range=255
```
