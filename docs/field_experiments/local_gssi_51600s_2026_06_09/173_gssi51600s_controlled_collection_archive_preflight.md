# Field Experiment 173: Controlled Collection Archive Preflight

Date: 2026-06-25

## Purpose

Preflight a candidate real controlled-collection archive root against the run
`171` archive layout before checksum, intake, structural, and provenance gates.

This is a CPU-only preflight. It does not create measured field evidence, run
DZT preprocessing, launch field FWI, use GPU/HPC, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/173_gssi51600s_controlled_collection_archive_preflight
```

Key artifacts:

```text
data/field_controlled_collection_archive_preflight.csv
data/field_controlled_collection_archive_preflight_summary.json
figures/field_controlled_collection_archive_preflight.png
docs/FIELD_COLLECTION_ARCHIVE_PREFLIGHT.md
scripts/run_gssi_field_controlled_collection_archive_preflight.py
scripts/test_gssi_field_controlled_collection_archive_preflight.py
scripts/script_snapshot_manifest.json
```

## Result

```text
preflight checks:                  23
passed checks:                     0
failed checks:                     23
blocking findings:                 23
directory checks:                  7
real-file checks:                  9
metadata-artifact checks:          6
archive ready for checksum/intake: false
provenance acceptance ready:       false
structural rerun ready:            false
field FWI ready:                   false
GPU/HPC ready:                     false
```

The default pending archive root is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/pending_controlled_collection_archive
```

It currently contains no real controlled-collection archive, so the preflight
fails as expected.

## Interpretation

The field branch now has a preflight before the checksum and intake gates. It
requires the archive root, seven directories, nine nonempty DZT files, and six
nonempty metadata artifacts to exist before the checksum ledger and intake
manifest should be trusted.

This is not measured field evidence. It is the shape gate that a future real
archive must pass before checksum, intake, structural, provenance, field FWI,
GPU, or field 3D/HPC work can proceed.

## Decision

Do not run checksum, intake, structural, provenance, field FWI, GPU, or field
3D/HPC gates until a real archive passes this preflight.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_archive_preflight.py
3 passed
```

Figure check:

```text
field_controlled_collection_archive_preflight.png
1996x790, dynamic range=255
```
