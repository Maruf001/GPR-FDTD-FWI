# Field Experiment 324: Antenna Aperture Metadata Addendum Validator

Date: 2026-06-29

## Purpose

Validate the saved run `323` controlled-field antenna aperture metadata
addendum from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/324_gssi51600s_controlled_collection_real_return_antenna_aperture_metadata_addendum_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
source packet items:                57
antenna aperture metadata items:    4
updated packet items:               61
updated acceptance checks:          201
updated measured requirements:      54
updated metadata requirements:      36
updated global metadata values:     15
updated file metadata values:       21
BEM 3-sample aperture relative L2:  0.08009547612144642
antenna aperture metadata required: true
antenna coupling metadata required: true
updated packet contract ready:      true
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The validator checks packet counts, the four antenna metadata rows, updated
packet-row taxonomy, BEM aperture motivation, downstream field blocked states,
figure validation, and script snapshots.

## Interpretation

The run `323` addendum is internally consistent. It adds four blocking antenna
aperture/coupling metadata records and keeps the measured-evidence gate closed.

## Decision

Use run `324` as the validator for run `323`. Sensitivity hardening remains
required before closing the field antenna metadata block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_antenna_aperture_metadata_addendum_validator.py
3 passed
```

Figure check:

```text
3617x922, dynamic range=255
```
