# Experiment 10: Realistic Antenna Modelling

**Date**: 2026-03-30

## Objective

Replace the idealised point source with a distributed dipole antenna model that produces a more realistic radiation pattern.

## Files Created

- `core/source_antenna.py` — `DipoleAntenna` (distributed transmitter), `DipoleReceiver` (spatially-integrated receiver), and `run_with_antenna()` convenience function.

## Method

The antenna is modelled as a vertical line of soft current sources with half-cosine amplitude tapering:

$$w_k = \cos\left(\frac{\pi}{2} \cdot \frac{|k - k_{\text{center}}|}{n_{\text{half}} + 0.5}\right)$$

normalised so $\sum w_k = 1$ (total injected amplitude equals the point-source value). This distributes the excitation over `2 * n_half + 1` cells centred at the transmitter position.

The receiver similarly integrates $E_z$ over its aperture with the same cosine weighting, approximating the spatial averaging of a finite antenna.

## Test Configuration

- Antenna length: 20 mm (10 cells, quarter-wavelength in concrete at 1.5 GHz)
- Source position: x = 250 mm (above centre rebar)
- Rebar model: 3 rebars at 50 mm cover depth

## Results

| Metric | Point source | Dipole antenna |
|--------|-------------|----------------|
| Max amplitude | 1.58e-2 | 5.18e-2 |
| RMS trace difference | — | 6.30e-3 |
| **Relative RMS difference** | — | **39.8%** |

## Analysis

The dipole antenna produces a **40% RMS difference** from the point source, with notably higher amplitude (3.3×). Key effects:

1. **Enhanced near-field coupling** — the distributed source excites a broader wavefront that couples more efficiently into the concrete, increasing the received signal amplitude.

2. **Modified radiation pattern** — the point source radiates omnidirectionally, while the dipole has a directional pattern with nulls along the antenna axis. This changes the relative strengths of direct wave, surface reflection, and rebar reflections.

3. **Spatial averaging at receiver** — the distributed receiver integrates $E_z$ over its aperture, which acts as a low-pass spatial filter and smooths rapid field variations.

**Practical implications**: For quantitative FWI that matches real GPR data, antenna modelling is important. However, for rebar detection (a qualitative task based on hyperbola identification), the point source is an adequate approximation.

## Baseline Preserved

Original `core/source.py` and `core/fdtd.py` unchanged. The antenna module is a new standalone file that uses the existing FDTD simulator.
