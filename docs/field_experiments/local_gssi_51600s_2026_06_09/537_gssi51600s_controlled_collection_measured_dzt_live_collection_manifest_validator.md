# Field Experiment 537: Measured-DZT Live Collection Manifest Validator

Date: 2026-06-30

## Purpose

Validate the saved run `536` measured-DZT collection manifest.

The validator checks that the manifest has nine DZT files across three
families, that no live DZT file or placeholder exists, and that live receipt,
parser/provenance/archive, field FWI, and field 3D/HPC remain blocked.

This is CPU-only artifact validation. It does not ingest DZT files, run a
parser, accept provenance, launch field FWI, launch GPU work, or promote field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/537_gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validator_check_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validator_summary.json
figures/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              6
checks passed:                       6
checks failed:                       0
required DZT files:                  9
live DZT files present:              0
placeholder files created:           0
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
```

## Interpretation

The measured-DZT collection manifest validates as a collection checklist, not
as measured evidence.

## Decision

Keep receipt, parser/provenance/archive, field FWI, and field 3D/HPC blocked
until real DZT files are staged.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_measured_dzt_live_collection_manifest_validator.py
3 passed
```

Figure check:

```text
2285x839, dynamic range=255
```
