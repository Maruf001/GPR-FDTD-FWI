# Field Experiment 530: Controlled Collection Metadata Live-Path Rescan

Date: 2026-06-30

## Purpose

Rescan the live external return paths for controlled-collection metadata and
paired measured DZT files after run `527`.

This run turns the metadata completion route into a concrete live-path status:
which expected metadata JSON and measured DZT files exist on disk now, which
parents exist, and which actions can start.

This is CPU-only filesystem and readiness auditing. It does not create live
metadata, create DZT files, parse DZT, run provenance validation, run field
FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/530_gssi51600s_controlled_collection_metadata_live_path_rescan
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_live_path_rescan_item_rows.csv
data/gssi51600s_controlled_collection_metadata_live_path_rescan_action_rows.csv
data/gssi51600s_controlled_collection_metadata_live_path_rescan_summary.json
figures/gssi51600s_controlled_collection_metadata_live_path_rescan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source route ready:                       true
live items:                               33
live actions:                             4
parent directories present:               33
live files present:                       0
live files nonempty:                      0
live files accepted:                      0
global metadata files expected/missing:   15 / 15
per-file metadata files expected/missing: 9 / 9
paired DZT files expected/missing:        9 / 9
final receipt required/missing:           33 / 33
complete actions:                         0
live receipt ready:                       false
provenance ready:                         false
field FWI ready:                          false
field 3D/HPC ready:                       false
GPU priority:                             none
```

The four live-path actions are:

| Order | Action | Required | Present | Accepted | Missing | Can start |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | global metadata live files | 15 | 0 | 0 | 15 | true |
| 2 | paired measured DZT files | 9 | 0 | 0 | 9 | true |
| 3 | per-file metadata live files | 9 | 0 | 0 | 9 | false |
| 4 | final live receipt gate | 33 | 0 | 0 | 33 | false |

## Interpretation

The live return root has the expected directory structure, but none of the
thirty-three live files exist. The field-side blocker is therefore concrete:
fifteen global metadata JSON files, nine measured DZT files, and nine per-file
metadata JSON files are still required.

## Decision

Keep live receipt, parser/provenance/archive readiness, controlled field
evidence, field FWI, and field 3D/HPC blocked until real metadata and measured
DZT files are returned.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_live_path_rescan.py
3 passed
```

Figure check:

```text
2572x850, dynamic range=255
```
