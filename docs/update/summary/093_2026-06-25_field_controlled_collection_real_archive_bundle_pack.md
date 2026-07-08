# Field Controlled Collection Real Archive Bundle Pack

Date: 2026-06-25

## Scope

This checkpoint records field run `178`, a portable collection-day bundle for
the controlled real archive.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/178_gssi51600s_controlled_collection_real_archive_bundle_pack
```

Tracked note:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/178_gssi51600s_controlled_collection_real_archive_bundle_pack.md
```

## Result

```text
bundle source files:             16
forms:                           5
contracts:                       5
references:                      6
all bundle hashes match sources: true
bundle ready for collection day: true
archive members:                 19
archive size bytes:              8863
archive SHA-256:                 dd6ed7c7900d75077840c8ab2292c67465282a48e497b2e93c713aefed19ce2a
worksheet rows:                  20
measured file rows:              9
metadata rows:                   11
real archive acceptance ready:   false
field FWI ready:                 false
```

## Decision

Run `178` is the current field collection-day handoff bundle. It improves
operator readiness but does not create measured field evidence. Field FWI,
heavy GPU work, field 3D/HPC, and neural-network training remain blocked until
real files and metadata pass archive, checksum, intake, structural, and
provenance gates.

## Milestone Snapshot

This milestone froze:

```text
run_gssi_field_controlled_collection_real_archive_bundle_pack.py
sha256: 6926e7e264f3033e7135b5ca091228e6c888d5eb392e00d7cba5781b0c8bc6f9

test_gssi_field_controlled_collection_real_archive_bundle_pack.py
sha256: 3cc7fee9dc66979ffca742efbe79de36518cb8b39d66555ec50d4ebf0c40609b
```

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

Marathon status: active. The next useful branch is snapshot-policy refresh and
then report/presentation or another bounded readiness artifact.
