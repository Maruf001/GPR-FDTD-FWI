# Technical Context For AI Diagram Generation

Document number: 001

Date: 2026-06-04

Purpose: This document is technical context for a future AI assistant that has
no prior knowledge of this repository. It preserves geometry definitions,
coordinate conventions, simulation settings, inversion/search details, data
products, campaign results, and visual-generation instructions for engineering
diagrams and experiment illustrations.

Primary source directories:

- `config.py`
- `core/`
- `gpu/`
- `inversion/`
- `run_multi_rebar_coordinate_optimizer.py`
- `run_multi_rebar_local_geometry_profile.py`
- `run_multi_rebar_common_radius_profile.py`
- `run_single_rebar_source_profiled_polish.py`
- `run_rebar_detection_pipeline.py`
- `docs/experiments/`
- `outputs/experiments/`

Latest completed experiment at the time of this document: experiment 434,
`outputs/experiments/434_multi_rebar_right_source_shape_basis_fit_stage4c_dense_radius`.

## 1. Project And System Overview

The project builds a two-dimensional ground-penetrating radar simulation and
inversion workflow for estimating rebar geometry inside concrete.

Technical goal:

- Simulate ground-penetrating radar wave propagation through an air/concrete
  domain containing circular steel rebar cross-sections.
- Generate synthetic observed A-scan and B-scan data from known target
  geometries.
- Search over candidate rebar x position, depth z position, and radius.
- Compare predicted B-scans against observed B-scans using source-profiled
  normalized least-squares objectives.
- Report not only the best candidate, but also confidence labels, ambiguity
  intervals, and near-tied competing geometries.

Confirmed from `config.py`, `core/geometry.py`, `gpu/fdtd_gpu_v2.py`,
`run_multi_rebar_common_radius_profile.py`,
`run_multi_rebar_coordinate_optimizer.py`, and
`run_multi_rebar_local_geometry_profile.py`.

Core pipeline for the recent experiments:

```text
parameter vector / candidate grid
  -> geometry builder with circular rebars
  -> FDTD forward simulation
  -> predicted B-scan, shape (nt, n_scan_positions)
  -> source-profile fitting over nuisance parameters
  -> normalized least-squares loss
  -> rank candidates
  -> confidence and ambiguity reporting
```

Important terminology:

- GPR: Ground-penetrating radar.
- FDTD: Finite-difference time-domain forward solver.
- FWI: Full waveform inversion. In the recent local geometry experiments, this
  mostly means waveform-matching search over explicit geometry grids, not a
  continuous gradient optimizer.
- A-scan: one receiver time trace from one transmitter/receiver scan position.
- B-scan: a stack of A-scans across multiple scan positions. In code this has
  shape `(nt, n_positions)`.
- Tx/Rx: transmitter/receiver pair.
- CPML: Convolutional perfectly matched layer absorbing boundary.

What is being recovered:

- Rebar center x coordinate, in millimeters.
- Rebar center z coordinate, in millimeters.
- Rebar radius, in millimeters.
- Source nuisance parameters, used for objective comparison:
  frequency scale, time shift, amplitude scale, and in the latest branch,
  primary/ringdown basis coefficients.

The recent campaigns are not neural-network training campaigns. The
"architecture" is a deterministic physics simulation and search/reporting
pipeline. There are earlier adjoint and inversion-engine files in the repo, but
experiments 270-434 mainly use explicit candidate-grid sweeps with GPU FDTD.

## 2. Coordinate System And Units

### Coordinate Axes

Confirmed from `config.py`, `core/geometry.py`, `core/materials.py`, and
`core/utils.py`.

The physical domain uses meters internally and millimeters in most experiment
commands and reports.

Coordinate convention:

| Quantity | Meaning | Units | Source |
| --- | --- | ---: | --- |
| `x` | lateral horizontal coordinate along scan line | m internally, mm in CLI/results | `config.py`, runners |
| `z` | vertical coordinate increasing downward | m internally, mm in CLI/results | `core/materials.py` |
| origin | top-left of physical non-PML domain | x=0, z=0 | inferred from `pos_to_index` and geometry setup |
| concrete surface | air/concrete interface | z=40 mm | `CONCRETE_TOP = AIR_THICKNESS = 0.04` |
| antenna height | Tx/Rx z position | z=38 mm, 2 mm above concrete surface | `TX_Z = RX_Z = 0.038` |
| rebar center | center of circular cross-section | absolute physical x/z, not cover depth | `build_rebar_model` |
| cover depth | depth below concrete surface | `rebar_z_mm - 40 mm` | inferred from config |
| radius | circle radius, not diameter | mm in experiment commands | run manifests |

Important diagram rule:

When an experiment says a rebar is at `z=90 mm`, this is the absolute z
coordinate measured from the top of the physical air/concrete domain. It is not
90 mm of concrete cover. Since the concrete surface is at `z=40 mm`, that
rebar has 50 mm cover below the concrete surface.

### Domain And Grid

Confirmed from `config.py` and `_override_grid` in
`run_single_rebar_inversion.py`.

Default configuration:

| Parameter | Value | Meaning |
| --- | ---: | --- |
| `DOMAIN_X` | 0.50 m | physical domain width, 500 mm |
| `DOMAIN_Z` | 0.30 m | physical domain height/depth, 300 mm |
| `AIR_THICKNESS` | 0.04 m | air layer thickness, 40 mm |
| `CONCRETE_TOP` | 0.04 m | concrete surface at z=40 mm |
| `DX`, `DZ` | 0.002 m | default 2 mm square grid |
| `NPML` | 15 cells | default PML thickness, 30 mm |
| `NX_INNER`, `NZ_INNER` | 250, 150 | physical domain cells at 2 mm |
| `NX`, `NZ` | 280, 180 | total grid including PML |
| `DT` | about 4.2456 ps | default time step |
| `T_MAX` | 8 ns | total simulated time |
| `NT` | 1885 | default time samples |

Most recent production experiments use `--grid-step-mm 1.0`. The grid override
preserves the physical PML thickness by increasing `NPML`.

Grid after `--grid-step-mm 1.0`:

| Parameter | Value |
| --- | ---: |
| `DX`, `DZ` | 1.0 mm |
| `NPML` | 30 cells |
| `NX_INNER`, `NZ_INNER` | 500, 300 |
| `NX`, `NZ` | 560, 360 |
| `DT` | about 2.1228 ps |
| `NT` | 3769 |

PML mapping:

- Physical coordinates ignore PML.
- Grid indices include PML offset.
- Conversion is `grid_index = round(position / spacing) + NPML`, confirmed from
  `core/utils.py`.
- For most engineering diagrams, draw the physical domain only. Add PML only if
  the diagram is explicitly about the computational grid.

### Rebar Center And Radius Convention

Confirmed from `run_multi_rebar_common_radius_profile.py`,
`run_multi_rebar_local_geometry_profile.py`, and `core/geometry.py`.

CLI and JSON fields usually use:

```text
x_values_mm = [x1, x2, ...]
z_values_mm = [z1, z2, ...]
radius_values_mm = [r1, r2, ...]
```

The geometry builder converts these to `rebars=(z_m, x_m, radius_m)` before
calling `build_rebar_model`.

Radius is always radius, not diameter. For a radius of 6 mm, draw a 12 mm
diameter circle.

## 3. Rebar Geometry And Structural Configurations

### Default Single-Layer Rebar Configuration

Confirmed from `config.py`.

Default config has three same-depth rebars:

| Rebar index | x center | z center | radius | cover below concrete surface |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 150 mm | 90 mm | 6 mm | 50 mm |
| 1 | 250 mm | 90 mm | 6 mm | 50 mm |
| 2 | 350 mm | 90 mm | 6 mm | 50 mm |

