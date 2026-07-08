# BEM Experiment 331: Project-Grid Adapter Interface Evolution Audit

Date: 2026-06-28

## Purpose

Audit how the original run `037` seven-item BEM/project-grid adapter contract
became the later run `092` and run `093` eight-item reusable grid-aware payload
interface.

This run answers a narrow implementation question:

```text
What exactly changed between the first adapter contract and the later payload
interface, and did the executable smoke emit every later interface item?
```

This is an artifact audit. It does not run FDTD, GPU/HPC work, field data,
field FWI, neural-network training, or synthetic 2D archive promotion.

## Output

```text
outputs/bem_experiments/331_project_core_bem_project_grid_adapter_interface_evolution_audit
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_interface_evolution_audit_mapping.csv
data/project_core_bem_project_grid_adapter_interface_evolution_audit_validation_checks.csv
data/project_core_bem_project_grid_adapter_interface_evolution_audit_summary.json
figures/project_core_bem_project_grid_adapter_interface_evolution_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
old interface items:              7
new interface items:              8
run 093 emitted items:            8
mapped old items:                 7
retained items:                   5
tightened items:                  2
new payload-output items:         1
validation checks:                7
passed checks:                    7
failed checks:                    0
interface evolution ready:        true
field claim ready:                false
3D validation ready:              false
GPU work ready:                   false
field FWI ready:                  false
```

The interface evolution is:

| Old item | New item | Evolution |
| --- | --- | --- |
| `project_grid_target_cells` | `project_grid_target_cells` | retained |
| `target_cell_weights` | `target_cell_weights` | retained |
| `tx_background_field_at_cells` | `tx_background_field_at_cells` | retained |
| `rx_background_field_at_cells` | `rx_background_field_at_cells` | retained |
| `source_spectrum` | `source_spectrum` | retained |
| `scattering_formula_variants` | `grid_aware_scattering_formula` | tightened |
| `per_frequency_complex_scale` | `per_frequency_complex_scale_policy` | tightened |
| none | `adapter_output_frequency_bins` | new payload output |

## Interpretation

The first adapter contract was not discarded. Five physical payload items are
retained directly, two items are tightened into explicit grid-aware formula and
controlled calibration-policy items, and one new output item makes the adapter
responsible for emitting comparator-ready complex frequency-bin predictions.

Run `093` emits all eight later interface items:

```text
target cells:          753
target weights:        753
Tx fields:             7 x 753 x 17
Rx fields:             7 x 753 x 17
source spectrum:       17
formula output:        7 x 17
scale policy:          17
adapter output bins:   7 x 17
```

## Decision

Use run `331` as the interface-evolution map for future BEM adapter
implementation work. Continue only inside controlled BEM/FDTD payload gates
until field, historical-archive, 3D, GPU, and field-FWI prerequisites are
actually satisfied.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_interface_evolution_audit.py
4 passed
```

Figure validation:

```text
3328x901, dynamic range=255
```
