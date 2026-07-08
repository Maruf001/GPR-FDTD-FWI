# Field Experiment 464: Live Receipt Verifier Current-State Audit

Date: 2026-06-30

## Purpose

Audit the current field live-file state with a reusable receipt verifier shell.

Runs `462` and `463` showed that the collection-day packet is prepared but no
live measured files are present. This run adds a receipt verifier that can scan
the locked 33-row receipt manifest, compute checksums for present files, parse
metadata JSON files, and write a current receipt report without promoting field
evidence.

This run does not copy measured files, accept field evidence, rerun the parser,
rerun provenance, rerun archive acceptance, launch field FWI, launch GPU work,
or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/464_gssi51600s_controlled_collection_live_receipt_verifier_current_state_audit
```

Key artifacts:

```text
data/live_receipt_verifier_report.csv
data/gssi51600s_controlled_collection_live_receipt_verifier_current_state_audit_summary.json
figures/gssi51600s_controlled_collection_live_receipt_verifier_current_state_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source live-boundary sensitivity ready: true
receipt verifier available:             true
verifier exit code:                     0
receipt report written:                 true
required receipt rows:                  33
DZT receipt rows:                       9
metadata JSON receipt rows:             24
present files:                          0
nonempty files:                         0
missing files:                          33
metadata JSON parse-ready files:        0
receipt-ready rows:                     0
controlled field evidence rows:         0
all receipts ready:                     false
parser ready:                           false
provenance ready:                       false
archive ready:                          false
field FWI ready:                        false
field 3D/HPC ready:                     false
audit ready:                            true
```

## Interpretation

The verifier is operational, but the current live staging state is still empty.
All 33 required files are missing: nine measured DZT files and 24 completed
metadata JSON files. The report is useful as a repeatable collection-day check,
but it is not field evidence because no receipt row passes.

## Decision

Use run `464` as the current live receipt verification checkpoint. Do not rerun
parser, provenance, archive acceptance, field FWI, GPU work, or field 3D/HPC
until all 33 receipt rows pass the verifier.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_verifier.py
tests/test_gssi_field_controlled_collection_live_receipt_verifier_current_state_audit.py
8 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
