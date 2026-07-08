# Field Experiment 472: Live Receipt Acceptance Gate Staging Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `471` staging-gap validator with controlled damage to the
run `470` artifacts.

This run checks that the validator fails when source readiness, directory
state, file counts, receipt readiness, family readiness, action readiness,
downstream field processing, figure metadata, or script snapshots are damaged.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/472_gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       15
expected pass cases:                     1
expected fail cases:                     14
actual pass cases:                       1
actual fail cases:                       14
unexpected cases:                        0
damaged cases:                           14
parser ready:                            false
provenance ready:                        false
archive ready:                           false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The exact source audit passes. Damaged states fail for:

```text
source readiness removal
directory-count drift
directory absence
unexpected-file promotion
required-file-count drift
DZT-count drift
metadata JSON-count drift
file-presence promotion
receipt-readiness promotion
family-readiness promotion
action-readiness promotion
field-FWI promotion
figure damage
missing script snapshots
```

## Interpretation

The staging-gap validator is sensitive to the intended failure modes. It cannot
silently treat absent files as present, receipt rows as accepted, or downstream
field processing as ready.

## Decision

Use runs `470-472` as the guarded current live-staging checkpoint. Field
processing remains blocked until all 33 real receipt files exist and pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validation_sensitivity.py

10 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
