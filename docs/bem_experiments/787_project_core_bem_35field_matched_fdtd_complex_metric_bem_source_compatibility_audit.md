# BEM Experiment 787: Complex Metric BEM Source Compatibility Audit

Date: 2026-07-01

## Purpose

Check whether the accepted BEM-side scalar return files can fill the BEM fields
required by the new complex-metric BEM/FDTD schema.

Run `784` showed that the future complex-metric packet needs 558 BEM complex
value cells: `bem_real` and `bem_imag` for 279 receiver-frequency rows. This
run checks whether the already accepted BEM-side scalar files from run `557`
can be reused directly.

## Output

```text
outputs/bem_experiments/787_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_source_file_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_compatibility_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source BEM acceptance ready:                  true
source dependency audit ready:                true
source dependency sensitivity ready:          true
accepted BEM files:                           2
accepted BEM source-hash rows:                279
accepted BEM scalar-norm rows:                279
required complex-metric rows:                 279
required BEM complex columns:                 2
required BEM complex cells:                   558
compatible BEM complex columns:               0
compatible BEM complex cells:                 0
reusable sampling columns:                    2
reusable sampling cells:                      558
direct scalar-norm repackage ready:           false
new BEM complex-field exporter required:      true
real BEM/FDTD comparison ready:               false
field transfer ready:                         false
3D/HPC ready:                                 false
gpu priority:                                 none
```

## Interpretation

The accepted BEM-side source is complete for scalar scattered norms, but it is
not a complex-field source. It has receiver indices and frequencies, so the
sampling grid can be reused. It does not contain `bem_real` or `bem_imag`, so
it cannot fill the complex-metric BEM value columns.

## Decision

Do not repackage scalar BEM norms as complex BEM fields. Build a BEM
complex-field exporter before attempting a BEM-side partial complex-metric
producer fill.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2536x844, dynamic range=255
```
