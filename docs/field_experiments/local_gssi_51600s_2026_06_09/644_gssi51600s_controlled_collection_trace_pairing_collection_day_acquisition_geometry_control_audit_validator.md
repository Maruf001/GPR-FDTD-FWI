# Field Experiment 644: Collection-Day Acquisition Geometry Control Audit Validator

Date: 2026-07-02

## Purpose

Validate the run `643` acquisition-geometry control audit from saved artifacts.

This run checks the six control rows, required metadata state, no-file field
state, BEM geometry metric basis, blocked downstream scope, figure output, and
script snapshots.

This is a CPU-only validation run. It does not use new measured field files,
rerun the first-return acceptance gate, run field FWI, start field 3D/HPC, or
promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/644_gssi51600s_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator
```

## Result

```text
validation checks:                       6
passed checks:                           6
failed checks:                           0
geometry control rows:                   6
metadata-required controls:              6
currently satisfied controls:            0
geometry-sensitive blocking controls:    6
expected metadata files:                 9
expected DZT files:                      9
expected measured pairs:                 9
live files:                              0
missing files:                           18
BEM peak offset span at z=0:             2.6214537950832346 dB
BEM max relative L2 across offset:       0.7099232724148534
BEM max relative L2 across antenna z:    0.4171376953084501
BEM max relative L2 across full grid:    0.9115427115447009
geometry-control metadata ready:         false
geometry-sensitive interpretation ready: false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
validation ready:                        true
```

Validation checks:

| Check order | Validation check | Passed |
| ---: | --- | --- |
| 1 | source audit identity and readiness | true |
| 2 | control shape and required metadata | true |
| 3 | field no-file state preserved | true |
| 4 | BEM geometry metric basis | true |
| 5 | downstream claims blocked | true |
| 6 | figure and scripts valid | true |

## Interpretation

The acquisition-geometry control audit validates as a field-side metadata
checklist. The checklist is structurally ready, but none of the controls are
satisfied because the first-return radar files and paired metadata files are
still absent.

## Decision

Use runs `643-644` as the guarded acquisition-geometry control checklist. Keep
field evidence, field FWI, GPU escalation, and field 3D/HPC blocked until the
first-return files and paired geometry metadata are present and pass the
guarded acceptance path.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator.py
8 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
run_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator.py
pass
```

Figure check:

```text
2771x862, dynamic range=255
```
