# BEM Experiment 563: Matched-FDTD Return Fillable Template-Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `562` validator for the blank matched-FDTD return
templates.

Runs `561-562` created and validated two fillable FDTD return templates. This
run checks that the validator accepts only the exact blank template pack and
rejects damaged or prematurely promoted states.

This run does not fill FDTD values, run FDTD, compare BEM with FDTD, launch
GPU/HPC work, or promote field transfer.

## Output

```text
outputs/bem_experiments/563_project_core_bem_35field_matched_fdtd_return_fillable_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_fillable_template_pack_validation_sensitivity_rows.csv
data/project_core_bem_35field_matched_fdtd_return_fillable_template_pack_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_fillable_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                   true
sensitivity cases:                        10
expected pass cases:                      1
expected fail cases:                      9
actual pass cases:                        1
actual fail cases:                        9
unexpected outcomes:                      0
damaged cases:                            9
BEM/FDTD comparison ready:                false
3D validation claim ready:                false
field transfer ready:                     false
GPU priority:                             none
sensitivity ready:                        true
```

The damaged cases cover:

| Case | Expected | Actual | Failed check |
| --- | --- | --- | --- |
| summary readiness false | fail | fail | source template-pack readiness |
| missing hash-template row | fail | fail | template value columns blank |
| duplicate norm-template identity | fail | fail | template value columns blank |
| filled hash value | fail | fail | template value columns blank |
| filled norm value | fail | fail | template value columns blank |
| ready-file promotion | fail | fail | no evidence or downstream promotion |
| downstream promotion | fail | fail | no evidence or downstream promotion |
| figure damage | fail | fail | figure and script snapshots present |
| script-snapshot damage | fail | fail | figure and script snapshots present |

## Interpretation

The blank matched-FDTD return templates are now guarded against common false
promotion paths. The validator rejects missing or duplicated row identities,
premature real-looking values, premature ready-file or comparison promotion,
and damaged reporting artifacts.

This still does not create matched-FDTD evidence. The two real return CSVs must
be filled by real matched-FDTD output before any BEM/FDTD comparison can be
accepted.

## Decision

Use runs `561-563` as the guarded matched-FDTD fillable-template block. Keep
BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field transfer, and
field FWI blocked until real matched-FDTD values fill the templates and pass the
run `556` command checks.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_fillable_template_pack_validation_sensitivity.py
4 passed
```

Figure check:

```text
2645x914, dynamic range=255
```