These are centered horizontally with 100 mm spacing. Rebar index order is
left-to-right.

### Variable-Radius Close-Spacing Geometry, Experiments 270-418

Confirmed from experiment run manifests such as:

- `outputs/experiments/276_coordinate_optimizer_close50_seed34_sources4_txrx40_objectives/run_manifest.json`
- `outputs/experiments/302_coordinate_optimizer_close30_seed34_sources4_txrx35_objectives/run_manifest.json`
- `outputs/experiments/332_coordinate_optimizer_close14_seed34_sources4_txrx45_objectives/run_manifest.json`
- `outputs/experiments/357_coordinate_optimizer_close14_seed34_sources4_txrx50_noise15p361328125_objectives/run_manifest.json`

This campaign uses three same-depth rebars with different radii:

```text
radii = [5, 6, 8] mm
z centers = [90, 90, 90] mm
left x = 190 mm
center x = 250 mm
right x varies by close-spacing label
```

The label `closeXX` means:

```text
right_rebar_x_mm - center_rebar_x_mm = XX mm
```

So `close14` means center x=250 mm, right x=264 mm. Since the middle radius is
6 mm and the right radius is 8 mm, close14 is a tangent/contact case:
`6 + 8 = 14 mm`.

Table:

| Structure name | Number of rebars | Center x positions | Depths z | Radii | Center-right spacing | Experiments | Technical notes |
| --- | ---: | --- | --- | --- | ---: | --- | --- |
| close50 | 3 | [190, 250, 300] mm | [90, 90, 90] mm | [5, 6, 8] mm | 50 mm | 270-289 | Source-count and Tx/Rx-offset design. Clean with 4 sources and 35-40 mm offset; 25 mm offset failed. |
| close45 | 3 | [190, 250, 295] mm | [90, 90, 90] mm | [5, 6, 8] mm | 45 mm | 290-293 | Clean under 4 sources, 35 mm Tx/Rx offset. |
| close40 | 3 | [190, 250, 290] mm | [90, 90, 90] mm | [5, 6, 8] mm | 40 mm | 294-297 | Clean under 4 sources, 35 mm offset. |
| close35 | 3 | [190, 250, 285] mm | [90, 90, 90] mm | [5, 6, 8] mm | 35 mm | 298-301 | Clean under 4 sources, 35 mm offset. |
| close30 | 3 | [190, 250, 280] mm | [90, 90, 90] mm | [5, 6, 8] mm | 30 mm | 302-305 | Tightest replicated clean result under 35 mm offset. |
| close28 | 3 | [190, 250, 278] mm | [90, 90, 90] mm | [5, 6, 8] mm | 28 mm | 311-319 | Ambiguous at 35 mm offset; clean at 45 mm offset. |
| close25 | 3 | [190, 250, 275] mm | [90, 90, 90] mm | [5, 6, 8] mm | 25 mm | 306-310, 320-323 | Failed at 35 mm; point-correct but ambiguous at 40 mm; clean at 45 mm. |
| close20 | 3 | [190, 250, 270] mm | [90, 90, 90] mm | [5, 6, 8] mm | 20 mm | 324-327 | Clean at 45 mm offset. |
| close15 | 3 | [190, 250, 265] mm | [90, 90, 90] mm | [5, 6, 8] mm | 15 mm | 328-331 | Clean at 45 mm offset. Physical gap between middle/right circles is 1 mm. |
| close14 | 3 | [190, 250, 264] mm | [90, 90, 90] mm | [5, 6, 8] mm | 14 mm | 332-418 | Tangent/contact case. Clean at 45 mm offset up to 15.3125 percent noise; clean at 50 mm offset up to 19.642333984375 percent noise. |

Difficulty summary:

- Easy/clean: close50 with 4 sources and adequate offset; close45 through
  close30 at 35 mm offset; close28 through close14 at 45 mm offset.
- Ambiguous: close28 at 35 mm; close25 at 40 mm; close14 at high noise just
  above the clean endpoint.
- Failed or not clean: 3-source close50; 25 mm Tx/Rx offset close50;
  close25 at 35 mm.

### Source-Shape Multi-Rebar Geometry, Experiments 425-434

Confirmed from:

- `docs/experiments/51_multi_rebar_source_shape_basis_fit.md`
- `outputs/experiments/425_*/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/432_*/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/434_*/data/multi_rebar_local_geometry_summary.json`

This branch uses the default three-rebar geometry:

```text
x centers = [150, 250, 350] mm
z centers = [90, 90, 90] mm
radii = [6, 6, 6] mm
```

The tested target changes by experiment:

| Target | Index | True x/z/r | Experiments |
| --- | ---: | --- | --- |
| left | 0 | x=150 mm, z=90 mm, r=6 mm | 425, 426, 433 |
| center | 1 | x=250 mm, z=90 mm, r=6 mm | 427, 429, 430, 431, 432 |
| right | 2 | x=350 mm, z=90 mm, r=6 mm | 428, 434 |

Candidate windows:

| Run type | x grid | z grid | radius grid | Candidate geometries |
| --- | --- | --- | --- | ---: |
| narrow fixed x/z | one x, one z | true x/z | [5.8, 6.0, 6.2, 7.4, 7.8] mm | 5 |
| compact x/z/r | true x +/- 1 mm | true z +/- 1 mm | [5.8, 6.0, 6.2] mm | 27 |
| high-radius compact | true x +/- 1 mm | true z +/- 1 mm | [5.8, 6.0, 6.2, 7.4, 7.8] mm | 45 |
| high-radius wide x/z | true x +/- 2 mm | true z +/- 2 mm | [5.8, 6.0, 6.2, 7.4, 7.8] mm | 125 |
| dense Stage 4C | true x +/- 2 mm | true z +/- 2 mm | 5.4:7.8:0.2 mm | 325 |

Dense Stage 4C completed for all three targets:

| Experiment | Target | x grid | z grid | radius grid | Result |
| ---: | --- | --- | --- | --- | --- |
| 432 | center | 248-252 mm | 88-92 mm | 5.4-7.8 mm by 0.2 | true x/z/r first in all cases |
| 433 | left | 148-152 mm | 88-92 mm | 5.4-7.8 mm by 0.2 | true x/z/r first in all cases |
| 434 | right | 348-352 mm | 88-92 mm | 5.4-7.8 mm by 0.2 | true x/z/r first in all cases |

All three dense runs show a secondary branch around `z=91 mm` and
`r=6.8-7.0 mm`, but it remains below the true branch and the adjacent
`r=6.2 mm` branch at true x/z.

## 4. Antenna, Source, Receiver, And Scan Setup

### Meaning Of "Source"

Confirmed from `run_multi_rebar_common_radius_profile.build_scan_positions`
and `gpu/fdtd_gpu_v2.FDTDSimulatorGPU_v2.run_batch`.

In this project, `sources` in the recent experiment commands means the number
of Tx/Rx scan positions. It does not mean:

- number of independent source wavelets;
- number of B-scans;
- number of physical transmitter types;
- number of neural-network inputs.

One source position equals one Tx/Rx pair and produces one A-scan trace. A set
of source positions produces one B-scan.

### Tx/Rx Geometry

Confirmed from `config.py` and `run_multi_rebar_common_radius_profile.py`.

Default antenna constants:

| Parameter | Value | Meaning |
| --- | ---: | --- |
| `TX_Z` | 38 mm | transmitter vertical position |
| `RX_Z` | 38 mm | receiver vertical position |
| `TX_RX_OFFSET` default | 20 mm | receiver x is transmitter x + offset |
| `SCAN_START_X` | 50 mm | first transmitter x |
| `SCAN_END_X` | 450 mm | last transmitter x |
| `SCAN_STEP` | 4 mm | full detection scan step |
| `INVERSION_SCAN_STEP` | 8 mm | candidate inversion scan grid before source subsampling |

