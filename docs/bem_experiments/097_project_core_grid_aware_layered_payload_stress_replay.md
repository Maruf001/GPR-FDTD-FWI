# BEM Experiment 097: Grid-Aware Layered Payload Stress Replay

Date: 2026-06-25

## Purpose

Replay the run `096` layered payload interface across the four fresh layered
stress cases used by the scalar Sommerfeld proxy ladder.

Run `096` emitted the actual layered payload arrays for the base epsr-9 case.
This run asks whether the same executable payload interface survives the
fresh-case layered stress envelope before the BEM replacement contract is
refreshed.

This is CPU-only. It runs project-core 2D FDTD target/background traces and
layered target-cell field recordings. It does not use field data, GPU kernels,
FWI, 3D/HPC work, neural-network training, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/097_project_core_grid_aware_layered_payload_stress_replay
```

Key artifacts:

```text
data/project_core_grid_aware_layered_payload_stress_replay_summary.json
data/project_core_grid_aware_layered_payload_stress_cases.csv
data/project_core_grid_aware_layered_payload_stress_all_scan_metrics.csv
data/project_core_grid_aware_layered_payload_stress_leave_one_metrics.csv
data/project_core_grid_aware_layered_payload_stress_worst_payload_arrays.npz
data/project_core_grid_aware_layered_payload_stress_worst_payload_shapes.csv
figures/project_core_grid_aware_layered_payload_stress_replay.png
docs/PROJECT_CORE_GRID_AWARE_LAYERED_PAYLOAD_STRESS_REPLAY.md
scripts/run_project_core_grid_aware_layered_payload_stress_replay.py
scripts/test_project_core_grid_aware_layered_payload_stress_replay.py
scripts/script_snapshot_manifest.json
```

## Result

```text
case count:                         4
passed cases:                       4
failed cases:                       0
worst case:                         base_epsr9
worst leave-one-scan L2:            0.6497571611891657
layered payload stress ready:       true
ready for layered contract refresh: true
ready for half-space promotion:     false
ready for outputs/experiments promo: false
ready for field transfer:           false
ready for 3D validation:            false
ready for GPU work:                 false
```

Case metrics:

| Case | epsr | x m | z m | Target cells | Best all-scan L2 | Best leave-one L2 | Ready |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| base_epsr9 | 9.0 | 0.13 | 0.09 | 533 | 0.5236861579717635 | 0.6497571611891657 | true |
| left_shift_epsr9 | 9.0 | 0.11 | 0.09 | 533 | 0.5291768105847588 | 0.6274272306214017 | true |
| deep_z_epsr9 | 9.0 | 0.13 | 0.11 | 533 | 0.47886263348109803 | 0.5830498205741614 | true |
| high_contrast_epsr12 | 12.0 | 0.13 | 0.09 | 533 | 0.4958414526878226 | 0.6201923660960406 | true |

The worst-case saved payload keeps the same interface shapes as run `096`,
including:

```text
reference_layered_surface        19 x 533 x 17
proxy_layered_surface            19 x 533 x 17
fitted_layered_surface           19 x 533 x 17
leave_one_layered_surface        19 x 533 x 17
tx_background_field_at_cells      5 x 533 x 17
rx_background_field_at_cells      5 x 533 x 17
adapter_output_frequency_bins     5 x 17
adapter_band                      5 x 1885
fdtd_band                         5 x 1885
```

## Interpretation

The executable layered payload interface survives the fresh layered stress
envelope. This ties the older run `066` Sommerfeld proxy stress evidence to the
new run `096` saved payload arrays.

This is still a scoped local 2D/project-core result. It does not promote
measured-field, 3D, GPU, FWI, or historical `outputs/experiments` claims.

## Decision

Use this as the layered payload stress checkpoint. The next duplicated-script
branch should refresh the BEM replacement contract around the new payload
artifacts while keeping higher-level promotions blocked.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test:

```text
scripts/run_project_core_grid_aware_layered_payload_stress_replay.py
scripts/test_project_core_grid_aware_layered_payload_stress_replay.py
scripts/script_snapshot_manifest.json
```

Recorded SHA-256 values:

```text
run_project_core_grid_aware_layered_payload_stress_replay.py
0097f37d35d03a2d91ef9b303a792951514444c884851ee9869a5c23609b0fb9

test_project_core_grid_aware_layered_payload_stress_replay.py
3b12e52e7b62263265a661dfe42f0ba2281bd60476e28724cc953be3f8618694
```

## Validation

Focused tests:

```text
tests/test_project_core_grid_aware_layered_payload_stress_replay.py
2 passed
```

Figure check:

```text
project_core_grid_aware_layered_payload_stress_replay.png  2572x721, dynamic range=255
```
