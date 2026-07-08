# Field Experiment 179: Controlled Collection Real Archive Bundle Unpack Smoke

Date: 2026-06-25

## Purpose

Verify that the run `178` controlled-collection real-archive handoff bundle can
be unpacked after transfer and that its packaged checksum ledger verifies.

This run does not create measured field evidence and does not launch field FWI,
heavy GPU work, field 3D/HPC, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/179_gssi51600s_controlled_collection_real_archive_bundle_unpack_smoke
```

Key artifacts:

```text
data/field_controlled_collection_real_archive_bundle_unpack_members.csv
data/field_controlled_collection_real_archive_bundle_unpack_checksums.csv
data/field_controlled_collection_real_archive_bundle_unpack_summary.json
docs/FIELD_COLLECTION_REAL_ARCHIVE_BUNDLE_UNPACK_SMOKE.md
figures/field_controlled_collection_real_archive_bundle_unpack_smoke.png
extracted_bundle/
scripts/run_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
scripts/test_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                         178
source archive SHA-256:             dd6ed7c7900d75077840c8ab2292c67465282a48e497b2e93c713aefed19ce2a
source archive hash matches run178: true
archive members:                    19
archive safe members:               19
archive unsafe members:             0
checksum entries:                   18
checksum entries passing:           18
checksum entries failing:           0
unpack smoke ready:                 true
bundle ready for collection day:    true
real archive acceptance ready:      false
field FWI ready:                    false
GPU work ready:                     false
field 3D/HPC ready:                 false
```

## Interpretation

The collection-day bundle is transport-readable: it unpacks into one safe root,
all `19` archive members are path-safe, and all `18` checksum entries match the
extracted files.

This still does not make the archive measured field evidence. The bundle
contains forms, contracts, references, checksums, and sequence notes only.
Real measured files and real metadata still have to be collected and passed
through the archive, checksum, intake, structural, and provenance gates.

## Decision

Use the run `178` bundle for operator handoff. Keep real archive acceptance,
field FWI, heavy GPU work, field 3D/HPC, and neural-network training blocked
until real measured files and metadata pass the gates.

## Milestone Snapshot

This is a result-driven field milestone. It froze:

```text
run_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
sha256: d30ffa113fca7ac1d24dff923d956adc7526f80f2ec8e219d7dde3ba49c42cd6

test_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
sha256: f1a19a7091ffd846e6add538f68485800cb9b92eacb2cc224df5141223b33652
```

Subsequent field bundle-consumer experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
3 passed
```

Figure check:

```text
field_controlled_collection_real_archive_bundle_unpack_smoke.png
1852x738, dynamic range=255
```
