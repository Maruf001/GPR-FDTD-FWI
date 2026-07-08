# BEM Experiment 522: Bempp 35-Field Candidate Value Export Validator

Date: 2026-06-30

## Purpose

Validate run `521`, the Bempp-side candidate value export for the 35-field
return schema.

Run `521` produced two candidate BEM return-file tables: a source-lineage hash
manifest and scattered-field norm values. This validator confirms that those
files are complete and finite while preserving the evidence boundary.

## Output

```text
outputs/bem_experiments/522_project_core_bem_bempp_35field_candidate_value_export_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_candidate_value_export_validator_checks.csv
data/project_core_bem_bempp_35field_candidate_value_export_validator_summary.json
figures/project_core_bem_bempp_35field_candidate_value_export_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation checks passed:                  5
blocking failures:                         0
candidate value-export validation ready:   true
candidate BEM value export ready:          true
candidate source-hash entries:             279
candidate scattered-norm entries:          279
ready frequency rows:                      9
accepted real return files:                0
matched FDTD return files present:         false
accepted evidence ready:                   false
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
```

## Decision

Use run `522` as the artifact guard for the run `521` candidate BEM value
export. The candidate BEM-side values are complete enough to support the next
BEM-side validation step, but not enough to make a BEM/FDTD comparison claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_candidate_value_export.py
tests/test_project_core_bem_bempp_35field_candidate_value_export_validator.py
8 passed
```

Figure check:

```text
2501x834, dynamic range=255
```
