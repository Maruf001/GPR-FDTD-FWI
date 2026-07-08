# Field Experiment 170: Checksum Ledger Preflight Smoke

Date: 2026-06-25

## Purpose

Create a synthetic pass-case for the run `169` checksum-ledger preflight using
tiny generated files with computed SHA-256 values.

This is CPU-only validator smoke. It does not create measured field evidence,
run DZT preprocessing, launch field FWI, use GPU/HPC, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/170_gssi51600s_controlled_collection_checksum_ledger_preflight_smoke
```

Key artifacts:

```text
data/field_controlled_collection_checksum_ledger_preflight_smoke_ledger.csv
data/field_controlled_collection_checksum_ledger_preflight_smoke_findings.csv
data/field_controlled_collection_checksum_ledger_preflight_smoke_roles.csv
data/field_controlled_collection_checksum_ledger_preflight_smoke_summary.json
figures/field_controlled_collection_checksum_ledger_preflight_smoke.png
docs/FIELD_COLLECTION_CHECKSUM_LEDGER_PREFLIGHT_SMOKE.md
```

## Result

```text
synthetic ledger rows:              9
synthetic accepted rows:            9
synthetic findings:                 0
synthetic blocking findings:        0
synthetic preflight ready:          true
blank template blocking findings:   45
synthetic file count:               9
scientific field claim ready:       false
field FWI ready:                    false
GPU/HPC ready:                      false
```

Per-role result:

| File role | Rows | Accepted | Blocking findings | Ready |
| --- | ---: | ---: | ---: | --- |
| amplitude reference | 3 | 3 | 0 | true |
| controlled profile repeat | 3 | 3 | 0 | true |
| time-zero reference | 3 | 3 | 0 | true |

## Interpretation

The checksum preflight is achievable: when every ledger row has an accepted
status, a real path, a matching computed SHA-256 value, operator initials, and a
UTC timestamp, the run `169` preflight returns zero findings.

This is still not measured field evidence. The files in this run are generated
synthetic payloads and are only a validator smoke test.

## Decision

Use this only to verify the checksum-ledger gate mechanics. Keep provenance
acceptance, structural rerun, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training blocked until the real controlled-collection files fill
the ledger and pass the same preflight.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_checksum_ledger_preflight_smoke.py
1 passed
```

Figure check:

```text
1744x774, dynamic range=255
```
