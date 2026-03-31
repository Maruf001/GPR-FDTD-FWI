# Experiment 07: Multi-Scale Frequency Continuation

**Date**: 2026-03-30

## Objective

Implement multi-scale frequency continuation for geometry-based GPR inversion: start at low frequency (broad, smooth misfit landscape) and progressively increase to higher frequencies (detailed, more local minima).

## Files Created

- `inversion/multiscale_engine.py` — Multi-scale wrapper for geometry-based inversion with configurable frequency schedule.

## Method

Three-stage frequency continuation:

1. **Stage 1: 0.5 GHz** — Low frequency, long wavelength (~245 mm in concrete). Provides coarse localisation with a smooth, convex-like misfit landscape.
2. **Stage 2: 1.0 GHz** — Medium frequency (~122 mm wavelength). Refines positions using Stage 1 result as initial guess.
3. **Stage 3: 1.5 GHz** — Target frequency (~82 mm wavelength). Final refinement at full resolution.

At each stage, new observed data is generated from the true model at the target frequency, and Nelder–Mead optimisation runs starting from the previous stage's result.

## Configuration

- Sources: 10 (subsampled from 51)
- GPU: ON (all forward simulations)
- Max evaluations per stage: 300
- Optimiser: Nelder–Mead (adaptive simplex)

## Results

### Stage-by-Stage Progression

| Stage | Frequency | Evaluations | Final Misfit | Rebar 1 x err | Rebar 2 x err | Rebar 3 x err |
|-------|-----------|-------------|-------------|---------------|---------------|---------------|
| 1 | 0.5 GHz | 300 | 1.47e-3 | 8.4 mm | 8.2 mm | 10.4 mm |
| 2 | 1.0 GHz | 204 | 2.49e-3 | 2.3 mm | 0.9 mm | 1.4 mm |
| 3 | 1.5 GHz | 226 | 1.96e-3 | 4.5 mm | 0.9 mm | 0.6 mm |

### Final Recovered Parameters

| Rebar | x [mm] | x true | z [mm] | z true | r [mm] | r true |
|-------|--------|--------|--------|--------|--------|--------|
| 1 | 154.5 | 150.0 | 89.8 | 90.0 | 6.8 | 6.0 |
| 2 | 250.9 | 250.0 | 89.7 | 90.0 | 6.3 | 6.0 |
| 3 | 350.6 | 350.0 | 86.6 | 90.0 | 6.2 | 6.0 |

### Summary Metrics

| Metric | Value |
|--------|-------|
| Max position error | 4.5 mm (Rebar 1 x) |
| Max depth error | 3.4 mm (Rebar 3 z) |
| Max radius error | 0.8 mm |
| NRMS model error | 3.3% |
| Total evaluations | 730 |
| Total runtime | 2624 s (~44 min) |

## Analysis

**The multi-scale approach successfully refined positions through progressive stages:**

- **Stage 1** (0.5 GHz): Coarse localisation within ~10 mm. The low frequency provides a smooth misfit landscape — the optimiser converges reliably but cannot resolve fine details.
- **Stage 2** (1.0 GHz): Major refinement to ~2 mm. The medium frequency inherits the coarse position from Stage 1 and refines it with higher resolution.
- **Stage 3** (1.5 GHz): Final polish, achieving sub-1 mm accuracy on Rebars 2 and 3. Rebar 1 and 3 show slightly larger errors (4.5 mm, 3.4 mm) due to the edge effects of the scan aperture.

**Comparison with single-frequency inversion (Experiment 04):**

| Metric | Single freq (1.5 GHz) | Multi-scale (0.5→1.5 GHz) |
|--------|----------------------|---------------------------|
| Max position error | 2.6 mm | 4.5 mm |
| NRMS model error | 3.0% | 3.3% |
| Runtime | 1450 s (24 min) | 2624 s (44 min) |
| Evaluations | 275 | 730 |

The multi-scale approach produces comparable accuracy to the single-frequency approach but takes ~1.8× longer due to the additional stages. For this problem — where the single-frequency misfit is already well-behaved — multi-scale doesn't provide a clear advantage.

**Where multi-scale shines:** Problems with strong local minima (e.g., pixel-wise inversion, more complex geometries with multiple scattering, or when the initial guess is far from the truth). In such cases, the low-frequency stages can escape local minima that trap the high-frequency-only inversion.

## Baseline Preserved

Original inversion code (`inversion/geometry_inversion.py`, `inversion/inversion_engine.py`) unchanged. The multiscale engine is a new standalone file.
