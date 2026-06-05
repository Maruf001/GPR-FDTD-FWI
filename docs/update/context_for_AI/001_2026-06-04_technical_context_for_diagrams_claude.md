# GPR-FDTD-FWI — Technical Context for Diagram Generation

Document: 001 · Date: 2026-06-04 · Author tag: _claude
Purpose: a **self-contained technical reference** for an AI assistant with **no prior context**, written so that it can generate accurate engineering diagrams, geometry cross-sections, antenna/scan schematics, optimization-pipeline diagrams, and campaign visuals. Priority is **technical completeness and correctness**, not narrative.

Grounding convention used throughout:
- **Confirmed from `path:line`** — read directly from the repo.
- **Derived** — computed from confirmed values (formula shown).
- **Inferred** — strongly implied but not a literal constant.
- **UNRESOLVED** — not determinable from the files read; needs manual confirmation.

All file paths are relative to repo root `/home/lam001/Documents/GPR-FDTD-FWI/`.

---

## 1. Project and system overview

**Technical goal.** Simulate ground-penetrating radar (GPR) over reinforced concrete and solve the *inverse* problem: recover the geometry of buried steel reinforcing bars (**rebar**) — each bar's lateral position `x`, depth `z`, and radius `r` — from simulated radar traces.

**What is simulated (forward model).** A 2-D finite-difference time-domain (**FDTD**) electromagnetic solver, **TMz polarization** with field components `Ez, Hx, Hy` on a Yee staggered grid, leapfrog time stepping. Confirmed from `core/fdtd.py:2-12,57-59`. Absorbing boundaries via **CPML** (convolutional perfectly matched layer). Confirmed from `core/fdtd.py:27,62-63`, `config.py:108-116`.

**Physical scene.** A rectangular 2-D cross-section: a thin **air** layer on top, a **concrete** slab below, with circular **steel rebar** cross-sections embedded in the concrete. Materials confirmed from `config.py:23-34`:
- Concrete: `eps_r = 6.0`, `sigma = 0.01 S/m`.
- Steel rebar: `eps_r = 1.0`, `sigma = 1e7 S/m` (effectively a perfect conductor at GPR frequencies).
- Air: `eps_r = 1.0`, `sigma = 0.0`. All `mu_r = 1.0` (`config.py:39`).

**Acquisition.** A surface GPR survey: a transmitter/receiver (**Tx/Rx**) antenna pair is stepped along the surface; at each position one forward simulation produces one time trace (**A-scan**); the traces are stacked into a 2-D image (**B-scan**). See §4–5. Confirmed from `core/scan.py:1-7,82-112`.

**Inverse problem / search strategy.** The production rebar-sizing is **NOT gradient descent / neural training**. It is a **staged coordinate search with source-wavelet profiling**: enumerate a small grid of candidate `(x, z, r)` for one bar at a time, simulate each candidate's B-scan, and score it against the observed B-scan with a normalized least-squares misfit, while fitting a few source-pulse nuisance parameters at each candidate. A gradient-based adjoint-state FWI solver also exists in the repo (`inversion/adjoint.py`) and underpins the original dense/pixel inversion, but the multi-rebar campaigns below use the candidate-search optimizer. Confirmed from `run_multi_rebar_coordinate_optimizer.py`, `inversion/multi_rebar_coordinate.py`, `inversion/source_profile.py`.

**Objective / loss.** Normalized, mute-windowed, trace-space least squares (formula in §7). Confirmed from `inversion/source_profile.py:86-99`.

**Physical parameters recovered.** Per rebar: `x` (lateral, mm), `z` (depth, mm), `r` (radius, mm). Plus per-evaluation source-nuisance parameters (frequency scale, time shift, amplitude, and optionally a ringdown coefficient) that are *fit, not reported as the target*. Confirmed from `inversion/multi_rebar_coordinate.py:64-75`, `inversion/source_profile.py`.

---

## 2. Coordinate system and units

This section is the most important for correct diagrams.

**Axes (physical, in the x–z plane — a vertical cross-section).**
- **x** = horizontal / lateral position along the scan line. Increases to the **right**. Range `0 … 500 mm` (inner domain). Confirmed `config.py:54` (`DOMAIN_X = 0.50 m`).
- **z** = **depth**, increasing **downward** (z = 0 at the top of the model, larger z = deeper). Range `0 … 300 mm`. Confirmed `config.py:55` (`DOMAIN_Z = 0.30 m`) and array convention `[iz, ix]` with iz = depth/row, ix = lateral/col (`core/fdtd.py:7`, `core/materials.py:15-17`).
- The model is a **2-D slice**; rebars are infinite cylinders perpendicular to the slice, so they appear as **circles** in cross-section.

**Vertical layering (depths measured from z = 0, the top of the air layer).** Confirmed from `config.py:57-65`:
- `z = 0 … 40 mm`: **air** (antenna standoff). `AIR_THICKNESS = 0.04 m`.
- `z = 40 mm`: **concrete surface** (`CONCRETE_TOP = 0.04 m`).
- `z = 40 … 300 mm`: **concrete**.
- **Rebar centers at `z = 90 mm`** = 40 mm air + 50 mm cover. `REBAR_COVER = 0.050 m`. **Important for diagrams: 90 mm is from the air-surface top, i.e. only 50 mm below the concrete surface.**
- **Antennas at `z = 38 mm`** = 2 mm above the concrete surface, inside the air. `TX_Z = RX_Z = AIR_THICKNESS - 0.002 = 0.038 m` (`config.py:128-129`).

**Origin.** Physical `(x=0, z=0)` = top-left corner of the **inner** domain. Confirmed via `pos_to_index(pos, d, npml) = round(pos/d) + npml` (`core/utils.py:69`): physical 0 maps to grid index `NPML`, i.e. the PML border sits at negative-equivalent indices outside the physical domain.

**Units used across the project.**
| Quantity | CLI / report unit | Internal unit | Conversion | Source |
| --- | --- | --- | --- | --- |
| x, z, radius | **mm** | meters | `/1000` | `run_multi_rebar_local_geometry_profile.py:154` |
| Tx/Rx offset | **mm** | meters | `/1000` | `run_multi_rebar_coordinate_optimizer.py:587-591` |
| time shift | **ps** | seconds | `×1e-12` | `run_multi_rebar_coordinate_optimizer.py:646` |
| frequency | **GHz** | Hz | `×1e9` | `run_multi_rebar_coordinate_optimizer.py:584` |
| grid spacing | **mm** (`--grid-step-mm`) | meters | `/1000` | `run_single_rebar_inversion.py:87-104` |
| noise level | **fraction / %** of RMS | — | — | `run_single_rebar_source_profiled_polish.py:77-96` |

