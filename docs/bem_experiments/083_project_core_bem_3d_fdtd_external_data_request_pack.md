# BEM Experiment 083: External 3D FDTD Data Request Pack

Date: 2026-06-25

## Purpose

Package the concrete files and acceptance gates needed to request or generate
external full-Maxwell 3D FDTD target/background data for the BEM comparison.

Run `082` selected external 3D FDTD import as the preferred validation-data
path. This run turns that decision into a handoff packet.

This is a CPU-only packaging run. It does not launch 3D FDTD, field FWI,
GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/083_project_core_bem_3d_fdtd_external_data_request_pack
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_external_request_runs.csv
data/project_core_bem_3d_fdtd_external_request_artifacts.csv
data/project_core_bem_3d_fdtd_external_request_acceptance_gates.csv
data/project_core_bem_3d_fdtd_external_data_request_pack_summary.json
figures/project_core_bem_3d_fdtd_external_data_request_pack.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXTERNAL_DATA_REQUEST_PACK.md
scripts/run_project_core_bem_3d_fdtd_external_data_request_pack.py
scripts/test_project_core_bem_3d_fdtd_external_data_request_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
requested FDTD runs:              2
request artifacts:                7
receiver count:                   31
frequency count:                  4
frequency rows per run:           124
total frequency rows expected:    248
acceptance gates:                 7
all request artifacts exist:      true
top engine candidate:             external_3d_fdtd_import
external request ready:           true
real external FDTD data present:  false
real BEM/FDTD comparison ready:   false
3D validation claim ready:        false
local 3D FDTD launch ready:       false
```

Requested runs:

| Role | Target present | Receivers | Frequencies |
| --- | --- | ---: | ---: |
| fdtd_target | true | 31 | 4 |
| fdtd_background | false | 31 | 4 |

The seven request artifacts are the target/background manifest templates,
receiver positions, frequency bins, time-trace schema, and target/background
frequency-bin import templates.

## Interpretation

The external 3D FDTD request is now concrete. A collaborator or external FDTD
tool should run exactly two paired cases and return either receiver time traces
matching the run `080` schema or filled frequency-bin tables matching run
`077`.

This is not returned data. It does not support 3D validation until real
target/background outputs pass manifest validation, extraction/template checks,
and the run `075` comparator.

## Decision

Use this pack to request or generate external full-Maxwell 3D FDTD
target/background outputs. Keep real BEM/FDTD comparison and 3D validation
claims blocked until returned data pass all seven acceptance gates.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_external_data_request_pack.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_external_data_request_pack.png
2105x808, dynamic range=255
```
