# Field Experiment 648: Controlled Collection Geometry Tolerance Addendum Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `647` validator for the geometry-tolerance addendum.

The sensitivity pass confirms that the exact addendum validator state passes,
while damaged field controls, damaged counts, damaged BEM tolerance basis, and
premature downstream promotion fail.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/648_gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:             true
scenario count:                     16
expected pass count:                1
expected fail count:                15
observed pass count:                1
observed fail count:                15
unexpected outcome count:           0
damaged scenarios rejected:         15
tolerance rows:                     4
blocking tolerance rows:            4
expected metadata files:            9
expected DZT files:                 9
expected measured pairs:            9
live files:                         0
missing files:                      18
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The geometry-tolerance addendum is guarded as a field collection control. It
does not become field evidence, and it does not open field FWI or 3D/HPC work
without the missing measured files and paired metadata.

## Decision

Use runs `646-648` as the guarded field geometry-tolerance addendum block.
The next field-side step remains real controlled collection and metadata
binding.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_geometry_tolerance_addendum.py
tests/test_gssi_field_controlled_collection_trace_pairing_geometry_tolerance_addendum_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_geometry_tolerance_addendum_validation_sensitivity.py
9 passed
```

Figure validation:

```text
2717x856, dynamic range=255
```
