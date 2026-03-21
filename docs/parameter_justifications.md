# Parameter Justifications

This document explains the physical reasoning behind every parameter choice in `config.py`. These are the kinds of questions an interviewer will ask.

---

## Material Parameters

### Concrete: εr = 6, σ = 0.01 S/m

- **Relative permittivity**: Literature values for dry concrete at microwave frequencies range from 5 to 10. The value of 6 is widely used in GPR simulation studies and corresponds to typical structural concrete with low-to-moderate moisture content.
- **Conductivity**: 0.01 S/m represents a low-loss dielectric. Concrete is not a good conductor; this value introduces realistic attenuation without being overly lossy. Higher moisture would increase both εr and σ.
- **Source**: Bungey et al. (2006), gprMax documentation, Daniels (2004) "Ground Penetrating Radar".

### Rebar: εr = 1, σ = 1e7 S/m

- **Conductivity**: Steel has σ ≈ 5.96 × 10^6 S/m. We use 10^7 which, at the FDTD grid resolution, makes the rebar behave as a **perfect electric conductor (PEC)**.
- **Permittivity**: Set to 1 (vacuum) because at this conductivity level, the displacement current is negligible compared to the conduction current. The wave is almost entirely reflected.
- **Magnetic permeability**: Set to μr = 1 (simplified). Carbon steel has μr ≈ 100-1000, but at GPR frequencies the skin depth in steel is << 1 mm, so the wave cannot penetrate — the magnetic properties only affect the immediate surface, which we cannot resolve at 2 mm grid spacing anyway.

### Air: εr = 1, σ = 0

- Standard free-space values. The air layer represents the antenna standoff.

---

## Source Parameters

### Center Frequency: 1.5 GHz

- **Range consideration**: Commercial GPR systems for concrete use 1-2.5 GHz antennas. Higher frequencies give better resolution but lower penetration.
- **Resolution**: At 1.5 GHz in concrete (εr=6), wavelength = c/(f·√εr) = 82 mm. The resolution limit is ~λ/2 = 41 mm, sufficient to detect 12 mm rebars (the reflection signature is dominated by the impedance contrast, not the rebar size relative to wavelength).
- **Penetration**: At 1.5 GHz with σ = 0.01 S/m, the skin depth in concrete is ~0.5 m, far exceeding our 300 mm domain depth. Adequate for imaging rebars at 50 mm cover depth.
- **Ricker wavelet bandwidth**: The effective bandwidth extends to ~2.5 × fc = 3.75 GHz.

### Wavelet Delay: t_delay = 1/fc = 0.667 ns

- Ensures the wavelet amplitude is negligible at t = 0, preventing numerical artifacts from an impulsive start. At t = 0, the Ricker wavelet value is exp(−π²) ≈ 5 × 10^−5 of the peak — effectively zero.

---

## Geometry Parameters

### Domain: 500 × 300 mm

- **Width (500 mm)**: Covers 3 rebars at 100 mm spacing with 150 mm margins on each side. Provides sufficient lateral extent for the scan aperture.
- **Depth (300 mm)**: Typical concrete slab thickness. Provides room for the rebar layer plus wave propagation below the rebars.

### Air Layer: 40 mm

- Represents the physical standoff between the antenna and the concrete surface. Real GPR antennas operate at 5-20 mm standoff, but we use 40 mm to clearly separate the direct wave from the surface reflection in the B-scan.

### Rebars: 3 × 12 mm diameter, 50 mm cover, 100 mm spacing

- **Diameter (12 mm)**: Standard #4 rebar (12.7 mm). Common in structural concrete.
- **Cover depth (50 mm)**: Typical concrete cover ranges from 25-75 mm depending on exposure class. 50 mm is a common value for interior structural elements.
- **Spacing (100 mm)**: Represents a moderately reinforced section. Standard spacing ranges from 75-300 mm.
- **Number (3)**: Enough to demonstrate the scanner's ability to resolve multiple targets while keeping the simulation manageable.

---

## Grid Parameters