Tx/Rx pair convention:

```text
Tx = (scan_x, TX_Z)
Rx = (scan_x + tx_rx_offset, RX_Z)
```

The scan x value stored in `scan_x` is the transmitter x, not the pair
midpoint. The pair midpoint is `scan_x + tx_rx_offset / 2`.

The receiver index is clipped at the right edge of the physical domain:
`rec_ix = min(rec_ix, cfg.NX - cfg.NPML - 1)`. This matters only for the last
scan position when a large offset would push the receiver past the domain.

### Scan Positions For Recent Runs

The inversion scan grid before subsampling is 51 transmitter positions:

```text
50, 58, 66, ..., 442, 450 mm
```

When `--sources N` is less than 51, the runner selects approximately evenly
spaced indices using `np.linspace`.

At 1 mm grid, selected transmitter positions are:

| `--sources` | Tx x positions |
| ---: | --- |
| 3 | [50, 250, 450] mm |
| 4 | [50, 178, 314, 450] mm |
| 5 | [50, 146, 250, 346, 450] mm |
| 7 | [50, 114, 178, 250, 314, 378, 450] mm |

Examples of four-source Tx/Rx positions:

| Offset | Tx x positions | Rx x positions | Pair midpoints |
| ---: | --- | --- | --- |
| 20 mm | [50, 178, 314, 450] | [70, 198, 334, 470] | [60, 188, 324, 460] |
| 35 mm | [50, 178, 314, 450] | [85, 213, 349, 485] | [67.5, 195.5, 331.5, 467.5] |
| 40 mm | [50, 178, 314, 450] | [90, 218, 354, 490] | [70, 198, 334, 470] |
| 45 mm | [50, 178, 314, 450] | [95, 223, 359, 495] | [72.5, 200.5, 336.5, 472.5] |
| 50 mm | [50, 178, 314, 450] | [100, 228, 364, 499 clipped] | [75, 203, 339, about 474.5] |

For the source-shape branch, the default 20 mm Tx/Rx offset is used unless
specified otherwise. Five-source source-shape runs use:

```text
Tx x = [50, 146, 250, 346, 450] mm
Rx x = [70, 166, 270, 366, 470] mm
```

### Waveform And Source Shape

Confirmed from `core/source.py` and
`run_single_rebar_source_profiled_polish.py`.

Base source:

- Ricker wavelet.
- Center frequency usually 1.5 GHz.
- Formula implemented in `core/source.ricker_wavelet`.
- Delay is `1 / f_center` so the wavelet starts near zero.

Observed source wavelet can be perturbed by:

- frequency scale, for example 1.1;
- time shift, for example -50 ps;
- amplitude scale, for example 1.1;
- additive delayed ringdown:
  - ringdown scale such as 0.20, 0.25, or 0.30;
  - ringdown delay usually 180 ps;
  - ringdown frequency scale usually 0.8.

Modeled source profile can fit:

- frequency scale grid, commonly `[0.9, 1.0, 1.1]`;
- time shift grid:
  - coordinate optimizer often `[-50, 0, 50] ps`;
  - some single-rebar source-shape runs use
    `[-80, -50, -25, 0, 25, 50, 80] ps`;
- scalar amplitude by least squares;
- in the source-shape branch, primary and delayed-ringdown basis coefficients.

### Absorbing Boundary

Confirmed from `config.py`, `gpu/fdtd_gpu_v2.py`, and `gpu/cpml_gpu.py`.

The FDTD solver uses CPML absorbing boundaries. Default PML physical thickness
is 30 mm. At the default 2 mm grid this is 15 cells. At the 1 mm grid override
it becomes 30 cells.

Diagram-ready interpretation:

- Draw the concrete slab as a rectangle from z=40 mm to z=300 mm.
- Draw an air layer from z=0 to z=40 mm.
- Draw Tx and Rx as two small markers at z=38 mm, above the surface.
- Draw Rx to the right of Tx by the configured offset.
- Draw a scan arrow along +x from 50 mm to 450 mm.
- Draw one source position as one Tx/Rx pair.
- Draw a B-scan as the stack of A-scans from multiple Tx/Rx pairs.

## 5. Data Products: A-Scan, B-Scan, And Simulation Outputs

### A-Scan

Confirmed from `gpu/fdtd_gpu_v2.py` and `core/fdtd.py`.

An A-scan is one receiver time trace:

```text
trace[t] = Ez(rec_iz, rec_ix, t)
```

In the GPU batch solver, one A-scan corresponds to one batch element, one
source/receiver pair, and one output column.

### B-Scan

Confirmed from `gpu/fdtd_gpu_v2.py`,
`run_multi_rebar_common_radius_profile.simulate_bscan`, and detection B-scan
NPZ files.

A B-scan is a two-dimensional array:

```text
bscan.shape = (nt, n_positions)
```

Axes:

- axis 0: time samples;
- axis 1: scan positions / A-scans.

Example confirmed from
`outputs/experiments/118_detection_seeded_two_stage_refinement_smoke/stages/detection/data/detection_bscan.npz`:

```text
observed_bscan.shape = (1885, 101)
clean_bscan.shape    = (1885, 101)
scan_x.shape         = (101,)
time.shape           = (1885,)
```

That detection run used the default 2 mm grid and full 4 mm scan step. Recent
1 mm local inversion runs usually do not save full observed B-scan NPZ files,
but the in-memory shape follows the same convention. For a 1 mm grid and four
source positions, the B-scan shape is generally `(3769, 4)`. For a 1 mm grid
and five source positions, it is generally `(3769, 5)`.

### Clean, Observed, Predicted, Residual

Confirmed from `run_multi_rebar_common_radius_profile.build_observed_cases`,
`run_single_rebar_source_profiled_polish._add_noise`, and
`inversion/source_profile.py`.

Definitions:

- clean B-scan: true-model simulation with the configured observed wavelet,
  before noise;
- observed B-scan: clean B-scan plus optional additive Gaussian noise;
- predicted/synthetic B-scan: candidate-geometry simulation with a modeled
  source wavelet or source basis;
- residual: source-profiled synthetic minus observed, after optional time
  shift, amplitude fit, source-basis fit, objective filtering, and mute window.

The normalized least-squares objective is implemented as:

```text
residual = (amplitude_scale * synthetic - observed) * mute
misfit = 0.5 * sum(residual^2) / max(0.5 * sum((observed * mute)^2), 1e-30)
```

For source-basis fitting, the amplitude-scale form is replaced by:

```text
synthetic = primary_coefficient * primary_basis
          + ringdown_coefficient * ringdown_basis
```

The fitted `ringdown_scale` reported in CSV/JSON is:

```text
ringdown_coefficient / primary_coefficient
```

### Preprocessing And Objective Windows

Confirmed from `inversion/adjoint.py`, `inversion/objective_variants.py`, and
`inversion/rebar_detection.py`.

In local FWI/search objectives:

- A time-domain mute window suppresses early direct wave and late arrivals.
- Default objective window is from 1.0 ns to 7.0 ns with 0.3 ns cosine tapers.
- Objective variants can apply time windows and bandpass filters.
- Recent coordinate optimizer variants often include:
  - `base:1.0,7.0,0.3,none,none,0.0`;
  - `highband:1.0,7.0,0.3,1.1,3.4,0.15`.
- Recent source-shape dense runs use only the `base` variant.

In detection:

- B-scan background is removed, usually by median across scan positions.
- Envelope is computed, using Hilbert transform if available.
- Candidate hyperbolas are scored over x/z grids.
- Detection B-scans are saved as NPZ with arrays:
  `observed_bscan`, `clean_bscan`, `scan_x`, `time`,
  `truth_x_values_mm`, `truth_z_values_mm`, and
  `truth_radius_values_mm`.

