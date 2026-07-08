# GSSI 51600S Crossline Metadata Refresh Checkpoint

## Scope

- Rechecked the trusted GSSI 51600S local data folder after adding the measured-geometry planner.
- Confirmed the local folder contains only four DZT/DZX pairs and no separate survey-note CSV, JSON, TXT, or route file.
- Inspected the DZX sidecars directly and reran the provenance audit.

## Result

- DZX file count: `4`
- Along-scan spacing is present:
  - `unitsPerScan = 0.003333 m`
  - `scanPerMeters = 300`
- Crossline waypoint coordinates are not present:
  - every DZX waypoint y value is `0.0`
  - `crossline_waypoint_coordinates_present = false`
- Decision remains:
  `crossline_spacing_not_metadata_confirmed`

## Artifact

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/123_gssi51600s_crossline_spacing_provenance_refresh_after_geometry_planner`

## Interpretation

The local GSSI metadata confirms along-scan sampling but not spacing between the four profile files. The current predictor should therefore continue to treat y position and finite length as geometry-conditioned unless the crossline profile coordinates are supplied or explicitly estimated by the optimizer.

## Validation

- `python -m pytest tests/test_gssi51600s_crossline_spacing_provenance_audit.py -q`
- Result: `3 passed in 0.29s`

## Next Step

Use the measured-geometry planner if real profile positions become available. If not, the next product-facing path is to make the optimizer-estimated spacing/offset posterior more explicit in the predictor output without calling it measured metadata.
