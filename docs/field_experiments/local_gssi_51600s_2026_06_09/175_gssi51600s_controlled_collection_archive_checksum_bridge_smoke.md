# Field Experiment 175: Archive Checksum Bridge Smoke

Date: 2026-06-25

## Purpose

Verify that the archive layout and checksum ledger interoperate: a complete
archive should provide the nine file paths that the checksum ledger hashes and
accepts.

This is a synthetic integration smoke connecting runs `168`, `171`, `173`, and
`174`.

This run does not create measured field evidence, run DZT preprocessing, field
FWI, GPU/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/175_gssi51600s_controlled_collection_archive_checksum_bridge_smoke
```

Key artifacts:

```text
data/field_controlled_collection_archive_checksum_bridge_ledger.csv
data/field_controlled_collection_archive_checksum_bridge_findings.csv
data/field_controlled_collection_archive_checksum_bridge_roles.csv
data/field_controlled_collection_archive_checksum_bridge_smoke_summary.json
figures/field_controlled_collection_archive_checksum_bridge_smoke.png
docs/FIELD_COLLECTION_ARCHIVE_CHECKSUM_BRIDGE_SMOKE.md
scripts/run_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py
scripts/test_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
archive preflight checks:           23
archive blocking findings:          0
checksum ledger rows:               9
checksum accepted rows:             9
checksum findings:                  0
checksum blocking findings:         0
combined synthetic smoke pass:      true
synthetic smoke only:               true
scientific field claim ready:       false
field FWI ready:                    false
GPU/HPC ready:                      false
```

## Interpretation

The archive layout and checksum ledger can work as one workflow: all synthetic
archive checks pass, and all nine archived files hash into accepted checksum
ledger rows.

This is not measured field evidence. Real controlled-collection files must pass
the same archive, checksum, intake, structural, and provenance gates before any
scientific field claim or field FWI path reopens.

## Decision

Use run `175` as an integration smoke for the archive-to-ledger workflow. Do
not treat it as evidence that the real field archive is present.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py
2 passed
```

Compile check:

```text
run_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py: pass
tests/test_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py: pass
```

Figure check:

```text
1816x772, dynamic range=255
```
