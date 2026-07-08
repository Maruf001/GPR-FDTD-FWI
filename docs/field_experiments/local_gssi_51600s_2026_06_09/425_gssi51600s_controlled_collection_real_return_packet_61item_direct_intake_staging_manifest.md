# Field Experiment 425: Direct Intake Staging Manifest

Date: 2026-06-30

## Purpose

Convert the 33 open direct real-input gaps from the field packet filesystem
audit into a concrete staging manifest.

Runs `419-424` showed that all direct real-input slots remain open: templates
and synthetic references exist, but no accepted real field files exist. This
run defines where the real files should be staged and what actions must happen
after staging. It does not stage files, parse files, accept provenance, accept
an archive, or create measured field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/425_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_staging_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest.png
scripts/script_snapshot_manifest.json
```

## Result

```text
direct intake staging manifest ready:      true
direct real-input slots:                   33
measured DZT files required:               9
global metadata JSON files required:       15
per-file metadata JSON files required:     9
staging actions:                           5
filesystem gaps:                           33
blank-template candidate files:            62
synthetic-reference candidate files:       33
staged real files:                         0
accepted measured-evidence files:          0
template/synthetic allowed rows:           0
real packet files present:                 false
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The five ordered actions are:

| Priority | Action | Required rows |
| ---: | --- | ---: |
| 1 | stage measured DZT files | 9 |
| 2 | stage global metadata JSON files | 15 |
| 3 | stage per-file metadata JSON files | 9 |
| 4 | rerun intake parser | 33 |
| 5 | rerun provenance and archive gates | 33 |

Template files and synthetic references are explicitly disallowed for all
actions.

## Decision

Use run `425` as the direct intake staging manifest for a future real field
packet. Keep provenance acceptance, archive acceptance, measured field evidence,
field FWI, GPU work, and field 3D/HPC blocked until real files are staged and
pass the gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest.py
5 passed
```

Figure check:

```text
2411x846, dynamic range=255
```
