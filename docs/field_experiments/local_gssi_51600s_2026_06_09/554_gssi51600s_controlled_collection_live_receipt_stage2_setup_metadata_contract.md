# Field Experiment 554: Stage-2 Setup Metadata Contract

Date: 2026-07-01

## Purpose

Define the exact live metadata contract for controlled-collection stage `2`,
the setup measurement controls.

This run extends the stage-1 live metadata contract from run `553`. It does
not create measured field evidence, accept live field files, run DZT parsing,
promote provenance/archive state, launch field FWI, or launch field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/554_gssi51600s_controlled_collection_live_receipt_stage2_setup_metadata_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_stage2_setup_metadata_contract_contract_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage2_setup_metadata_contract_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage2_setup_metadata_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage-2 metadata files required:        4
stage-2 metadata value fields required: 16
stage-2 live parents present:           4
stage-2 live metadata files present:    0
stage-2 accepted live receipt items:    0
stage-1 + stage-2 metadata files:       11
stage-1 + stage-2 metadata fields:      44
full live receipt items required:       33
full metadata value fields required:    96
live receipt ready:                     false
parser ready:                           false
provenance ready:                       false
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
```

Expected live stage-2 metadata files:

```text
antenna_footprint_and_phase_center_geometry.json
antenna_ground_coupling_and_lift_condition.json
antenna_positioning_and_polarization_control.json
gain_setting.json
```

## Interpretation

The second live replacement stage is now exact: four setup-control metadata
JSON files, each requiring `value`, `units`, `recorded_by`, and
`recorded_at_utc`. These files document the antenna footprint and phase-center
geometry, ground-coupling and lift condition, antenna positioning and
polarization control, and gain setting before the measured traces are
collected.

No live stage-2 metadata files are present yet.

## Decision

Use this contract as the controlled-collection setup checklist after the
stage-1 pre-collection metadata files. Keep live receipt, parser/provenance,
controlled field evidence, field FWI, and field 3D/HPC blocked until real live
files pass the receipt gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage2_setup_metadata_contract.py
3 passed
```

Figure check:

```text
1924x844, dynamic range=255
```
