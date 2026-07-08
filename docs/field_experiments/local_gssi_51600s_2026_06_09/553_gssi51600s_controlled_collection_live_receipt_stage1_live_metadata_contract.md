# Field Experiment 553: Stage-1 Live Metadata Contract

Date: 2026-07-01

## Purpose

Define the exact live metadata files that must replace the stage-1 synthetic
metadata smoke from run `552`.

This run does not create live field evidence, accept live receipt, parse field
data, accept provenance, promote an archive, run field FWI, or run field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/553_gssi51600s_controlled_collection_live_receipt_stage1_live_metadata_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_stage1_live_metadata_contract_contract_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage1_live_metadata_contract_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage1_live_metadata_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract metadata files:          7
required value fields:            28
live parent directories present:  7
live metadata files present:      0
accepted live receipt items:      0
full live receipt items:          33
full metadata value fields:       96
live receipt ready:               false
parser ready:                     false
provenance ready:                 false
archive ready:                    false
field FWI ready:                  false
field 3D/HPC ready:               false
```

The seven expected live metadata files are:

```text
antenna_model_serial_and_nominal_frequency.json
antenna_serial.json
material.json
software_version.json
survey_method.json
system.json
truth_source.json
```

## Interpretation

The first real field replacement is now exact: seven pre-collection metadata
JSON files with four required values each. All parent directories exist, but no
stage-1 live metadata files are present yet.

## Decision

Use this as the live stage-1 metadata contract. Keep live receipt, parser,
provenance, archive promotion, field FWI, and field 3D/HPC blocked until real
live files pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage1_live_metadata_contract.py
3 passed
```

Figure check:

```text
1924x844, dynamic range=255
```
