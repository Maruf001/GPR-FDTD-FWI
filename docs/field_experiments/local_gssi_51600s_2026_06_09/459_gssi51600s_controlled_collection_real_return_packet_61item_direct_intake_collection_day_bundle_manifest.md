# Field Experiment 459: Direct-Intake Collection-Day Bundle Manifest

Date: 2026-06-30

## Purpose

Create a single collection-day bundle manifest that joins the 33 required live
field files with the validated metadata JSON templates.

Runs `457-458` guarded the metadata templates. This run combines those
templates with the run `455` copy checklist so the collection handoff has one
table for measured DZT files, completed metadata JSON files, linked templates,
and current evidence status.

This run does not copy measured files, write to live staging, accept
provenance, build a field archive, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/459_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_bundle_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source checklist ready:                    true
source template pack ready:                true
source template validation ready:          true
bundle file entries:                       33
DZT file entries:                          9
metadata JSON entries:                     24
metadata templates linked:                 24
live files present:                        0
receipt checks ready:                      0
evidence-ready entries:                    0
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Interpretation

The controlled collection handoff now has one practical manifest. It shows the
nine measured DZT files still needed, the 24 metadata JSON files still needed,
and the available template path for every metadata JSON file.

No live field file is present yet, so field evidence remains blocked.

## Decision

Use run `459` as the collection-day bundle manifest. Copy measured DZT files
and completed real metadata JSON files into live staging, then rerun receipt,
parser, provenance, and archive gates before any field FWI or field 3D/HPC
work.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_validator.py
8 passed
```

Figure check:

```text
2142x843, dynamic range=255
```
