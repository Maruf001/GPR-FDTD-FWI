# Field Prediction Multi-Stack Transfer Readiness Checkpoint

## What changed
- Parameterized the real RD3 stack manifest builder so it can ingest field groups beyond `0701` while preserving the existing `0701` default.
- Expanded the RAD metadata audit target list to include `Data Set/pipe/07011/ASCII`.
- Extended transfer readiness so extra real stack summaries can be included as `dataset=path`.
- Built new real 3D stack artifacts from `data/2025-01-13_GPR_Dataset/Data Set.zip`:
  - `262_field_3d_0704_stack_manifest`
  - `263_field_3d_0806_stack_manifest`
  - `264_field_3d_07011_stack_manifest`
- Built updated product readiness:
  - `068_field_prediction_transfer_readiness_with_extra_field_stacks`

## Key numbers
- `external_2025_pipe_0701`: ready, stack shape `38 x 479 x 740`, time range `187.109 ns`.
- `external_2025_pipe_0704`: ready, stack shape `15 x 484 x 224`, time range `189.0625 ns`.
- `external_2025_pipe_0806`: ready, stack shape `8 x 486 x 902`, time range `189.84375 ns`.
- `external_2025_pipe_07011`: ready, stack shape `8 x 512 x 179`, time range `200.0 ns`.
- `gssi51600s`: still limited for this finite-length 3D predictor, stack shape `4 x 510 x 274`, time range `5.0 ns`.

## Current decision
`transfer_readiness_current_3d_predictor_has_multiple_real_3d_stacks_ready`.

This is product-relevant: the current finite-length 3D predictor is no longer a single-stack-only pipeline. It now has multiple real field stacks available for transfer tests.

## What remains blocked
- Y spacing is still an assumption label, not measured survey geometry.
- The new stacks are intake-ready, but the optimizer has not yet been run on them.
- Diameter remains a near-best range in the current `0701` release candidate; no unique scalar diameter claim should be made yet.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_prediction_transfer_readiness.py -q`: `18 passed`.
- Broader product/intake focused suite: `23 passed`.
- `python -m py_compile run_field_3d_rad_grid_metadata_audit.py run_field_3d_0701_stack_manifest.py run_field_prediction_transfer_readiness.py`: passed.
- `git diff --check` on touched files: passed.
- GPU was lightly loaded at branch start; no heavy optimizer was launched in this branch.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/261_field_3d_rad_grid_metadata_audit_with_transfer_groups`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/262_field_3d_0704_stack_manifest`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/263_field_3d_0806_stack_manifest`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/264_field_3d_07011_stack_manifest`
- `outputs/validation_exp_on_field_data/product_leaderboard/068_field_prediction_transfer_readiness_with_extra_field_stacks`

## Next defensible task
Adapt the finite-length Fast-GPR optimizer/product configuration so one of the new ready stacks can be fit directly. Prefer `0704` first because it has 15 profiles and moderate trace count, then run a bounded AdamW/Adamax comparison on the real receiver-mean scattered objective.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
