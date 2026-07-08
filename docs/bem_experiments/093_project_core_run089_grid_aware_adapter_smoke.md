# BEM Experiment 093: Project-Core Run089 Grid-Aware Adapter Smoke

Date: 2026-06-25

## Purpose

Instantiate the run `092` adapter contract on the run `089` geometry and emit
the full project-grid adapter payload.

Run `092` defined the eight required interface quantities. This smoke run
checks that they can be produced as real arrays and that the resulting
frequency-bin adapter output reproduces the accepted run `091` grid-aware
scattering gate.

This is a CPU-only smoke. It reruns the small project-core FDTD background
target-field recordings needed to populate the Tx/Rx target-cell fields. It
does not use GPU kernels, field data, field FWI, 3D/HPC work, neural-network
training, or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/093_project_core_run089_grid_aware_adapter_smoke
```

Key artifacts:

```text
data/project_core_run089_grid_aware_adapter_smoke_summary.json
data/project_core_run089_grid_aware_adapter_payload.npz
data/project_core_run089_grid_aware_adapter_payload_shapes.csv
data/project_core_run089_grid_aware_adapter_interface_validation.csv
data/project_core_run089_grid_aware_adapter_variant_metrics.csv
data/project_core_run089_grid_aware_adapter_frequency_scales.csv
figures/project_core_run089_grid_aware_adapter_smoke.png
docs/PROJECT_CORE_RUN089_GRID_AWARE_ADAPTER_SMOKE.md
scripts/run_project_core_run089_grid_aware_adapter_smoke.py
scripts/test_project_core_run089_grid_aware_adapter_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
target cells:                         753
target weight sum:                    0.008474879999999999
selected frequency bins:              17
Tx field shape:                       7 x 753 x 17
Rx field shape:                       7 x 753 x 17
adapter output frequency shape:       7 x 17
interface items present:              8 / 8
best variant:                         receiver_conjugate_div_source
best time symmetric L2:               0.5800814918790826
best spectral symmetric L2:           0.5800814918790829
run 091 reference L2:                 0.5800814918790829
reproduces run 091 gate:              true
adapter smoke ready:                  true
ready for fresh-case stress:          true
ready for half-space promotion:       false
ready for outputs/experiments promo:  false
ready for field transfer:             false
ready for 3D validation:              false
ready for GPU work:                   false
```

The payload now contains:

```text
target_iz, target_ix, target_x_m, target_z_m
target_weights
tx_background_field_at_cells
rx_background_field_at_cells
source_spectrum
adapter_output_frequency_bins
fdtd_scattered_frequency_bins
adapter_band
fdtd_band
```

## Interpretation

The run `092` contract is executable on the run `089` geometry. This closes the
immediate adapter-schema gap: the run `091` positive result is no longer only a
script-internal computation; it is now a saved adapter payload with explicit
interface arrays and validation tables.

This does not promote the continuous analytic-cylinder bridge. It also does
not promote half-space, field, historical `outputs/experiments`, 3D, GPU, or
FWI work. It only permits a fresh-case stress branch of the reusable adapter.

## Decision

Use this smoke payload as the reusable BEM/project-core adapter checkpoint.
The next duplicated-script branch should stress this adapter on fresh matched
geometries or material contrasts before any broader promotion.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test:

```text
scripts/run_project_core_run089_grid_aware_adapter_smoke.py
scripts/test_project_core_run089_grid_aware_adapter_smoke.py
scripts/script_snapshot_manifest.json
```

Recorded SHA-256 values:

```text
run_project_core_run089_grid_aware_adapter_smoke.py
65f8eb953a44379094e7554d11914c4b4f446f9292764d4f1a5c2afccfe7a38f

test_project_core_run089_grid_aware_adapter_smoke.py
0d371378cccb75cc61ffc955dafb029f3489892518bb2454eaae79ad0dd66da3
```

## Validation

Focused tests:

```text
tests/test_project_core_run089_grid_aware_adapter_smoke.py
2 passed
```

Figure check:

```text
project_core_run089_grid_aware_adapter_smoke.png  2590x734, dynamic range=255
```
