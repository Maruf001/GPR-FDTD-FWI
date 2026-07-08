# BEM Experiment 096: Grid-Aware Layered Payload Smoke

Date: 2026-06-25

## Purpose

Execute the layered payload smoke requested by run `095`.

Run `095` established that the homogeneous grid-aware adapter path and the
scalar Sommerfeld layered proxy both have passing prerequisite evidence. This
run emits the actual layered adapter payload arrays and checks the all-scan and
leave-one-scan gates on the base epsr-9 layered case.

This is CPU-only. It runs project-core 2D FDTD target/background traces and
layered target-cell field recordings for the payload. It does not use field
data, GPU kernels, FWI, 3D/HPC work, neural-network training, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/096_project_core_grid_aware_layered_payload_smoke
```

Key artifacts:

```text
data/project_core_grid_aware_layered_payload_smoke_summary.json
data/project_core_grid_aware_layered_payload_smoke_arrays.npz
data/project_core_grid_aware_layered_payload_shapes.csv
data/project_core_grid_aware_layered_payload_interface_validation.csv
data/project_core_grid_aware_layered_payload_all_scan_metrics.csv
data/project_core_grid_aware_layered_payload_leave_one_metrics.csv
data/project_core_grid_aware_layered_payload_frequency_scales.csv
figures/project_core_grid_aware_layered_payload_smoke.png
docs/PROJECT_CORE_GRID_AWARE_LAYERED_PAYLOAD_SMOKE.md
scripts/run_project_core_grid_aware_layered_payload_smoke.py
scripts/test_project_core_grid_aware_layered_payload_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
case:                                base_epsr9
interface z:                         0.04 m
lower epsr:                          6.0
lower sigma:                         0.01 S/m
target center:                       x=0.13 m, z=0.09 m
target radius:                       0.025 m
target epsr:                         9.0
target cells:                        533
surface samples:                     19
selected frequency bins:             17
Tx field shape:                      5 x 533 x 17
Rx field shape:                      5 x 533 x 17
adapter output shape:                5 x 17
interface items present:             12 / 12
field leave-one-x L2:                0.3928483810786592
best all-scan variant:               product_div_source
best all-scan L2:                    0.5236861579717635
best leave-one-scan variant:         product_no_div
best leave-one-scan L2:              0.6497571611891657
layered payload smoke ready:         true
ready for layered stress replay:     true
ready for half-space promotion:      false
ready for outputs/experiments promo: false
ready for field transfer:            false
ready for 3D validation:             false
ready for GPU work:                  false
```

Payload arrays include:

```text
reference_layered_surface        19 x 533 x 17
proxy_layered_surface            19 x 533 x 17
fitted_layered_surface           19 x 533 x 17
leave_one_layered_surface        19 x 533 x 17
tx_background_field_at_cells      5 x 533 x 17
rx_background_field_at_cells      5 x 533 x 17
adapter_output_frequency_bins     5 x 17
fdtd_scattered_frequency_bins     5 x 17
adapter_band                      5 x 1885
fdtd_band                         5 x 1885
```

Gate metrics:

| Variant | All-scan L2 | Leave-one-scan L2 | Ready |
| --- | ---: | ---: | --- |
| product_div_source | 0.5236861579717635 | 0.6497571611891657 | true |
| product_no_div | 0.5236861579717637 | 0.6497571611891657 | true |
| receiver_conjugate_div_source | 1.0557772249492456 | 1.302927555077259 | false |

## Interpretation

The run `095` layered contract is now executable. The payload contains the
layer/interface metadata, target cells, target weights, scalar Sommerfeld
proxy surfaces, fitted and leave-one surfaces, scan-level Tx/Rx target-cell
fields, frequency-bin adapter output, and the band-limited comparison against
project-core FDTD.

This closes the layered payload-smoke gap. It does not promote measured-field,
3D, GPU, FWI, or historical `outputs/experiments` claims.

## Decision

Use this as the layered payload smoke checkpoint. The next duplicated-script
branch can replay or stress the layered payload, but promotion remains blocked
until that stress branch passes.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test:

```text
scripts/run_project_core_grid_aware_layered_payload_smoke.py
scripts/test_project_core_grid_aware_layered_payload_smoke.py
scripts/script_snapshot_manifest.json
```

Recorded SHA-256 values:

```text
run_project_core_grid_aware_layered_payload_smoke.py
600361bb3c9200ef9d4cc8eb0efcae7948f9f6cd24cd433011edce9499d9a6f5

test_project_core_grid_aware_layered_payload_smoke.py
e83cab13b30253cd553e00174f1696ff2e872eae2eeffaa3ede0e230895e5e1e
```

## Validation

Focused tests:

```text
tests/test_project_core_grid_aware_layered_payload_smoke.py
3 passed
```

Figure check:

```text
project_core_grid_aware_layered_payload_smoke.png  2572x716, dynamic range=255
```
