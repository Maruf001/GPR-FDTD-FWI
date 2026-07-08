# Field Experiment 645: Collection-Day Acquisition Geometry Control Audit Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `644` acquisition-geometry control audit validator.

This run checks that the validator accepts only the exact saved control-audit
state and rejects damaged controls, missing metadata requirements, false
control satisfaction, false live-file promotion, BEM metric damage, source
readiness damage, geometry metadata promotion, interpretation promotion,
field-evidence/FWI/3D promotion, GPU-priority promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/645_gssi51600s_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             26
expected pass scenarios:               1
expected fail scenarios:               25
observed pass scenarios:               1
observed fail scenarios:               25
unexpected outcomes:                   0
damaged scenarios:                     25
damaged scenarios rejected:            25
geometry control rows:                 6
metadata-required controls:            6
currently satisfied controls:          0
geometry-sensitive blocking controls:  6
expected metadata files:               9
expected DZT files:                    9
expected measured pairs:               9
live files:                            0
missing files:                         18
geometry-control metadata ready:       false
geometry-sensitive interpretation ready:false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

Rejected damaged states include:

```text
audit-not-ready state
field-decision source readiness damage
BEM-geometry source readiness damage
row removal
control-id damage
metadata-required damage
false control satisfaction
blocking-control demotion
metadata-count damage
DZT-count damage
pair-count damage
live-file promotion
acceptance-rerun promotion
BEM offset-metric damage
BEM antenna-z metric damage
BEM full-grid metric damage
geometry-metadata promotion
geometry-interpretation promotion
field-evidence promotion
field-FWI promotion
field-3D/HPC promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The acquisition-geometry control validator is fail-closed. It accepts the exact
saved checklist state and rejects damaged controls or premature promotion.

## Decision

Use runs `643-645` as the guarded field acquisition-geometry control checklist.
Keep field evidence, field FWI, GPU escalation, and field 3D/HPC blocked until
the first-return files and paired geometry metadata are present and pass the
guarded acceptance path.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validation_sensitivity.py
11 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
run_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator.py
run_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validation_sensitivity.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validation_sensitivity.py
pass
```

Figure check:

```text
3671x896, dynamic range=255
```
