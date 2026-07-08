# BEM Experiment 745: Strict Real-Producer Stage-1 Live Return Contract

Date: 2026-07-01

## Purpose

Define the exact live return contract for replacing the stage-1 synthetic smoke
from run `744` with real producer files.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/745_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_live_return_contract
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_live_return_contract_contract_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_live_return_contract_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_live_return_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract files:                    2
contract rows:                     2
stage-1 live parents present:      2
stage-1 live files present:        0
stage-1 receiver-frequency pairs:  1
stage-1 receiver index:            15
stage-1 frequency:                 1.0 GHz
full strict file rows required:    558
strict acceptance ready:           false
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

Expected live stage-1 files:

```text
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_input_files/fdtd_source_hash_manifest_stage1_real_input.csv
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_input_files/fdtd_scattered_norm_values_stage1_real_input.csv
```

## Interpretation

The real stage-1 replacement is now exact: two one-row files, both at receiver
index `15` and `1.0 GHz`. The first file must return a lowercase 64-character
source hash; the second must return a positive finite scattered norm. Both
also require solver run identifier, solver status, solver log hash, and real
FDTD export flag.

No live stage-1 files are present yet.

## Decision

Use this contract for the first real BEM/FDTD producer return. Keep full strict
acceptance, real BEM/FDTD comparison, 3D validation, GPU/HPC work, field
transfer, and field FWI blocked until full live producer files are returned and
strict-accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_live_return_contract.py
3 passed
```

Figure check:

```text
1744x844, dynamic range=255
```
