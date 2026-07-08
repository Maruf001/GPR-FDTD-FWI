# BEM Experiment 826: Complex FDTD Adapter Input Stage-1 Positive Control Smoke

Date: 2026-07-01

## Purpose

Exercise the first staged complex FDTD handoff packet from run `823` with an
output-local synthetic positive control.

This run fills only the stage-1 one-row packet with finite real and imaginary
FDTD values and valid-looking provenance so the row-level adapter validator can
exercise its positive path. It does not write to the external return path and
does not create real BEM/FDTD evidence.

## Output

```text
outputs/bem_experiments/826_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke
```

Key artifacts:

```text
data/stage1_positive_control/stage01_only_complex_fdtd_input_positive_control.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke_validation_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staged packet ready:        true
positive-control files:            1
positive-control rows:             1
accepted stage-1 rows:             1
rejected stage-1 rows:             0
full required rows:                279
stage-1 fraction of full input:    0.003584
external input file present:       false
synthetic positive control only:   true
full input valid:                  false
accepted as real external input:   false
completed stage files ready:       false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
```

## Interpretation

The one-row stage-1 packet can be populated with finite complex FDTD values and
pass row-level adapter validation. This proves the smallest staged packet is
mechanically usable.

The result is not evidence. It covers only one of the 279 required
receiver-frequency identities and uses output-local synthetic values.

## Decision

Use this run as positive-control coverage for the staged complex-input path.
Keep full external input acceptance, completed stage files, real comparison,
field transfer, and 3D/HPC blocked until real FDTD values cover the full
guarded input.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke.py
2 passed
```

Figure check:

```text
2644x919, dynamic range=255
```
