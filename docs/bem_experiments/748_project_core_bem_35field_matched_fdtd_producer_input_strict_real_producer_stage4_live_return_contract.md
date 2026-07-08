# BEM Experiment 748: Strict Real-Producer Stage-4 Live Return Contract

Date: 2026-07-01

## Purpose

Define the exact live return contract for replacing the stage-4 midband
receiver matrix with real producer files.

This run extends the stage-3 live contract from run `747`. It does not create
real FDTD evidence, accept live producer files, run FDTD, run 3D validation,
launch GPU/HPC work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/748_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage4_live_return_contract
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage4_live_return_contract_contract_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage4_live_return_contract_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage4_live_return_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract files:                    2
contract rows:                     240
stage-4 live parents present:      2
stage-4 live files present:        0
stage-4 receiver-frequency pairs:  120
stage-4 receiver count:            30
stage-4 frequency count:           4
full strict file rows required:    558
strict acceptance ready:           false
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

Expected live stage-4 files:

```text
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_input_files/fdtd_source_hash_manifest_stage4_real_input.csv
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_input_files/fdtd_scattered_norm_values_stage4_real_input.csv
```

The four stage-4 frequencies are:

```text
0.75, 1.25, 1.5, and 2.0 GHz
```

The stage-4 receiver indices are:

```text
0 through 14 and 16 through 30
```

The center receiver `15` is excluded because it is covered by the stage-1 and
stage-2 center-receiver returns.

## Interpretation

The real stage-4 replacement is now exact: two 120-row files for the midband
receiver matrix. The source-hash manifest must return lowercase 64-character
source hashes. The scattered-norm file must return positive finite scattered
norms. Both files also require solver run identifier, solver status, solver log
hash, and real FDTD export flag for each row.

No live stage-4 files are present yet.

## Decision

Use this contract for the fourth real BEM/FDTD producer return after the
center-pair, center-receiver frequency-sweep, and center-frequency
receiver-sweep returns. Keep full strict acceptance, real BEM/FDTD comparison,
3D validation, GPU/HPC work, field transfer, and field FWI blocked until the
complete live producer files are returned and strict-accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage4_live_return_contract.py
3 passed
```

Figure check:

```text
1852x844, dynamic range=255
```
