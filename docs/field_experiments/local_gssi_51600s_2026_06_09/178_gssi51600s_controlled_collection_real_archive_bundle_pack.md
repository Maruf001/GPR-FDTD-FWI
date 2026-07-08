# Field Experiment 178: Controlled Collection Real Archive Bundle Pack

Date: 2026-06-25

## Purpose

Package the real-archive worksheet, archive layout, checksum ledger, intake
manifest, and gate instructions into one collection-day handoff bundle.

This run does not create measured field evidence and does not launch field FWI,
heavy GPU work, field 3D/HPC, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/178_gssi51600s_controlled_collection_real_archive_bundle_pack
```

Key artifacts:

```text
bundle/
bundle/CHECKSUMS.sha256
bundle/COLLECTION_DAY_SEQUENCE.md
bundle/README.md
bundle/forms/
bundle/contracts/
bundle/reference/
data/gssi51600s_controlled_collection_real_archive_bundle.tar.gz
data/field_controlled_collection_real_archive_bundle_files.csv
data/field_controlled_collection_real_archive_bundle_summary.json
docs/FIELD_COLLECTION_REAL_ARCHIVE_BUNDLE_PACK.md
figures/field_controlled_collection_real_archive_bundle_pack.png
scripts/run_gssi_field_controlled_collection_real_archive_bundle_pack.py
scripts/test_gssi_field_controlled_collection_real_archive_bundle_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
bundle source files:             16
forms:                           5
contracts:                       5
references:                      6
helper files:                    3
all bundle hashes match sources: true
bundle ready for collection day: true
archive members:                 19
archive members unique:          true
archive members sorted:          true
archive size bytes:              8863
archive SHA-256:                 dd6ed7c7900d75077840c8ab2292c67465282a48e497b2e93c713aefed19ce2a
worksheet rows:                  20
measured file rows:              9
metadata rows:                   11
max current gate blockers:       89
real archive acceptance ready:   false
field FWI ready:                 false
GPU work ready:                  false
field 3D/HPC ready:              false
```

The bundle archive is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/178_gssi51600s_controlled_collection_real_archive_bundle_pack/data/gssi51600s_controlled_collection_real_archive_bundle.tar.gz
```

## Interpretation

Run `178` turns the field-side collection design into a portable handoff
artifact. It contains the forms to fill, the archive layout contracts, the
checksum and intake templates, and the operator sequence.

It still contains no real measured files or real metadata. Real archive
acceptance, measured-field claims, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training remain blocked until real files and metadata fill the
bundle-derived archive and pass the gates.

## Decision

Use run `178` as the current field collection-day bundle. Do not promote the
dry-run archive to measured evidence, and do not launch field FWI, heavy GPU
work, field 3D/HPC, or neural-network training until the real archive passes
archive, checksum, intake, structural, and provenance gates.

## Milestone Snapshot

This is a result-driven field milestone. It froze:

```text
run_gssi_field_controlled_collection_real_archive_bundle_pack.py
sha256: 6926e7e264f3033e7135b5ca091228e6c888d5eb392e00d7cba5781b0c8bc6f9

test_gssi_field_controlled_collection_real_archive_bundle_pack.py
sha256: 3cc7fee9dc66979ffca742efbe79de36518cb8b39d66555ec50d4ebf0c40609b
```

Subsequent field collection-day or return-intake experiments should start from
a duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_archive_bundle_pack.py
3 passed
```

Archive and figure checks:

```text
tar members: 19 unique / 19 total
field_controlled_collection_real_archive_bundle_pack.png
1924x774, dynamic range=255
```
