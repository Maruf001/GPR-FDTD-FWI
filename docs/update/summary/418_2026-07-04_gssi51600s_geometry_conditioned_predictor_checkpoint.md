# 2026-07-04 GSSI 51600S Geometry-Conditioned Predictor Checkpoint

## What changed

- Added `run_gssi51600s_geometry_conditioned_predictor.py`.
- The command reports a prediction conditioned on either:
  - the dense joint MAP spacing, or
  - a user/measured crossline spacing supplied with `--spacing-m`.
- Added tests for nearest spacing selection, MAP-spacing behavior, and out-of-grid spacing handling.
- Added the new command to the current product bundle source snapshots.

## Key numbers

- Current product bundle with the conditioned predictor: `118_gssi51600s_current_prediction_bundle_with_geometry_conditioned_predictor`
- MAP-spacing conditioned prediction:
  - selected spacing: `0.22 m`
  - branch state: `short_only`
  - length: `0.1833631247 m`
  - subset length range: `0.1832021773-0.1835240722 m`
  - diameter: `17.30563678 mm`
  - relative permittivity: `2.042056620`
  - conductivity: `0.0026600763 S/m`
- Explicit `0.24 m` spacing prediction:
  - branch state: `short_only`
  - length: `0.1833861023 m`
  - subset length range: `0.1832049042-0.1835673004 m`
  - diameter: `17.30563957 mm`
  - relative permittivity: `2.042079926`
  - conductivity: `0.0026600725 S/m`
- Explicit `0.20 m` spacing prediction:
  - branch state: `contains_long`
  - length: `0.2002782226 m`
  - subset length range: `0.1832225174-0.2173339278 m`

## Current decision

The predictor now has a product-style bridge from measured crossline geometry to spacing-conditioned 3D rebar properties. Without measured spacing, the default uses the dense joint MAP spacing and keeps the claim boundary clear. With measured spacing, it reports the nearest dense-grid spacing row and whether that row is short-only or contains the long branch.

## What remains blocked

- A supplied spacing can only be release-promoted if it comes from measured crossline geometry or a validated profile-position optimizer.
- If a supplied spacing is not close to the dense spacing grid, the command marks that a new spacing run is required instead of silently extrapolating.

## Next defensible task

Add a measured-geometry intake file format or profile-position optimizer so the conditioned predictor can take real acquisition geometry directly, rather than requiring manual `--spacing-m` input.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_current_prediction_bundle.py run_gssi51600s_geometry_conditioned_predictor.py`
- `python -m pytest tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_geometry_conditioned_predictor.py -q`
- Product bundle regenerated with the new predictor snapshot.
- Broader focused validation is pending after this checkpoint.
- The local marathon request remains active.
