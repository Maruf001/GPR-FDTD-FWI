# Field Experiment 536: Measured-DZT Live Collection Manifest

Date: 2026-06-30

## Purpose

Create a non-live collection manifest for the nine measured DZT files required
by the controlled field packet.

Runs `530-532` showed that DZT live parent directories exist, but no measured
DZT files are present. This run records the exact collection checklist without
creating placeholder DZT files.

This is CPU-only manifest generation and readiness auditing. It does not
ingest DZT files, run a parser, accept provenance, launch field FWI, launch GPU
work, or promote field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/536_gssi51600s_controlled_collection_measured_dzt_live_collection_manifest
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_dzt_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_family_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_action_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_summary.json
figures/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest.png
scripts/script_snapshot_manifest.json
```

## Result

```text
required DZT files:                  9
controlled profile repeats:          3
time-zero references:                3
amplitude references:                3
parent directories present:          9
live DZT files present:              0
live DZT files accepted:             0
placeholder files created:           0
complete families:                   0
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
```

## Interpretation

The measured-DZT collection target is now explicit: three controlled profile
repeats, three time-zero references, and three amplitude references. None are
currently present.

## Decision

Use this manifest as the DZT collection checklist. Do not create placeholders
or run field parsing/FWI before real DZT files are staged and accepted.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_measured_dzt_live_collection_manifest.py
3 passed
```

Figure check:

```text
2284x851, dynamic range=255
```
