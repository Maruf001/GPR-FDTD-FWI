# BEM Experiment 720: Producer Input Strict Contract-Hash Guard Prototype

Date: 2026-07-01

## Purpose

Prototype an exact contract-hash guard for the matched-FDTD producer input
files.

Run `717` showed that the current exporter accepts an arbitrary valid-looking
64-character contract hash. This run implements the stricter rule in a
prototype path: the producer row must carry the exact canonical hash for its
file-level input contract.

This is CPU-only guard prototyping. It does not run FDTD, execute the shared
exporter on real files, create accepted return files, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/720_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_probe_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype.png
scripts/script_snapshot_manifest.json
```

## Result

```text
producer input file keys:              2
required producer rows:              558
probe cases:                           8
current exporter pass cases:           4
strict guard pass cases:               2
strict guard fail cases:               6
canonical hashes accepted:             2
arbitrary hashes rejected:             2
blank or non-hex hashes rejected:      4
ready for shared exporter patch:    true
exporter execution ready:          false
real BEM/FDTD comparison ready:     false
GPU/HPC ready:                     false
```

## Interpretation

The prototype closes the exact gap identified in run `717`: canonical hashes
pass, while arbitrary hex hashes no longer pass.

## Decision

Use this prototype as the immediate basis for a guarded shared-exporter patch.
Do not accept real producer returns until the shared acceptance path is
hardened and validated.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype.py
3 passed
```

Figure check:

```text
2284x847, dynamic range=255
```
