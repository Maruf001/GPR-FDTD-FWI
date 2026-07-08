# Field Experiment 582: Collection-Day Return Preflight Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `581` preflight-gate validator by damaging the saved run
`580` state in controlled ways.

This run answers whether the validator accepts only the exact saved pre-return
state and rejects premature promotion of missing files, readable-file flags,
stageable items, executed commands, field-table acceptance, field FWI, field
3D/HPC, damaged figures, and damaged script snapshots.

This is a CPU-only validation-sensitivity run. It does not create measured DZT
files, does not fill metadata JSON files, does not stage files into the live
return area, does not execute copy commands, and does not promote parser,
provenance, field FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/582_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:           true
scenarios:                        21
expected pass scenarios:          1
expected fail scenarios:          20
observed pass scenarios:          1
observed fail scenarios:          20
unexpected outcomes:              0
damaged scenarios:                20
damaged scenarios rejected:       20
gpu priority:                     none
```

The exact saved state passes. The damaged states all fail as expected:

```text
source readiness damage
item-count damage
stage-count damage
metadata-count damage
DZT-count damage
candidate-file false promotion
metadata JSON-valid false promotion
metadata nonblank false promotion
DZT nonzero-size false promotion
DZT readable-header false promotion
preflight-passed false promotion
ready-to-stage false promotion
executed-command false promotion
trace-pairing false promotion
field-table false promotion
controlled-evidence false promotion
field FWI false promotion
field 3D/HPC false promotion
figure damage
script-snapshot damage
```

## Interpretation

The validator is sensitive to every state change that would make an incomplete
field return appear more complete than it is. The only accepted state is the
saved run `580` state: thirty-three required return items are listed, but zero
real field files pass preflight and zero items are stageable.

## Decision

Use runs `580-582` as the guarded collection-day return preflight block. The
next field-side step is still the real controlled collection return: filled
metadata JSON files, measured DZT files, and then guarded preflight plus intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity.py

9 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity.py: pass
```

Figure check:

```text
3292x877, dynamic range=255
```
