# Field Experiment 196: Controlled Archive DZT Signature Guard Audit

Date: 2026-06-27

## Purpose

Harden the controlled archive intake gate so placeholder files cannot satisfy
the real-file requirement.

Earlier archive preflight runs checked whether expected files existed and were
nonempty. That is useful, but not sufficient: the synthetic smoke archives
contain tiny text files named `.DZT`, which are useful for pipeline testing but
must never be accepted as measured GSSI files. This run adds a conservative DZT
signature guard: expected extension, minimum file size, and the observed GSSI
DZT binary header prefix.

This is a CPU-only file audit. It does not create real measured files, accept
the archive, run field FWI, launch GPU/HPC work, run field 3D, or train neural
networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/196_gssi51600s_controlled_archive_dzt_signature_guard_audit
```

Key artifacts:

```text
data/field_controlled_archive_dzt_signature_rows.csv
data/field_controlled_archive_dzt_signature_group_summary.csv
data/field_controlled_archive_dzt_signature_guard_audit_summary.json
figures/field_controlled_archive_dzt_signature_guard_audit.png
docs/FIELD_CONTROLLED_ARCHIVE_DZT_SIGNATURE_GUARD_AUDIT.md
scripts/run_gssi_field_controlled_archive_dzt_signature_guard_audit.py
scripts/test_gssi_field_controlled_archive_dzt_signature_guard_audit.py
```

## Result

```text
DZT size floor bytes:                        65536
GSSI DZT header prefix hex:                  ff07
expected pending slots:                      9
expected pending signature passes:           0
expected pending missing files:              9
controlled profile repeat slots:             3
time-zero reference slots:                   3
amplitude reference slots:                   3
current real reference files checked:        4
current real reference signature passes:     4
synthetic placeholder files checked:         9
synthetic placeholders rejected:             9
DZT signature guard ready:                   true
pending archive real files present:          false
checksum/intake ready:                       false
controlled evidence ready:                   false
real archive acceptance ready:               false
field FWI ready:                             false
field 3D/HPC ready:                          false
GPU priority:                                none
```

Signature groups:

| Group | Rows | Passes | Missing | Size failures | Header failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| current_real_gssi_reference_file | 4 | 4 | 0 | 0 | 0 |
| expected_pending_archive_slot | 9 | 0 | 9 | 9 | 9 |
| synthetic_placeholder_named_dzt | 9 | 0 | 0 | 9 | 9 |

## Interpretation

The signature guard behaves as intended. It accepts the four observed real GSSI
DZT files in the current archive and rejects the nine tiny synthetic
placeholder files used by earlier smoke tests.

The pending controlled archive still has zero passing real-file slots because
the nine required controlled files are absent.

## Decision

Use the DZT signature guard before checksum/intake acceptance so placeholder
files cannot satisfy the real-file gate. Keep controlled evidence, field FWI,
GPU work, and field 3D/HPC blocked until the nine controlled files pass this
guard and all downstream gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_dzt_signature_guard_audit.py
5 passed
```

Figure validation:

```text
field_controlled_archive_dzt_signature_guard_audit.png
2896x840, dynamic range=255
```
