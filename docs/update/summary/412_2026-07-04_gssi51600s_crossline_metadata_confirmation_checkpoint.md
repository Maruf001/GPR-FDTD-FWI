# 2026-07-04 GSSI 51600S Crossline Metadata Confirmation Checkpoint

## What changed

- Rechecked local GSSI sidecar metadata and nearby project notes for crossline/profile spacing information.
- Files inspected:
  - `data/2026-06-09_GSSI_model_51600S/PROJECT001C__013.DZX`
  - `data/2026-06-09_GSSI_model_51600S/PROJECT001C__014.DZX`
  - `data/2026-06-09_GSSI_model_51600S/PROJECT001C__015.DZX`
  - `data/2026-06-09_GSSI_model_51600S/PROJECT001C__016.DZX`
- Also checked the earlier 3D experiment plan sections around local GSSI metadata requirements.

## Key metadata facts

- All four DZX files report:
  - `unitsPerScan = 0.003333`
  - `scanPerMeters = 300.000000`
  - `gridId = Grid`
  - `samplesPerScan = 512`
  - `dielectric = 2.25`
  - `depthRange = 0.45`
- The profile waypoints in each DZX file record:
  - start local coordinates: `0.000000, 0.000000, 0`
  - end local coordinates near `-0.003332, 0.000000, 0`
- No DZX field inspected provides the spacing between `PROJECT001C__013` through `PROJECT001C__016`.
- The older 3D plan explicitly treats field metadata as mandatory before local GSSI 51600S data can support 3D inversion claims.

## Current decision

Crossline spacing remains unconfirmed from local metadata. The current optimizer evidence and product bundle should continue to report geometry-conditioned finite-length predictions.

## What remains blocked

- Need acquisition notes, survey sheet, collection operator notes, grid layout, or another metadata source that states the spacing between the four GSSI profiles.
- The DZX sidecars are sufficient for along-scan sampling but not crossline spacing.

## Next defensible task

Use the current prediction bundle as the working deliverable and request/locate acquisition geometry metadata. If no metadata exists, treat crossline spacing as an optimization/uncertainty parameter in the product interface.

## Validation/resource checks

- DZX metadata was inspected directly.
- Local text search found along-scan metadata but no crossline profile spacing in the trusted GSSI data folder.
- Marathon request remains active; continue only with tasks that reduce or clearly communicate the crossline-geometry uncertainty.