## 6. Noise, Random Seeds, And Repeatability

Noise implementation is confirmed from
`run_single_rebar_source_profiled_polish._add_noise` and
`run_rebar_detection_pipeline.add_noise`.

Noise model:

```text
noise = Gaussian(0, noise_std)
noise_std = noise_fraction * RMS(clean_bscan)
observed = clean_bscan + noise
```

Properties:

- Additive, zero-mean Gaussian noise.
- Applied directly to the clean B-scan array.
- Noise fraction is relative to clean signal RMS.
- Seed controls the random noise realization only.
- Initial geometry is controlled separately by explicit command arguments.
- Search grids are deterministic once observed data and candidate grid are
  fixed.

Common noise labels:

| Label fragment | Fraction | Percent RMS |
| --- | ---: | ---: |
| `noise05` | 0.05 | 5 percent |
| `noise10` | 0.10 | 10 percent |
| `noise15` | 0.15 | 15 percent |
| `noise20` | 0.20 | 20 percent |
| `noise19p642333984375` | 0.196423333984375 | 19.642333984375 percent |

Seed usage:

| Campaign | Noise level | Seeds | What seed controls | Observed effect |
| --- | ---: | --- | --- | --- |
| Stage 6 confidence, notes 40-44 | 10 percent and source mismatch/noise rows | 13, 21, 34, 55 | noise realization | Point recovery broadly correct; many weak margins required interval reporting. |
| close50 source/offset branch, 270-289 | 10 percent | 13, 21, 34 | noise realization | Four sources and adequate offset replicated clean; three sources failed. |
| close45-close14 spacing branch, 290-335 | 10 percent | 13, 21, 34 | noise realization | Clean limits depended strongly on Tx/Rx offset. |
| close14 45 mm noise bisection, 337-356 | 15 to 20 percent and midpoints | mostly 34 for probes, then 13/21/34 for replicated endpoints | noise realization | 15.3125 percent replicated clean; slightly higher levels became x-ambiguous. |
| close14 50 mm noise bisection, 357-418 | 15.361328125 to 19.642372131347656 percent | 13, 21, 34 for replicated endpoints; seed34 for upper probes | noise realization | 19.642333984375 percent replicated clean; upper endpoint became x-ambiguous at numerical cutoff edge. |
| source-shape single-rebar, 421-424 | 0, 5, 10 percent | 13, 21 | noise realization | Ringdown source-shape error caused high-radius branch until source-basis coefficients were fit. |
| source-shape multi-rebar, 425-434 | 0, 5, 10 percent | 13, 21 | noise realization | All compact and dense target gates passed with source-basis fitting; weakest dense margins in noisy ringdown rows. |

Important distinction:

Source mismatch cases use deterministic source perturbations such as
`frequency_scale=1.1`, `time_shift_ps=-50`, and `amplitude_scale=1.1`. The
seed in those labels still controls only noise if noise is nonzero.

## 7. Inversion And Optimization Setup

### Recent Local Geometry Search Strategy

Confirmed from `run_multi_rebar_coordinate_optimizer.py`,
`run_multi_rebar_local_geometry_profile.py`, and
`inversion/multi_rebar_coordinate.py`.

The recent experiments mainly use candidate-grid search. They do not update a
continuous model with gradients in experiments 270-434.

For each candidate geometry:

1. Build a material model with circular rebar inclusions.
2. Simulate one or more B-scans using GPU FDTD.
3. Fit source nuisance parameters against each observed case.
4. Compute normalized least-squares misfit.
5. Rank candidates by misfit.
6. Report best candidate, next distinct-radius candidate, margins, confidence
   labels, ambiguity intervals, and top-k candidates.

### Coordinate Optimizer, Experiments 270-418

Typical command pattern confirmed from run manifests for experiments 270-418.

Truth:

```text
true_x_values_mm = [190, 250, variable_right_x]
true_z_values_mm = [90, 90, 90]
truth_radius_values_mm = [5, 6, 8]
```

Initial state:

```text
initial_x_values_mm = true x values
initial_z_values_mm = [90, 90, 85]
initial_radius_values_mm = [6, 6, 6]
target_indices = [2]
passes = 1
```

The difficult target is index 2, the rightmost bar. Its initial z and radius
are intentionally wrong: true `z=90 mm, r=8 mm`, initial `z=85 mm, r=6 mm`.

Typical search window:

| Parameter | Values | Count | Notes |
| --- | --- | ---: | --- |
| target x | current x + [-2, -1, 0, 1, 2] mm | 5 | local lateral search |
| target z | current z + [0, 5, 10] mm | 3 | from initial 85 gives [85, 90, 95] |
| target radius | current r + [-1, -0.5, 0, 0.5, 1, 1.5, 2] mm | 7 | from initial 6 gives [5, 5.5, ..., 8] |
| total | 5 x 3 x 7 | 105 | per coordinate step |

Observed cases per seed:

```text
noiseXX_seedS: frequency_scale=1.0, time_shift_ps=0, amplitude_scale=1.0,
               noise_fraction=XX, noise_seed=S

source_mismatch_noiseXX_seedS: frequency_scale=1.1, time_shift_ps=-50,
                               amplitude_scale=1.1,
                               noise_fraction=XX, noise_seed=S
```

The coordinate state is updated from the selected `update_case_label`, usually
the source-mismatch noisy row. Confidence is still reported for all cases.

How many FDTD simulations per typical coordinate run:

- Observed data: 2 B-scan solves, one per observed case.
- Candidate synthetics: 105 candidate geometries x 3 modeled frequency scales
  = 315 B-scan solves.
- Diagnostic objective variants do not add FDTD simulations; they filter or
  window existing traces.
- Total: about 317 B-scan solves for a typical 105-candidate, two-case,
  three-source-profile-scale coordinate run.
- Each B-scan contains `sources` A-scans. For the standard four-source runs,
  each B-scan has four A-scans.

Observed runtime for the common 4-source coordinate runs is about 21-24 minutes
per seed on the local NVIDIA GB10 system.

### Multi-Rebar Source-Shape Local Geometry Profile, Experiments 425-434

Confirmed from `run_multi_rebar_local_geometry_profile.py` and experiment
summaries 425-434.

This runner varies one target rebar while keeping neighboring rebars fixed.

Common source-shape settings:

| Parameter | Value |
| --- | --- |
| backend | `gpu-cpml` |
| grid step | 1.0 mm |
| sources | 5 |
| frequency | 1.5 GHz |
| Tx/Rx offset | default 20 mm |
| source frequency scales | [0.9, 1.0, 1.1] |
| source time shifts | [-50, 0, 50] ps |
| ringdown delay | 180 ps |
| ringdown frequency scale | 0.8 |
| fit ringdown coefficient | true |
| objective | base window 1-7 ns, 0.3 ns taper |

Observed cases for dense source-shape runs:

| Case | Observed source |
| --- | --- |
| `nominal` | frequency scale 1.0, shift 0 ps, amplitude 1.0, no noise, no ringdown |
| `ringdown020` | ringdown scale 0.20, no noise |
| `ringdown025_noise10_seed21` | ringdown scale 0.25, 10 percent noise, seed 21 |
| `source_mismatch_ringdown025_noise10_seed13` | frequency scale 1.1, shift -50 ps, amplitude 1.1, ringdown 0.25, 10 percent noise, seed 13 |

How many FDTD simulations per dense source-shape run:

- Observed data: 4 B-scan solves, one per observed case.
- Candidate synthetics: for each candidate geometry and each modeled frequency
  scale, the runner simulates:
  - primary Ricker basis B-scan;
  - delayed ringdown basis B-scan.
