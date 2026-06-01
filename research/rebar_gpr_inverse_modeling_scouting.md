# Rebar Location, Depth, Diameter, and Radius Estimation from GPR B-Scans

**Focus:** inverse modeling, FDTD/FWI, shape or geometry inversion, hyperbola fitting/migration, dictionary matching, Bayesian/global optimization, and ML methods only when they estimate physical parameters.

**Target use case:** single-rebar cases and 2D cylindrical cross-sections in reinforced concrete.

**Prepared:** 2026-05-28

---

## Executive summary

For a single rebar in concrete, the most practical reusable stack is:

1. **gprMax** for synthetic forward simulation of a cylindrical PEC rebar in concrete.
2. **RGPR**, **GPRPy**, or **lweileeds/hyperbola_recognition** for preprocessing, migration, hyperbola picking, and location/depth baselines.
3. A custom inverse layer over the forward model: dictionary matching, Bayesian optimization, shuffled-complex/global optimization, or full-waveform inversion.
4. Optional ML only when the outputs remain physical: cover depth, lateral position, radius/diameter, concrete permittivity, conductivity/moisture, and source/antenna parameters.

The core identifiability lesson is important: **cover depth and lateral position are much easier than diameter/radius**. Diameter/radius is weakly identifiable from hyperbola curvature alone because concrete velocity, time-zero, source wavelet, antenna offset, SNR, and finite target size are coupled. More credible diameter/radius approaches use waveform matching, amplitude information, polarization, calibrated simulation dictionaries, global/Bayesian optimization, or ML trained on physics-labeled synthetic data and validated against known specimens.

---

## Recommended implementation path

### Stage 1: Build a controlled synthetic benchmark

Use **gprMax** to create a single cylindrical PEC rebar in concrete. Sweep:

- Rebar radius or diameter.
- Cover depth.
- Lateral rebar location.
- Concrete relative permittivity and conductivity.
- Scan step size.
- Source wavelet center frequency.
- Tx-Rx offset.
- Noise level and time-zero perturbation.

Start with a clean 2D-style model before moving to a realistic 3D antenna model.

### Stage 2: Establish geometry-only baselines

Use **RGPR** or **hyperbola_recognition** to estimate:

- Hyperbola apex.
- Lateral rebar position.
- RMS velocity.
- Cover depth.

Treat diameter/radius from geometry-only methods as a weak baseline and test its failure modes against gprMax simulations.

### Stage 3: Add radius-sensitive inversion

Use one of the following objective functions:

- Full B-scan window waveform misfit.
- Apex-centered A-scan waveform misfit.
- Migrated image patch similarity.
- Extracted hyperbola outline matching.
- Amplitude/energy-zone features.
- Hybrid waveform + geometry + amplitude objective.

Search over at least:

- Depth.
- Radius/diameter.
- Concrete permittivity.
- Time-zero shift.
- Source wavelet amplitude/scale.
- Optional conductivity or moisture proxy.

Suggested optimizers:

- Coarse dictionary/grid search.
- Bayesian optimization.
- Shuffled complex evolution or other global optimizer.
- Local least-squares refinement after global search.

### Stage 4: Add ML only after physics baselines

Use ML as either:

- A **surrogate forward model** replacing expensive FDTD inside inversion, or
- A **physical-parameter regressor/classifier** trained on gprMax synthetic data.

Avoid generic object detection unless the output is a physical parameter such as rebar center, cover depth, radius, or standard bar diameter class.

---

## Compact source matrix

