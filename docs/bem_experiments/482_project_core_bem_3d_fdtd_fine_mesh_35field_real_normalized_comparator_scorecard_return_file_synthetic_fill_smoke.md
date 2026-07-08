# BEM Experiment 482: Synthetic Return-File Fill Smoke

Date: 2026-06-29

## Purpose

Fill the four blank return-file templates from run `476` with deterministic
synthetic values and verify that they can be merged into the 35-field
normalized-comparator scorecard shape.

This is a parser and consumer smoke test only. The filled values are not real
BEM or FDTD returned data.

## Output

```text
outputs/bem_experiments/482_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_filled_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_scorecard_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_synthetic_return_file_hashes.csv
data/synthetic_return_files/
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source manifest ready:                         true
synthetic return-file fill smoke ready:         true
synthetic return files:                         4
filled synthetic entries:                       1116
source-hash entries:                            558
valid source-hash entries:                      558
scattered-norm entries:                         558
finite scattered-norm entries:                  558
merged scorecard rows:                          279
receiver count:                                 31
frequency count:                                9
mean synthetic normalized norm difference:      0.011899240440684099
max synthetic normalized norm difference:       0.017999697624207837
synthetic return values are evidence:           false
real return files present:                      false
real BEM/FDTD comparison ready:                 false
3D validation ready:                            false
GPU/HPC ready:                                  false
field transfer ready:                           false
field FWI ready:                                false
```

## Interpretation

The four-file return contract is internally consumable: the synthetic source
hashes and synthetic scattered-field norms can be parsed, grouped by
receiver-frequency row, and merged into a complete 279-row scorecard.

This does not validate any real BEM/FDTD agreement. It only validates the file
shape and downstream consumer path.

## Decision

Use this run as a synthetic consumer smoke for the four-file return contract.
Keep real comparison, 3D validation, GPU/HPC work, field transfer, and field
FWI blocked until the four files are filled with real returned values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke.py
4 passed
```

Figure check:

```text
3508x884, dynamic range=255
```
