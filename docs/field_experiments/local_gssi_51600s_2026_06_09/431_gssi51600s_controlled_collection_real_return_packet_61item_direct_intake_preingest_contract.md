# Field Experiment 431: Direct Intake Pre-Ingest Contract

Date: 2026-06-30

## Purpose

Convert the latest 33 direct staging paths into a strict pre-ingest contract.

Run `425` listed the required direct input paths, and runs `428-430` folded
that staging manifest into the field claim boundary. This run adds the
machine-checkable layer immediately before parser/provenance reruns: required
directories, required file extensions, DZT signature checks, JSON parse checks,
SHA-256 requirements, and current filesystem state.

This is a field-side contract run only. It does not create placeholder field
files, ingest real DZT data, accept measured evidence, run field FWI, launch
3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/431_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_preingest_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_directory_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
pre-ingest contract ready:                true
pre-ingest rows:                          33
required directories:                     5
present directories:                      0
actions:                                  6
measured DZT rows:                        9
global metadata JSON rows:                15
file metadata JSON rows:                  9
expected extension failures:              0
current files present:                    0
current SHA-256 records present:          0
DZT signature checks required:            9
JSON parse checks required:               24
template/synthetic substitutions allowed: 0
pre-ingest accepted rows:                 0
real packet files present:                false
real packet accepted:                     false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
```

The six ordered actions are:

| Priority | Action | Required | Currently complete |
| ---: | --- | ---: | ---: |
| 1 | create required staging directories | 5 | 0 |
| 2 | copy measured DZT files | 9 | 0 |
| 3 | write global metadata JSON files | 15 | 0 |
| 4 | write per-file metadata JSON files | 9 | 0 |
| 5 | run pre-ingest existence, extension, checksum, DZT, and JSON checks | 33 | 0 |
| 6 | rerun parser, provenance gate, and archive acceptance | 33 | 0 |

## Interpretation

The field-side blocker is now more concrete than "missing files." The project
has exact paths and exact pre-ingest checks for every direct input:

```text
9 DZT files require DZT signature checks and SHA-256 records.
24 metadata JSON files require JSON parsing and SHA-256 records.
No template or synthetic substitution is allowed.
```

No current file can be promoted. The staging root is still empty, and all
evidence, provenance, archive, FWI, and 3D/HPC states remain blocked.

## Decision

Use run `431` as the current field-side pre-ingest contract before any parser,
provenance, archive, field FWI, or field 3D/HPC rerun from field inputs.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract.py
5 passed
```

Figure check:

```text
2645x846, dynamic range=255
```
