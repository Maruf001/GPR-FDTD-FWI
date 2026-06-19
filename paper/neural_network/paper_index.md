Yes, I understand exactly what you mean. My honest read is:

**You are not reinventing the entire wheel.**
The broad problem of detecting rebars from GPR data is very well studied. People have done hyperbola fitting, migration, FWI, inverse scattering, MIMO acquisition, CNN/YOLO-style detection, synthetic gprMax datasets, and even 3D deep-learning inversion.

But **your exact current formulation is not simply “already solved” in a clean plug-and-play way**. What you are doing is more specific:

> Given a controlled multi-rebar geometry, how close can rebars be before a parametric inversion can no longer confidently separate the true geometry from nearby wrong branches, as a function of Tx/Rx offset, source count, frequency, noise realization, and ambiguity margins?

That is more like a **resolution-limit / identifiability / acquisition-design study**, not merely “detect rebar in GPR.”

## The important distinction

A lot of existing work answers:

> Can we detect rebars?
> Can we locate rebar depth?
> Can we estimate diameter/radius?
> Can a neural network recognize rebar hyperbolas?
> Can FWI improve diameter estimates?

Your work asks something slightly sharper:

> When multiple rebars are close enough that their GPR responses overlap, can we still separate the correct geometry from nearly equivalent alternatives, and can we quantify when the answer becomes ambiguous?

That last part — **truth selected but not clean because a nearby wrong branch is almost as good** — is the interesting part. Many papers report accuracy, detection rate, or mean error, but fewer explicitly build the kind of “near-best competitor / margin / ambiguity interval / multi-seed robustness” framework you are describing.

## What is definitely already known

The field already knows that closely spaced rebars are hard to resolve. This is basic GPR physics. Lateral resolution depends strongly on wavelength, depth, antenna frequency, scan spacing, and clutter/noise. For example, Sensors & Software gives a simple resolution discussion where 1000 MHz data can resolve rebars at 15 cm and 10 cm spacing, is just resolvable around 7 cm, and cannot resolve 3 cm spacing as separate objects in that example. They also emphasize that theoretical resolution is only approximate because noise and clutter make close hyperbolas harder to separate. ([sensoft.ca][1])

The GSSI concrete handbook says similar things from the practical concrete-scanning side: lateral resolution is controlled by wavelength, and in most cases two targets at the same depth separated by less than about 2 inches, or about 5 cm, appear as one object. It also notes that Tx/Rx offset matters in concrete scanning because the transmitter–receiver spacing can be comparable to the target depth. ([GSSI Geophysical Survey Systems, Inc.][2])

That is actually very relevant to your current close25/close28/close30 work. You are testing separations around **25–30 mm**, which is below the rough practical “same-depth targets may merge” regime. So your ambiguity result is not surprising; it is physically meaningful.

## Work that is close to your direction

There is already serious work on **diameter/radius/depth estimation**. Jazayeri et al. used full-waveform inversion of common-offset GPR B-scans for reinforced concrete mapping and reported that FWI improved rebar diameter estimates compared with conventional ray-based methods. Their method used sparse blind deconvolution to estimate the source wavelet, then used a ray-based reflectivity analysis to initialize FWI; they tested synthetic and real cases with 1 and 2.6 GHz antennas and reported diameter errors below 11% for shallow enough cover. ([ScienceDirect][3])

There is also a theoretical-database approach by Xiang, Ou, and Rashidi that directly targets simultaneous rebar depth and size estimation from GPR. They identify/separate hyperbola signals, compare extracted outlines to a database of theoretical hyperbolas, and report strong depth/size accuracy. Importantly, their abstract explicitly mentions extracting outlines from **interlaced hyperbolas**, which is close to your multi-rebar concern. ([arXiv][4])

There is also MIMO-array work. Cheng, Sun, Tan, and Fan use an ultra-wideband MIMO GPR array, diffraction stacking, and a 3 dB drop method to estimate rebar diameter. Their paper explicitly investigates bars with different diameters, depths, and spacing, and argues that MIMO configurations improve resolution and reduce side lobes compared with conventional SISO GPR. ([ScienceDirect][5])

There is inverse-scattering work that is even closer mathematically. Brancaccio 2022 formulates a 2D inverse-scattering problem for metallic bars embedded in a dielectric, using multi-monostatic measurements and a discrete candidate-position formulation. That is very close in spirit to “which candidate geometry is present?” But that paper focuses on detecting/localizing bars; it assumes known dielectric information and simplifies the physics by neglecting mutual coupling between bars. So it is relevant, but not the same as your full “location + radius + ambiguity branch + acquisition limit” study. ([MDPI][6])

## ML / neural network side

The ML side exists too, but much of it is detection/classification rather than physically interpretable inversion.

For example, Xiang et al. used CNN/AlexNet-style recognition for automatic rebar detection and explicitly studied different rebar arrangements, including closely spaced meshes. Their result says dense/uneven rebar arrangements are harder because signal interference increases. ([arXiv][7])

Lei et al. used Faster R-CNN to detect hyperbola regions in GPR B-scans, followed by clustering and hyperbola fitting. That is useful for automatic detection and localization, but again it is mainly image-feature extraction and fitting, not full parametric ambiguity analysis. ([ScienceDirect][8])

There are also more advanced deep-learning GPR inversion/forward-surrogate papers. Dai et al. proposed a deep-learning GPR forward solver that predicts B-scans from subsurface permittivity/conductivity maps; the abstract reports 1.28% mean relative error and a huge speedup compared with classical solvers. ([arXiv][9]) Their group also has 3DInvNet, a deep-learning 3D GPR inversion method with public code/datasets, reconstructing 3D permittivity maps from C-scans. ([arXiv][10])

