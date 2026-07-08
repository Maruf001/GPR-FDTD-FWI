# BEM Experiment 746: Strict Real-Producer Stage-2 Live Return Contract

Date: 2026-07-01

## Purpose

Define the exact live return contract for replacing the stage-2 center-receiver
frequency sweep with real producer files.

This run extends the stage-1 live contract from run `745`. It does not create
real FDTD evidence, accept live producer files, run FDTD, run 3D validation,
launch GPU/HPC work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/746_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage2_live_return_contract
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage2_live_return_contract_contract_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage2_live_return_contract_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage2_live_return_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract files:                    2
contract rows:                     16
stage-2 live parents present:      2
stage-2 live files present:        0
stage-2 receiver-frequency pairs:  8
stage-2 receiver index:            15
stage-2 frequency count:           8
full strict file rows required:    558
strict acceptance ready:           false
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

Expected live stage-2 files:

```text
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_input_files/fdtd_source_hash_manifest_stage2_real_input.csv
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_input_files/fdtd_scattered_norm_values_stage2_real_input.csv
```

The eight stage-2 frequencies are:

```text
0.4, 0.5, 0.75, 1.25, 1.5, 2.0, 2.5, and 3.0 GHz
```

All rows use receiver index `15`.

## Interpretation

The real stage-2 replacement is now exact: two eight-row files for the center
receiver frequency sweep. The source-hash manifest must return lowercase
64-character source hashes. The scattered-norm file must return positive
finite scattered norms. Both files also require solver run identifier, solver
status, solver log hash, and real FDTD export flag for each row.

No live stage-2 files are present yet.

## Decision

Use this contract for the second real BEM/FDTD producer return after the
stage-1 center-pair smoke return. Keep full strict acceptance, real BEM/FDTD
comparison, 3D validation, GPU/HPC work, field transfer, and field FWI blocked
until the complete live producer files are returned and strict-accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage2_live_return_contract.py
3 passed
```

Figure check:

```text
1852x844, dynamic range=255
```