- Dense Stage 4C candidate count: 325 geometries.
- Modeled scales: 3.
- Basis wavelets: 2.
- Candidate synthetic B-scan solves: 325 x 3 x 2 = 1950.
- Total B-scan solves: about 1954.
- Each B-scan has 5 A-scans.

This explains progress logs like `25/325`: the progress counter is geometry
candidate progress, not total FDTD B-scan solve count and not total A-scan
count.

### Parameter Bounds And Search Grids

Recent important parameter grids:

| Parameter | Meaning | Lower | Upper | Units | Used in |
| --- | --- | ---: | ---: | --- | --- |
| target x offset | local lateral coordinate around current state | -2 | +2 | mm | coordinate optimizer 270-418 |
| target z offset | local depth coordinate around current state | 0 | +10 | mm | coordinate optimizer 270-418 |
| radius offset | local radius around current state | -1 | +2 | mm | coordinate optimizer 270-418 |
| compact source-shape x | local target x | true-1 | true+1 | mm | 426-430 |
| compact source-shape z | local target z | true-1 | true+1 | mm | 426-430 |
| compact source-shape radius | local target radius | 5.8 | 6.2 | mm | 426-429 |
| high-radius compact radius | include old failure branches | 5.8 | 7.8 | mm | 430 |
| wide x/z source-shape x | local target x | true-2 | true+2 | mm | 431-434 |
| wide x/z source-shape z | local target z | true-2 | true+2 | mm | 431-434 |
| dense source-shape radius | Stage 4C radius sweep | 5.4 | 7.8 | mm | 432-434 |
| source frequency scale | modeled wavelet frequency multiplier | 0.9 | 1.1 | dimensionless | source profiling |
| source time shift | modeled trace shift | -50 | +50 | ps | recent source-shape dense runs |
| ringdown scale | fitted delayed-pulse coefficient ratio | fitted | fitted | dimensionless | source-basis runs |

### Confidence And Identifiability

Confirmed from `inversion/candidate_confidence.py` and aggregate JSON files.

Confidence labels depend on best-vs-next distinct-radius margin:

| Label | Required margin |
| --- | --- |
| strong | absolute margin >= 1.0e-3 and relative margin >= 1.0e-2 |
| moderate | absolute margin >= 5.0e-4 and relative margin >= 5.0e-3 |
| weak | positive margin below moderate thresholds |
| ambiguous | nonpositive margin |

Ambiguity interval:

- Includes candidates within 1.5 percent of the best objective.
- Reports x, z, and radius min/max among near-best candidates.
- A row can be point-correct but still x-ambiguous.

Identifiability lessons:

- Radius can remain strong while lateral x becomes ambiguous. This is the
  close14 high-noise failure mode in experiments 413-418.
- Tight spacing often introduces coupled x/radius competitors, for example
  close25 and close28 under smaller Tx/Rx offset.
- Source-shape mismatch can create a wrong high-radius branch, for example
  `r=7.8 mm` in experiment 421.
- Dense source-shape grids expose shifted-depth/high-radius branches near
  `z=91 mm, r=6.8-7.0 mm`, but these remain secondary in experiments 432-434.

## 8. Model And Computational Architecture Details

### Forward Simulation Architecture

Confirmed from `gpu/fdtd_gpu_v2.py`, `core/materials.py`, `core/geometry.py`,
and `config.py`.

Physics model:

- 2D TMz electromagnetic FDTD.
- Fields: `Ez`, `Hx`, `Hy`.
- Material arrays: `epsilon_r`, `sigma`, `mu_r`, shape `(Nz, Nx)`.
- Air background above concrete.
- Concrete region from z=40 mm downward.
- Steel rebars as circular inclusions with high conductivity.
- Source injection adds to `Ez[src_iz, src_ix]`.
- Receiver samples `Ez[rec_iz, rec_ix]`.
- CPML absorbing boundaries on all sides.

Material constants:

| Material | Relative permittivity | Conductivity |
| --- | ---: | ---: |
| air | 1.0 | 0 S/m |
| concrete | 6.0 | 0.01 S/m |
| steel rebar | 1.0 | 1.0e7 S/m |

Geometry modes:

- `hard`: grid nodes inside the circle become rebar material.
- `subcell`: material properties are blended by subcell circular area
  fractions; conductivity is blended in log space.

Recent experiments 270-434 mostly use `geometry_mode=hard` unless explicitly
stated otherwise.

### Inversion/Search Architecture

Diagram-ready architecture:

```text
candidate x/z/r grid
  -> per-candidate rebar arrays
  -> MaterialModel
  -> GPU FDTD B-scan simulation
  -> source-profile LS or source-basis LS
  -> normalized objective
  -> ranking and confidence report
```

For source-shape coefficient fitting:

```text
candidate geometry
  -> simulate primary basis B-scan
  -> simulate delayed-ringdown basis B-scan
  -> fit [primary_coefficient, ringdown_coefficient] by weighted LS
  -> compute normalized misfit
```

There is no neural-network architecture used in experiments 270-434. Earlier
repository components include adjoint-gradient inversion and detector logic,
but the recent high-confidence local geometry work uses deterministic
candidate-grid physics simulations.

### Detection Architecture

Confirmed from `inversion/rebar_detection.py` and
`run_rebar_detection_pipeline.py`.

Detection pipeline:

```text
observed B-scan
  -> median background removal
  -> envelope image
  -> score candidate Tx-target-Rx hyperbolas
  -> non-maximum suppression
  -> candidate x/z windows
```

Hyperbola travel time uses:

```text
src_x = scan_x
rec_x = scan_x + tx_rx_offset
travel_time = (distance(Tx,target) + distance(target,Rx)) / velocity
```

Velocity is based on concrete relative permittivity. The detector estimates x/z
seed windows only, not radius.

## 9. Experiment Campaign Map, 270-434

