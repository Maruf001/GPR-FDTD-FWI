# Field Experiment 279: Collection-Day Critical Path Validator

Date: 2026-06-28

## Purpose

Validate the saved run `278` critical-path audit from artifacts.

This is an artifact-only validator. It does not ingest real field data, run
field preprocessing, run FDTD, run field FWI, launch GPU/HPC work, or claim
field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/279_gssi51600s_controlled_collection_real_return_collection_day_critical_path_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_critical_path_validator_checks.csv
data/field_controlled_collection_real_return_collection_day_critical_path_validator_summary.json
figures/field_controlled_collection_real_return_collection_day_critical_path_validator.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_CRITICAL_PATH_VALIDATOR.md
```

## Result

```text
validation checks:              8
passed checks:                  8
failed checks:                  0
validation ready:               true
critical-path stages:           3
requirement rows:               57
measured requirements:          50
measured requirements complete: 0
required real DZT files:        9
metadata values:                32
checksums:                      9
acceptance gates:               7
acceptance gates ready:         0
provenance acceptance ready:    false
controlled field evidence ready:false
field FWI ready:                false
field 3D/HPC ready:             false
gpu priority:                   none
```

## Interpretation

Run `278` validates as the current field critical-path view. It preserves the
exact three-stage split, 50 measured requirements, seven gates, and
zero-complete current archive state.

## Decision

Use run `279` as the validator for the field critical-path audit. Keep
provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, field 3D/HPC, and GPU work blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_critical_path_audit.py
tests/test_gssi_field_controlled_collection_real_return_collection_day_critical_path_validator.py

6 passed
```

Figure validation:

```text
3365x895, dynamic range=255
```
