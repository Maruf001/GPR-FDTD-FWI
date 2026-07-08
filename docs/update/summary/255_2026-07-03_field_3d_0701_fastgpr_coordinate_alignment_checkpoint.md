# 255 2026-07-03 Field 3D 0701 Fast-GPR Coordinate Alignment Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_coordinate_alignment_audit.py`.
- Added focused tests in `tests/test_field_3d_0701_fastgpr_coordinate_alignment_audit.py`.
- Generated artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/017_field_3d_0701_fastgpr_coordinate_alignment_audit/`.
- Quantified why runs `014-016` are useful optimizer/interface smokes but not yet physically meaningful field geometry fits.

## Method

The audit compares the run `007` field stack coordinates against the run `014`
Fast-GPR bridge config:

- field trace spacing and current bridge receiver aperture
- local contiguous field trace aperture
- source motion
- field sample interval vs Fast-GPR `dt`
- field window time span vs Fast-GPR time span
- field sample-window start vs Fast-GPR zero-time start

## Key Numbers

| axis | field value | Fast-GPR value | field/Fast-GPR | status |
| --- | ---: | ---: | ---: | --- |
| current x receiver aperture | `18.9184 m` | `0.75 m` | `25.2245` | mismatch |
| local contiguous x window | `0.384 m` | `0.75 m` | `0.5120` | compatible if local traces are used |
| source motion | `0.15 m` | `0.15 m` | `1.0` | bridge-internal only |
| time sample interval | `0.390625 ns` | `0.1 ns` | `3.90625` | mismatch |
| time window span | `11.718748 ns` | `3.0 ns` | `3.90625` | mismatch |
| time window start | `15.624998 ns` | `0.0 ns` | `inf` | missing time-zero alignment |

## Current Decision

`field_3d_0701_fastgpr_bridge_coordinate_alignment_blocked_current_window`

The Fast-GPR bridge is shape-compatible but not coordinate-compatible with the
current field window. The tiny optimizer losses in runs `014-016` are therefore
optimizer-coupling diagnostics, not physical geometry-fitting evidence.

## Claim Boundary

Do not use runs `014-016` to claim rebar x/y/z/radius/length. They prove that
Fast-GPR can ingest a real field-window-shaped tensor and backpropagate. They do
not yet prove that the modeled acquisition coordinates match the field survey.

## Immediate Fix Direction

The next bridge should use:

- a local contiguous field trace window, not `linspace` over the full profile;
- Fast-GPR `dt` or field resampling chosen so the time intervals match;
- explicit time-zero/window offset handling before comparing waveforms;
- then rerun the scalar/anomaly optimizer and compare loss decrease against
  runs `015-016`.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_coordinate_alignment_audit.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_coordinate_alignment_audit.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_fastgpr_forward_smoke.py tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py tests/test_field_3d_0701_fastgpr_coordinate_alignment_audit.py -q`
- Focused project-env result: `44 passed`.
- Focused dev-env acceleration/optimizer/Fast-GPR result: `23 passed`.
- `git diff --check -- run_field_3d_0701_fastgpr_coordinate_alignment_audit.py tests/test_field_3d_0701_fastgpr_coordinate_alignment_audit.py`
- Figure check: `field_3d_0701_fastgpr_coordinate_alignment_audit.png` is `1804 x 801` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/017_field_3d_0701_fastgpr_coordinate_alignment_audit/data/field_3d_0701_fastgpr_coordinate_alignment_summary.json`
- Rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/017_field_3d_0701_fastgpr_coordinate_alignment_audit/data/field_3d_0701_fastgpr_coordinate_alignment_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/017_field_3d_0701_fastgpr_coordinate_alignment_audit/figures/field_3d_0701_fastgpr_coordinate_alignment_audit.png`

## Next Defensible Task

Build a corrected local-window Fast-GPR bridge using a contiguous field trace
window, matched/resampled time interval, and explicit time-zero offset. Then
rerun the scalar epsr optimizer to see whether the field loss decrease becomes
larger than the current `~1.5e-05` diagnostic changes.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.
