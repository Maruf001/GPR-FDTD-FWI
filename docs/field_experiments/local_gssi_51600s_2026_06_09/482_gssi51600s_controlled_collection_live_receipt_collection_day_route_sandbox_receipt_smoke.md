# Field Experiment 482: Controlled Collection Live Receipt Collection-Day Route Sandbox Receipt Smoke

Date: 2026-06-30

## Purpose

Exercise the collection-day route from runs `479-481` in an output-local
sandbox.

This run rewrites the 33 live route paths into a sandbox manifest inside its
own output directory, creates 33 synthetic placeholder files there, and runs the
live receipt verifier against that sandbox manifest.

This is a receipt-mechanics smoke only. It does not create measured field
evidence and does not place any file in the locked live external return paths.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/482_gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke
```

Key artifacts:

```text
data/sandbox_live_receipt_files/
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_sandbox_manifest.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_sandbox_receipt_report.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_synthetic_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke.png
scripts/
```

## Result

```text
source route ready:                 true
source route validation ready:      true
source route sensitivity ready:     true
sandbox file count:                 33
sandbox DZT-like placeholder files: 9
sandbox metadata JSON files:        24
sandbox nonempty files:             33
sandbox receipt-ready files:        33
sandbox required receipt checks:    183
sandbox metadata JSON parsed:       24
original live files present:        0
synthetic-only files:               33
measured field evidence files:      0
parser ready:                       false
provenance ready:                   false
archive ready:                      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The sandbox packet contains:

| Sandbox family | Files | Receipt checks |
| --- | ---: | ---: |
| Controlled profile repeat placeholders | 3 | 18 |
| Time-zero reference placeholders | 3 | 18 |
| Amplitude-reference placeholders | 3 | 18 |
| Global metadata JSON placeholders | 15 | 75 |
| Per-file metadata JSON placeholders | 9 | 54 |

## Interpretation

The receipt route mechanics can pass when all 33 expected files exist in a
sandbox and the metadata JSON files parse. The current live field packet still
has zero measured files and zero accepted evidence.

The synthetic DZT-like files are placeholders. They do not satisfy measured
DZT header parsing, provenance, archive acceptance, field FWI, or field 3D/HPC
requirements.

## Decision

Use run `482` as a receipt-mechanics smoke only. Keep parser, provenance,
archive, controlled field evidence, field FWI, GPU work, and field 3D/HPC
blocked until real measured files are placed in the locked live paths and all
downstream gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