| Campaign | Experiment range | Purpose | Geometry | Sources/scans | Noise/seeds | Key technical change | Result | Diagram ideas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| close50 source count | 270-280 | Find minimum source count at 40 mm Tx/Rx offset | [190,250,300] mm, radii [5,6,8] | 3,4,5 Tx/Rx positions | 10 percent, seeds 13/21/34 | Acquisition metadata and source-count comparison | 3 sources failed; 4 and 5 clean; 4 sources selected as practical | Source-count side-by-side B-scan columns; candidate ambiguity chart |
| close50 Tx/Rx offset | 281-289 | Find offset threshold for close50 | same close50 geometry | 4 positions | 10 percent, seeds 13/21/34 | Compare 25/30/35 mm offset | 35 mm robust; 30 mm thin margin; 25 mm failed | Tx/Rx offset schematic, margins vs offset chart |
| spacing under 35 mm offset | 290-305 | Tighten center-right spacing with standard offset | close45, close40, close35, close30 | 4 positions, 35 mm offset | 10 percent, seeds 13/21/34 | Move right bar left while keeping acquisition fixed | close30 tightest clean replicated spacing at 35 mm | Geometry cross-section series with decreasing spacing |
| close25/close28 rescue | 306-323 | Test lower bound and larger-offset rescue | close25 and close28 | 4 positions, 35/40/45 mm offset | 10 percent, seeds 13/21/34 | Increase Tx/Rx offset after ambiguity | close28 and close25 clean at 45 mm, not clean at smaller offsets | Competing-solution diagram: truth vs shifted x/r |
| tangent geometry at 45 mm | 324-335 | Push to physical contact | close20, close15, close14 | 4 positions, 45 mm offset | 10 percent, seeds 13/21/34 | Larger offset resolves tighter spacing | close14 tangent clean at 45 mm | Tangent circular rebars, no gap between r=6 and r=8 circles |
| 45 mm close14 noise boundary | 336-356 | Determine noise limit and test source-count rescue | close14 | 3/4/5/7 positions, 45 mm offset | 15-20 percent, seeds 13/21/34 | Noise bisection and source-count escalation | 15.3125 percent clean; 5/7 sources did not rescue 15.361328125 percent ambiguity | Noise-boundary chart; source-count runtime vs ambiguity |
| 50 mm close14 noise boundary | 357-418 | Test larger-offset rescue and close final boundary | close14 | 4 positions, 50 mm offset | 15.361328125 to 19.642372131347656 percent | 50 mm Tx/Rx offset and fine bisection | 19.642333984375 percent replicated clean; final upper point x-ambiguous | Cutoff-margin plot; 1 mm x-interval schematic |
| staged replay packaging | 419 | Package variable-radius staged pipeline | variable-radius staged cases from earlier runs | replay, no new GPU inversion | seeds 13/21/34 from prior runs | Replay plan with commands | Confirms 7-source focused refinement collapses x intervals | Pipeline diagram: detection -> focus -> joint radius |
| material/source animation packaging | 420 | Visualize known material/source ambiguity branches | single-rebar branches from earlier experiments | animation only | no new optimizer claim | Separate material and source branch comparisons | Visualization package complete | Wavefield comparison panels |
| single-rebar source-shape stress | 421-424 | Test delayed source ringdown | single rebar x=250,z=90,r=6 | 5 positions, 20 mm offset | 0/5/10 percent, seeds 13/21 | Add delayed ringdown, then fit source basis | Old source profile failed at r=7.8; coefficient basis fixed all rows | Source wavelet decomposition; radius profile before/after |
| multi-rebar source-shape compact gates | 425-429 | Scale source-basis fit to multi-rebar local windows | [150,250,350] mm, all r=6 | 5 positions, 20 mm offset | 0/5/10 percent, seeds 13/21 | Fit primary/ringdown basis with local x/z/r | Left/center/right compact windows passed | Three-target cross-section; source-basis pipeline |
| high-radius/wide source-shape gates | 430-431 | Reintroduce old high-radius failure branches | center target in default three-rebar scene | 5 positions | 0/10 percent and source mismatch cases | Include r=7.4/7.8 and wider x/z | True geometry still first; high-radius candidates not near-ties | Candidate landscape around true geometry |
| dense all-target source-shape Stage 4C | 432-434 | Complete dense source-shape local radius coverage | left/center/right targets, all r=6 | 5 positions | nominal, ringdown020, noisy ringdown, source mismatch/noisy ringdown | Dense 5 x 5 x 13 grid with source-basis LS | All three targets passed; secondary z=91,r=6.8-7.0 branch visible but below truth | Three-panel dense radius profiles; secondary-branch overlay |

### Key Aggregate Results For Close-Spacing Campaigns

Confirmed from `coordinate_confidence_aggregate.json` files.

| Experiment | Condition | Truth rows | Labels | x-ambiguity rows | max x interval | min radius margin | mean radius margin |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: |
| 280 | close50, 4 sources, 40 mm Tx/Rx | 6/6 | strong 6 | 0 | 0 mm | 0.004817 | 0.006377 |
| 289 | close50, 4 sources, 35 mm Tx/Rx | 6/6 | strong 6 | 0 | 0 mm | 0.004273 | 0.005188 |
| 305 | close30, 4 sources, 35 mm Tx/Rx | 6/6 | strong 6 | 0 | 0 mm | 0.001496 | 0.002433 |
| 310 | close25, 4 sources, 40 mm Tx/Rx | 6/6 | strong 3, moderate 2, weak 1 | 3 | 1 mm | 0.000488 | 0.001133 |
| 314 | close28, 4 sources, 35 mm Tx/Rx | 6/6 | strong 3, moderate 1, weak 2 | 3 | 1 mm | 0.000283 | 0.000992 |
| 319 | close28, 4 sources, 45 mm Tx/Rx | 6/6 | strong 6 | 0 | 0 mm | 0.002182 | 0.003208 |
| 323 | close25, 4 sources, 45 mm Tx/Rx | 6/6 | strong 6 | 0 | 0 mm | 0.002507 | 0.003648 |
| 335 | close14, 4 sources, 45 mm Tx/Rx | 6/6 | strong 6 | 0 | 0 mm | 0.002574 | 0.003978 |
| 349 | close14, 45 mm, 15.3125 percent noise | 6/6 | strong 6 | 0 | 0 mm | 0.002402 | 0.003744 |
| 356 | close14, 45 mm, source-count rescue test | 6/6 | strong 6 | 4 | 1 mm | 0.001500 | 0.003072 |
| 412 | close14, 50 mm, 19.642333984375 percent noise | 6/6 | strong 6 | 0 | 0 mm | 0.001977 | 0.003251 |

Experiment 418 summarized the final 50 mm noise boundary:

```text
promoted clean endpoint = 19.642333984375 percent RMS
ambiguous upper endpoint = 19.642372131347656 percent RMS
final bracket width = 3.814697265625e-05 percent RMS
failure mode = x interval opens by 1 mm
radius evidence remains strong
```

### Latest Source-Shape Dense Results

Confirmed from experiments 432-434 summary JSON, case-summary CSVs, and figure
notes.

| Experiment | Target | Runtime | Candidate geometries | Candidate rows | Weakest margin | Result |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 432 | center | 10526.3 s | 325 | 1300 | 0.0001813 | true x=250,z=90,r=6 first in all four cases |
| 433 | left | 10486.9 s | 325 | 1300 | 0.0002675 | true x=150,z=90,r=6 first in all four cases |
| 434 | right | 10208.4 s | 325 | 1300 | 0.0002288 | true x=350,z=90,r=6 first in all four cases |

Experiment 434 top-candidate pattern:

- best: `x=350, z=90, r=6.0`;
- nearest competitor: `x=350, z=90, r=6.2`;
- secondary shifted-depth branch: `x=350, z=91, r=6.8-7.0`;
- shifted x candidates appear lower than the adjacent-radius and
  shifted-depth branches.

## 10. Current Best Configuration And Current State

### Confirmed Results

Latest completed experiment:

```text
434_multi_rebar_right_source_shape_basis_fit_stage4c_dense_radius
```

Current best source-shape local geometry configuration:

| Parameter | Value |
| --- | --- |
| geometry | three rebars at x=[150,250,350] mm, z=[90,90,90] mm, r=[6,6,6] mm |
| target coverage | left, center, right completed in dense Stage 4C source-shape runs |
| grid step | 1 mm |
| Tx/Rx offset | 20 mm default |
| sources | 5 scan positions |
| frequency | 1.5 GHz |
| source profile | frequency scales [0.9,1.0,1.1], shifts [-50,0,50] ps |
| source-shape fit | primary plus delayed ringdown basis |
| ringdown basis | 180 ps delay, 0.8 frequency scale |
| dense geometry grid | target x +/- 2 mm, z +/- 2 mm, radius 5.4:7.8:0.2 mm |
| objective | normalized least squares, 1-7 ns mute, 0.3 ns taper |

Current best close-spacing/noise configuration:

| Parameter | Value |
| --- | --- |
| geometry | close14 tangent: x=[190,250,264] mm, z=[90,90,90] mm, r=[5,6,8] mm |
| acquisition | 4 sources, 50 mm Tx/Rx offset |
| clean endpoint | 19.642333984375 percent RMS noise |
| source cases | nominal noisy and source-mismatch noisy rows |
| result | 6/6 truth rows, strong 6, zero x ambiguity at endpoint |
| remaining ambiguity | just above endpoint, lateral x interval opens by 1 mm |

### Likely Interpretations

- Increasing Tx/Rx offset improves lateral separability for close multi-rebar
  geometries more effectively than simply adding more source positions.
- Delayed source ringdown can mimic a larger rebar if the source model cannot
  represent the delayed pulse independently.
