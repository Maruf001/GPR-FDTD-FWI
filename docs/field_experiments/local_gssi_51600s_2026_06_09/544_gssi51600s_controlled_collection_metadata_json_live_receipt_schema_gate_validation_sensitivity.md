# Field Experiment 544: Metadata JSON Live Receipt Schema Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `543` validator against damaged and prematurely promoted
metadata receipt states.

This run is validation sensitivity only. It does not stage metadata files,
stage DZT files, run parsers, rerun provenance/archive gates, run field FWI,
run field 3D/HPC, launch GPU work, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/544_gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
cases:                           21
expected passes:                 1
expected failures:               20
actual passes:                   1
actual failures:                 20
unexpected outcomes:             0
damaged cases:                   20
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
sensitivity ready:               true
```

The exact run `542` state passes. The damaged cases fail as expected:

```text
source readiness loss
metadata row removal
group row removal
action row removal
global metadata count damage
required value count damage
parent-directory damage
JSON extension damage
live-file promotion
JSON parseability promotion
schema-pass promotion
SHA-256 promotion
blank-value reduction
paired DZT dependency promotion
action completion promotion
live receipt promotion
field FWI promotion
field 3D/HPC promotion
figure damage
script-snapshot damage
```

## Interpretation

The metadata JSON validator is fail-closed for missing files, damaged shape,
guard drift, artificial metadata promotion, artificial DZT dependency
promotion, downstream promotion, and missing evidence artifacts.

## Decision

Use runs `542-544` as the current metadata JSON live receipt boundary. Real
archive acceptance and downstream field work remain blocked until all 24 live
metadata JSON files pass with real non-placeholder values and the nine paired
DZT files pass receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_json_live_receipt_schema_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
3041x850, dynamic range=255
```