**Grid units.** Space is discretized into square cells of side `DX = DZ`. **Two grid resolutions are in play:**
- **Config default `2 mm`** (`config.py:88-89`): grid `NX = 280, NZ = 180` (incl. 15-cell PML each side), `NT ≈ 1885` time steps, `DT ≈ 4.246 ps`. Confirmed `config.py:145-148`; Derived.
- **Production runs override to `1 mm`** via `--grid-step-mm 1.0`. Derived (formula `config.py:98-105`, override `run_single_rebar_inversion.py:87-104`): `DT ≈ 2.123 ps`, `NT ≈ 3769`, `NPML = 30`, `NX = 560`, `NZ = 360`. **All experiments 270–434 use the 1 mm grid.** Confirmed from run notes (e.g. `docs/experiments/51_*` commands all pass `--grid-step-mm 1.0`).

**Rebar center coordinate convention.** Internally a rebar is a tuple **`(z_center, x_center, radius)` in meters — z FIRST** (`core/geometry.py:29-33,52-63`). At the CLI/report level it is given as separate `x`, `z`, `r` in mm. (Caution: `build_single_rebar_model` takes `(x_center, z_center, radius)` — x first — a known order-mismatch hazard, `core/geometry.py:82`.)

**Radius / diameter convention.** `radius` is a true physical radius in mm (half the diameter). Rasterized onto the grid by marking every cell whose center lies within distance `r` of the bar center as steel: a cell is steel iff `dz_phys² + dx_phys² ≤ radius_m²` (`core/materials.py:81-86`). So `r = 6 mm` ⇒ 12 mm diameter (a "#4" bar, `config.py:62`); `r = 8 mm` ⇒ 16 mm; `r = 5 mm` ⇒ 10 mm.

**Source/receiver position representation.** Positions are **absolute physical coordinates** (meters internally, mm at CLI), converted to grid indices by `pos_to_index`. The candidate *search* uses **offsets from the current estimate** (mm), not absolute coordinates (§7). Scan positions are absolute x in mm. Confirmed `core/scan.py:88-90`, `inversion/multi_rebar_coordinate.py:41-49`.

**Multiple coordinate systems / mappings.**
1. Physical meters (config, geometry) ↔ 2. CLI millimeters (`×1000`) ↔ 3. grid indices `(iz, ix)` via `round(pos/d) + NPML`. The PML offset means grid index `NPML` = physical 0. Confirmed `core/utils.py:51-74`.

---

## 3. Rebar geometry and structural configurations

The project uses **two distinct 3-rebar scenes** for two different research questions. They must not be conflated.

### 3.1 Default / "wide" scene (equal radii) — used by the source-shape campaign
- 3 bars, same depth `z = 90 mm`, **equal radius `r = 6 mm`**, centers at `x = 150, 250, 350 mm` (100 mm spacing). Symmetric. Confirmed `config.py:70-74` (`REBAR_POSITIONS` → z=0.09 m, x=0.15/0.25/0.35 m), `REBAR_SPACING = 0.100 m` (`config.py:65`).
- This is the **"Stage 4C"** scene used in experiments 425–434.

### 3.2 Variable-radius close-spacing scene — used by the resolution/noise campaign
- 3 bars, same depth `z = 90 mm`, **unequal radii `r = [5, 6, 8] mm`** (left, center, right), centers at `x = [190, 250, 250+N] mm`. Asymmetric. Left and center bars fixed; the **right `r = 8 mm` bar** is moved toward the center bar. Confirmed from run 332 summary: `true_x = [190, 250, 264]`, `true_z = [90,90,90]`, `truth_radius_values_mm = [5, 6, 8]` (`outputs/experiments/332_*/data/multi_rebar_coordinate_optimizer_summary.json`).
- The label `closeN` means the right bar center is `N` mm from the center bar (`x_right = 250 + N`). Confirmed from `docs/update/summary/001_2026-06-02_more_elaborative_update.md:40-47`.

**`closeN` decode table** (right bar center `x = 250 + N`; left=190/r5, center=250/r6 fixed):

| Label | Right bar x (mm) | Center→right gap (mm) | Physical state at r=8 vs r=6 (radii sum = 14 mm) |
| --- | ---: | ---: | --- |
| close50 | 300 | 50 | well separated |
| close45 | 295 | 45 | separated |
| close40 | 290 | 40 | separated |
| close35 | 285 | 35 | separated |
| close30 | 280 | 30 | clean limit @35 mm Tx/Rx |
| close28 | 278 | 28 | transition band |
| close25 | 275 | 25 | ambiguous @40 mm Tx/Rx |
| close20 | 270 | 20 | — |
| close15 | 265 | 15 | clean @45 mm Tx/Rx |
| close14 | 264 | 14 | **tangent** (8 mm + 6 mm radii = 14 mm gap → circles touch) |

### 3.3 Configuration summary table

| Structure | # bars | Center x (mm) | Depth z (mm) | Radii (mm) | Spacing (mm) | Symmetry | Experiments | Recovery difficulty |
| --- | ---: | --- | ---: | --- | --- | --- | --- | --- |
| Wide / Stage-4C | 3 | 150, 250, 350 | 90 | 6, 6, 6 | 100 | symmetric | 425–434 (source-shape); earlier 063–106 | Easy spacing; tests source-shape robustness |
| close50 … close14 | 3 | 190, 250, 250+N | 90 | 5, 6, 8 | left-center 60, center-right = N | asymmetric | 270–418 | Center-right separation is the limiter |
| Single rebar | 1 | 250 | 70–110 (varies) | 4–10 | — | — | 001–062, 107–201 (earlier; baseline, mature) | Solved; radius is the delicate parameter |

Difficulty/ambiguity notes (Confirmed from `docs/experiments/48_research_handoff_matrix.md`, the campaign aggregates, and `docs/update/summary/002_2026-06-04_summary_update_claude.md`):
- **Easy / clean:** wide scene (all source-shape gates pass); close50–close30 at 35 mm Tx/Rx; close15/close14 at 45 mm Tx/Rx (10% noise).
- **Ambiguous:** close25 at 40 mm Tx/Rx (truth selected but 3/6 rows keep a 1 mm lateral interval); close28 at 35 mm (transition band).
- **The recurring near-degeneracy** is a *coupled shift*: truth `(x, r=8)` vs competitor `(x+1, r=7.5)` — a 1 mm lateral move traded against a 0.5 mm radius shrink produces nearly identical data. Confirmed from `docs/update/summary/001_2026-06-02_more_elaborative_update.md:248-256`, and run 332 confidence rows (`next_radius_mm = 7.5` vs `best_radius_mm = 8.0`).

---

## 4. Antenna, source, receiver, and scan setup

### 4.1 What "source" / "number of sources" means — DEFINITIVE

**`--sources N` = N transmitter (scan) positions = N A-scans = N columns of the B-scan.** It is NOT the number of distinct source wavelets (there is one wavelet shape), nor the number of B-scans (one B-scan per model evaluation). Confirmed from:
- `core/scan.py:82-112` — one loop iteration per scan x-position, each runs one forward sim and writes one column `bscan[:, i] = result['trace']`.
- `run_multi_rebar_common_radius_profile.py:118-141,154-164` — `simulate_bscan` returns `(NT, len(scan_positions))`; `len(scan_positions) = N sources`.

