# BEM 3D External Decision Brief Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records BEM run `099`, which condenses the current 3D
BEM/FDTD validation-data state into one decision artifact.

No local 3D FDTD, GPU/HPC work, field FWI, or neural-network training was
launched.

## Output

```text
outputs/bem_experiments/099_project_core_bem_3d_external_decision_brief
```

Tracked note:

```text
docs/bem_experiments/099_project_core_bem_3d_external_decision_brief.md
```

## Result

```text
decision items:                       4
ready items:                          3
blocked items:                        1
requested external FDTD runs:         2
receiver count:                       31
frequency count:                      4
expected frequency rows:              248
synthetic return smoke pass:          true
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
local 3D FDTD launch ready:           false
GPU/HPC ready:                        false
```

## Interpretation

The 3D BEM validation route is now explicit. The project is ready to request or
accept paired full-Maxwell 3D FDTD target/background outputs, but it is not
ready to claim validated 3D BEM behavior because no real returned files exist.

The external request is concrete: two paired runs, 31 receivers, four
frequencies, and 248 complex frequency rows.

## Decision

Use run `099` as the current 3D handoff decision. Ask the team who will generate
or return the paired target/background full-Maxwell 3D FDTD outputs. Keep local
3D launch, real BEM/FDTD comparison, 3D validation, GPU/HPC escalation, and FWI
blocked until the real return passes the acceptance gates.

## Milestone Snapshot

This is a result-driven milestone. The exact script and focused test were frozen
under the output-local `scripts/` folder:

```text
run_project_core_bem_3d_external_decision_brief.py
sha256: dc1770cd9dec1108141d095632bca7c7a66b8a568250dec1917781d6034e42f8

test_project_core_bem_3d_external_decision_brief.py
sha256: 2b40e077e7c1a03114c37426d9585e5c500ca9d4bbfb80052a2cb47da6ab663b
```

Subsequent related experiments should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_decision_brief.py
2 passed
```

Figure check:

```text
project_core_bem_3d_external_decision_brief.png
1674x770, dynamic range=255
```

Marathon status: active. The next defensible branch is to refresh the snapshot
audit and then decide whether the team-facing presentation pack should absorb
run `099`.