- Fitting primary and ringdown source-basis coefficients is the current best
  mitigation for the tested field-like source-shape error.
- The dense source-shape Stage 4C results suggest the old high-radius failure
  branch is suppressed when the source basis is fit, at least in local
  same-radius multi-rebar windows with neighboring bars fixed at truth.

### Unresolved Or Needs Manual Confirmation

- The source-shape branch is still a local geometry sweep with neighboring
  rebars fixed at truth. It is not yet a full detector-to-source-shape
  end-to-end multi-rebar pipeline.
- The source-shape model has one delayed ringdown basis with fixed delay and
  frequency scale. It is not a general arbitrary wavelet inversion.
- The recent experiments are synthetic and two-dimensional.
- Candidate geometry overlap prevention is not a general automatic constraint
  in the local runner; recent grids are manually chosen to avoid invalid or
  irrelevant overlaps except for the intentional tangent close14 case.
- The detector branch estimates x/z seed windows but not radius; radius is
  resolved in subsequent FWI/search stages.

## 11. Visual Generation Specifications

Use clean engineering diagram style. Avoid cartoon style. Use millimeter units.
Unless explicitly showing PML or computational grid, draw the physical domain
only.

### Visual 1: Physical Domain And Coordinate System

- Type: engineering cross-section.
- Purpose: establish coordinate frame.
- Show:
  - physical domain 500 mm wide by 300 mm deep;
  - air layer from z=0 to z=40 mm;
  - concrete from z=40 mm to z=300 mm;
  - concrete surface line at z=40 mm;
  - x axis left-to-right;
  - z axis downward;
  - Tx/Rx markers at z=38 mm.
- Labels:
  - `x [mm]`;
  - `z [mm], positive downward`;
  - `concrete surface z=40 mm`;
  - `antenna height z=38 mm, 2 mm above surface`;
  - `PML excluded from physical drawing`.
- Source values:
  - `config.py`;
  - `core/geometry.py`;
  - `core/utils.py`.

### Visual 2: Default Three-Rebar Geometry

- Type: engineering cross-section.
- Purpose: show baseline three-rebar setup.
- Geometry:
  - circles at x=[150,250,350] mm;
  - z=[90,90,90] mm;
  - radius=6 mm for all;
  - concrete surface at z=40 mm.
- Labels:
  - each rebar index: 0, 1, 2;
  - center coordinates;
  - radius and diameter;
  - 100 mm center-to-center spacing;
  - cover depth 50 mm.
- Corresponds to:
  - `config.py`;
  - source-shape experiments 425-434.

### Visual 3: Variable-Radius Close14 Tangent Geometry

- Type: engineering cross-section.
- Purpose: illustrate physical tangent/contact spacing.
- Geometry:
  - x=[190,250,264] mm;
  - z=[90,90,90] mm;
  - radii=[5,6,8] mm;
  - middle and right circles tangent because spacing=14 mm and radii sum=14 mm.
- Labels:
  - `close14`;
  - `center-right spacing=14 mm`;
  - `r_middle=6 mm`;
  - `r_right=8 mm`;
  - `tangent/contact case`;
  - cover depth 50 mm.
- Corresponds to:
  - experiments 332-418.

### Visual 4: Close-Spacing Geometry Series

- Type: side-by-side cross-section strip.
- Purpose: show how spacing tightens across campaigns.
- Panels:
  - close50: right x=300 mm;
  - close30: right x=280 mm;
  - close25: right x=275 mm;
  - close14: right x=264 mm.
- Keep left x=190 mm and center x=250 mm fixed.
- Use same radii [5,6,8] mm.
- Label which configurations were clean or ambiguous:
  - close50 clean with adequate offset;
  - close30 tightest clean under 35 mm offset;
  - close25 interval-supported unless larger offset;
  - close14 clean with 45/50 mm offset.
- Corresponds to:
  - experiments 270-418.

### Visual 5: Tx/Rx Offset Comparison

- Type: side-by-side antenna schematic.
- Purpose: show why offset is an acquisition parameter.
- Show:
  - same four transmitter x positions [50,178,314,450] mm;
  - Tx at z=38 mm;
  - Rx to right of Tx;
  - offsets 35, 40, 45, 50 mm.
- Labels:
  - `Tx`;
  - `Rx`;
  - `Tx/Rx offset`;
  - `scan_x is Tx x`;
  - `pair midpoint = scan_x + offset/2`.
- Notes:
  - for 50 mm offset at Tx=450 mm, Rx is clipped to about x=499 mm.
- Corresponds to:
  - experiments 281-289;
  - experiments 316-418.

### Visual 6: A-Scan And B-Scan Data Structure

- Type: data schematic.
- Purpose: clarify one source position vs B-scan.
- Show:
  - one Tx/Rx pair produces one A-scan trace over time;
  - multiple Tx/Rx pairs produce a B-scan matrix;
  - matrix axes: time samples vertical, scan/source position horizontal.
- Labels:
  - `A-scan = one trace, shape (nt,)`;
  - `B-scan = stack of traces, shape (nt, n_positions)`;
  - examples:
    - default detection B-scan `(1885,101)`;
    - 1 mm 4-source local run `(3769,4)`;
    - 1 mm 5-source local run `(3769,5)`.
- Corresponds to:
  - `gpu/fdtd_gpu_v2.py`;
  - detection B-scan NPZ files.

### Visual 7: Candidate-Grid Search Pipeline

- Type: flowchart.
- Purpose: show inversion/search architecture.
- Flow:
  - candidate x/z/r grid;
  - geometry builder;
  - GPU FDTD B-scan simulation;
  - source-profile fit;
  - normalized LS objective;
  - ranked top-k candidates;
  - confidence label and ambiguity interval.
- Include:
  - coordinate optimizer grid 5 x 3 x 7 = 105 geometries;
  - dense Stage 4C grid 5 x 5 x 13 = 325 geometries.
- Corresponds to:
  - `run_multi_rebar_coordinate_optimizer.py`;
  - `run_multi_rebar_local_geometry_profile.py`;
  - `inversion/candidate_confidence.py`.

### Visual 8: Source Wavelet And Ringdown Basis

- Type: waveform decomposition diagram.
- Purpose: explain source-shape calibration.
- Show:
  - primary Ricker pulse;
  - delayed ringdown pulse at +180 ps;
  - observed wavelet as primary + scale * ringdown;
  - source-basis fit estimates primary and ringdown coefficients.
- Labels:
  - center frequency 1.5 GHz;
  - ringdown frequency scale 0.8;
  - ringdown scale examples 0.20, 0.25, 0.30.
- Corresponds to:
  - experiments 421-424;
  - `run_single_rebar_source_profiled_polish.py`;
  - `inversion/source_profile.py`.

### Visual 9: Source-Shape Failure And Fix

- Type: before/after comparison panel.
- Purpose: show why source-basis fitting matters.
- Left panel:
  - experiment 421, old source profile;
  - ringdown025 selects r=7.8 mm instead of r=6.0 mm.
- Right panel:
  - experiment 424, source-basis coefficient fit;
  - ringdown020, ringdown030, noisy ringdown rows recover r=6.0 mm.
- Labels:
  - `old amplitude/time/frequency profile`;
  - `primary + ringdown coefficient fit`;
  - `wrong high-radius branch suppressed`.
- Corresponds to:
  - `docs/experiments/50_field_like_source_shape_calibration.md`.

### Visual 10: Dense Stage 4C Source-Shape Candidate Landscape

- Type: three-panel candidate landscape or ranked-candidate schematic.
- Purpose: show all-target dense source-shape result.
- Panels:
  - center target, experiment 432;
  - left target, experiment 433;
  - right target, experiment 434.