### 4.2 Tx/Rx geometry — common-offset bistatic pair

- **Bistatic, fixed-offset**: at each scan position, transmitter at lateral `x`, receiver at `x + TX_RX_OFFSET` (offset to the +x side). Confirmed `core/scan.py:88-90`, `run_multi_rebar_common_radius_profile.py:133-140`:
  ```
  src_ix = pos_to_index(x_pos, DX, NPML)
  rec_ix = pos_to_index(x_pos + tx_rx_offset_m, DX, NPML)   # Rx = Tx + offset
  ```
- Both antennas at the **same depth** `z = 38 mm` (2 mm above concrete surface, in air). `src_iz = pos_to_index(TX_Z)`, `rec_iz = pos_to_index(RX_Z)`, with `TX_Z = RX_Z = 0.038 m`. Confirmed `core/scan.py:48-49`, `config.py:128-129`.
- Tx and Rx **move together** across the scan (common-offset survey). The receiver index is clamped to stay inside the domain: `rec_ix = min(rec_ix, NX - NPML - 1)` (`run_multi_rebar_common_radius_profile.py:139`).
- **Tx/Rx offset values used:** config default **20 mm** (`config.py:125`); experiments sweep **20, 25, 30, 35, 40, 45, 50 mm** via `--tx-rx-offset-mm` (Confirmed from experiment folder names 281–417 and `run_multi_rebar_coordinate_optimizer.py:513`). The offset is the **dominant lever** for separating close bars (§9).

### 4.3 Scan line geometry (how N sources map to x-positions)

- The full candidate aperture is **x = 50 mm → 450 mm in 8 mm steps** (51 nodes). This 8 mm step is **`cfg.INVERSION_SCAN_STEP = 0.008 m` and is hardcoded — it is NOT changed by `--grid-step-mm`.** Confirmed `config.py:122-124,140`, `run_multi_rebar_common_radius_profile.py:125`, `run_multi_rebar_coordinate_optimizer.py:587-591`.
- `--sources N` **evenly subsamples** the 51 nodes by index: `idx = unique(linspace(0, 50, N, int))`. Confirmed `run_multi_rebar_common_radius_profile.py:126-131`. Derived realized positions:

| `--sources` | Scan x-positions (mm) | Spacing pattern |
| ---: | --- | --- |
| 3 | 50, 250, 450 | ~200 mm |
| 4 | 50, 178, 314, 450 | ~128 mm |
| 5 | 50, 146, 250, 346, 450 | ~96 mm |
| 7 | 50, 114, 178, 250, 314, 378, 450 | ~64 mm |

(These match the experiment notes, e.g. "7 sources at 50, 114, 178, 250, 314, 378, 450 mm".) The default config scan (`SCAN_STEP = 4 mm`, ~100 positions) is used only by the legacy `Scanner` (`config.py:124`, `core/scan.py:39-41`); the multi-rebar campaigns use the 8 mm / N-source subsampling.

### 4.4 Source wavelet

- **Ricker wavelet** (2nd derivative of a Gaussian; zero DC). Confirmed `core/source.py:35-38`:
  ```
  t_delay = 1 / f_center
  tau     = t - t_delay
  arg     = (pi * f_center * tau)^2
  w(t)    = (1 - 2*arg) * exp(-arg)
  ```
  Peak/delay `t0 = 1/f_center`. Time axis `t = arange(NT) * DT` (`core/source.py:61-63`).
- **Center frequency `f_center = 1.5 GHz`.** Confirmed `config.py:48`, and `--frequency-ghz 1.5` default (`run_multi_rebar_coordinate_optimizer.py:514`).
- **Source injection** is a **soft (additive)** point source into `Ez` at the Tx cell: `Ez[src_iz, src_ix] += source_val` each step. Confirmed `core/fdtd.py:105-115`.

### 4.5 Time window, grid, boundaries (numerical setup)

| Parameter | 2 mm grid (config default) | 1 mm grid (production runs) | Source |
| --- | --- | --- | --- |
| Cell size DX=DZ | 2 mm | 1 mm | `config.py:88-89` / override |
| Time step DT | 4.246 ps | 2.123 ps (Derived) | `config.py:98-99` |
| Time steps NT | 1885 | 3769 (Derived) | `config.py:105` |
| Total time T_MAX | 8 ns | 8 ns | `config.py:104` |
| PML cells NPML | 15 | 30 (Derived) | `config.py:112` |
| Grid NX × NZ | 280 × 180 | 560 × 360 (Derived) | `config.py:147-148` |
| Courant factor | 0.9 | 0.9 | `config.py:98` |
| CPML order / κ_max / α_max | 3 / 5.0 / 0.05 | same | `config.py:113-115` |

### 4.6 Diagram-ready interpretation (how to draw the acquisition)

Draw a **vertical cross-section** (x horizontal, z increasing downward):
1. **Domain rectangle**: width 500 mm (x: 0→500), height 300 mm (z: 0→300). Optionally show a hatched PML border ~30 mm thick on all four outer edges (label "CPML absorbing boundary").
2. **Air layer**: top band `z = 0…40 mm` (light). **Concrete surface line** at `z = 40 mm`. **Concrete**: `z = 40…300 mm` (gray).
3. **Rebars**: circles centered at `z = 90 mm` (50 mm below the concrete surface). For the wide scene, three equal circles (r = 6 mm) at x = 150, 250, 350 mm. For the close scene, three circles r = 5/6/8 mm at x = 190/250/(250+N).
4. **Antennas**: a **Tx marker and an Rx marker** as two small boxes just above the concrete surface at `z = 38 mm`, separated horizontally by the **Tx/Rx offset** (e.g. 35 mm), Rx to the right of Tx. Label the offset.
5. **Scan**: a horizontal **scan path/arrow along +x** at `z ≈ 38 mm` spanning x = 50→450 mm; mark the **N source positions** as ticks (e.g. for N=4: 50, 178, 314, 450 mm). Show the Tx/Rx pair as "stepping" along this path.
6. Label: x (mm), z (mm, downward = depth), radii, spacing, Tx/Rx offset, f = 1.5 GHz Ricker.

---

## 5. Data products: A-scan, B-scan, and simulation outputs

- **A-scan** = a single recorded time trace: `Ez(t)` sampled at the receiver cell over all `NT` time steps. Shape `(NT,)`, float64, variable `trace`. Confirmed `core/fdtd.py:143-190` (`run(...)` returns `{'trace': trace, ...}` with `trace[n] = Ez[rec_iz, rec_ix]`). **One source/scan position ⇒ one A-scan.**
- **B-scan** = the stack of A-scans across scan positions. Shape **`(NT, n_scans)`** (rows = time samples, columns = scan x-positions), float64, variable `bscan`. Confirmed `core/scan.py:79,103`, `run_multi_rebar_common_radius_profile.py:160-163`.
  - **Axes for plotting a B-scan**: vertical = two-way travel time (0 → 8 ns, increasing downward), horizontal = scan x-position (50 → 450 mm). Each buried bar appears as a **hyperbola** (apex above the bar, arms spreading with antenna offset).
