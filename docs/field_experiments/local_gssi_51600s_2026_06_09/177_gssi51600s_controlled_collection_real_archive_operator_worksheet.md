# Field Experiment 177: Real Archive Operator Worksheet

Date: 2026-06-25

## Purpose

Reduce collection-day ambiguity by joining the run `172` operator handoff and
run `176` real-archive acceptance contract into one fillable worksheet.

This is an operator-facing field artifact. It does not accept the dry-run
archive as measured evidence and does not launch field FWI, GPU work, field
3D/HPC, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/177_gssi51600s_controlled_collection_real_archive_operator_worksheet
```

Key artifacts:

```text
data/field_controlled_collection_real_archive_operator_worksheet.csv
data/field_controlled_collection_real_archive_operator_gate_order.csv
data/field_controlled_collection_real_archive_operator_worksheet_summary.json
docs/FIELD_COLLECTION_REAL_ARCHIVE_OPERATOR_WORKSHEET.md
figures/field_controlled_collection_real_archive_operator_worksheet.png
scripts/run_gssi_field_controlled_collection_real_archive_operator_worksheet.py
scripts/test_gssi_field_controlled_collection_real_archive_operator_worksheet.py
scripts/script_snapshot_manifest.json
```

## Result

```text
worksheet rows:                    20
file rows:                         9
metadata rows:                     11
metadata artifacts:                3
operator gate phases:              8
checksum-gate worksheet rows:      9
intake-gate worksheet rows:        20
max current gate blockers:         89
worksheet ready for collection:    true
real archive acceptance ready:     false
field FWI ready:                   false
GPU work ready:                    false
field 3D/HPC ready:                false
```

## Worksheet Scope

The worksheet has one row per collection-day item:

```text
3 controlled profile-repeat files
3 time-zero reference files
3 amplitude-reference files
11 measured metadata values
```

Each row carries the archive-relative target path, the operator action, fields
to fill, required gate, current blocker count, and acceptance check.

## Interpretation

The field-side blocker is now easier to execute but not scientifically closed.
Run `177` reduces operator ambiguity by making the real archive fill task a
single 20-row worksheet tied to the checksum, intake, structural, and
provenance gates.

The current archive still cannot support measured-field claims, field FWI, GPU
work, or field 3D/HPC until the worksheet is filled with real measured files
and real metadata and the run `176` gates pass.

## Decision

Use this worksheet on collection day. Do not relabel the synthetic archive or
dry-run packet as field evidence. Keep provenance acceptance, field FWI, heavy
GPU work, field 3D/HPC, and neural-network training blocked until the real
archive passes archive, checksum, intake, structural, and provenance gates.

## Milestone Snapshot

This is a result-driven field milestone. The exact script and focused test were
frozen under the output-local `scripts/` folder:

```text
run_gssi_field_controlled_collection_real_archive_operator_worksheet.py
sha256: 18e0e1c0e88cc960fc11a1937656091d2bdec8278b70837f2f35d903cabc3e83

test_gssi_field_controlled_collection_real_archive_operator_worksheet.py
sha256: c4e5334165de6b716ada6fcd9a2c6963769d23e23cfd87641618c2d7a6f709a5
```

Subsequent field-side worksheet or archive-intake experiments should start from
a duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_archive_operator_worksheet.py
4 passed
```

Figure check:

```text
field_controlled_collection_real_archive_operator_worksheet.png
2032x775, dynamic range=255
```
