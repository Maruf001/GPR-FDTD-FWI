# BEM Experiment 580: Matched FDTD Input-Bound Exporter Real-Input Staging Intake Manifest

Date: 2026-06-30

## Purpose

Create a four-file intake manifest for the guarded input-bound matched-FDTD
handoff defined by runs `577-579`.

This run defines the exact staged file names, producers, and acceptance rules
for the two real input CSV files and the two future accepted return CSV files.
It does not create files, run the exporter, or compare BEM and FDTD.

## Output

```text
outputs/bem_experiments/580_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_intake_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_action_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest.png
scripts/
```

## Result

```text
source scaffold ready:                   true
source validation ready:                 true
source sensitivity ready:                true
manifest rows:                           4
real input rows:                         2
accepted return rows:                    2
present staged files:                    0
nonempty staged files:                   0
accepted files:                          0
ready-for-exporter files:                0
ready-for-comparison files:              0
actions:                                 4
ready actions:                           0
exporter execution ready:                false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

The manifest rows are:

| File key | Role | Producer |
| --- | --- | --- |
| `fdtd_source_hash_manifest` | real input file | external matched-FDTD producer |
| `fdtd_source_hash_manifest` | accepted return file | input-bound exporter |
| `fdtd_scattered_norm_values` | real input file | external matched-FDTD producer |
| `fdtd_scattered_norm_values` | accepted return file | input-bound exporter |

## Interpretation

The BEM/FDTD handoff now has a concrete intake manifest. The current state is
still file-empty: no real input files are present, no accepted return files are
present, and no comparison evidence exists.

## Decision

Use run `580` as the practical four-file intake manifest for the next real
matched-FDTD handoff. Keep exporter execution and BEM/FDTD comparison blocked
until the two real input CSV files exist and pass acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validator.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validation_sensitivity.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest.py

13 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