So your hunch is correct: people have absolutely used optimization, FWI, inverse scattering, MIMO acquisition, and deep learning for closely related GPR/rebar problems.

## Why your Codex direction still makes sense

Your Codex agent is not necessarily going in a useless direction. It seems to be turning the project into a **controlled identifiability benchmark**.

That is different from saying “I invented GPR rebar detection.” You should not claim that.

A better framing would be:

> Existing methods can detect/localize rebars and, in some cases, estimate diameter/depth. Our current work focuses on a controlled multi-rebar resolution-limit study: under a specified GPR-like simulation setup, how close can two rebars be before the inverse problem becomes ambiguous, and how do acquisition choices such as source count and Tx/Rx offset affect that ambiguity?

That is a credible and non-delusional framing.

## The biggest gap I see

I did **not** find, from this search, a clean reusable public repo that does exactly what your update describes:

```text
multi-rebar 2D parametric inversion
recover x, z, radius
sweep close spacing
sweep Tx/Rx offset
sweep source count
inject multiple random-noise seeds
track truth selection vs near-best wrong branches
report objective margins and ambiguity intervals
define clean vs ambiguous resolution limit
```

Pieces of this exist, but the full workflow as a reproducible “resolution-limit + ambiguity-margin” study is not something I would assume has already been solved.

The closest reusable components are:

`gprMax` for FDTD simulation, including 2D/3D GPR modeling and metal-cylinder examples; it is open source under GPL-3.0 and has examples with 1.5 GHz Ricker wavelets and 40 mm Tx/Rx offset B-scans over a metal cylinder. ([GitHub][11])

`hyperbola_recognition`, a MATLAB repo implementing hyperbola detection/fitting routines for GPR B-scans, useful as a baseline feature-extraction method. ([GitHub][12])

`3DInvNet`, which is much more advanced deep-learning inversion code, but targeted to 3D permittivity reconstruction rather than your exact parametric multi-rebar ambiguity sweep. ([GitHub][13])

## My bottom-line answer

You are **not the only person working on multi-rebar GPR detection/inversion**. That field is definitely active and mature enough that you should assume prior art exists.

But you are also **not obviously wasting time**. Your specific angle — close-spacing transition, Tx/Rx/source-count sensitivity, radius/location ambiguity, noise-seed replication, and clean-vs-ambiguous resolution limit — looks like a narrower and potentially useful contribution.

The right way to position it is not:

> Nobody has solved rebar detection before.

The right way is:

> Prior work has shown rebar detection, localization, diameter estimation, FWI, MIMO imaging, and ML-based recognition. Our contribution is a controlled acquisition-aware identifiability study for closely spaced multi-rebar inversion, emphasizing not just point recovery but whether the true geometry is clearly distinguishable from near-degenerate alternatives.

That is the clean, intellectually honest framing.

[1]: https://www.sensoft.ca/blog/understanding-gpr-resolution-and-target-detection/ "
  Understanding GPR Resolution and Target Detection 
            "
[2]: https://www.geophysical.com/wp-content/uploads/2017/10/GSSI-Concrete-Handbook.pdf "GSSI Handbook For Concrete Inspection"
[3]: https://www.sciencedirect.com/science/article/abs/pii/S0950061819325449 "Reinforced concrete mapping using full-waveform inversion of GPR data - ScienceDirect"
[4]: https://arxiv.org/abs/2005.09643 "[2005.09643] An Innovative Approach to Determine Rebar Depth and Size by Comparing GPR Data with a Theoretical Database"
[5]: https://www.sciencedirect.com/science/article/abs/pii/S0950061822035802 "Estimating the diameter of reinforcing bars using an ultra-wideband MIMO GPR array - ScienceDirect"
[6]: https://www.mdpi.com/2076-3417/12/18/9217 "A Quasi-Quadratic Inverse Scattering Approach to Detect and Localize Metallic Bars within a Dielectric"
[7]: https://arxiv.org/abs/1907.09997 "[1907.09997] An Improved Convolutional Neural Network System for Automatically Detecting Rebar in GPR Data"
[8]: https://www.sciencedirect.com/science/article/abs/pii/S0926580519301347 "Automatic hyperbola detection and fitting in GPR B-scan image - ScienceDirect"
[9]: https://arxiv.org/abs/2207.06527?utm_source=chatgpt.com "A Deep Learning-Based GPR Forward Solver for Predicting B-Scans of Subsurface Objects"
[10]: https://arxiv.org/abs/2305.05425?utm_source=chatgpt.com "3DInvNet: A Deep Learning-Based 3D Ground-Penetrating Radar Data Inversion"
[11]: https://github.com/gprMax/gprMax "GitHub - gprMax/gprMax: gprMax is open source software that simulates electromagnetic wave propagation using the Finite-Difference Time-Domain (FDTD) method for numerical modelling of Ground Penetrating Radar (GPR) · GitHub"
[12]: https://github.com/lweileeds/hyperbola_recognition "GitHub - lweileeds/hyperbola_recognition: This repository presents the c3_algorithm for detecting and fitting hypobolae from Ground Penetrating Radar (GPR) B-scan images. · GitHub"
[13]: https://github.com/qiqi-dai/3dinvnet?utm_source=chatgpt.com "Qiqi-Dai/3DInvNet"
