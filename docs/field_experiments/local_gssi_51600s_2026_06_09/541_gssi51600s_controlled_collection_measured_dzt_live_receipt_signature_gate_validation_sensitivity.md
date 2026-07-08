# Field Experiment 541: Measured DZT Live Receipt Signature Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `540` validator against damaged and prematurely promoted
states.

This run is validation sensitivity only. It does not stage real DZT files,
create measured evidence, run parsers, rerun provenance/archive gates, run
field FWI, run field 3D/HPC, launch GPU work, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/541_gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
cases:                           18
expected passes:                 1
expected failures:               17
actual passes:                   1
actual failures:                 17
unexpected outcomes:             0
damaged cases:                   17
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
sensitivity ready:               true
```

The exact run `539` state passes. The damaged cases fail as expected:

```text
source readiness loss
DZT row removal
family row removal
action row removal
minimum-size guard drift
header-prefix guard drift
extension guard damage
live-file promotion
signature-pass promotion
SHA-256 promotion
family completion promotion
action completion promotion
live receipt promotion
field FWI promotion
field 3D/HPC promotion
figure damage
script-snapshot damage
```

## Interpretation

The validator is fail-closed for the current live DZT receipt boundary. It does
not accept shape damage, guard drift, artificial file promotion, checksum
promotion, downstream promotion, or missing evidence artifacts.

## Decision

Use runs `539-541` as the current measured-DZT live receipt boundary. Real
archive acceptance and downstream field work remain blocked until all nine
measured DZT files are present and pass the binary guard.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_measured_dzt_live_receipt_signature_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
2825x848, dynamic range=255
```
