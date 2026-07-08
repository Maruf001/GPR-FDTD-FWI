# Field Experiment 461: Direct-Intake Collection-Day Bundle Manifest Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `460` collection-day bundle-manifest validator.

Run `460` validated the run `459` bundle manifest as a complete handoff table
and not field evidence. This run verifies that the validator rejects damaged
bundle shape, broken metadata-template links, premature live-file promotion,
premature evidence promotion, downstream promotion, and damaged reporting
artifacts.

This run does not copy measured files, write to live staging, accept
provenance, build a field archive, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/461_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                   true
sensitivity cases:                        11
expected pass cases:                      1
expected fail cases:                      10
actual pass cases:                        1
actual fail cases:                        10
unexpected outcomes:                      0
damaged cases:                            10
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
GPU priority:                             none
sensitivity ready:                        true
```

The damaged cases cover source readiness drift, missing bundle rows, DZT/JSON
count drift, removed metadata-template links, missing template paths, premature
live-file promotion, premature evidence promotion, downstream field-evidence
promotion, figure damage, and script-snapshot damage.

## Interpretation

The collection-day bundle validator is now guarded against common false-pass
states. It accepts only the exact non-evidence handoff manifest and rejects
malformed or prematurely promoted versions.

## Decision

Use runs `459-461` as the guarded collection-day bundle block. Keep field
evidence, provenance acceptance, archive acceptance, field FWI, GPU work, and
field 3D/HPC blocked until the 33 live files are copied and the receipt,
parser, provenance, and archive gates are rerun.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validation_sensitivity.py
4 passed
```

Figure check:

```text
2789x909, dynamic range=255
```