- **How many A-scans / B-scans per evaluation:** `n_scans = N sources` (3–9 in these campaigns); **one B-scan per (model, source-wavelet) pair**. A single candidate geometry evaluation simulates one B-scan per modeled source-frequency scale (×2 if a ringdown basis is used). Confirmed `run_multi_rebar_local_geometry_profile.py:304-311`.
- **Target (observed) vs predicted (modeled) data**: the *observed* B-scan is simulated once from the true model with the (possibly perturbed/noisy) observed wavelet; the *predicted* B-scan is simulated per candidate from the candidate model with the modeled wavelet. The **residual** is `(amplitude·predicted − observed)` inside the mute window. Confirmed `inversion/source_profile.py:96`, `run_multi_rebar_common_radius_profile.py:178-189`.
- **Preprocessing/windowing**: a **time-domain mute window** (cosine-tapered gate, unity ~1.3–6.7 ns, zero before 1 ns / after 7 ns) is applied as a per-time weight before computing misfit — it suppresses the direct air/surface wave and focuses on rebar reflections. Confirmed `inversion/adjoint.py:37-69`, used at `run_multi_rebar_local_geometry_profile.py:761`. Optional **bandpass** filtering is available via objective variants but the default `base` variant applies **no bandpass** (`inversion/objective_variants.py`, default `base:1.0,7.0,0.3,none,none,0.0`). No background subtraction or normalization beyond the misfit's energy normalization (§7). The detector stage (earlier campaigns) does median background removal + Hilbert envelope, but that is the detector, not the FWI objective (`docs/experiments/47_detection_to_fwi_pipeline.md`).
- **Key variable names / shapes** (Confirmed):
  - `bscan` : `(NT, n_scans)` float64.
  - `trace` : `(NT,)` float64 (one A-scan).
  - `Ez, Hx, Hy` : `(NZ, NX)` float64 (field arrays, `core/fdtd.py:57-59`).
  - `epsilon_r, sigma, mu_r` : `(NZ, NX)` float64 (material arrays, `core/materials.py:45-47`).
  - mute `weight` : `(NT,)` float64.

---

## 6. Noise, random seeds, and repeatability

**Noise model — additive Gaussian, scaled to the B-scan RMS.** Confirmed `run_single_rebar_source_profiled_polish.py:77-96`:
```
clean_rms = sqrt(mean(bscan**2))          # global RMS over ALL time samples and traces
noise_std = noise_fraction * clean_rms     # one scalar std for the whole B-scan
noise     = default_rng(seed).normal(0, noise_std, size=bscan.shape)
observed  = clean_bscan + noise            # additive, zero-mean, i.i.d. per sample
```
- **Type:** additive, zero-mean, Gaussian, independent per sample (white).
- **Amplitude definition:** **relative** — `noise_fraction` is a fraction of the **RMS of the entire clean B-scan** (not per-trace, not absolute). E.g. `0.10` = 10% RMS noise; the noise-boundary campaign used values like `0.19642…`.
- **Where applied:** added **once to the observed data** per case, after simulating the clean B-scan. Modeled candidate B-scans are noise-free. Confirmed `run_multi_rebar_common_radius_profile.py:188-189`.
- **Seed:** `numpy.random.default_rng(noise_seed)` — a noise *realization* selector. Fully deterministic given the seed. Confirmed `run_single_rebar_source_profiled_polish.py:86`.

**What seeds control / do NOT control.** Seeds control **only the noise realization** of the observed data. They do **not** change the initial guess, the search start, or the candidate grid (those are deterministic). So a given experiment is deterministic per seed; "stochasticity" enters only through which noise pattern is drawn. Confirmed (no other RNG use in the evaluation path; the candidate grid and update are deterministic, `inversion/multi_rebar_coordinate.py`).

