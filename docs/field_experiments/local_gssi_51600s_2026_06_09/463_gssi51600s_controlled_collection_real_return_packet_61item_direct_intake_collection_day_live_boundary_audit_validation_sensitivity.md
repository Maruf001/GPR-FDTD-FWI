# Field Experiment 463: Collection-Day Live Boundary Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Sensitivity-test the run `462` collection-day live-boundary audit.

Run `462` separated prepared collection-day artifacts from live measured field
files. This run checks that the audit rejects common damaged states instead of
promoting templates, commands, or partial file counts into field evidence.

This run does not copy measured files, execute receipt commands, rerun parser
or provenance gates, accept a real archive, launch field FWI, or promote field
3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/463_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source audit ready:                  true
sensitivity cases:                   8
expected pass cases:                 1
expected fail cases:                 7
actual pass cases:                   1
actual fail cases:                   7
unexpected cases:                    0
damaged cases:                       7
real packet files present:           false
real packet accepted:                false
controlled field evidence ready:     false
provenance acceptance ready:         false
archive acceptance ready:            false
field FWI ready:                     false
field 3D/HPC ready:                  false
sensitivity ready:                   true
```

Damaged cases rejected:

| Case | Damage |
| --- | --- |
| template ready false | metadata template-pack readiness false |
| bundle validation ready false | bundle-manifest validator readiness false |
| live file promotion | live file count promoted without real files |
| missing count drift | missing live-file count drifts from 33 |
| command execution promotion | receipt command marked executed |
| receipt ready promotion | receipt check marked ready before files exist |
| downstream promotion | premature controlled field-evidence promotion |

## Interpretation

The live-boundary audit is sensitive to the states that would otherwise cause
false field readiness: partial live-file promotion, command execution
promotion, receipt readiness promotion, and downstream evidence promotion.

## Decision

Use runs `462` and `463` as the guarded field live-boundary block. The next
field-enabling work remains copying nine measured DZT files and 24 completed
metadata JSON files, then running the 33 receipt commands and rerunning parser,
provenance, and archive gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
1709x847, dynamic range=255
```
