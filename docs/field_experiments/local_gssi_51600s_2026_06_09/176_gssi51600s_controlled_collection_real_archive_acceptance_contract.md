# Field Experiment 176: Real Archive Acceptance Contract

Date: 2026-06-25

## Purpose

Consolidate the controlled-collection gates from runs `163`-`175` into one
real-archive acceptance contract.

This is a field-operation contract artifact. It does not create measured field
evidence, run DZT preprocessing, run FDTD/FWI, launch GPU work, or perform
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/176_gssi51600s_controlled_collection_real_archive_acceptance_contract
```

Key artifacts:

```text
data/field_controlled_collection_real_archive_acceptance_contract.csv
data/field_controlled_collection_real_archive_acceptance_contract_summary.json
figures/field_controlled_collection_real_archive_acceptance_contract.png
docs/FIELD_COLLECTION_REAL_ARCHIVE_ACCEPTANCE_CONTRACT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
contract stages:                         8
metadata values required:                11
real files required:                     9
controlled profile files required:       3
time-zero reference files required:       3
amplitude-reference files required:      3
archive directories required:            7
metadata artifacts required:             6
intake manifest current blockers:        89
checksum ledger current blockers:        45
archive preflight current blockers:      23
provenance current blockers:             42
synthetic archive-checksum bridge pass:  true
real archive acceptance ready:           false
scientific field claim ready:            false
structural validation rerun ready:        false
provenance acceptance ready:             false
field FWI ready:                         false
GPU work ready:                          false
field 3D/HPC ready:                      false
```

The eight contract stages are:

| Stage | Source run | Required items | Current blockers | Real acceptance ready |
| --- | --- | ---: | ---: | --- |
| provenance closure requirements | 163 | 6 | 42 | false |
| intake manifest template/preflight | 164-165 | 20 | 89 | false |
| checksum ledger template/preflight | 168-169 | 9 | 45 | false |
| archive layout/preflight | 171-173 | 15 | 23 | false |
| operator handoff | 172 | 8 | 0 | false |
| archive-checksum bridge smoke | 175 | 9 | 0 | false |
| structural and provenance rerun | 160-163 | 2 | 42 | false |
| field FWI/GPU/3D escalation | 176 | 0 | 1 | false |

## Interpretation

The field path is now operationally designed through archive layout, intake
manifest, checksum ledger, operator handoff, synthetic archive preflight, and
synthetic archive-to-ledger integration.

The blocker is not procedure design. The blocker is that the real archive has
not been filled. Real acceptance still requires 11 measured metadata values,
nine measured files, six metadata artifacts, matching SHA-256 checksums, and
successful structural/provenance reruns on the real archive.

## Decision

Use this run as the current real-archive acceptance contract. Do not launch
field FWI, heavy GPU work, field 3D/HPC, neural-network training, or measured
field scientific claims until a real archive passes the archive, checksum,
intake, structural, and provenance gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_archive_acceptance_contract.py
2 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_real_archive_acceptance_contract.py: pass
tests/test_gssi_field_controlled_collection_real_archive_acceptance_contract.py: pass
```

Figure check:

```text
2140x769, dynamic range=255
```

Script snapshots:

```text
run_gssi_field_controlled_collection_real_archive_acceptance_contract.py
sha256=3e1d2a94fc8d0e58025b382420c246b2f452001ae1d767c1d4ea3c69fbeab3c3

test_gssi_field_controlled_collection_real_archive_acceptance_contract.py
sha256=5823e111e49d40a314c7f414f3d8511b7c31488ed39d1887188db330627657c8
```
