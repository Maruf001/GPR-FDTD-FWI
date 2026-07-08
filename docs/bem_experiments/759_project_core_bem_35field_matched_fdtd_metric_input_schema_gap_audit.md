# BEM Experiment 759: Metric Input Schema Gap Audit

Date: 2026-07-01

## Purpose

Check whether the current BEM/FDTD return schema can support the amplitude and
phase metrics defined in runs `756-758`.

The current live-return contract was designed around source hashes and scalar
scattered-field norms. Amplitude/phase comparison needs complex-valued BEM and
FDTD rows, so this run audits the schema before any real comparison is enabled.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/759_project_core_bem_35field_matched_fdtd_metric_input_schema_gap_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_metric_input_schema_gap_audit_required_column_rows.csv
data/project_core_bem_35field_matched_fdtd_metric_input_schema_gap_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_metric_input_schema_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                         true
source metric sensitivity ready:             true
metric required columns:                     13
current equivalent columns:                  5
missing metric columns:                      8
complex component columns present:           false
current contract supports scalar norm only:  true
current contract supports amplitude/phase:   false
schema addendum required:                    true
full strict file rows required:              558
receiver-frequency pairs required:           279
real BEM/FDTD comparison ready:              false
gpu priority:                                none
```

Required columns:

| Column | Present now | Why required |
| --- | --- | --- |
| pair_id | false | join BEM and FDTD rows one-to-one |
| receiver_index | false | locate the receiver sample |
| frequency_hz | false | locate the frequency sample |
| bem_real | false | compute BEM complex amplitude and phase |
| bem_imag | false | compute BEM complex amplitude and phase |
| fdtd_real | false | compute FDTD complex amplitude and phase |
| fdtd_imag | false | compute FDTD complex amplitude and phase |
| normalization_label | false | record the amplitude normalization policy |
| returned_fdtd_source_hash | true | tie the row to the FDTD producer input |
| solver_run_id | true | tie the row to the solver execution |
| solver_status | true | require completed solver execution |
| solver_log_sha256 | true | tie the row to an immutable solver log |
| real_fdtd_exported | true | prevent synthetic rows from entering real comparison |

## Interpretation

The current staged return contract is enough to check scalar scattered norms,
but it cannot support phase-aware comparison. The missing columns are not
cosmetic: the comparison needs row identity, receiver/frequency coordinates,
complex BEM values, complex FDTD values, and the normalization label.

## Decision

Add a real numeric return schema before enabling amplitude/phase BEM/FDTD
comparison. Keep real comparison, 3D validation, GPU/HPC, field transfer, and
field FWI blocked until that schema is defined, returned with real values, and
accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_gap_audit.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_metric_input_schema_gap_audit.py: pass
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_gap_audit.py: pass
```

Figure check:

```text
1744x844, dynamic range=255
```
