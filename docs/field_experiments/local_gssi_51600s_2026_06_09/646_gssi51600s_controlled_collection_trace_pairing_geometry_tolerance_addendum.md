# Field Experiment 646: Controlled Collection Geometry Tolerance Addendum

Date: 2026-07-02

## Purpose

Translate the guarded 32-panel BEM fine-offset result into a field collection
addendum. Runs `950-952` showed that a `5` mm Tx/Rx spacing change remains
visible after a selected 32-panel cross-check. This run turns that result into
collection-day tolerance controls without promoting the current field archive
to measured evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/646_gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_tolerance_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_geometry_tolerance_addendum.png
scripts/
```

## Result

```text
source field-control block ready:              true
source BEM tolerance block ready:              true
tolerance rows:                                4
blocking tolerance rows:                       4
expected metadata files:                       9
expected DZT files:                            9
expected measured pairs:                       9
live files:                                    0
missing files:                                 18
32-panel BEM peak offset span at z=0:          0.6390885783938787 dB
32-panel BEM max relative L2 at z=0:           0.16690711298912922
32/16 peak span ratio:                         1.000001606550095
32/16 relative-L2 ratio:                       0.9999977170783472
geometry tolerance metadata ready:             false
controlled field evidence ready:               false
field FWI ready:                               false
field 3D/HPC ready:                            false
gpu priority:                                  none
```

The four tolerance addendum rows are:

| Order | Tolerance item | Current status |
| ---: | --- | --- |
| 1 | Tx/Rx spacing measurement | pending real files |
| 2 | Tx/Rx spacing repeat tolerance | pending real files |
| 3 | panel-resolution basis | planning constraint only |
| 4 | metadata binding | pending real files |

## Interpretation

The field collection plan now has a tolerance-scale geometry requirement
grounded in the BEM result: Tx/Rx spacing must be recorded for each controlled
profile repeat, time-zero reference, and amplitude reference. Repeats with
about `5` mm or greater spacing deviation should be flagged before any
geometry-sensitive interpretation.

This does not change the field evidence state. The nine radar files and nine
paired metadata files are still absent, so controlled field evidence, field
FWI, and field 3D/HPC remain closed.

## Decision

Use run `646` as the collection-day geometry-tolerance addendum. Do not run
field FWI, heavy GPU work, or field 3D/HPC until real measured files and
metadata are present and pass the existing acceptance gates.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_geometry_tolerance_addendum.py
3 passed
```

Figure validation:

```text
2465x842, dynamic range=255
```