**Seed values used:** `13, 21, 34` are the standard three noise realizations in the multi-rebar campaigns (each run aggregates `3 seeds × 2 observed cases = 6 rows`). Confirmed from folder names and `docs/update/summary/001_2026-06-02_more_elaborative_update.md:114-135`. (The coordinate optimizer's *built-in default* case is noise-free, `nominal:…,0.0,0`, seed 0 — `run_multi_rebar_coordinate_optimizer.py:65`; the campaigns override this with explicit noisy cases.)

**Observed "cases" per seed.** Two per seed: a **nominal** case (frequency scale 1.0, 0 ps, amplitude 1.0) and a **source-mismatch** case (frequency scale 1.1, −50 ps, amplitude 1.1) — both at the same noise level/seed. This tests robustness to an incorrectly-assumed source pulse. Confirmed `run_multi_rebar_local_geometry_profile.py:59-62`.

**Noise / seed effect table.**
| Campaign | Noise level (RMS) | Seed(s) | Seed controls | Observed effect |
| --- | --- | --- | --- | --- |
| Lateral sweep (290–335) | 10% | 13, 21, 34 | noise realization of observed B-scan | Clean recovery down to tangent (close14) at 45 mm Tx/Rx; results consistent across all 3 seeds |
| Noise bisection (336–418) | 15%–19.64% (binary search) | 13, 21, 34 (seed34 led the bracket) | noise realization | Higher noise eventually breaks "clean" via lateral-x ambiguity; clean ceiling **19.642333984375%** at 50 mm Tx/Rx (`outputs/experiments/418_*/data/noise_boundary_summary.json`) |
| Source-shape (425–434) | 0%, 5%, 10% | 13, 21 | noise realization | True radius recovered in all rows; weakest margin 1.813e-4 at 10% noisy ringdown (`docs/experiments/51_*`) |

**Deterministic vs stochastic:** All runs are deterministic given (geometry, acquisition, noise_fraction, seed). The only randomness is the seeded Gaussian noise draw. Confirmed.

---

## 7. Inversion / optimization setup

### 7.1 Parameters optimized

Per target rebar: `x`, `z`, `radius` (mm). The optimizer updates **one bar at a time**; the other bars stay at their current estimate. Confirmed `inversion/multi_rebar_coordinate.py:52-75`.

Per-candidate **source-nuisance parameters** (fit, not the target):
- source **frequency scale** (grid: `0.9, 1.0, 1.1`), source **time shift** (grid: `−80, −50, −25, 0, 25, 50, 80` ps), source **amplitude** (closed-form scalar fit, default on), and optionally a **ringdown coefficient** (linear least-squares; §7.5). Confirmed `run_multi_rebar_coordinate_optimizer.py:529-536`, `inversion/source_profile.py`.

### 7.2 Search strategy (NOT gradient descent)

- **Exhaustive grid evaluation over a local window**, one bar at a time, optional multiple passes, optional guarded "revisit" pass. Confirmed `run_multi_rebar_coordinate_optimizer.py:621-671`, `inversion/multi_rebar_coordinate.py`.
- The candidate window is built as **offsets around the current estimate** (not absolute bounds): `candidate_axis = current_value + each_offset`. Confirmed `inversion/multi_rebar_coordinate.py:41-61`.
- For each candidate geometry: simulate B-scan(s), grid-search the source frequency-scale × time-shift, fit amplitude, compute misfit; rank candidates ascending by misfit. Confirmed `run_multi_rebar_local_geometry_profile.py:247-393`, `inversion/source_profile.py:102-203`.
- **Initial guess (default):** `x = [150, 250, 350]`, `z = [90, 90, 90]`, `r = [6, 6, 6]` mm. Confirmed `run_multi_rebar_coordinate_optimizer.py:519-521`. (In the close-spacing campaign the initial radii are 6 mm and the optimizer recovers the true `[5, 6, 8]`; the detector/assignment stages seed `x`.)

### 7.3 Search-window "bounds" (offsets, mm)

| Parameter | Default offset window | Count | Close-campaign override (target-2 sweep) | Count | Source |
| --- | --- | ---: | --- | ---: | --- |
| x offsets | `−1, 0, 1` | 3 | `−2, −1, 0, 1, 2` | 5 | `run_multi_rebar_coordinate_optimizer.py:524` / run 332 summary |
| z offsets | `−1, 0, 1` | 3 | `0, 5, 10` (downward-biased) | 3 | `:525` / run 332 |
| radius offsets | `−0.4, −0.2, 0, 0.2, 0.4` | 5 | `−1, −0.5, 0, 0.5, 1, 1.5, 2` | 7 | `:526` / run 332 |
| **candidates / target step** | 3×3×5 | **45** | 5×3×7 | **105** | Derived |

**Important — no hard absolute bounds.** There are **no enforced min/max clamps** on absolute `x`, `z`, or `r`; the only limits are the offset window around the current state and the grid extent (UNRESOLVED whether any absolute clamp exists — none found, `run_multi_rebar_coordinate_optimizer.py`). Source params: `frequency_scale > 0`, `amplitude_scale > 0`, `ringdown_frequency_scale > 0`, `noise_fraction ≥ 0`, `tx_rx_offset ≥ 0`, `passes ≥ 1`. Confirmed `run_single_rebar_source_profiled_replication.py:103-108`, `run_multi_rebar_coordinate_optimizer.py:551-554`.

### 7.4 Objective / loss (exact)

Normalized, mute-weighted, trace-space least squares. Confirmed `inversion/source_profile.py:86-99`:
```
misfit = Σ[ W·(a·predicted − observed) ]²  /  Σ[ W·observed ]²
```
where `W` = mute window weight `(NT,)`, sums over **all time samples and all traces** (whole B-scan), `a` = fitted amplitude scale. Dimensionless, ≥ 0. **No explicit regularization** in the candidate-search objective (the dense adjoint FWI in `config.py:135` has `TV_WEIGHT = 0.01` total-variation, but that is the separate gradient solver, not this search). Convergence/stopping: fixed grid + fixed passes (no iterative tolerance); the "result" is the lowest-misfit candidate. Confirmed.

### 7.5 Source-shape (ringdown) basis fit

When `--fit-ringdown-coefficient` is on, the modeled source per frequency scale is a **2-element linear basis**: a primary Ricker B-scan + a delayed "ringdown" Ricker B-scan (ringdown = Ricker at `0.8×` frequency, delayed `180 ps`). The two coefficients are solved by weighted least squares over the full muted trace space (`np.linalg.lstsq`). Reported `source_ringdown_scale = c_ringdown / c_primary`. Confirmed `inversion/source_profile.py:206-287`, `run_multi_rebar_local_geometry_profile.py:273-303`. The 180 ps delay and 0.8 frequency ratio are **fixed** (only the two amplitudes are fit).

### 7.6 Confidence labels, margin, ambiguity intervals

Confirmed `inversion/candidate_confidence.py`, `inversion/frequency_weighting.py:116-153`:
- **Margin** = objective gap between the best candidate and the **next candidate with a *different* radius** (`atol = 1e-9`): `margin_abs = next_radius_misfit − best_misfit`; `margin_rel = margin_abs / |best_misfit|`. It is an **objective-value gap, not a millimeter distance.**
- **Confidence thresholds** (both absolute AND relative must be met): `strong` ⇔ `margin_abs ≥ 1e-3` AND `margin_rel ≥ 1e-2`; `moderate` ⇔ `margin_abs ≥ 5e-4` AND `margin_rel ≥ 5e-3`; else `weak`; `≤ 0` ⇒ `ambiguous`. Confirmed `inversion/candidate_confidence.py:11-44`.
- **Ambiguity interval**: all candidates within **1.5% of the best objective** (`threshold = best_misfit·(1 + 1.5e-2)`) are "still plausible"; the interval is `[min, max]` of their `x` (and `z`, `radius`). A width > 0 means a competing position/radius is not ruled out. Confirmed `inversion/candidate_confidence.py:90-140`.
- **"Clean"** (used in the campaigns) = all rows select truth, all `strong`, all ambiguity widths 0. Confirmed (e.g. run 335 aggregate: `strong=6, x_ambiguity_row_count=0`).

### 7.7 Multi-rebar assignment, ordering, identifiability

- **Assignment / ordering:** the staged pipeline updates targets in a fixed index order (`target_indices = [0,1,2]`); a separate detector→assignment step (earlier campaigns) chooses one seed per physical bar to avoid label-switching/duplicates. Confirmed `run_multi_rebar_coordinate_optimizer.py:621-622`, `docs/experiments/47_*` (assignment by min x-separation).
- **Guarded / broad-ambiguity revisit:** an optional extra pass re-checks a target whose result is weak/broad (rebuilds the radius offsets to span the reported ambiguity interval). Confirmed `inversion/multi_rebar_coordinate.py:96-160`, `run_multi_rebar_coordinate_optimizer.py:747-841`.
- **Identifiability (Confirmed from results):**
  - **Reliable:** lateral `x` and depth `z` are recovered robustly; **radius** is the historically delicate parameter (hard-grid rasterization causes radius "plateaus" where adjacent radii fill identical cells — `core/materials.py:81-86`; mitigated by subcell geometry `core/materials.py:88-133`).
  - **Ambiguous near the limits:** the **coupled `(x, r) ↔ (x+1, r−0.5)`** branch (a 1 mm lateral move vs a 0.5 mm radius shrink) is the persistent near-tie; and in dense grids a **shifted-depth `z≈91, r≈6.8–7.0`** branch appears at ~rank 3 (secondary). Numerically, competing solutions sit within ~0.05–1.5% of the best objective near the limits (the 1.5% ambiguity tolerance is exactly calibrated to flag these). Confirmed `docs/experiments/51_*:604-606`, run 332/335 confidence rows.

---

## 8. Model / architecture details

**This project's "architecture" is a simulation + search pipeline, not a neural network.** There is no trained model, no latent vector, no surrogate net in the production path. (An adjoint-state gradient FWI solver exists — `inversion/adjoint.py`, with TV regularization `config.py:135` — and was used for the early dense/pixel inversion and 3-rebar geometry recovery, but the 270–434 campaigns use the candidate-search optimizer.) Inferred/Confirmed from the code structure.

### 8.1 Forward simulation architecture (per A-scan)

```
material model (eps_r, sigma, mu_r arrays, shape (NZ,NX))
        │  get_update_coefficients → Ca, Cb ;  get_magnetic_coefficient → Dh
        ▼
FDTD time loop over NT steps (leapfrog, TMz):
   update H (Hx,Hy from Ez)  →  CPML correct H  →  update E (Ez from Hx,Hy)
   →  CPML correct E  →  inject soft source Ez[src]+=w[n]  →  record trace[n]=Ez[rec]
        ▼
A-scan trace (NT,)
```
Confirmed `core/fdtd.py:80-141,143-190`, `core/materials.py:135-173`. FDTD update equations: `Ca=(1−loss)/(1+loss)`, `Cb=(dt/eps)/(1+loss)`, `loss=σ·dt/(2·eps)`, `eps=eps0·eps_r`, `Dh=dt/(mu0·mu_r)` (`core/materials.py:135-173`).

### 8.2 Inversion (candidate-search) architecture (per target step)

```
parameter offsets (x,z,r)  →  geometry builder (rasterize circles onto grid)
        →  FDTD B-scan per source-frequency-scale (and ringdown basis)
        →  source profiling (freq-scale × time-shift grid + amplitude/ringdown LS fit)
        →  normalized muted-L2 misfit vs observed B-scan
        →  rank candidates → best (x,z,r) + margin + confidence + ambiguity interval
        →  update one bar's state → next target / next pass / guarded revisit
```
Confirmed `run_multi_rebar_local_geometry_profile.py`, `run_multi_rebar_coordinate_optimizer.py`, `inversion/source_profile.py`, `inversion/candidate_confidence.py`.

### 8.3 Diagram-ready architecture descriptions
- **Forward pipeline:** "parameter vector `(x,z,r)` → geometry builder (circles on a 2-D grid) → FDTD time-stepping → predicted B-scan → muted-L2 loss vs target B-scan → rank/score."
- **Optimization loop:** "for each rebar (one at a time): build a local `(x,z,r)` candidate grid → simulate each → score → pick best → update that bar → repeat for next bar / next pass → guarded revisit if ambiguous."
- **Cross-section:** "concrete block with air layer on top, a Tx/Rx pair scanning along the surface, circular rebar targets at 90 mm depth."

### 8.4 What changed / was kept over experiments
- **Kept:** candidate-search + source-profiling + confidence/ambiguity reporting; 4 sources; 1 mm grid; 1.5 GHz Ricker.
- **Added:** acquisition-aware reporting (Tx/Rx metadata); broad-ambiguity guarded revisit; the **primary+ringdown source-shape basis fit** (experiments 421–434).
- **Rejected/deferred (earlier):** W2/optimal-transport objective, free material inversion, blind multi-frequency averaging, source-count escalation (5/7 didn't help), large free-form source models (the ringdown basis is kept deliberately small/interpretable). Confirmed `docs/experiments/48_research_handoff_matrix.md`.

---

## 9. Experiment campaign map (≈270 → 434)

Standing setup unless noted: 1 mm grid, 1.5 GHz Ricker, `gpu-cpml` backend, candidate-search optimizer, 3 seeds (13/21/34) × 2 cases (nominal + source-mismatch), 10% noise. Confirmed from folder names and `docs/experiments/48,50,51` + `docs/update/summary/002_*`.

| Campaign | Exp range | Purpose | Geometry | Sources / Tx-Rx | Noise / seeds | Key technical change | Result | Diagram ideas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Source-count & offset baseline | 270–289 | Fix source count and Tx/Rx region for close50 | close50 `[5,6,8]` x=[190,250,300] | 3/4/5 src; 20/25/30/35 mm | 10%, s13/21/34 | settle **4 sources + 35 mm** | 4 src robust; 5/7 no help | bar chart: margin vs sources/offset |
| Lateral resolution sweep | 290–335 | Tightest separable spacing | close45→close14 `[5,6,8]` | 4 src; 35→45 mm | 10%, s13/21/34 | widen Tx/Rx as lever | **clean to close30 @35 mm; clean to close14 (tangent) @45 mm** | cross-section series close50→close14; offset comparison 35 vs 45 mm |
| Noise-ceiling bisection | 336–418 | Max tolerable noise at tangent | close14 `[5,6,8]` | 4 src; 45→50 mm | **binary search 15→19.64%**, s13/21/34 (s34 leads) | bisect noise RMS to numerical edge | clean ceiling **19.642333984375% @50 mm**; failure = lateral-x ambiguity (radius stays strong); stopped at FP edge (`418`) | noise-vs-margin convergence curve; clean/ambiguous boundary chart |
| Consolidation | 419–420 | Reproducibility/visuals | variable-radius close60 | — | — | replay plan (15-stage); branch animations | packaging, no new physics | pipeline/replay diagram |
| Single-rebar source-shape | 421–424 | Source "ringdown" robustness | single bar x=250, z=90, r=6 | 5 src; 20 mm | ringdown 0.20/0.25/0.30 + 5/10% noise | **primary+ringdown basis-coefficient fit** | 421 fails (picks r=7.8); 424 basis fit recovers r=6.0 in all rows | wavelet shape (primary vs primary+ringdown); radius-profile fail→fix |
| Multi-rebar source-shape gates | 425–434 | Source-shape with neighbors present | **wide `[6,6,6]`** x=[150,250,350] | 5 src; 20 mm | nominal/ringdown/noise, s13/21 | apply basis fit per target; compact→dense grids | all 3 targets correct (compact); center+left dense pass; right (434) **running**; weakest margin 1.813e-4; high-radius decoys (7.4/7.8) never top | per-target cross-section; radius-profile curves; ringdown coefficient recovery |

Failure modes / what each taught:
- **Lateral sweep:** Tx/Rx offset >> source count as a disambiguation lever; tangent bars are separable with adequate offset. (`docs/experiments/48_*` rows "Close14 tangent…".)
- **Noise bisection:** beyond the noise ceiling the system is *point-correct but x-interval-ambiguous*, never silently wrong; the boundary is fundamentally lateral, not radial. (`outputs/experiments/418_*`.)
- **Source-shape:** an unmodeled ringing source can masquerade as a larger bar (a real field-data risk); a small interpretable basis fixes it; validated with neighbors present (but neighbors fixed at truth). (`docs/experiments/50,51`.)

Compute cost (for "per-cycle" annotations): one forward B-scan ≈ N source-position FDTD solves ≈ ~1 s/source on the GB10 GPU; a coordinate target-step ≈ 105 candidates × 3 frequency-scales ≈ ~315 B-scans ≈ ~23 min; the dense source-shape grids = 325 candidates × (primary+ringdown × 3 scales) ≈ ~2.9 h (`--progress-every 25` → "25/325" checkpoints). Confirmed `docs/experiments/48,51`, run 332 (`elapsed_time_s = 1401`).

---

## 10. Current best configuration and current state

**Latest experiment:** 433 complete (left-target dense source-shape); **434 (right-target dense) is running as of 2026-06-04** (folder created, `data/`/`figures/` empty, no `run_manifest.json` yet). Confirmed by inspection (`outputs/experiments/434_*` empty subdirs; 433 manifest `created_utc = 2026-06-04T21:39:51Z`).

**Best / representative acquisition configuration** (Confirmed from `docs/experiments/48_research_handoff_matrix.md`):
- **4 sources, 45 mm Tx/Rx offset** → cleanly resolves the tightest geometry (close14 tangent) at 10% noise.
- **50 mm Tx/Rx** → extends the clean noise ceiling to **19.642333984375% RMS** for close14.
- **1 mm grid, 1.5 GHz Ricker**, candidate-search optimizer, source-profiling (freq 0.9/1.0/1.1, shift ±80 ps, amplitude fit), confidence + ambiguity reporting mandatory.
- For source-shape robustness: **primary+ringdown basis-coefficient fit** (180 ps delay, 0.8 freq ratio).

**Representative recovered vs target (close14, run 332, seed34):**
- Truth: `x=[190,250,264]`, `z=[90,90,90]`, `r=[5,6,8]`.
- Recovered (target-2 update, both cases): `x=264, z=90, r=8.0`; next radius 7.5; **strong**, margins 2.70e-3 / 5.27e-3; **zero ambiguity width**. Confirmed `outputs/experiments/332_*/data/multi_rebar_coordinate_optimizer_summary.json`.

**Status classification:**
- **Confirmed:** lateral resolution down to tangent (close14) is clean at 45 mm Tx/Rx, 10% noise; noise ceiling ~19.64% at 50 mm; source-shape basis fit recovers radius under ringing for all three targets (compact windows; dense for center+left).
- **Likely interpretation:** the dominant lever is Tx/Rx offset; source-count escalation is not worth the cost; the basis fit should remain a *diagnostic*, not the default production objective.
- **Uncertain / unresolved:** (a) the source-shape gates fix neighbors at truth — not yet a joint multi-bar source-shape inversion; (b) the two hard axes (tight spacing + source ringing) have never been combined; (c) whether 45–50 mm Tx/Rx offsets are physically realizable in field GPR hardware; (d) all results are synthetic, 2-D.

---

## 11. Visual Generation Specifications

Diagram style for all: **clean engineering/schematic style, labeled axes (x in mm horizontal; z in mm increasing downward = depth), metric units, no cartoon styling.** Unless stated, draw a **2-D vertical cross-section** in the x–z plane.

### Visual 1 — Wide three-rebar scene (cross-section)
- Type: engineering cross-section. Corresponds to: Stage-4C / source-shape campaign (exp 425–434).
- Show: domain rectangle 500 mm (x) × 300 mm (z); air band z=0–40 mm; concrete surface line at z=40 mm; concrete z=40–300 mm; **three equal circles r=6 mm (12 mm dia.) at x=150, 250, 350 mm, z=90 mm**; a Tx/Rx pair at z=38 mm; optional 30 mm CPML hatched border.
- Label: x positions (150/250/350), depth 90 mm (and "50 mm cover below surface"), radius 6 mm, spacing 100 mm, f=1.5 GHz.

### Visual 2 — Variable-radius close-spacing scene (cross-section, parametric)
- Type: engineering cross-section. Corresponds to: lateral/noise campaign (exp 270–418).
- Show: same domain; **three circles r=5/6/8 mm at x=190, 250, 250+N mm, z=90 mm** (left small, center medium, right large). Draw at least two panels: `close50` (N=50, x_right=300) and `close14` (N=14, x_right=264, the r=8 and r=6 circles **touching/tangent**).
- Label: x=190/250/(250+N); radii 5/6/8 mm (diameters 10/12/16 mm); center-right gap N mm; note "radii sum 8+6=14 mm → tangent at close14".

### Visual 3 — Tx/Rx offset comparison
- Type: side-by-side schematic. Corresponds to: exp 281–417 (offset is the dominant lever).
- Show: two copies of the surface with a Tx and an Rx marker at z=38 mm; left panel offset **35 mm**, right panel **45 mm** (and/or 50 mm). Rx to the right of Tx.
- Label: Tx, Rx, offset distance, scan direction (+x). Add a caption note: "wider offset → better separation of close bars."

### Visual 4 — Common-offset scan geometry
- Type: cross-section with scan path. Corresponds to: §4.3.
- Show: the surface with the Tx/Rx pair stepping along +x; **N=4 source positions ticked at x=50, 178, 314, 450 mm** (or N=7 at 50/114/178/250/314/378/450); each tick = one A-scan.
- Label: aperture 50–450 mm, "8 mm node grid subsampled to N sources", one A-scan per Tx position.

### Visual 5 — A-scan → B-scan data product
- Type: data schematic / panel. Corresponds to: §5.
- Show: (left) a single A-scan waveform amplitude vs time (0–8 ns); (right) a B-scan image with **vertical axis = time (0–8 ns, down)**, **horizontal axis = scan x (50–450 mm)**, with **hyperbola arcs** over each rebar (apex above the bar). Indicate B-scan shape `(NT, n_scans)`.
- Label: A-scan = Ez(t) at receiver; B-scan = stack of N A-scans; mute window 1–7 ns.

### Visual 6 — Coupled-ambiguity (competing solution) diagram
- Type: comparison panel. Corresponds to: the persistent near-tie (§3.3, §7.7).
- Show: two nearly-identical close-up cross-sections of the right bar: truth `(x=264, r=8.0)` vs competitor `(x=265, r=7.5)`; and a tiny objective-bar comparison showing margin ~2.7e-3 (strong) vs near-tie at the noise ceiling.
- Label: "1 mm lateral shift traded for 0.5 mm radius shrink → nearly identical B-scan."

### Visual 7 — Optimization pipeline (block diagram)
- Type: pipeline/flow diagram. Corresponds to: §8.2.
- Show blocks: parameter offsets (x,z,r) → geometry builder (circles on grid) → FDTD B-scan(s) → source profiling (freq×shift grid + amplitude/ringdown LS) → muted-L2 misfit vs observed → rank + confidence/ambiguity → update one bar → loop (next target / pass / guarded revisit).
- Label: "one bar at a time; 45 or 105 candidates per step; normalized muted-L2 loss."

### Visual 8 — Forward FDTD pipeline (block diagram)
- Type: pipeline. Corresponds to: §8.1.
- Show: material arrays (eps_r, sigma, mu_r) → update coefficients (Ca, Cb, Dh) → leapfrog TMz loop (update H → CPML → update E → CPML → inject soft source → record receiver) → A-scan; repeat over N Tx positions → B-scan.

### Visual 9 — Noise-ceiling bisection convergence
- Type: line/convergence chart. Corresponds to: exp 336–418.
- Show: x-axis = experiment index / bisection step; y-axis = noise RMS %; a curve converging to **19.642333984375%** (clean) with the ambiguous edge at 19.642372%; mark "clean" vs "x-ambiguous" regions; note bracket width 3.8e-5% (numerical edge).

### Visual 10 — Source-shape ringdown fix (fail → fix)
- Type: 2-panel comparison + wavelet inset. Corresponds to: exp 421 (fail) → 424 (fix).
- Show: (inset) modeled wavelet = primary Ricker vs primary+delayed ringdown (180 ps delay, 0.8× frequency); (panel A) radius-misfit curve with old profile selecting r=7.8 mm (wrong); (panel B) with basis fit selecting r=6.0 mm (correct). Label fitted ringdown coefficient (≈0.20/0.25/0.30).

### Visual 11 — Resolution-limit summary chart
- Type: matrix/heatmap or table-chart. Corresponds to: lateral sweep.
- Show: rows = spacing (close50…close14), columns = Tx/Rx offset (35/40/45 mm); cells colored clean (green) / ambiguous (amber); annotate close30@35 mm and close14@45 mm as the clean frontiers.

### Visual 12 — Depth/layer stack legend (reference inset)
- Type: labeled vertical scale. Corresponds to: §2.
- Show: a vertical bar from z=0 to 300 mm with bands: air (0–40), concrete surface line (40), concrete (40–300), antenna line (38), rebar centerline (90); annotate "depth measured from air-surface top; 90 mm = 50 mm below concrete surface."

---

## 12. Evidence and source grounding (consolidated)

| Technical detail | Status | Source |
| --- | --- | --- |
| Materials (concrete 6/0.01, steel 1/1e7, air 1/0, mu_r=1) | Confirmed | `config.py:23-39` |
| f_center = 1.5 GHz, Ricker formula | Confirmed | `config.py:48`, `core/source.py:35-38` |
| Domain 500×300 mm, air 40 mm, cover 50 mm, rebar z=90 mm | Confirmed | `config.py:53-74` |
| Default scene x=150/250/350, r=6, spacing 100 mm | Confirmed | `config.py:65-74` |
| Close scene x=[190,250,264], r=[5,6,8], z=90 (close14) | Confirmed | `outputs/experiments/332_*/data/multi_rebar_coordinate_optimizer_summary.json` |
| 2 mm grid: NX280/NZ180/NT1885/NPML15 | Confirmed | `config.py:145-148` |
| 1 mm production grid: NX560/NZ360/NT3769/NPML30/DT2.123ps | Derived | `config.py:98-105`, `run_single_rebar_inversion.py:87-104` |
| "sources" = Tx/scan positions = A-scans = B-scan columns | Confirmed | `core/scan.py:82-112`, `run_multi_rebar_common_radius_profile.py:154-164` |
| Bistatic common-offset, Rx = Tx + offset, z=38 mm | Confirmed | `core/scan.py:48-49,88-90`, `config.py:128-129` |
| Scan aperture 50–450 mm @ 8 mm; N sources subsample by linspace | Confirmed | `config.py:122-124,140`, `run_multi_rebar_common_radius_profile.py:125-131` |
| Tx/Rx offsets 20–50 mm; dominant lever | Confirmed | folder names 281–417, `docs/experiments/48_*` |
| B-scan shape (NT, n_scans); A-scan = trace (NT,) | Confirmed | `core/scan.py:79,103`, `core/fdtd.py:143-190` |
| Mute window 1–7 ns cosine taper | Confirmed | `inversion/adjoint.py:37-69` |
| Noise = additive Gaussian, std = fraction × clean-B-scan RMS, seeded | Confirmed | `run_single_rebar_source_profiled_polish.py:77-96` |
| Seeds 13/21/34 = noise realizations only | Confirmed | folder names, `docs/update/summary/001_..._more_elaborative_update.md` |
| Objective = normalized muted-L2; no reg in search | Confirmed | `inversion/source_profile.py:86-99` |
| Search = candidate grid (offset windows), one bar at a time | Confirmed | `inversion/multi_rebar_coordinate.py:41-75`, `run_multi_rebar_coordinate_optimizer.py:621-671` |
| Default offsets 3×3×5=45; close override 5×3×7=105 | Confirmed | `run_multi_rebar_coordinate_optimizer.py:524-526`, run 332 |
| No hard absolute x/z/r bounds | Confirmed (absence) | `run_multi_rebar_coordinate_optimizer.py` (no clamp found) |
| Confidence thresholds (strong 1e-3/1e-2; moderate 5e-4/5e-3; ambiguity 1.5%) | Confirmed | `inversion/candidate_confidence.py:11-44,90-140` |
| Margin = best-vs-next-distinct-radius objective gap | Confirmed | `inversion/frequency_weighting.py:116-153` |
| Ringdown basis: primary + 180 ps/0.8× delayed Ricker, lstsq coeffs | Confirmed | `inversion/source_profile.py:206-287`, `run_multi_rebar_local_geometry_profile.py:273-303` |
| Noise ceiling 19.642333984375% @50 mm Tx/Rx (close14) | Confirmed | `outputs/experiments/418_*/data/noise_boundary_summary.json` |
| Source-shape gates pass all 3 targets; weakest margin 1.813e-4 | Confirmed | `docs/experiments/51_*` |
| 434 (right dense) running, not complete | Confirmed (inspection) | empty `outputs/experiments/434_*/{data,figures}`, no manifest |
| Soft source code vs docstring `-Cb` scaling | UNRESOLVED | `core/fdtd.py:105-115` (code adds `source_val` directly) |
| Exact post-1mm-override NPML/NT (uses `_override_grid`) | Derived (not asserted as literal) | `run_single_rebar_inversion.py:87-104` |

**Known caveats for the diagram AI:**
- Depth `z = 90 mm` is from the **air-surface top**, i.e. **50 mm below the concrete surface** — do not place bars 90 mm below the concrete surface.
- z increases **downward**.
- Radius is a true physical radius (diameter = 2r); r=6/5/8 mm ⇒ 12/10/16 mm diameters.
- "sources" are **scan positions**, not wavelets; draw them as Tx-position ticks along the surface.
- The recent campaigns use the **1 mm** grid, not the 2 mm config default.
- Two different 3-bar scenes exist (wide equal-radius vs close variable-radius) — pick the right one per campaign.