### Grid Spacing: dx = dz = 2 mm

- **Wavelength criterion**: At f_max = 3.75 GHz in concrete (εr=6), λ_min = 32.7 mm. With dx = 2 mm, we have 16.3 points per shortest wavelength. The standard guideline is ≥10 (minimum) to ≥20 (good). Our choice is well within acceptable range.
- **Rebar resolution**: Rebar radius = 6 mm → 3 grid cells. This gives a recognizable circular shape. Finer grids (1 mm) would give 6 cells/radius but double the computation.
- **Square grid**: dx = dz simplifies the CFL condition and CPML implementation, and avoids anisotropic numerical dispersion.

### Time Step: dt ≈ 4.24 ps (Courant factor 0.9)

- **CFL limit**: dt_max = dx/(c₀·√2) = 4.714 ps
- **Safety margin**: We use 90% of the CFL limit. This provides numerical stability margin without unnecessarily increasing the number of time steps.
- **Why not 0.5?**: A lower Courant number requires more time steps for the same physical time. At 0.9, we need ~1887 steps vs ~3538 at 0.5. The accuracy difference is negligible because the dominant error source is spatial dispersion (controlled by points/wavelength), not temporal.

### Total Simulation Time: 8 ns

- **Two-way travel time**: For a wave to reach the bottom of the concrete (260 mm at ~c₀/2.45) and return: ~4.2 ns
- **Buffer**: An additional ~4 ns allows for late arrivals, multiple reflections between rebars, and complete signal decay in the CPML.

---

## CPML Parameters

### 15 Layers, Cubic Grading

- **Layer count**: 15 layers × 2 mm = 30 mm of PML. This provides ~50-60 dB attenuation for normally-incident waves. Standard recommendations are 10-20 layers.
- **Polynomial order (m = 3)**: Cubic grading is the standard choice in the literature. It provides a smooth transition that minimizes discrete PML reflections.
- **κ_max = 5**: Controls coordinate stretching for evanescent wave absorption. Standard value from Roden & Gedney (2000).
- **α_max = 0.05**: Prevents late-time instability (a known issue with standard PML). The CFS extension with α > 0 provides this stability.

### σ_max Derivation

Theoretical optimal: σ_max = 0.8 × (m+1) / (dh × √(μr/εr))

For our case (air boundary): σ_max ≈ 0.8 × 4 / (0.002 × 1) = 1600 S/m per unit length.

---

## Scanning Parameters

### Scan Range: 50-450 mm, Step: 4 mm

- **Margins (50 mm from edges)**: Keeps the source well outside the PML region (PML occupies the outer 30 mm of the computational domain).
- **Step size (4 mm = 2 grid cells)**: Provides dense spatial sampling for good B-scan image quality. This gives ~100 scan positions, typical for high-resolution GPR surveys.

### Tx-Rx Offset: 20 mm

- Commercial GPR systems use co-located (monostatic) or bistatic configurations. We use a 20 mm offset to represent a typical bistatic antenna pair while keeping Tx and Rx close enough that the B-scan appears similar to a zero-offset section.

---

## Inversion Parameters

### 30 Iterations

- For steepest descent, 20-50 iterations is typical for convergence in FWI. More iterations give diminishing returns due to the local nature of gradient-based optimization.

### TV Regularization Weight: 0.01

- Balances data fit and model smoothness. Too large → over-smoothed model that ignores data. Too small → noisy model driven by data noise. The value 0.01 is chosen empirically and can be adjusted based on convergence behavior.

### εr Bounds: [1, 15]

- **Lower bound (1)**: Physical minimum (vacuum/air).
- **Upper bound (15)**: Exceeds the maximum expected εr in the model (concrete = 6, saturated concrete ≈ 12). Provides room for the optimizer to explore without artificial constraint tightness.

### Coarser Scan Step for Inversion: 8 mm

- Halves the number of sources from ~100 to ~50, reducing computational cost by 2x. Each source requires a forward + adjoint simulation. The spatial sampling is still adequate for the inversion resolution.
