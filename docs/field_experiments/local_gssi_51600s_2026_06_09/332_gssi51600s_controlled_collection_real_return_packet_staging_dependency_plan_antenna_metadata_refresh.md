# Field Experiment 332: Antenna-Aware Staging Dependency Plan Refresh

Date: 2026-06-29

## Purpose

Refresh the controlled field return-packet staging dependency plan after the
antenna aperture/coupling metadata addendum and the 61-item acceptance-gate
refresh.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/332_gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_stage_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_dependency_edges.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh.png
scripts/script_snapshot_manifest.json
```

## Result

```text
staging plan ready:                 true
source acceptance gate ready:        true
stage count:                        7
dependency edges:                   9
packet items required:              61
missing packet items:               61
missing measured DZT files:         9
metadata requirements:              36
missing global metadata values:     15
missing per-file metadata values:   21
antenna metadata addendum items:    4
missing checksum rows:              9
missing acceptance results:         7
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The older staging dependency plan covered the previous 57-item measured return
packet. The current packet target is 61 items because antenna aperture,
footprint/phase-center, coupling/lift-off, and positioning/polarization
metadata are now blocking field requirements.

The seven-stage order is unchanged:

| Stage | Required missing items |
| --- | ---: |
| Controlled profile repeats | 3 |
| Time-zero references | 3 |
| Amplitude references | 3 |
| Global metadata values | 15 |
| Per-file metadata values | 21 |
| SHA-256 checksum rows | 9 |
| Acceptance-result files | 7 |

The current archive still has zero measured packet items, so this is a staging
plan, not field evidence.

## Decision

Use this refreshed dependency plan as the current controlled field return-packet
staging sequence. Do not run provenance acceptance, archive acceptance, field
FWI, GPU work, or field 3D/HPC until the 61-item packet is present and passes
the antenna-aware acceptance gate.

## Validation

Focused source test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh.py
3 passed
```

Figure validation:

```text
3760x961, dynamic range=255
```
