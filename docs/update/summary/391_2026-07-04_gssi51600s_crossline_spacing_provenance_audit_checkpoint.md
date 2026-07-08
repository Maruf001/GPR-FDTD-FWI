# GSSI51600S Crossline Spacing Provenance Audit Checkpoint

## What Changed

- Added `run_gssi51600s_crossline_spacing_provenance_audit.py`.
- Added unit tests for DZX parsing and crossline-spacing provenance classification.
- Generated a GSSI51600S metadata audit artifact for the four trusted field profiles.
- Confirmed that the current GSSI sidecars support along-scan spacing but do not metadata-confirm the profile-to-profile crossline spacing.

## Key Numbers

- Artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/085_gssi51600s_crossline_spacing_provenance_audit_current/`.
- Decision: `crossline_spacing_not_metadata_confirmed`.
- DZX file count: `4`.
- Along-scan `unitsPerScan`: `0.003333 m`.
- Along-scan `scanPerMeters`: `300.0`.
- Waypoint y coordinates: all `0.0`.
- Crossline spacing metadata status: `absent_not_metadata_confirmed`.

## Current Decision

The strict GSSI product track remains blocked on `crossline_y_geometry_confirmed`. The assumption-conditioned prediction track remains valid as a clearly labeled field-data estimate, because the 3D y position and finite length are tied to an explicit y-spacing assumption rather than measured sidecar metadata.

## Validation

- `python -m pytest tests/test_gssi51600s_crossline_spacing_provenance_audit.py -q` passed with `3 passed`.
- `python -m py_compile run_gssi51600s_crossline_spacing_provenance_audit.py` passed.
- The generated summary reports `crossline_spacing_not_metadata_confirmed` and records the DZX-derived along-scan spacing values.

## Next Defensible Task

Keep the GSSI 51600S predictor as the release-facing path, search for an external source of the true profile spacing or reconstruct it from acquisition notes, and only use the public 2025 dataset's rebar subset after a separate importer verifies that its files are actually from the rebar class.

The local marathon request remains active.
