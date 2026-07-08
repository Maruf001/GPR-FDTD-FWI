# BEM Experiment 586: Matched FDTD Input-Bound Exporter Real-Input Staging Receipt Gate Synthetic Fill Smoke

Date: 2026-06-30

## Purpose

Exercise the run `583-585` external receipt gate with controlled synthetic
files stored only inside this run output folder.

This run verifies that the gate accepts correctly shaped synthetic files and
rejects malformed synthetic files. It does not write to the real external
staging paths, does not run FDTD, does not run the exporter, and does not
create BEM/FDTD comparison evidence.

## Output

```text
outputs/bem_experiments/586_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke
```

Key artifacts:

```text
data/synthetic_receipt_files/
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_smoke_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke.png
scripts/
```

## Result

```text
source gate ready:                       true
source validation ready:                 true
source sensitivity ready:                true
synthetic cases:                         4
expected accepted cases:                 2
expected rejected cases:                 2
actual accepted cases:                   2
actual rejected cases:                   2
unexpected cases:                        0
synthetic accepted rows:                 558
real evidence files:                     0
external staged files:                   0
external accepted files:                 0
exporter execution ready:                false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

The two valid synthetic files each contain 279 accepted rows. The two invalid
synthetic files are rejected.

## Interpretation

The receipt gate is not only a file-presence audit. Its content validation can
accept correctly shaped files and reject malformed files. The smoke remains
non-evidence because all synthetic files are local to this run output folder,
and the external real staging area remains empty.

## Decision

Use run `586` as a synthetic consumer smoke for the external receipt gate. Keep
real BEM/FDTD comparison blocked until actual external staged files pass the
same gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke.py

4 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
