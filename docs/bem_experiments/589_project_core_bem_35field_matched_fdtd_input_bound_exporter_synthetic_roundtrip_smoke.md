# BEM Experiment 589: Matched FDTD Input-Bound Exporter Synthetic Roundtrip Smoke

Date: 2026-06-30

## Purpose

Exercise the input-bound exporter write path using the valid synthetic receipt
files from run `586`.

This run writes accepted return CSVs only inside this run output folder. It
does not run FDTD, does not write external staged files, and does not create
real BEM/FDTD comparison evidence.

## Output

```text
outputs/bem_experiments/589_project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke
```

Key artifacts:

```text
data/synthetic_roundtrip_return_files/fdtd_source_hash_manifest_synthetic_return.csv
data/synthetic_roundtrip_return_files/fdtd_scattered_norm_values_synthetic_return.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_roundtrip_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke.png
scripts/
```

## Result

```text
source smoke ready:                      true
source validation ready:                 true
source sensitivity ready:                true
roundtrip cases:                         4
valid synthetic cases:                   2
invalid synthetic references:            2
roundtrip successes:                     2
return files written:                    2
roundtrip input rows:                    558
roundtrip accepted rows:                 558
unexpected cases:                        0
real evidence files:                     0
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

## Interpretation

The full-schema exporter path works for two 279-row synthetic inputs. This
confirms the write path after receipt acceptance, while preserving the
non-evidence boundary.

## Decision

Use run `589` as an output-local exporter-path smoke. Keep real BEM/FDTD
comparison blocked until actual external staged files pass the receipt gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
