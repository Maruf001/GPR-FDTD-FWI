# BEM Experiment 790: Complex Metric BEM Complex Component Partial Export

Date: 2026-07-01

## Purpose

Fill the BEM-side complex component fields for the five-stage complex-metric
BEM/FDTD return schema.

Runs `787-789` showed that accepted scalar BEM scattered norms cannot be
repackaged as complex fields. This run reruns the fine-mesh Bempp receiver
solve and exports the `scattered_ey` complex component into the same five-stage
receiver-frequency contract used by the FDTD return plan.

## Output

```text
outputs/bem_experiments/790_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export
```

Key artifacts:

```text
data/bem_complex_component_partial_stage_files/
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_frequency_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_partial_file_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source compatibility ready:                 true
source compatibility sensitivity ready:     true
source template pack ready:                 true
component:                                  scattered_ey
normalization label:                        raw_scattered_ey_component
frequencies solved:                         9
frequency failures:                         0
partial stage files:                        5
partial metric rows:                        279
finite BEM complex rows:                    279
BEM complex value cells filled:             558
FDTD value cells blank:                     558
FDTD provenance/status cells blank:         1395
normalization labels filled:                279
real FDTD-export flags true:                0
partial files passing preflight:            0
Bempp solve elapsed time:                   189.35 seconds
real BEM/FDTD comparison ready:             false
field transfer ready:                       false
3D/HPC ready:                               false
gpu priority:                               none
```

## Interpretation

The BEM side of the complex-metric packet is now real, not just a template. All
279 receiver-frequency rows have finite `bem_real` and `bem_imag` values for
the `scattered_ey` component.

The files remain partial. They intentionally leave `fdtd_real`, `fdtd_imag`,
FDTD source hash, solver ID, solver status, solver log hash, and real
FDTD-export flag blank. This prevents them from passing the real-return
preflight gate by themselves.

## Decision

Use run `790` as BEM-side complex-component evidence only. Do not stage these
partial files into the real BEM/FDTD intake path or promote comparison until
matched FDTD complex values and FDTD provenance/status fields are returned.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validation_sensitivity.py

10 passed
```

Figure check:

```text
2824x880, dynamic range=255
```
