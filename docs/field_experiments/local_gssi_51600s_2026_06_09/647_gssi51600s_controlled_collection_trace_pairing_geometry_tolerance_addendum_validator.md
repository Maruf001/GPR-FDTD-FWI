# Field Experiment 647: Controlled Collection Geometry Tolerance Addendum Validator

Date: 2026-07-02

## Purpose

Validate the geometry-tolerance addendum from run `646`.

The validator checks that the addendum has the intended four tolerance rows,
keeps the current no-file field state intact, uses the guarded 32-panel BEM
fine-offset result as its tolerance basis, and does not promote controlled
field evidence, field FWI, field 3D/HPC, or GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/647_gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validator_validation_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validator_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_validator.png
scripts/
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
tolerance rows:                            4
blocking tolerance rows:                   4
expected metadata files:                   9
expected DZT files:                        9
expected measured pairs:                   9
live files:                                0
missing files:                             18
32-panel BEM peak offset span at z=0:      0.6390885783938787 dB
32-panel BEM max relative L2 at z=0:       0.16690711298912922
32/16 peak span ratio:                     1.000001606550095
32/16 relative-L2 ratio:                   0.9999977170783472
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

The six checks cover:

| Order | Check |
| ---: | --- |
| 1 | addendum identity and readiness |
| 2 | tolerance-row shape |
| 3 | field no-file state |
| 4 | BEM tolerance basis |
| 5 | downstream scope remains blocked |
| 6 | figure and script snapshots are valid |

## Interpretation

The geometry-tolerance addendum validates as a collection control, not as field
evidence. It preserves the current requirement for nine real radar files and
nine paired metadata files before any acceptance-gate rerun or field inversion
work.

## Decision

Use runs `646-647` as the guarded field geometry-tolerance addendum. The next
field-side step remains real file collection and metadata binding, not field
FWI or 3D/HPC escalation.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_geometry_tolerance_addendum.py
tests/test_gssi_field_controlled_collection_trace_pairing_geometry_tolerance_addendum_validator.py
6 passed
```

Figure validation:

```text
2609x859, dynamic range=255
```
