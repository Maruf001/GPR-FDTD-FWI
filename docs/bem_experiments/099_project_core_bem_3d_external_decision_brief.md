# BEM Experiment 099: Project-Core BEM 3D External Decision Brief

Date: 2026-06-25

## Purpose

Condense the current 3D BEM/FDTD validation-data state into one decision
artifact.

Runs `082`-`088` established that the defensible 3D validation route is not a
local ad hoc 3D FDTD launch or a direct port of the current 2D TMz solvers. The
selected route is an external full-Maxwell 3D FDTD import with paired
target/background outputs and strict metadata, frequency-bin, and checksum
acceptance gates.

This run does not launch 3D FDTD, GPU/HPC work, field FWI, or neural-network
training.

## Output

```text
outputs/bem_experiments/099_project_core_bem_3d_external_decision_brief
```

Key artifacts:

```text
data/project_core_bem_3d_external_decision_brief.csv
data/project_core_bem_3d_external_decision_brief_summary.json
docs/PROJECT_CORE_BEM_3D_EXTERNAL_DECISION_BRIEF.md
figures/project_core_bem_3d_external_decision_brief.png
scripts/run_project_core_bem_3d_external_decision_brief.py
scripts/test_project_core_bem_3d_external_decision_brief.py
scripts/script_snapshot_manifest.json
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

## Decision Rows

| Item | Status | Ready | Metric | Value |
| --- | --- | ---: | --- | ---: |
| validation data path | ready decision | 1 | top candidate | external 3D FDTD import |
| external request pack | ready request | 1 | expected frequency rows | 248 |
| return bundle pipeline | synthetic smoke only | 1 | synthetic return blockers | 0 |
| real 3D validation claim | blocked until real return | 0 | real external FDTD data present | 0 |

## Interpretation

The 3D BEM validation path is ready for an external FDTD data request, not for a
validation claim. The request is concrete: two paired target/background
full-Maxwell 3D FDTD runs, 31 receivers, four frequencies, and 248 complex
frequency rows.

The return pipeline has only synthetic proof of satisfiability. No real paired
target/background files are present, so real 3D BEM/FDTD comparison, 3D
validation claims, local 3D FDTD launch, GPU/HPC escalation, and field/FWI
promotion remain blocked.

## Decision

Ask the team who will generate or return the paired target/background
full-Maxwell 3D FDTD outputs. Keep local 3D launch, real comparison, and 3D
validation blocked until real returned files pass the metadata and frequency-bin
gates.

## Milestone Snapshot

This is a result-driven milestone. The run script and focused test were frozen
into the output-local `scripts/` folder.

```text
run_project_core_bem_3d_external_decision_brief.py
sha256: dc1770cd9dec1108141d095632bca7c7a66b8a568250dec1917781d6034e42f8

test_project_core_bem_3d_external_decision_brief.py
sha256: 2b40e077e7c1a03114c37426d9585e5c500ca9d4bbfb80052a2cb47da6ab663b
```

Subsequent related experiments should start from a duplicated run-specific
script, not by editing this frozen copy.

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
