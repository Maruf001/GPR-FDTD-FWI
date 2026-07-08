# BEM Experiment 561: Matched-FDTD Return Fillable Template Pack

Date: 2026-06-30

## Purpose

Create two fillable CSV templates for the missing matched-FDTD return files.

Run `560` showed that no existing exact FDTD return source can be used. This
run materializes the required receiver-frequency row identities from the
value-domain contract into blank templates: one source-hash manifest and one
scattered-norm value file.

This run does not fill real FDTD values, accept FDTD evidence, compare BEM with
FDTD, launch GPU/HPC work, or promote field transfer.

## Output

```text
outputs/bem_experiments/561_project_core_bem_35field_matched_fdtd_return_fillable_template_pack
```

Key artifacts:

```text
data/fillable_fdtd_return_templates/fdtd_source_hash_manifest_real_return_template.csv
data/fillable_fdtd_return_templates/fdtd_scattered_norm_values_real_return_template.csv
data/project_core_bem_35field_matched_fdtd_return_fillable_template_pack_manifest_rows.csv
data/project_core_bem_35field_matched_fdtd_return_fillable_template_pack_summary.json
figures/project_core_bem_35field_matched_fdtd_return_fillable_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source locator ready:                      true
template files:                            2
template rows:                             558
source-hash template rows:                 279
scattered-norm template rows:              279
SHA-256 value-domain rows:                 279
positive-float value-domain rows:          279
blank value cells:                         558
real values:                               0
evidence-ready rows:                       0
ready template files:                      0
BEM/FDTD comparison ready:                 false
3D validation claim ready:                 false
field transfer ready:                      false
GPU priority:                              none
```

## Interpretation

The exact FDTD return-file row identities are now available as fillable
templates. This reduces execution ambiguity but does not create evidence. The
two templates must be filled only from real matched-FDTD output.

## Decision

Use run `561` as the fillable template pack for the matched-FDTD return files.
After real values are produced, run the command checks from run `556`, then
rerun row-identity, value-domain, and comparison acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_fillable_template_pack.py
tests/test_project_core_bem_35field_matched_fdtd_return_candidate_source_locator_audit.py
9 passed
```

Figure check:

```text
2106x843, dynamic range=255
```