- Show:
  - true candidate at z=90, r=6.0;
  - adjacent-radius competitor at z=90, r=6.2;
  - secondary shifted-depth branch around z=91, r=6.8-7.0.
- Labels:
  - candidate grid: x +/- 2 mm, z +/- 2 mm, r=5.4:7.8:0.2 mm;
  - all targets pass;
  - secondary branch remains below truth.
- Corresponds to:
  - experiments 432-434.

### Visual 11: Close14 Noise Boundary

- Type: chart plus small geometry inset.
- Purpose: communicate final noise endpoint.
- Show:
  - close14 tangent geometry inset;
  - x-axis noise percent RMS;
  - clean endpoint at 19.642333984375 percent;
  - ambiguous upper endpoint at 19.642372131347656 percent;
  - ambiguity is 1 mm lateral x interval, not radius.
- Labels:
  - `4 sources`;
  - `50 mm Tx/Rx offset`;
  - `strong radius evidence`;
  - `x interval opens above endpoint`.
- Corresponds to:
  - experiments 357-418;
  - experiment 418 summary.

### Visual 12: Runtime And Simulation Cost

- Type: bar chart or table infographic.
- Purpose: show why experiment design uses staged/dense gates.
- Bars:
  - coordinate optimizer 105 geometries x 2 cases: about 21-24 min;
  - compact source-shape 27 geometries x 4 cases: about 14.6 min;
  - high-radius wide 125 geometries x 4 cases: about 68 min;
  - dense Stage 4C 325 geometries x 4 cases: about 2.8-2.9 h.
- Labels:
  - NVIDIA GB10;
  - GPU FDTD with CPML;
  - B-scan solves vs candidate rows.
- Corresponds to:
  - run summaries 270-434.

## 12. Evidence And Source Grounding

This section lists the main claims and their grounding.

### Confirmed From Code

| Claim | Source file |
| --- | --- |
| Domain is 500 mm x 300 mm with 40 mm air layer | `config.py` |
| Concrete surface is z=40 mm | `config.py`, `core/geometry.py` |
| Tx/Rx z is 38 mm | `config.py` |
| Default Tx/Rx offset is 20 mm | `config.py` |
| `sources` means scan positions | `run_multi_rebar_common_radius_profile.py` |
| Rx x is Tx x plus offset | `build_scan_positions` in `run_multi_rebar_common_radius_profile.py` |
| B-scan shape is `(nt, n_positions)` | `gpu/fdtd_gpu_v2.py` |
| Source is injected into `Ez` and receiver samples `Ez` | `gpu/fdtd_gpu_v2.py` |
| Material arrays are `(Nz, Nx)` with z first, x second | `core/materials.py` |
| Rebar centers are converted from x/z/r mm to `(z,x,r)` meters | `run_multi_rebar_local_geometry_profile.py`, `core/geometry.py` |
| Noise is additive Gaussian with std=fraction*clean RMS | `run_single_rebar_source_profiled_polish.py`, `run_rebar_detection_pipeline.py` |
| Objective is normalized least squares with mute window | `inversion/source_profile.py`, `inversion/adjoint.py` |
| Confidence thresholds and ambiguity interval use 1.5 percent relative window | `inversion/candidate_confidence.py` |
| Source-basis fit uses weighted least squares over primary/ringdown traces | `inversion/source_profile.py` |

### Confirmed From Experiment Notes

| Claim | Source note |
| --- | --- |
| Stage 6 recovered 24/24 but most rows were weak | `docs/experiments/40_stage6_all_target_confidence_synthesis.md` |
| Ambiguity interval reporting was added and became mandatory | `docs/experiments/41_ambiguity_interval_reporting.md` |
| Coordinate optimizer became reporting-first | `docs/experiments/42_reporting_first_coordinate_optimizer.md` |
| Noise seed replication showed point accuracy with weak margins | `docs/experiments/43_coordinate_optimizer_noise_replication.md` |
| Seed-offset stress showed guarded revisit/rescue behavior | `docs/experiments/44_coordinate_optimizer_seed_offset_stress.md` |
| Experiments 270-419 close-spacing and noise boundary campaign | `docs/experiments/45_radius_confidence_objective_matrix.md` |
| Detector-to-FWI pipeline design and earlier single-rebar packaging | `docs/experiments/47_detection_to_fwi_pipeline.md` |
| Handoff matrix and current branch decisions | `docs/experiments/48_research_handoff_matrix.md` |
| Material/source branch visualization scope | `docs/experiments/49_material_source_branch_animation_summary.md` |
| Source-shape calibration experiments 421-424 | `docs/experiments/50_field_like_source_shape_calibration.md` |
| Multi-rebar source-shape basis-fit experiments 425-434 | `docs/experiments/51_multi_rebar_source_shape_basis_fit.md` and experiment 434 figure notes |

### Confirmed From Output Artifacts

Close-spacing aggregates:

- `outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/289_coordinate_confidence_close50_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/305_coordinate_confidence_close30_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/310_coordinate_confidence_close25_sources4_txrx40_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/314_coordinate_confidence_close28_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/319_coordinate_confidence_close28_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/323_coordinate_confidence_close25_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/335_coordinate_confidence_close14_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/349_coordinate_confidence_close14_sources4_txrx45_noise15p3125_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/412_coordinate_confidence_close14_sources4_txrx50_noise19p642333984375_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/418_coordinate_confidence_close14_txrx50_noise_boundary_summary/data/noise_boundary_summary.json`

Source-shape artifacts:

- `outputs/experiments/421_source_shape_ringdown_profiled_replication/data/source_profiled_replication_summary.json`
- `outputs/experiments/424_source_shape_ringdown_basis_fit_matrix/data/source_profiled_replication_summary.json`
- `outputs/experiments/425_multi_rebar_left_source_shape_basis_fit_narrow/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/426_multi_rebar_left_source_shape_basis_fit_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/427_multi_rebar_center_source_shape_basis_fit_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/428_multi_rebar_right_source_shape_basis_fit_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/429_multi_rebar_center_source_shape_basis_fit_hard_noise_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/430_multi_rebar_center_source_shape_basis_fit_high_radius_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/431_multi_rebar_center_source_shape_basis_fit_high_radius_wide_xz/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/432_multi_rebar_center_source_shape_basis_fit_stage4c_dense_radius/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/433_multi_rebar_left_source_shape_basis_fit_stage4c_dense_radius/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/434_multi_rebar_right_source_shape_basis_fit_stage4c_dense_radius/data/multi_rebar_local_geometry_summary.json`

### Inferred But Well Supported

- The word "depth" in many notes maps to absolute z coordinate, not concrete
  cover depth. This is inferred by comparing `config.py` with run manifests:
  rebar `z=90 mm` and concrete surface `z=40 mm` imply 50 mm cover.
- `closeXX` means center-right center spacing in millimeters. This is inferred
  from run manifests where center x remains 250 mm and right x is
  `250 + XX`.
- Source-count runtime scales mostly with number of A-scans in each B-scan, but
  not perfectly linearly because of GPU batch overhead, CPML, Python
  orchestration, and source-profile postprocessing.

### Unresolved / Needs Manual Confirmation Before External Publication

- Whether to call the antenna geometry "bistatic" in external prose. Code uses
  a fixed offset Tx/Rx pair, so "offset bistatic pair" is technically accurate,
  but some GPR communities may use different terminology.
- Whether the 2D cross-section should be described as transverse to infinitely
  long rebars or as a simplified slice. The code represents circular
  cross-sections in 2D; actual 3D bar length is not modeled.
- Whether field/lab source wavelets can be represented well by one delayed
  ringdown basis. Current evidence only covers controlled synthetic ringdown
  cases.
- Whether dense source-shape success with neighboring bars fixed at truth will
  hold in a full end-to-end detector-seeded multi-rebar optimization.
