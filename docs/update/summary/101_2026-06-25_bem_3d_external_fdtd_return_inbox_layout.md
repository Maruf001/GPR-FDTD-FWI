# BEM 3D External FDTD Return Inbox Layout

Date: 2026-06-25

## Scope

This checkpoint records BEM run `103`, which creates the intake-side folder,
metadata template, required-file list, and install commands for the real
external full-Maxwell 3D FDTD target/background return requested by runs
`100`-`102`.

No fake returned FDTD data was generated. No BEM/FDTD comparison, 3D
validation, local 3D FDTD launch, GPU/HPC work, field FWI, or neural-network
training was started.

## Output

```text
outputs/bem_experiments/103_project_core_bem_3d_external_fdtd_return_inbox_layout
docs/bem_experiments/103_project_core_bem_3d_external_fdtd_return_inbox_layout.md
```

## Result

```text
source runs:                    085, 102
requested FDTD runs:             2
receivers:                       31
frequencies:                     4
expected total frequency rows:   248
inbox directories:               4
required return files:           2
metadata fields:                 12
placeholder data files:          0
return inbox layout ready:       true
real external FDTD data present: false
real BEM/FDTD comparison ready:  false
3D validation claim ready:       false
local 3D FDTD launch ready:      false
GPU/HPC ready:                   false
```

The run produces the exact return paths:

```text
return_inbox/frequency_bins/project_core_bem_3d_fdtd_target_frequency_bins.csv
return_inbox/frequency_bins/project_core_bem_3d_fdtd_background_frequency_bins.csv
```

## Decision

Use run `103` as the BEM 3D external-return inbox contract. Keep BEM/FDTD
comparison, 3D validation, local 3D FDTD launch, and GPU/HPC blocked until real
returned target/background files and metadata pass the existing gates.

## Milestone Snapshot

Frozen scripts:

```text
run_project_core_bem_3d_external_fdtd_return_inbox_layout.py
sha256: 25eaf89fa682c61b3711b5bd3b39fdd80cf61bb4e697f97c5ae84ce6a26a5112

test_project_core_bem_3d_external_fdtd_return_inbox_layout.py
sha256: cf52a152a1334a7ead45a4a695079940792f272e230400196eaa1022011ff0d9
```

Future BEM 3D return-intake experiments should begin from a duplicated
run-specific script, then be modified for the new question.

## Validation

Focused test:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_project_core_bem_3d_external_fdtd_return_inbox_layout.py -q
3 passed
```

Figure check:

```text
1492x738, dynamic range=255
```