| Source | Type | Estimated parameters | Forward model | Inversion / optimizer | Radius/diameter identifiable? | Code/license | Link |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gprMax | code/package | Not an estimator by itself; user specifies/sweeps rebar depth, lateral position, radius/diameter, concrete permittivity/conductivity, antenna offset, waveform. | Finite-difference time-domain (FDTD) solution of Maxwell's equations; 2D-style and 3D setups possible. | None built in; use as forward solver inside dictionary matching, FWI, Bayesian optimization, or ML-data generation. | Yes as controlled ground truth in simulation; identifiability from data depends on waveform calibration, concrete properties, SNR, and acquisition geometry. | Public GitHub; GPL-3.0 license according to repository metadata at the time of scouting. | [link](https://github.com/gprMax/gprMax) |
| gprMax simple 2D examples | code/package | User-controlled geometry and materials; not an estimator. | gprMax FDTD examples. | None. | Useful for synthetic ground truth radius/diameter sweeps. | Part of gprMax documentation/project. | [link](https://docs.gprmax.com/en/latest/examples_simple_2D.html) |
| GprMax-UI | code/package | Same physical parameters as the underlying gprMax model if the user sweeps them. | gprMax underneath. | Not a dedicated inverse solver. | Same as gprMax: useful for controlled simulations, not a radius estimator by itself. | Public GitHub; MIT license according to repository metadata at the time of scouting. | [link](https://github.com/OpenSciML/gprmaxui) |
| RGPR | code/package | Hyperbola apex, RMS velocity, depth; migration velocity; not radius by default. | Processing and geometric hyperbola model, not FDTD. | Interactive/processing-driven hyperbola fitting and migration workflows. | Depth/location yes; radius/diameter not directly solved. | Free/open-source R package; verify exact license from repository/package metadata before redistribution. | [link](https://github.com/emanuelhuber/RGPR) |
| RGPR hyperbola-fitting tutorial | code/package | Vertex/apex position, RMS velocity, depth. | Analytical hyperbola travel-time geometry. | Interactive point picking and curve fitting. | No continuous rebar radius estimate; useful for depth/location and velocity. | Tutorial from RGPR documentation. | [link](https://emanuelhuber.github.io/RGPR/09_RGPR_tutorial_hyperbola_fitting/) |
| GPRPy | code/package | Mainly processing/geometry outputs; not a physical radius estimator by default. | Processing package, not a Maxwell/FDTD model. | Processing workflows, not dedicated FWI or Bayesian inversion. | No direct radius inversion. | Public GitHub; MIT license according to repository metadata at the time of scouting. | [link](https://github.com/NSGeophysics/GPRPy) |
| lweileeds/hyperbola_recognition | code/package | Hyperbola parameters; position/velocity-related quantities after fitting. | Image-domain hyperbola model. | C3 clustering, ML classification, and orthogonal-distance hyperbola fitting. | Good depth/location/velocity baseline; radius only indirect and not robust alone. | Public MATLAB repository; no explicit license was visible in the prior scouting pass. | [link](https://github.com/lweileeds/hyperbola_recognition) |
| Aziz & Alipour 2025, Bayesian-optimized FDTD workflow | code/paper | Radar calibration parameters, dielectric properties, depth/distance-like quantities. | Simplified 1D/2D FDTD radar models. | Bayesian optimization. | Not rebar-radius-specific, but the optimization pattern is reusable. | Paper is open access. Associated code/license should be verified from the paper or repository if used. | [link](https://www.sciencedirect.com/science/article/pii/S2352710225004802) |
| Jazayeri et al. 2019, FWI for rebar diameter in concrete | paper | Rebar depth, position, diameter, concrete electromagnetic properties, source wavelet. | gprMax 3D FDTD synthetic models; real GSSI/Noggin datasets. | Source-waveform estimation, ray-based initial model, and full-waveform inversion. | Yes, with waveform-level inversion and calibrated source/concrete model; much stronger than geometry-only fitting. | No public code found in prior scouting. | [link](https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf) |
| Liu et al. 2018, FWI for cylindrical object radius | paper | Cylinder coordinates, radius/diameter, medium properties, effective source wavelet. | 3D FDTD. | Full-waveform inversion with shuffled complex evolution/global optimization. | Yes, but computationally expensive and strongly dependent on waveform/model accuracy. | No public code found in prior scouting. | [link](https://pubs.geoscienceworld.org/seg/geophysics/article-pdf/83/6/H43/4536142/geo-2017-0815.1.pdf) |
| Patsia et al. 2023, FWI with deep-learning forward modeling | paper | Rebar depth and radius. | Deep-learning surrogate forward solver trained on 3D FDTD simulations. | FWI using the surrogate forward model instead of full FDTD. | Yes; designed specifically to estimate depth and radius faster than conventional FWI. | No public code found in prior scouting. | [link](https://abdn.elsevierpure.com/en/publications/gpr-full-waveform-inversion-with-deep-learning-forward-modeling-a/) |
| Giannakis et al. 2020, ML estimates depth/radius/water content from a single A-scan | paper | Depth, radius, volumetric water content. | gprMax/FDTD-generated training library and ML forward/inverse mapping. | Two neural networks and random forest regression. | Yes, but radius uncertainty is not negligible; paper reports radius uncertainty on the order of millimeters. | No public code found in prior scouting. | [link](https://aura.abdn.ac.uk/server/api/core/bitstreams/ecdeab2f-72da-4a74-81c6-b84ad2f0c097/content) |
| Mechbal & Khamlichi 2017, hyperbola + amplitude post-processing | paper | Wave velocity, apex coordinates, radius, conductivity. | Analytical hyperbola plus diffracted-amplitude model. | Two-stage: Hough/hyperbola fitting first, amplitude-based radius/conductivity post-processing second. | More plausible than curvature-only because amplitude is used; still calibration-sensitive. | No public code found in prior scouting. | [link](https://www.sciencedirect.com/science/article/abs/pii/S0963869517301810) |
| Shihab & Al-Nuaimy 2005, cylindrical radius model | paper | Permittivity, depth, radius. | Analytical hyperbolic signature with finite target radius. | Image processing and curve fitting. | Claimed in controlled cases; later literature warns about nonuniqueness/noise sensitivity. | No public code found in prior scouting. | [link](https://link.springer.com/article/10.1007/s11220-005-0004-1) |
| Ristić et al. 2009, simultaneous cylinder radius and velocity | paper | Cylinder radius and electromagnetic wave velocity. | Analytical hyperbola/radius geometry. | Three-step geometric method over candidate velocities. | Claimed in method, but practical robustness is the concern. | No public code found in prior scouting. | [link](https://www.sciencedirect.com/science/article/abs/pii/S0098300409000661) |
| Xiang, Ou & Rashidi 2020, theoretical hyperbola database / dictionary matching | paper | Rebar depth and size. | Theoretical hyperbola database. | Direct-wave removal, signal reconstruction/separation, outline extraction, matching to theoretical hyperbolas. | Reported size estimation; should be independently validated. | No public code found in prior scouting. | [link](https://arxiv.org/abs/2005.09643) |
| Zatar, Nghiem & Nguyen 2024, automated depth/diameter algorithm | paper | Rebar spacing, depth, diameter. | Theoretical hyperbola / biquadratic travel-time equations. | Automated hyperbola extraction, time-zero and velocity estimation, matching measured and theoretical curves. | Diameter estimated in selected cases; authors note hyperbola shape changes weakly for smaller diameters. | In-house code; data availability restricted/request-based according to paper note in prior scouting. | [link](https://www.mdpi.com/2076-3417/14/13/5808) |
| Chang, Lin & Lien 2009, radius from reflection energy/migration traces | paper | Radius and cover/depth. | Theoretical/physical model for rebar reflections and energy zone behavior. | Digital image processing, migration traces, and power-reflectivity variation in an energy zone. | Claimed radius estimates with relatively small error for tested bars. | No public code found in prior scouting. | [link](https://www.sciencedirect.com/science/article/abs/pii/S0950061808001463) |
| Utsi & Utsi 2004, GPRmax3D diameter simulations | paper | Cover depth and diameter. | GPRmax3D simulations. | Simulation-based interpretation. | Early evidence that diameter can be inferred under controlled conditions. | No public code found in prior scouting. | [link](https://www.researchgate.net/publication/4095680_Measurement_of_reinforcement_bar_depths_and_diameters_in_concrete) |
| Zanzi/Arosio and related dual-polarized diameter methods | paper/method | Diameter and cover/depth. | Scattering/amplitude ratio physics. | Ratio of cross-polarized to co-polarized responses. | More identifiable than standard single co-polarized B-scans, but hardware-dependent. | No public code found in prior scouting. | [link](https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf) |
| Sun, Cheng & Fan 2023, dual-polarized wideband diameter estimation | paper | Diameter. | Scattering-width / wideband spectrum relationship. | Power-ratio method over wideband spectra. | Yes in the reported setup; requires dual-polarized data. | No public code found in prior scouting. | [link](https://www.researchgate.net/publication/318806865_Estimation_of_subsurface_cylindrical_object_properties_from_GPR_full-waveform_inversion) |
| Zhou et al. 2018, GPR + EMI dual sensor | paper | Cover depth and diameter. | GPR hyperbola/apex plus EMI calibration curves. | Constrained search / minimum MSE using GPR cover depth as a constraint. | Much more identifiable because EMI adds diameter sensitivity. | Paper available; code not found in prior scouting. | [link](https://pmc.ncbi.nlm.nih.gov/articles/PMC6163369/) |
| Lei et al. 2020, CNN-LSTM diameter classification | paper/ml | Diameter class rather than continuous radius. | gprMax simulations plus field data. | Hyperbola-region extraction and CNN-LSTM classification. | Yes as discrete diameter classification, not continuous radius regression. | No public repo found in prior scouting. | [link](https://www.mdpi.com/2079-9292/9/11/1804) |
| Park et al. 2021, YOLO-v3 diameter classification | paper/ml | Diameter class. | Processed/migrated GPR images. | YOLO-v3 object detector/classifier. | Yes as image-based class prediction, not physics inversion. | No public repo found in prior scouting. | [link](https://www.mdpi.com/2072-4292/13/10/2011) |
| Khedr, Metawie & Marzouk 2025, YOLOv8 diameter classification | paper/ml | Diameter class. | Image/data-driven. | YOLOv8 transfer learning; compared with Faster R-CNN and YOLOv7. | Diameter class only; not continuous radius inversion. | No public repo found in prior scouting. | [link](https://link.springer.com/article/10.1007/s11709-025-1177-4) |
| Limitations of hyperbola fitting for target radius | paper/caution | Target radius and wave velocity, with focus on ambiguity. | Hyperbola-fitting geometry. | Analytical/numerical sensitivity analysis. | Warns that curvature-only radius estimates are noise-sensitive and nonunique in practical settings. | No public code found in prior scouting. | [link](https://abdn.elsevierpure.com/en/publications/on-the-limitations-of-hyperbola-fitting-for-estimating-the-radius/) |

---

## Detailed source cards

### 1. [gprMax](https://github.com/gprMax/gprMax)

- **Type:** code/package
- **Problem setup:** General electromagnetic GPR simulation; directly suitable for concrete slabs with a single cylindrical PEC rebar target.
- **Estimated physical parameters:** Not an estimator by itself; user specifies/sweeps rebar depth, lateral position, radius/diameter, concrete permittivity/conductivity, antenna offset, waveform.
- **Forward model:** Finite-difference time-domain (FDTD) solution of Maxwell's equations; 2D-style and 3D setups possible.
- **Inversion / optimizer method:** None built in; use as forward solver inside dictionary matching, FWI, Bayesian optimization, or ML-data generation.
- **Antenna / frequency assumptions:** User-defined source/receiver/antenna. Documentation examples include simple 2D PEC cylinder models; concrete/rebar studies often use 1-3 GHz commercial antennas.
- **Whether diameter/radius is identifiable:** Yes as controlled ground truth in simulation; identifiability from data depends on waveform calibration, concrete properties, SNR, and acquisition geometry.
- **Data requirements:** Material model, waveform/antenna setup, grid spacing small enough to resolve target radius, scan step, receiver traces.
- **Code availability / license:** Public GitHub; GPL-3.0 license according to repository metadata at the time of scouting.
- **What we can directly reuse or validate against:** Core reusable forward model. Build synthetic B-scan libraries over radius, depth, permittivity, conductivity, source wavelet, and Tx-Rx offset.

### 2. [gprMax simple 2D examples](https://docs.gprmax.com/en/latest/examples_simple_2D.html)

- **Type:** code/package
- **Problem setup:** Tutorial-style simple 2D GPR examples, including PEC cylindrical targets relevant to a 2D rebar cross-section.
- **Estimated physical parameters:** User-controlled geometry and materials; not an estimator.
- **Forward model:** gprMax FDTD examples.
- **Inversion / optimizer method:** None.
- **Antenna / frequency assumptions:** Defined in the example input file; useful for checking grid resolution and B-scan syntax.
- **Whether diameter/radius is identifiable:** Useful for synthetic ground truth radius/diameter sweeps.
- **Data requirements:** gprMax input files and output traces.
- **Code availability / license:** Part of gprMax documentation/project.
- **What we can directly reuse or validate against:** Use as the quickest starting point for a PEC-cylinder/rebar input file.

### 3. [GprMax-UI](https://github.com/OpenSciML/gprmaxui)

- **Type:** code/package
- **Problem setup:** Graphical/workflow wrapper around gprMax with visualization/interpretation utilities.
- **Estimated physical parameters:** Same physical parameters as the underlying gprMax model if the user sweeps them.
- **Forward model:** gprMax underneath.
- **Inversion / optimizer method:** Not a dedicated inverse solver.
- **Antenna / frequency assumptions:** Same as gprMax input settings.
- **Whether diameter/radius is identifiable:** Same as gprMax: useful for controlled simulations, not a radius estimator by itself.
- **Data requirements:** gprMax-compatible models and outputs.
- **Code availability / license:** Public GitHub; MIT license according to repository metadata at the time of scouting.
- **What we can directly reuse or validate against:** Convenient batch-running/visualization helper if manual gprMax workflows become cumbersome.

### 4. [RGPR](https://github.com/emanuelhuber/RGPR)

- **Type:** code/package
- **Problem setup:** R package for GPR import, processing, visualization, migration, and hyperbola fitting.
- **Estimated physical parameters:** Hyperbola apex, RMS velocity, depth; migration velocity; not radius by default.
- **Forward model:** Processing and geometric hyperbola model, not FDTD.
- **Inversion / optimizer method:** Interactive/processing-driven hyperbola fitting and migration workflows.
- **Antenna / frequency assumptions:** Works with measured B-scans and many data formats; antenna handled through metadata/processing choices.
- **Whether diameter/radius is identifiable:** Depth/location yes; radius/diameter not directly solved.
- **Data requirements:** B-scan traces; suitable preprocessing; known or fit velocity/time-zero.
- **Code availability / license:** Free/open-source R package; verify exact license from repository/package metadata before redistribution.
- **What we can directly reuse or validate against:** Best reusable baseline for preprocessing, migration, velocity picking, hyperbola fitting, and validating depth estimates.

### 5. [RGPR hyperbola-fitting tutorial](https://emanuelhuber.github.io/RGPR/09_RGPR_tutorial_hyperbola_fitting/)

- **Type:** code/package
- **Problem setup:** Worked example of fitting a hyperbola in a GPR profile.
- **Estimated physical parameters:** Vertex/apex position, RMS velocity, depth.
- **Forward model:** Analytical hyperbola travel-time geometry.
- **Inversion / optimizer method:** Interactive point picking and curve fitting.
- **Antenna / frequency assumptions:** Dataset-specific; tutorial is processing-focused.
- **Whether diameter/radius is identifiable:** No continuous rebar radius estimate; useful for depth/location and velocity.
- **Data requirements:** Visible hyperbola in a B-scan; enough picked points along diffraction tail.
- **Code availability / license:** Tutorial from RGPR documentation.
- **What we can directly reuse or validate against:** Use to reproduce a clean baseline before adding radius-sensitive amplitude/waveform inversion.

### 6. [GPRPy](https://github.com/NSGeophysics/GPRPy)

- **Type:** code/package
- **Problem setup:** Python package for GPR processing and visualization.
- **Estimated physical parameters:** Mainly processing/geometry outputs; not a physical radius estimator by default.
- **Forward model:** Processing package, not a Maxwell/FDTD model.
- **Inversion / optimizer method:** Processing workflows, not dedicated FWI or Bayesian inversion.
- **Antenna / frequency assumptions:** Works with common GPR files; antenna assumptions are data-dependent.
- **Whether diameter/radius is identifiable:** No direct radius inversion.
- **Data requirements:** GPR profiles in supported formats.
- **Code availability / license:** Public GitHub; MIT license according to repository metadata at the time of scouting.
- **What we can directly reuse or validate against:** Useful Python-side I/O/visualization/preprocessing layer if avoiding R.

### 7. [lweileeds/hyperbola_recognition](https://github.com/lweileeds/hyperbola_recognition)

- **Type:** code/package
- **Problem setup:** Automatic hyperbola detection and fitting in GPR B-scan images.
- **Estimated physical parameters:** Hyperbola parameters; position/velocity-related quantities after fitting.
- **Forward model:** Image-domain hyperbola model.
- **Inversion / optimizer method:** C3 clustering, ML classification, and orthogonal-distance hyperbola fitting.
- **Antenna / frequency assumptions:** Image/B-scan based; not tied to a single antenna model.
- **Whether diameter/radius is identifiable:** Good depth/location/velocity baseline; radius only indirect and not robust alone.
- **Data requirements:** B-scan image/trace data with visible hyperbola; MATLAB toolboxes.
- **Code availability / license:** Public MATLAB repository; no explicit license was visible in the prior scouting pass.
- **What we can directly reuse or validate against:** Automatic picker/fitter before physical inversion; can replace manual hyperbola picking.

### 8. [Aziz & Alipour 2025, Bayesian-optimized FDTD workflow](https://www.sciencedirect.com/science/article/pii/S2352710225004802)

- **Type:** code/paper
- **Problem setup:** Simplified radar/FDTD modeling for subsurface sensing, material characterization, and depth/distance prediction.
- **Estimated physical parameters:** Radar calibration parameters, dielectric properties, depth/distance-like quantities.
- **Forward model:** Simplified 1D/2D FDTD radar models.
- **Inversion / optimizer method:** Bayesian optimization.
- **Antenna / frequency assumptions:** Validated against commercial GPRs; calibrates center frequency, waveform type, and bistatic separation.
- **Whether diameter/radius is identifiable:** Not rebar-radius-specific, but the optimization pattern is reusable.
- **Data requirements:** Measured or synthetic radar traces and calibration ranges.
- **Code availability / license:** Paper is open access. Associated code/license should be verified from the paper or repository if used.
- **What we can directly reuse or validate against:** Reuse the Bayesian optimization structure and calibration logic; replace the target model with a PEC cylinder/rebar radius parameter.

### 9. [Jazayeri et al. 2019, FWI for rebar diameter in concrete](https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf)

- **Type:** paper
- **Problem setup:** Surface-coupled common-offset B-scans over reinforced concrete; synthetic and real slabs.
- **Estimated physical parameters:** Rebar depth, position, diameter, concrete electromagnetic properties, source wavelet.
- **Forward model:** gprMax 3D FDTD synthetic models; real GSSI/Noggin datasets.
- **Inversion / optimizer method:** Source-waveform estimation, ray-based initial model, and full-waveform inversion.
- **Antenna / frequency assumptions:** Synthetic: about 2.4 GHz nominal and 3 cm Tx-Rx offset. Real examples include GSSI 2.6 GHz and Noggin 1000 MHz cases.
- **Whether diameter/radius is identifiable:** Yes, with waveform-level inversion and calibrated source/concrete model; much stronger than geometry-only fitting.
- **Data requirements:** Good B-scans, wavelet/source estimation, concrete velocity/permittivity estimate, initial model, FDTD/FWI compute budget.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** One of the strongest validation targets. Reproduce synthetic cases in gprMax and compare diameter error before/after waveform inversion.

### 10. [Liu et al. 2018, FWI for cylindrical object radius](https://pubs.geoscienceworld.org/seg/geophysics/article-pdf/83/6/H43/4536142/geo-2017-0815.1.pdf)

- **Type:** paper
- **Problem setup:** Subsurface cylindrical objects from common-offset GPR.
- **Estimated physical parameters:** Cylinder coordinates, radius/diameter, medium properties, effective source wavelet.
- **Forward model:** 3D FDTD.
- **Inversion / optimizer method:** Full-waveform inversion with shuffled complex evolution/global optimization.
- **Antenna / frequency assumptions:** Generic common-offset GPR; not concrete-only.
- **Whether diameter/radius is identifiable:** Yes, but computationally expensive and strongly dependent on waveform/model accuracy.
- **Data requirements:** B-scan data, calibrated wavelet, reasonable search bounds, FDTD simulations.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Very relevant algorithmic template for global optimization over radius/depth/permittivity/wavelet.

### 11. [Patsia et al. 2023, FWI with deep-learning forward modeling](https://abdn.elsevierpure.com/en/publications/gpr-full-waveform-inversion-with-deep-learning-forward-modeling-a/)

- **Type:** paper
- **Problem setup:** Reinforced-concrete slab digital twin; near-real-time inversion for rebar parameters.
- **Estimated physical parameters:** Rebar depth and radius.
- **Forward model:** Deep-learning surrogate forward solver trained on 3D FDTD simulations.
- **Inversion / optimizer method:** FWI using the surrogate forward model instead of full FDTD.
- **Antenna / frequency assumptions:** 3D digital twin of a GSSI 2000 MHz palm antenna.
- **Whether diameter/radius is identifiable:** Yes; designed specifically to estimate depth and radius faster than conventional FWI.
- **Data requirements:** Training simulations covering depth/radius/material ranges; measured B-scans for validation.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Blueprint for a fast neural surrogate: train gprMax-generated B-scan surrogate, then optimize radius/depth.

### 12. [Giannakis et al. 2020, ML estimates depth/radius/water content from a single A-scan](https://aura.abdn.ac.uk/server/api/core/bitstreams/ecdeab2f-72da-4a74-81c6-b84ad2f0c097/content)

- **Type:** paper
- **Problem setup:** Single trace above a rebar, using synthetic and real GPR.
- **Estimated physical parameters:** Depth, radius, volumetric water content.
- **Forward model:** gprMax/FDTD-generated training library and ML forward/inverse mapping.
- **Inversion / optimizer method:** Two neural networks and random forest regression.
- **Antenna / frequency assumptions:** GSSI 1.5 GHz antenna model; cylindrical PEC rebar; radius range 2-25 mm; depth range 0-30 cm.
- **Whether diameter/radius is identifiable:** Yes, but radius uncertainty is not negligible; paper reports radius uncertainty on the order of millimeters.
- **Data requirements:** Apex trace or local traces; synthetic training data covering material/depth/radius range; real validation traces.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Good training-range reference for physical-parameter ML. Extend from single A-scan to local B-scan patch.

### 13. [Mechbal & Khamlichi 2017, hyperbola + amplitude post-processing](https://www.sciencedirect.com/science/article/abs/pii/S0963869517301810)

- **Type:** paper
- **Problem setup:** Rebar radius estimation from raw B-scan data.
- **Estimated physical parameters:** Wave velocity, apex coordinates, radius, conductivity.
- **Forward model:** Analytical hyperbola plus diffracted-amplitude model.
- **Inversion / optimizer method:** Two-stage: Hough/hyperbola fitting first, amplitude-based radius/conductivity post-processing second.
- **Antenna / frequency assumptions:** Generic GPR B-scan over rebar.
- **Whether diameter/radius is identifiable:** More plausible than curvature-only because amplitude is used; still calibration-sensitive.
- **Data requirements:** Raw amplitudes, visible hyperbola, preprocessing preserving amplitude, velocity estimate.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Good lightweight baseline: fit hyperbola for geometry/velocity, then use amplitude/waveform features for radius.

### 14. [Shihab & Al-Nuaimy 2005, cylindrical radius model](https://link.springer.com/article/10.1007/s11220-005-0004-1)

- **Type:** paper
- **Problem setup:** Buried cylindrical target in a controlled test site; radargram fitting.
- **Estimated physical parameters:** Permittivity, depth, radius.
- **Forward model:** Analytical hyperbolic signature with finite target radius.
- **Inversion / optimizer method:** Image processing and curve fitting.
- **Antenna / frequency assumptions:** Generic GPR; controlled test site.
- **Whether diameter/radius is identifiable:** Claimed in controlled cases; later literature warns about nonuniqueness/noise sensitivity.
- **Data requirements:** Clear hyperbola, known or estimable permittivity/velocity, controlled acquisition.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Useful historical 2D cylindrical geometry formula; validate cautiously against gprMax synthetics.

### 15. [Ristić et al. 2009, simultaneous cylinder radius and velocity](https://www.sciencedirect.com/science/article/abs/pii/S0098300409000661)

- **Type:** paper
- **Problem setup:** Generic buried cylindrical object in B-scan.
- **Estimated physical parameters:** Cylinder radius and electromagnetic wave velocity.
- **Forward model:** Analytical hyperbola/radius geometry.
- **Inversion / optimizer method:** Three-step geometric method over candidate velocities.
- **Antenna / frequency assumptions:** Generic GPR.
- **Whether diameter/radius is identifiable:** Claimed in method, but practical robustness is the concern.
- **Data requirements:** Clear B-scan hyperbola and sufficient points on the reflection curve.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Pure geometry-only baseline against synthetic gprMax data, especially single-cylinder cases.

### 16. [Xiang, Ou & Rashidi 2020, theoretical hyperbola database / dictionary matching](https://arxiv.org/abs/2005.09643)

- **Type:** paper
- **Problem setup:** Rebar detection/estimation from GPR B-scans using theoretical hyperbola database matching.
- **Estimated physical parameters:** Rebar depth and size.
- **Forward model:** Theoretical hyperbola database.
- **Inversion / optimizer method:** Direct-wave removal, signal reconstruction/separation, outline extraction, matching to theoretical hyperbolas.
- **Antenna / frequency assumptions:** GPR B-scan over reinforced concrete.
- **Whether diameter/radius is identifiable:** Reported size estimation; should be independently validated.
- **Data requirements:** Good B-scan preprocessing, hyperbola outline extraction, template database over parameter ranges.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Directly implementable dictionary-matching idea: generate templates over depth/radius/velocity and match extracted outlines.

### 17. [Zatar, Nghiem & Nguyen 2024, automated depth/diameter algorithm](https://www.mdpi.com/2076-3417/14/13/5808)

- **Type:** paper
- **Problem setup:** Four reinforced-concrete slab specimens with different bar diameters and layouts.
- **Estimated physical parameters:** Rebar spacing, depth, diameter.
- **Forward model:** Theoretical hyperbola / biquadratic travel-time equations.
- **Inversion / optimizer method:** Automated hyperbola extraction, time-zero and velocity estimation, matching measured and theoretical curves.
- **Antenna / frequency assumptions:** 1.6 GHz antenna; 58 mm Tx-Rx offset; #3-#8 bars.
- **Whether diameter/radius is identifiable:** Diameter estimated in selected cases; authors note hyperbola shape changes weakly for smaller diameters.
- **Data requirements:** B-scans from RC slabs, time-zero correction, velocity estimate, automated hyperbola extraction.
- **Code availability / license:** In-house code; data availability restricted/request-based according to paper note in prior scouting.
- **What we can directly reuse or validate against:** Good practical validation paper for #3-#8 bar diameter/depth with a known antenna offset.

### 18. [Chang, Lin & Lien 2009, radius from reflection energy/migration traces](https://www.sciencedirect.com/science/article/abs/pii/S0950061808001463)

- **Type:** paper
- **Problem setup:** Reinforcing bars in concrete.
- **Estimated physical parameters:** Radius and cover/depth.
- **Forward model:** Theoretical/physical model for rebar reflections and energy zone behavior.
- **Inversion / optimizer method:** Digital image processing, migration traces, and power-reflectivity variation in an energy zone.
- **Antenna / frequency assumptions:** Controlled concrete/rebar experiments.
- **Whether diameter/radius is identifiable:** Claimed radius estimates with relatively small error for tested bars.
- **Data requirements:** Amplitude-preserving GPR data, migration/energy-zone extraction, controlled calibration.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Useful validation target for amplitude/energy-zone diameter methods.

### 19. [Utsi & Utsi 2004, GPRmax3D diameter simulations](https://www.researchgate.net/publication/4095680_Measurement_of_reinforcement_bar_depths_and_diameters_in_concrete)

- **Type:** paper
- **Problem setup:** Rebar depths and diameters in concrete; simulation and measurement comparison.
- **Estimated physical parameters:** Cover depth and diameter.
- **Forward model:** GPRmax3D simulations.
- **Inversion / optimizer method:** Simulation-based interpretation.
- **Antenna / frequency assumptions:** Simulations for multiple center frequencies; compared with real high-frequency GPR measurements.
- **Whether diameter/radius is identifiable:** Early evidence that diameter can be inferred under controlled conditions.
- **Data requirements:** Simulated and measured GPR responses for known rebars.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Historical benchmark and motivation for gprMax simulation studies.

### 20. [Zanzi/Arosio and related dual-polarized diameter methods](https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf)

- **Type:** paper/method
- **Problem setup:** Diameter estimation using co-polarized and cross-polarized GPR amplitudes.
- **Estimated physical parameters:** Diameter and cover/depth.
- **Forward model:** Scattering/amplitude ratio physics.
- **Inversion / optimizer method:** Ratio of cross-polarized to co-polarized responses.
- **Antenna / frequency assumptions:** Requires dual-polarized acquisition; frequency depends on system.
- **Whether diameter/radius is identifiable:** More identifiable than standard single co-polarized B-scans, but hardware-dependent.
- **Data requirements:** Dual-polarized GPR data with calibrated amplitudes.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Important caveat: may not transfer to ordinary single-polarization commercial B-scans.

### 21. [Sun, Cheng & Fan 2023, dual-polarized wideband diameter estimation](https://www.researchgate.net/publication/318806865_Estimation_of_subsurface_cylindrical_object_properties_from_GPR_full-waveform_inversion)

- **Type:** paper
- **Problem setup:** Rebar diameter estimation from perpendicular/parallel polarized reflected signals.
- **Estimated physical parameters:** Diameter.
- **Forward model:** Scattering-width / wideband spectrum relationship.
- **Inversion / optimizer method:** Power-ratio method over wideband spectra.
- **Antenna / frequency assumptions:** Dual-polarized antennas; simulations and experiments across media/depths/diameters.
- **Whether diameter/radius is identifiable:** Yes in the reported setup; requires dual-polarized data.
- **Data requirements:** Dual-polarized wideband traces, calibrated spectra, known/controlled acquisition.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Strong physical method if dual-polarized data are available; lower relevance for ordinary B-scans.

### 22. [Zhou et al. 2018, GPR + EMI dual sensor](https://pmc.ncbi.nlm.nih.gov/articles/PMC6163369/)

- **Type:** paper
- **Problem setup:** Rebar diameter and cover thickness using GPR plus electromagnetic induction.
- **Estimated physical parameters:** Cover depth and diameter.
- **Forward model:** GPR hyperbola/apex plus EMI calibration curves.
- **Inversion / optimizer method:** Constrained search / minimum MSE using GPR cover depth as a constraint.
- **Antenna / frequency assumptions:** Requires GPR plus EMI sensor; not GPR-only.
- **Whether diameter/radius is identifiable:** Much more identifiable because EMI adds diameter sensitivity.
- **Data requirements:** Matched GPR and EMI measurements, calibration specimens/curves.
- **Code availability / license:** Paper available; code not found in prior scouting.
- **What we can directly reuse or validate against:** Useful upper-bound/validation idea if another sensor is allowed.

### 23. [Lei et al. 2020, CNN-LSTM diameter classification](https://www.mdpi.com/2079-9292/9/11/1804)

- **Type:** paper/ml
- **Problem setup:** Single cylindrical target/rebar patches from GPR B-scans.
- **Estimated physical parameters:** Diameter class rather than continuous radius.
- **Forward model:** gprMax simulations plus field data.
- **Inversion / optimizer method:** Hyperbola-region extraction and CNN-LSTM classification.
- **Antenna / frequency assumptions:** Simulated concrete rebars with diameters 6-24 mm and cover 30-130 mm; field data included one rebar in dry sand.
- **Whether diameter/radius is identifiable:** Yes as discrete diameter classification, not continuous radius regression.
- **Data requirements:** Labeled simulated/field B-scan patches and standard bar-size classes.
- **Code availability / license:** No public repo found in prior scouting.
- **What we can directly reuse or validate against:** ML baseline if classifying standard bar sizes rather than regressing radius.

### 24. [Park et al. 2021, YOLO-v3 diameter classification](https://www.mdpi.com/2072-4292/13/10/2011)

- **Type:** paper/ml
- **Problem setup:** Rebar diameter prediction from B-scan and migrated GPR images.
- **Estimated physical parameters:** Diameter class.
- **Forward model:** Processed/migrated GPR images.
- **Inversion / optimizer method:** YOLO-v3 object detector/classifier.
- **Antenna / frequency assumptions:** GPR Live system, 0.2-4.0 GHz range; experiments in air.
- **Whether diameter/radius is identifiable:** Yes as image-based class prediction, not physics inversion.
- **Data requirements:** Labeled B-scan/migrated images.
- **Code availability / license:** No public repo found in prior scouting.
- **What we can directly reuse or validate against:** Detector/classifier baseline; migrated images reportedly improve diameter classification.

### 25. [Khedr, Metawie & Marzouk 2025, YOLOv8 diameter classification](https://link.springer.com/article/10.1007/s11709-025-1177-4)

- **Type:** paper/ml
- **Problem setup:** Experimental, site, and building GPR data for RC rebar classification.
- **Estimated physical parameters:** Diameter class.
- **Forward model:** Image/data-driven.
- **Inversion / optimizer method:** YOLOv8 transfer learning; compared with Faster R-CNN and YOLOv7.
- **Antenna / frequency assumptions:** Real GPR datasets; detailed acquisition assumptions need paper-level review.
- **Whether diameter/radius is identifiable:** Diameter class only; not continuous radius inversion.
- **Data requirements:** Labeled real B-scan images/classes.
- **Code availability / license:** No public repo found in prior scouting.
- **What we can directly reuse or validate against:** Lower priority for inverse modeling; useful as a modern detection/classification baseline.

### 26. [Limitations of hyperbola fitting for target radius](https://abdn.elsevierpure.com/en/publications/on-the-limitations-of-hyperbola-fitting-for-estimating-the-radius/)

- **Type:** paper/caution
- **Problem setup:** Analysis of limitations/nonuniqueness when estimating radius and velocity from hyperbola fitting.
- **Estimated physical parameters:** Target radius and wave velocity, with focus on ambiguity.
- **Forward model:** Hyperbola-fitting geometry.
- **Inversion / optimizer method:** Analytical/numerical sensitivity analysis.
- **Antenna / frequency assumptions:** Generic GPR hyperbola-fitting context.
- **Whether diameter/radius is identifiable:** Warns that curvature-only radius estimates are noise-sensitive and nonunique in practical settings.
- **Data requirements:** B-scan hyperbola; illustrates why extra waveform/amplitude/polarization constraints are needed.
- **Code availability / license:** No public code found in prior scouting.
- **What we can directly reuse or validate against:** Use as a sanity check: do not overclaim radius from geometry-only fitting.

---

## Identifiability notes for diameter/radius

### What is robust

- Lateral position is usually identifiable from the hyperbola apex.
- Cover depth is identifiable if velocity/permittivity and time-zero are known or estimated.
- Relative velocity/permittivity can be estimated from hyperbola curvature when the target is well isolated and the apex is clear.

### What is weak

- Radius/diameter from hyperbola curvature alone is weak, especially for common rebar diameters below a few centimeters.
- Diameter estimation is sensitive to:
  - Concrete permittivity and moisture.
  - Unknown or drifting time-zero.
  - Antenna offset.
  - Source wavelet and ringing.
  - Migration velocity.
  - Limited bandwidth.
  - Clutter from neighboring rebars, mesh, voids, or slab boundaries.

### What strengthens radius identifiability

- Full waveform matching.
- Calibrated source wavelet.
- Amplitude-preserving preprocessing.
- Known concrete EM properties or simultaneous inversion for them.
- Dual-polarized acquisition.
- Additional sensors such as EMI.
- Synthetic dictionary constrained to realistic bar sizes and cover-depth ranges.
- Physical ML trained on FDTD simulations and validated on known specimens.

---

## Suggested minimal benchmark for a single 2D cylindrical rebar

### Synthetic parameter grid

| Parameter | Suggested initial range |
|---|---:|
| Rebar radius | 3-16 mm |
| Cover depth | 20-150 mm |
| Relative permittivity | 4-12 |
| Conductivity | 0-0.05 S/m |
| Center frequency | 1-3 GHz |
| Tx-Rx offset | 20-80 mm |
| Scan step | 2-10 mm |
| Time-zero shift | small positive/negative perturbations |
| Noise | 0-10 percent relative amplitude |

### Validation metrics

- Lateral position error in mm.
- Cover-depth error in mm.
- Radius/diameter absolute error in mm.
- Radius/diameter class accuracy for standard bar sizes.
- Robustness to wrong permittivity.
- Robustness to time-zero error.
- Robustness to amplitude normalization.
- Runtime per inversion.

### Baseline comparisons

1. Hyperbola apex and curvature fit.
2. Kirchhoff or migration-based depth estimate.
3. Geometry-only finite-radius hyperbola method.
4. Dictionary matching against gprMax simulations.
5. Bayesian/global optimization against gprMax simulations.
6. Surrogate-assisted FWI or ML physical-parameter regression.

---

## Highest-priority sources for immediate reuse

1. **gprMax** — forward simulation and synthetic data generation.
2. **RGPR** — hyperbola fitting, migration, and processing baseline.
3. **lweileeds/hyperbola_recognition** — automatic hyperbola detection/fitting.
4. **Jazayeri et al. 2019** — best FWI validation target for rebar diameter in concrete.
5. **Liu et al. 2018** — global-optimization/FWI template for cylindrical radius.
6. **Patsia et al. 2023** — neural surrogate forward model inside FWI.
7. **Giannakis et al. 2020** — physical-parameter ML for depth/radius/water content.
8. **Xiang et al. 2020** and **Zatar et al. 2024** — theoretical hyperbola/dictionary matching for depth and size.

---

## Reference links

- [gprMax](https://github.com/gprMax/gprMax)
- [gprMax simple 2D examples](https://docs.gprmax.com/en/latest/examples_simple_2D.html)
- [GprMax-UI](https://github.com/OpenSciML/gprmaxui)
- [RGPR](https://github.com/emanuelhuber/RGPR)
- [RGPR hyperbola-fitting tutorial](https://emanuelhuber.github.io/RGPR/09_RGPR_tutorial_hyperbola_fitting/)
- [GPRPy](https://github.com/NSGeophysics/GPRPy)
- [lweileeds/hyperbola_recognition](https://github.com/lweileeds/hyperbola_recognition)
- [Aziz & Alipour 2025, Bayesian-optimized FDTD workflow](https://www.sciencedirect.com/science/article/pii/S2352710225004802)
- [Jazayeri et al. 2019, FWI for rebar diameter in concrete](https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf)
- [Liu et al. 2018, FWI for cylindrical object radius](https://pubs.geoscienceworld.org/seg/geophysics/article-pdf/83/6/H43/4536142/geo-2017-0815.1.pdf)
- [Patsia et al. 2023, FWI with deep-learning forward modeling](https://abdn.elsevierpure.com/en/publications/gpr-full-waveform-inversion-with-deep-learning-forward-modeling-a/)
- [Giannakis et al. 2020, ML estimates depth/radius/water content from a single A-scan](https://aura.abdn.ac.uk/server/api/core/bitstreams/ecdeab2f-72da-4a74-81c6-b84ad2f0c097/content)
- [Mechbal & Khamlichi 2017, hyperbola + amplitude post-processing](https://www.sciencedirect.com/science/article/abs/pii/S0963869517301810)
- [Shihab & Al-Nuaimy 2005, cylindrical radius model](https://link.springer.com/article/10.1007/s11220-005-0004-1)
- [Ristić et al. 2009, simultaneous cylinder radius and velocity](https://www.sciencedirect.com/science/article/abs/pii/S0098300409000661)
- [Xiang, Ou & Rashidi 2020, theoretical hyperbola database / dictionary matching](https://arxiv.org/abs/2005.09643)
- [Zatar, Nghiem & Nguyen 2024, automated depth/diameter algorithm](https://www.mdpi.com/2076-3417/14/13/5808)
- [Chang, Lin & Lien 2009, radius from reflection energy/migration traces](https://www.sciencedirect.com/science/article/abs/pii/S0950061808001463)
- [Utsi & Utsi 2004, GPRmax3D diameter simulations](https://www.researchgate.net/publication/4095680_Measurement_of_reinforcement_bar_depths_and_diameters_in_concrete)
- [Zanzi/Arosio and related dual-polarized diameter methods](https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf)
- [Sun, Cheng & Fan 2023, dual-polarized wideband diameter estimation](https://www.researchgate.net/publication/318806865_Estimation_of_subsurface_cylindrical_object_properties_from_GPR_full-waveform_inversion)
- [Zhou et al. 2018, GPR + EMI dual sensor](https://pmc.ncbi.nlm.nih.gov/articles/PMC6163369/)
- [Lei et al. 2020, CNN-LSTM diameter classification](https://www.mdpi.com/2079-9292/9/11/1804)
- [Park et al. 2021, YOLO-v3 diameter classification](https://www.mdpi.com/2072-4292/13/10/2011)
- [Khedr, Metawie & Marzouk 2025, YOLOv8 diameter classification](https://link.springer.com/article/10.1007/s11709-025-1177-4)
- [Limitations of hyperbola fitting for target radius](https://abdn.elsevierpure.com/en/publications/on-the-limitations-of-hyperbola-fitting-for-estimating-the-radius/)

---

## Notes

- This file is a working research-scouting artifact. Before formal citation in a paper, verify each bibliographic entry, DOI, repository license, and whether any code/data links have changed.
- For implementation, the safest first milestone is not diameter. First validate lateral position and cover depth on a single clean synthetic cylinder. Then add radius only after the velocity/time-zero/wavelet problem is controlled.
