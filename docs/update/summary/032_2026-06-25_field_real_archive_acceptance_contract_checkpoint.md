# Field Real Archive Acceptance Contract Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the field-side continuation after the grid-aware BEM
payload milestone. No field FWI, heavy GPU work, field 3D/HPC work, or neural-
network training was launched.

The result is a field-operation acceptance contract, not measured field
evidence.

## New Field Run

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/176_gssi51600s_controlled_collection_real_archive_acceptance_contract
```

Tracked note:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/176_gssi51600s_controlled_collection_real_archive_acceptance_contract.md
```

The run consolidates the field-side controlled-collection chain from runs
`163-175` into one real-archive acceptance contract.

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

## Interpretation

The field process is now designed through archive layout, intake manifest,
checksum ledger, operator handoff, archive preflight, and archive-to-ledger
integration smoke.

The remaining blocker is real evidence acquisition. The current archive cannot
be promoted by relabeling. A real collection must provide 11 measured metadata
values, nine measured files, six metadata artifacts, matching SHA-256 checksums,
and successful structural/provenance reruns.

## Current Decision

Use run `176` as the active real-archive acceptance contract. Do not launch
measured-field claims, field FWI, heavy GPU work, field 3D/HPC, or neural-
network training until a real archive passes the archive, checksum, intake,
structural, and provenance gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_archive_acceptance_contract.py
2 passed
```

Compile check:

```text
run_gssi_field_controlled_collection_real_archive_acceptance_contract.py: pass
tests/test_gssi_field_controlled_collection_real_archive_acceptance_contract.py: pass
```

Figure check:

```text
2140x769, dynamic range=255
```

Script snapshot manifest:

```text
run_gssi_field_controlled_collection_real_archive_acceptance_contract.py
sha256=3e1d2a94fc8d0e58025b382420c246b2f452001ae1d767c1d4ea3c69fbeab3c3

test_gssi_field_controlled_collection_real_archive_acceptance_contract.py
sha256=5823e111e49d40a314c7f414f3d8511b7c31488ed39d1887188db330627657c8
```

Whitespace check:

```text
git diff --check: pass
```

## Next Marathon Branch

The marathon remains active. Since the field side is blocked on real collection
rather than computation, the next defensible work should move to one of:

```text
1. presentation/report refresh around the BEM payload and field acceptance contract;
2. synthetic 2D claim-boundary or next-hypothesis audit;
3. tooling that reduces repeated manual validation across BEM/field outputs.
```
