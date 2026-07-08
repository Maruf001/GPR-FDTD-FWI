# Field Experiment 558: Stage-6 Session Closeout Contract

Date: 2026-07-01

## Purpose

Define the exact live metadata contract for controlled-collection stage `6`,
the session closeout records.

This run extends the stage-5 amplitude reference contract from run `557` and
closes the six-stage receipt contract sequence. It does not create measured
field evidence, accept live field files, run DZT parsing, promote
provenance/archive state, launch field FWI, or launch field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/558_gssi51600s_controlled_collection_live_receipt_stage6_session_closeout_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_stage6_session_closeout_contract_contract_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage6_session_closeout_contract_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage6_session_closeout_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage-6 metadata files required:        4
stage-6 metadata value fields required: 16
stage-6 live parents present:           4
stage-6 live metadata files present:    0
stage-6 accepted live receipt items:    0
cumulative receipt items through s6:    33
cumulative metadata fields through s6:  96
contract sequence closed:               true
full live receipt items required:       33
full metadata value fields required:    96
live receipt ready:                     false
parser ready:                           false
provenance ready:                       false
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
```

Expected live stage-6 metadata files:

```text
date_utc.json
notes.json
operator.json
weather.json
```

Each metadata file must carry `value`, `units`, `recorded_by`, and
`recorded_at_utc`.

## Interpretation

The sixth live replacement stage is now exact: four session closeout metadata
JSON records for date, notes, operator, and weather. With this stage, the
controlled field receipt contract covers all thirty-three live receipt items
and all ninety-six metadata value fields.

No live stage-6 files are present yet.

## Decision

Use this contract as the session-closeout checklist after the measurement and
reference stages. Keep live receipt, parser/provenance, controlled field
evidence, field FWI, and field 3D/HPC blocked until all real live files pass
the receipt gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage6_session_closeout_contract.py
3 passed
```

Figure check:

```text
1924x844, dynamic range=255
```
