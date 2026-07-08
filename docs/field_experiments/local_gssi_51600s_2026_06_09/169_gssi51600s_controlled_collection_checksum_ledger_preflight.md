# Field Experiment 169: Controlled Collection Checksum Ledger Preflight

Date: 2026-06-25

## Purpose

Validate the checksum ledger from run `168` before the intake manifest,
structural validator, and provenance gate are rerun on real controlled
collection files.

This is CPU-only gate tooling. It does not create measured field evidence, run
DZT preprocessing, launch field FWI, use GPU/HPC, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/169_gssi51600s_controlled_collection_checksum_ledger_preflight
```

Key artifacts:

```text
data/field_controlled_collection_checksum_ledger_preflight_findings.csv
data/field_controlled_collection_checksum_ledger_preflight_roles.csv
data/field_controlled_collection_checksum_ledger_preflight_summary.json
figures/field_controlled_collection_checksum_ledger_preflight.png
docs/FIELD_COLLECTION_CHECKSUM_LEDGER_PREFLIGHT.md
```

## Result

```text
ledger rows:                         9
findings:                            45
blocking findings:                   45
accepted rows:                       0
preflight ready:                     false
ready for provenance acceptance:     false
ready for structural rerun:          false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Per-role blockers:

| File role | Rows | Accepted | Blocking findings | Ready |
| --- | ---: | ---: | ---: | --- |
| amplitude reference | 3 | 0 | 15 | false |
| controlled profile repeat | 3 | 0 | 15 | false |
| time-zero reference | 3 | 0 | 15 | false |

## Interpretation

The blank checksum ledger fails exactly where it should: each of the nine
required real-file rows is missing accepted ledger status, real archived file
path, recorded SHA-256, operator initials, and UTC timestamp.

This adds a deterministic file-integrity gate for the future field day. When
real files are archived, the preflight will check basename agreement, file
existence, 64-character SHA-256 format, computed hash equality, operator
initials, timestamp format, and accepted/verified/complete ledger status.

## Decision

Use this preflight on the real collection-day checksum ledger before rerunning
the intake manifest, structural validator, and provenance gate. Keep
provenance acceptance, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training blocked until the real ledger passes.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_checksum_ledger_preflight.py
3 passed
```

Figure check:

```text
1816x807, dynamic range=255
```
