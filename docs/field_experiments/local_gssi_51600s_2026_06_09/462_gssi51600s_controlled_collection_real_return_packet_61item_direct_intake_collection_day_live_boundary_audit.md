# Field Experiment 462: Collection-Day Live Boundary Audit

Date: 2026-06-30

## Purpose

Audit the boundary between prepared collection-day artifacts and live measured
field files.

Runs `459`-`461` validated the collection-day bundle manifest. This run places
that bundle beside the filesystem gap, collection checklist, receipt command
plan, and metadata template pack to show exactly what is prepared and exactly
what is still missing.

This run does not copy measured files, execute receipt commands, rerun parser
or provenance gates, accept a real archive, launch field FWI, or promote field
3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/462_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_boundary_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source chain ready:                    true
boundary sides:                        3
prepared artifacts:                    57
required live files:                   33
required DZT files:                    9
required metadata JSON files:          24
metadata template files:               24
metadata template fields:              129
blank metadata-template fields:        96
live files present:                    0
missing live files:                    33
missing DZT files:                     9
missing metadata JSON files:           24
receipt commands:                      33
receipt commands executed:             0
receipt checks ready:                  0
evidence-ready rows:                   0
field FWI ready:                       false
field 3D/HPC ready:                    false
boundary audit ready:                  true
```

Boundary rows:

| Boundary side | Prepared items | Required live files | Present live files | Missing live files | State |
| --- | ---: | ---: | ---: | ---: | --- |
| DZT live files | 0 | 9 | 0 | 9 | missing measured DZT files |
| metadata JSON templates | 24 | 24 | 0 | 24 | templates ready but live metadata missing |
| receipt commands | 33 | 33 | 0 | 33 | commands ready but not executed |

## Interpretation

The field side is prepared for collection-day intake, but it is not field
evidence yet. The manifest, metadata templates, and receipt commands are
ready. No measured DZT files or completed metadata JSON files have been copied
into live staging, and no receipt command has been executed.

The current blocker is concrete: 33 live files are missing, made of nine DZT
files and 24 metadata JSON files.

## Decision

Use run `462` as the current field-side live-boundary checkpoint. Do not rerun
parser, provenance, archive, field FWI, or field 3D/HPC gates until the 33 live
files exist and the 33 receipt commands have passed.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_collection_day_live_boundary_audit.py
5 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
