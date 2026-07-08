# Field Real Archive Bundle Unpack Smoke

Date: 2026-06-25

## Scope

This checkpoint records field run `179`, which unpacks the run `178`
collection-day bundle into an isolated output folder and verifies its checksum
ledger.

No measured field evidence was created. No field FWI, heavy GPU work, field
3D/HPC, or neural-network training was started.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/179_gssi51600s_controlled_collection_real_archive_bundle_unpack_smoke
docs/field_experiments/local_gssi_51600s_2026_06_09/179_gssi51600s_controlled_collection_real_archive_bundle_unpack_smoke.md
```

## Result

```text
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

## Decision

The run `178` collection-day bundle is readable and checksum-consistent after
unpack. Use it for operator handoff. Keep real archive acceptance, field FWI,
heavy GPU work, field 3D/HPC, and neural-network training blocked until real
measured files and metadata pass the gates.

## Milestone Snapshot

Frozen scripts:

```text
run_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
sha256: d30ffa113fca7ac1d24dff923d956adc7526f80f2ec8e219d7dde3ba49c42cd6

test_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
sha256: f1a19a7091ffd846e6add538f68485800cb9b92eacb2cc224df5141223b33652
```

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_archive_bundle_unpack_smoke.py
3 passed
```

Figure check:

```text
1852x738, dynamic range=255
```
