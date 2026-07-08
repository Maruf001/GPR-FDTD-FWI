# Field Experiment 229: Controlled Archive Operator Collection Signoff Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `228` completed-worksheet signoff validator against
controlled damage cases.

It does not contain real measured files, fill real signoff values, accept an
archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/229_gssi51600s_controlled_archive_operator_collection_signoff_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_signoff_sensitivity_scenarios.csv
data/field_controlled_archive_operator_collection_signoff_sensitivity_summary.json
figures/field_controlled_archive_operator_collection_signoff_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_SIGNOFF_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_operator_collection_signoff_sensitivity.py
scripts/test_gssi_field_controlled_archive_operator_collection_signoff_sensitivity.py
```

## Result

```text
scenarios:                                  23
expected pass scenarios:                    1
expected failure scenarios:                 22
observed pass scenarios:                    1
observed failure scenarios:                 22
unexpected outcomes:                        0
completed worksheet signoff sensitivity:    true
real files present:                         false
completed signoff values present:           false
real archive acceptance ready:              false
checksum intake ready:                      false
controlled evidence ready:                  false
field FWI ready:                            false
field 3D/HPC ready:                         false
gpu priority:                               none
```

The exact run `227` contract passes. The 22 damaged variants fail as expected:

| Damage family | Examples |
| --- | --- |
| Source readiness drift | worksheet not ready, worksheet guard not ready, contract not ready |
| Cell-count drift | signoff row count, required-cell count, optional-cell count |
| Field/rule drift | missing row, wrong required flag, wrong field name, wrong validation rule |
| Worksheet coverage drift | wrong worksheet row index, wrong file role |
| Blank-value/intake drift | prefilled current value, row intake false, summary intake false |
| Downstream promotion | real files, signoff values, archive acceptance, checksum, evidence, field FWI, or field 3D/HPC marked ready |

## Interpretation

The completed-worksheet signoff validator has guarded sensitivity coverage. It
accepts the exact contract and rejects controlled corruption of source
readiness, signoff-cell structure, validation rules, worksheet coverage,
blank-value state, intake readiness, and archive/evidence/FWI claim boundaries.

## Decision

Use runs `227-229` as the guarded completed-worksheet signoff package. Real
files, real signoff values, archive acceptance, checksum intake, controlled
evidence, field FWI, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_signoff_sensitivity.py
6 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_signoff_sensitivity.png
3293x889, dynamic range=255
```
