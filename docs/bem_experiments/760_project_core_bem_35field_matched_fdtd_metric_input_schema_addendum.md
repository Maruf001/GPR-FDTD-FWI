# BEM Experiment 760: Metric Input Schema Addendum

Date: 2026-07-01

## Purpose

Define the real numeric return schema needed for amplitude/phase BEM/FDTD
comparison.

Run `759` showed that the current return contract supports scalar norm checks
only. This run defines the addendum files and columns needed to compute
amplitude relative error, wrapped phase error, and complex relative error on
the full receiver-frequency set.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/760_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_file_rows.csv
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_summary.json
figures/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                         true
source gap audit ready:                      true
addendum files:                              5
addendum parent directories present:         5
addendum files present:                      0
missing addendum files:                      5
addendum required rows:                      279
required fields per row:                     13
required metric cells:                       3627
required complex component cells:            1116
receiver-frequency pairs covered:            279
schema addendum defined:                     true
schema addendum filled:                      false
real BEM/FDTD comparison ready:              false
gpu priority:                                none
```

Addendum files:

| Stage | Stage label | Rows | Metric cells | Complex component cells |
| ---: | --- | ---: | ---: | ---: |
| 1 | center pair smoke | 1 | 13 | 4 |
| 2 | center receiver frequency sweep | 8 | 104 | 32 |
| 3 | center frequency receiver sweep | 30 | 390 | 120 |
| 4 | midband receiver matrix | 120 | 1560 | 480 |
| 5 | edgeband receiver matrix | 120 | 1560 | 480 |

Each addendum row requires:

```text
pair_id
receiver_index
frequency_hz
bem_real
bem_imag
fdtd_real
fdtd_imag
normalization_label
returned_fdtd_source_hash
solver_run_id
solver_status
solver_log_sha256
real_fdtd_exported
```

## Interpretation

The amplitude/phase comparison now has a concrete real-return schema. The
schema covers all 279 receiver-frequency pairs and requires 1,116 complex
component cells across BEM and FDTD values.

The schema is defined but not filled. No real numeric comparison can be made
until these five files are produced and accepted.

## Decision

Use run `760` as the real numeric return-schema addendum for future
amplitude/phase BEM/FDTD comparison. Keep real comparison, 3D validation,
GPU/HPC, field transfer, and field FWI blocked until the addendum files contain
accepted real numeric values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum.py: pass
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum.py: pass
```

Figure check:

```text
1888x846, dynamic range=255
```
