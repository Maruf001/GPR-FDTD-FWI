# Field Experiment 494: Controlled Collection Live Receipt Collection-Day Global Metadata Prefill Template Pack

Date: 2026-06-30

## Purpose

Create output-local templates for the 15 global metadata files identified by
run `491` as pre-collection work.

The templates are planning artifacts only. They are not written to the live
external return path and they do not count as receipt-ready field files.

This is a CPU-only file-template run. It does not create live measured files,
parse DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/494_gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack
```

Key artifacts:

```text
templates/global/*.json
data/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_template_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack.png
scripts/
```

## Result

```text
source policy ready:                    true
source validation ready:                true
source sensitivity ready:               true
templates:                              15
global metadata templates:              15
template files written:                 15
template JSON key count min:             9
template JSON key count max:             9
total required receipt checks:          75
value placeholders:                     30
current live files present:              0
current live receipt-ready files:         0
template/live path overlaps:             0
templates accepted as live receipt:       0
live receipt ready:                     false
parser ready:                           false
provenance ready:                       false
archive ready:                          false
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
gpu priority:                           none
template pack ready:                    true
```

Template fields:

```text
template_type
dataset_id
metadata_name
status
value
units
source_live_staging_relative_path
requires_measured_dzt
do_not_promote_as_live_receipt
```

## Interpretation

The field preparation task is now more concrete. Fifteen global metadata JSON
files can be drafted before the measurement day, but the drafted templates are
not evidence. They must be completed with real values and copied into the live
external return path only when they are ready for receipt checking.

The live field state remains unchanged: zero files are present and zero files
are receipt-ready.

## Decision

Use these templates to prefill global metadata before collection. Keep
receipt, parser, provenance, archive, field FWI, and field 3D/HPC blocked until
completed real files are placed in the live return path and pass receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack.py

3 passed
```

Figure validation:

```text
2285x848, dynamic range=255
```
