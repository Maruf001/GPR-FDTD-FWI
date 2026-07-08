# BEM Experiment 103: External FDTD Return Inbox Layout

Date: 2026-06-25

## Purpose

Create a concrete return-inbox scaffold for the paired full-Maxwell 3D FDTD
target/background files requested by runs `100`-`102`.

This run does not create returned FDTD data and does not launch BEM/FDTD
comparison, 3D validation, local 3D FDTD, GPU/HPC work, field FWI, or
neural-network training.

## Output

```text
outputs/bem_experiments/103_project_core_bem_3d_external_fdtd_return_inbox_layout
```

Key artifacts:

```text
data/project_core_bem_3d_external_fdtd_return_inbox_directories.csv
data/project_core_bem_3d_external_fdtd_return_inbox_required_files.csv
data/project_core_bem_3d_external_fdtd_return_inbox_metadata_template.csv
data/project_core_bem_3d_external_fdtd_return_inbox_layout_summary.json
return_inbox/README.md
return_inbox/frequency_bins/required_frequency_files.csv
return_inbox/metadata/return_metadata_template.csv
return_inbox/notes/install_commands.csv
docs/PROJECT_CORE_BEM_3D_EXTERNAL_FDTD_RETURN_INBOX_LAYOUT.md
figures/project_core_bem_3d_external_fdtd_return_inbox_layout.png
scripts/run_project_core_bem_3d_external_fdtd_return_inbox_layout.py
scripts/test_project_core_bem_3d_external_fdtd_return_inbox_layout.py
scripts/script_snapshot_manifest.json
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

The two required returned files are:

```text
return_inbox/frequency_bins/project_core_bem_3d_fdtd_target_frequency_bins.csv
return_inbox/frequency_bins/project_core_bem_3d_fdtd_background_frequency_bins.csv
```

Each file is expected to contain `124` rows, giving `248` total frequency-bin
rows across the paired target/background return.

## Interpretation

The run `102` request bundle is now paired with a concrete intake location and
metadata template. The external producer can return real frequency-bin CSVs and
the required metadata without guessing filenames, row counts, or install
commands.

The result is intentionally an intake scaffold. It contains no synthetic
stand-in target/background data and therefore cannot support a BEM/FDTD
comparison, 3D validation claim, local 3D launch, or GPU/HPC escalation.

## Decision

Use run `103` as the current BEM 3D external-return inbox contract. Keep
BEM/FDTD comparison, 3D validation, local 3D FDTD launch, and GPU/HPC blocked
until real returned files pass the metadata and frequency-bin gates.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_return_inbox_layout.py
sha256: 25eaf89fa682c61b3711b5bd3b39fdd80cf61bb4e697f97c5ae84ce6a26a5112

test_project_core_bem_3d_external_fdtd_return_inbox_layout.py
sha256: cf52a152a1334a7ead45a4a695079940792f272e230400196eaa1022011ff0d9
```

Subsequent BEM 3D return-intake experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_fdtd_return_inbox_layout.py
3 passed
```

Figure check:

```text
project_core_bem_3d_external_fdtd_return_inbox_layout.png
1492x738, dynamic range=255
```
