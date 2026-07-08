# Field Experiment 284: Positive-Control Fill Smoke

Date: 2026-06-28

## Purpose

Stage a private synthetic return inbox and test whether the current real-return
mechanics can recognize a complete packet.

Runs `263-283` show that the real return inbox is structurally ready but still
empty. This run checks the opposite side of the gate without touching that real
inbox: it creates a synthetic positive-control inbox inside this output folder,
fills nine non-empty DZT-shaped files, 32 metadata values, and nine matching
checksums, and confirms the scanner mechanics can count them.

This is not measured field data. It does not accept provenance, accept a real
archive, promote controlled field evidence, run field FWI, run field 3D/HPC, or
launch GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/284_gssi51600s_controlled_collection_real_return_positive_control_fill_smoke
```

Key artifacts:

```text
positive_control_return_inbox/
data/field_controlled_collection_real_return_positive_control_fill_smoke_synthetic_file_rows.csv
data/field_controlled_collection_real_return_positive_control_fill_smoke_synthetic_metadata_rows.csv
data/field_controlled_collection_real_return_positive_control_fill_smoke_synthetic_checksum_rows.csv
data/field_controlled_collection_real_return_positive_control_fill_smoke_summary.json
figures/field_controlled_collection_real_return_positive_control_fill_smoke.png
scripts/script_snapshot_manifest.json
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_POSITIVE_CONTROL_FILL_SMOKE.md
```

## Expected Result

```text
synthetic files present:                  9
synthetic metadata values present:        32
synthetic checksums present:              9
synthetic checksum matches:               9
unexpected files:                         0
zero-byte placeholders:                   0
extension failures:                       0
synthetic positive-control mechanics pass:true
real measured data present:               false
provenance acceptance ready:              false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

## Decision Rule

If the synthetic positive control passes, the field scanner mechanics are not
the blocker. The remaining blocker is still the absence of real measured DZT
files, measured metadata values, and checksums in the real return inbox.
