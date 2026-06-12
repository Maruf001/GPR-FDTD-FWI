# Literature Positioning Matrix For Rebar GPR-FWI

Date: 2026-06-07

Purpose: compare the project's likely contribution against directly competing
rebar-sizing papers and adjacent GPR-FWI robustness papers. This is a
positioning artifact, not a full systematic review.

Legend:

- `Y`: directly demonstrated or central to the paper.
- `P`: partial, indirect, limited, or not the central claim.
- `N`: not reported or not part of the method.
- `?`: not clear from the accessible abstract/source.

## Short Conclusion

The project should not claim novelty for "using GPR FWI to estimate rebar
diameter." That has already been demonstrated, especially by Jazayeri et al.
2019. A more defensible contribution is:

> Confidence-aware, source-profiled, geometry-parameterized FWI for multiple
> nearby rebars under controlled source mismatch, with explicit ambiguity
> margins and staged detector-to-refinement workflow.

That contribution is plausible because the direct rebar-sizing literature often
has one of these tradeoffs:

- special hardware: MIMO arrays, dual-polarization GPR, or GPR+EMI;
- black-box/training-data dependence: ML and YOLO approaches;
- sizing without explicit uncertainty: many methods report best estimates but
  not ambiguity intervals or top-k alternatives;
- source handling without multi-rebar ambiguity: FWI papers handle source
  wavelets, but rarely pair that with confidence-aware close-rebar sizing;
- FWI robustness work on permittivity/conductivity images rather than rebar
  geometry.

The project's main weakness remains validation. Several competitors include lab
or field data, while the current strongest project evidence is controlled
synthetic. A paper will need either lab/field data or a strong benchmark against
published baselines.

## Direct Rebar And Cylindrical-Target Sizing Matrix

| Source | Method family | Single rebar | Multiple rebars | Close spacing | Diameter/radius | Depth/location | Source uncertainty | Real/lab data | UQ/confidence | Optimizer robustness | Hardware/data assumptions | Gap relevance |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Hasan and Yazdani 2016, "Embedded Rebar Diameter in Concrete Using GPR" ([Wiley](https://onlinelibrary.wiley.com/doi/10.1155/2016/9714381)) | empirical/numerical amplitude relation | Y | P | N | Y | P | N | Y | N | N | high-frequency GPR; diameter inference assumes known/controlled cover and concrete properties | Establishes that amplitude-based sizing exists but is calibration-sensitive. |
| Zhou et al. 2018, GPR+EMI dual sensor ([MDPI Sensors](https://www.mdpi.com/1424-8220/18/9/2969)) | sensor fusion, calibrated EMI constrained by GPR cover | Y | P | P | Y | Y | N | Y | N | P | requires custom GPR+EMI sensor and EMI calibration set | Strong applied competitor, but special hardware. Project can contrast as GPR-only waveform inversion. |
| Jazayeri et al. 2019, reinforced concrete mapping with GPR FWI ([PDF](https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0950061819325449)) | common-offset GPR, SBD source-wavelet estimate, ray initialization, FWI | Y | P | P | Y | Y | Y | Y | P | P | common-offset commercial-style GPR; sparse blind deconvolution; FWI initialized by ray/hyperbola analysis | Closest prior art. Blocks broad novelty. Project must claim beyond it: confidence-aware multi-rebar/source-mismatch workflow, not FWI sizing itself. |
| Xiang, Ou, Rashidi 2020, theoretical database matching ([arXiv](https://arxiv.org/abs/2005.09643)) | hyperbola extraction plus theoretical database search | Y | P | P | Y | Y | N | ? | N | P | B-scan hyperbola outlines; precomputed theoretical curves | Relevant detector/baseline. It attacks depth-size coupling but not full waveform or source profiling. |
| Giannakis, Giannopoulos, Warren 2020/2021, ML diameter estimation ([PDF](https://www.pure.ed.ac.uk/ws/portalfiles/portal/139152639/IEEE_GRLS_FinalSubmission.pdf); [repository](https://repository.uwl.ac.uk/id/eprint/12883/)) | machine learning from GPR signal features | Y | N | N | Y | Y | N | P | P | P | training data quality and scenario coverage are central assumptions | Competes on fast sizing. Project can contrast physics-based uncertainty/top-k diagnostics. |
| Park et al. 2021, YOLO-v3 rebar diameter estimation ([MDPI Remote Sensing](https://www.mdpi.com/2072-4292/13/10/2011)) | object detection/classification on B-scan or migrated images | Y | P | P | Y | P | N | P | P | P | trained YOLO model; diameter classes; image preprocessing/migration | Good ML baseline for detection/sizing, but likely less transparent about physical ambiguity. |
| Patsia, Giannopoulos, Giannakis 2023, DL forward model plus FWI ([Edinburgh](https://www.research.ed.ac.uk/en/publications/gpr-full-waveform-inversion-with-deep-learning-forward-modelling-); [DOI](https://doi.org/10.1109/TGRS.2023.3303683)) | near-real-time learned forward solver used inside FWI | Y | P | ? | Y | Y | P | Y | N | Y | trained synthetic 3D antenna/slab digital twin; FWI accelerated by ML surrogate | Strong rebar-FWI competitor on speed and realistic antenna modeling. Project should not claim speed novelty without comparison. |
| Cheng et al. 2023, UWB MIMO GPR array sizing ([PDF](https://haihan-sun.github.io/files/GPR9.pdf); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0950061822035802)) | MIMO array imaging, diffraction stacking, 3 dB chord sizing | Y | Y | Y | Y | Y | N | Y | N | P | full-matrix MIMO UWB array, alignment assumptions | Strong practical sizing method, but needs richer hardware than a single/common-offset workflow. |
| Zatar, Nghiem, Nguyen 2024, detecting rebars with GPR ([MDPI Applied Sciences](https://www.mdpi.com/2076-3417/14/13/5808)) | automated hyperbola extraction, biquadratic/theoretical equations | Y | Y | P | Y | Y | N | Y | N | P | survey grids over RC slabs; theoretical hyperbola matching | Direct applied comparator for location/depth/diameter. Does not appear to handle full-wave source ambiguity. |
| Liu et al. 2025, dual-polarization GPR rebar characterization ([CoLab summary](https://colab.ws/articles/10.1016%2Fj.ndteint.2025.103391); [DOI](https://doi.org/10.1016/j.ndteint.2025.103391)) | analytical phase difference from orthogonally polarized channels | Y | P | P | Y | Y | P | Y | P | P | requires dual-polarization GPR; reports diameter errors below 1.3 mm / 9.1 percent in scenarios summarized | Very strong practical competitor, but special hardware. Project's niche is GPR-only/common-offset plus confidence-aware FWI. |
| Xia, Xie, Xue 2025, PG-DGOFWI ([Materials Research Forum](https://mrforum.com/product/9781644903513-28/); [DOI](https://doi.org/10.21741/9781644903513-28)) | prior-guided discrete global optimization FWI | Y | P | P | Y | Y | P | P | N | Y | discrete priors for rebar coordinates/dimensions; gprMax simulation and experimental tests | Very close methodologically: prior-guided discrete geometry FWI. Project needs to differentiate with source profiling, ambiguity intervals, and multi-seed close/variable-depth evidence. |
| Liu/Zeng et al. 2025, DeepMask-GPR ([MDPI Electronics](https://www.mdpi.com/2079-9292/14/24/4799)) | Mask R-CNN image segmentation, apex and radius estimation | Y | P | P | Y | Y | N | P | P | P | rendered B-scan images, labeled data, scale calibration | Useful image-based baseline for detector/localization; not a waveform inversion or source-uncertainty method. |

## Adjacent GPR-FWI Robustness Matrix

| Source | Method family | Single rebar | Multiple rebars | Close spacing | Diameter/radius | Depth/location | Source uncertainty | Real/lab data | UQ/confidence | Optimizer robustness | Hardware/data assumptions | Gap relevance |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Zhou, Klotzsche, Vereecken 2021, progressively expanded bandwidths ([Wiley](https://onlinelibrary.wiley.com/doi/10.1002/nsg.12154)) | crosshole GPR FWI with progressive bandwidth on source and observed data | N | N | N | N | P | Y | Y | N | Y | crosshole GPR; permittivity/conductivity imaging | Supports staged bandwidth ideas but does not solve rebar geometry. |
| Feng et al. 2022, WRI with multi-scale cumulative frequency ([MDPI Remote Sensing](https://www.mdpi.com/2072-4292/14/9/2162)) | wavefield reconstruction inversion for pipelines | N | P | P | P | Y | P | Y | N | Y | multi-offset GPR; frequency-domain WRI; pipeline models | Supports multiscale frequency scheduling and low-initial-model-dependence claims, not rebar sizing. |
| Feng et al. 2023, source-independent common-offset GPR FWI ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0926985122003627)) | convolution/source-independent dual-parameter FWI | N | N | N | N | P | Y | Y | N | Y | common-offset GPR; reference trace/time window; permittivity/conductivity inversion | Important source-wavelet competitor. Project can cite as evidence that source uncertainty is a known central barrier. |
| Lu et al. 2024, quadratic Wasserstein dual-parameter GPR FWI ([MDPI Remote Sensing](https://www.mdpi.com/2072-4292/16/22/4146)) | W2/Sinkhorn objective for permittivity and conductivity | N | N | N | N | P | N | P | N | Y | frequency-domain dual-parameter GPR FWI; synthetic tests | Supports objective-function/cycle-skipping discussion; not a final radius selector for this project. |
| Sun et al. 2025, implicit multiparameter GPR FWI ([GJI](https://academic.oup.com/gji/article/240/2/904/7908524)) | neural implicit representation for multiparameter FWI | N | N | N | N | Y | N | P | N | Y | multioffset GPR; continuous neural representation | Strong robustness/representation paper, but not rebar geometry. |
| Hunziker, Meles, Linde 2025, OT+LS crosshole GPR FWI ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0926985125000369)) | optimal-transport early iterations, LS final objective | N | N | N | N | P | N | P | N | Y | crosshole GPR; synthetic; open-source code | Supports staged objective switching and trace-shift diagnostics, not rebar size. |
| Wang, Chen, Liu 2025, source-independent field GPR FWI ([Crossref/DOI](https://doi.org/10.1190/geo2024-0283.1); [Zenodo data](https://zenodo.org/records/11075281)) | convolution objective plus SE-Wave-U-Net dynamic reference selection | N | N | N | N | Y | Y | Y | N | Y | field GPR; reference-trace extraction; source-independent objective | Stronger source-independent FWI evidence. Project should avoid claiming source-uncertainty handling as broadly novel. |
| Xia et al. 2025, noisy FWI for GPR detection ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0926985125003519)) | FWI with explicit noise models and priors | N | N | N | N | P | Y | Y | P | Y | noise-model assumptions; concrete moisture/content examples | Supports the need to model uncertainty/noise, but not rebar sizing ambiguity. |
| Xie et al. 2022, simplified uncertainty models for GPR depth ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0886779822000426)) | measurement uncertainty propagation for object depth | N | N | N | N | Y | Y | N | Y | N | common-offset GPR depth measurement; assumes diameter/separation negligible in simplified model | Shows uncertainty reporting exists for depth measurement, but not full waveform rebar radius ambiguity. |

## Project Row

| Source | Method family | Single rebar | Multiple rebars | Close spacing | Diameter/radius | Depth/location | Source uncertainty | Real/lab data | UQ/confidence | Optimizer robustness | Hardware/data assumptions | Gap relevance |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| This project, experiments 11-870; project-state report ([local notebook](../update/summary/003_2026-07-02_project_state_report.ipynb), [summary](../update/summary/003_2026-07-02_summary_update.md)) | detector-seeded, source-profiled, low-dimensional geometry FDTD/FWI with top-k confidence and ambiguity intervals | Y | Y | P | Y | Y | Y | N | Y | Y | controlled synthetic FDTD; common-offset/Tx-Rx policies; bounded search; source amplitude/time/frequency/ringdown profiling | Best niche is confidence-aware multi-rebar geometry FWI under source mismatch. Biggest weakness is no lab/field validation. |

## Publication Gap Assessment

### Gap 1: GPR-only geometry FWI with explicit ambiguity reporting

Direct competitors estimate diameter, but most report a best estimate or
classification result. The project already reports top candidates, ambiguity
intervals, weak/moderate/exact confidence, and unresolved branches. That can be
novel if formalized as a reproducible uncertainty/ambiguity protocol, not just
an implementation detail.

Claim strength: moderate.

Needed evidence:

- calibration showing intervals actually cover truth over a benchmark grid;
- plots comparing objective margin against radius error;
- explicit negative cases where ambiguity reporting prevents overclaiming.

### Gap 2: Source-profiled rebar geometry inversion

Source wavelet handling is not novel by itself: SBD, convolution objectives,
source-independent FWI, dynamic reference selection, and noise-model FWI exist.
The project's possible contribution is narrower: source amplitude/time/frequency
and ringdown are treated as nuisance dimensions inside a rebar geometry sizing
workflow, and the confidence report exposes when source mismatch creates radius
ambiguity.

Claim strength: moderate if tied to rebar geometry and ambiguity; weak if
claimed generally.

Needed evidence:

- controlled ablation: fixed source vs profiled source vs ringdown profiled
  source;
- comparison with a source-independent/convolution objective baseline if
  feasible;
- source-mismatch stress cases with reproducible seed policies.

### Gap 3: Multiple nearby rebars with variable depth/radius

Many practical papers handle multiple rebars or close spacing, but often with
special hardware or image/geometric assumptions. The project's variable-depth
and variable-radius staged workflow plus target-specific acquisition policies
could be valuable if the result is presented as a bounded, confidence-aware
inversion protocol.

Claim strength: potentially strong, but only for synthetic/benchmark scope.

Needed evidence:

- a close-spacing benchmark that proves the variable-depth workflow, not only a
  separate target-focused branch;
- comparison against hyperbola/database baselines on the same synthetic cases;
- runtime and failure-mode accounting.

### Gap 4: Practical workflow from detection to refinement

Detector -> assignment -> bounded coordinate refinement -> confidence aggregate
is a publishable engineering workflow if the paper shows it reduces search cost
and failure risk while preserving sizing quality.

Claim strength: moderate.

Needed evidence:

- ablation against brute-force/global or detector-only sizing;
- reproducible script table and runtime budget;
- failure cases where detector seeding is insufficient and how the confidence
  layer flags the issue.

## What Not To Claim

- Do not claim the first GPR FWI for rebar diameter.
- Do not claim source-wavelet uncertainty is newly discovered.
- Do not claim full uncertainty quantification unless intervals are calibrated
  statistically; call them ambiguity intervals or confidence diagnostics unless
  validated.
- Do not claim field readiness without real/lab data.
- Do not claim universal multi-rebar recovery if close spacing, shallow small
  radius, and fitted-ringdown branches remain separately guarded.

## Recommended Paper Framing

Working title:

> Confidence-aware source-profiled geometry FWI for resolving and sizing nearby
> reinforcing bars in controlled GPR data

Best paper type now:

- methods/benchmark paper, if supported by careful synthetic comparisons;
- stronger applied NDT paper, only after lab/field validation.

Minimum comparison set:

1. hyperbola/database fitting baseline;
2. fixed-source LS FWI baseline;
3. source-profiled FWI without ambiguity reporting;
4. full proposed detector-to-refinement confidence workflow.

Minimum experiment matrix:

| Axis | Required values |
|---|---|
| number of rebars | 1, 2, 3 |
| spacing | isolated, moderate, close, near-failure |
| depth pattern | same-depth, variable-depth |
| radius pattern | same-radius, variable-radius |
| source condition | matched, amplitude/time mismatch, ringdown mismatch |
| noise | 0, moderate, near-failure |
| reporting | best estimate, top-k, interval, unresolved flag |

## Sources Used

- Jazayeri et al. 2019, "Reinforced concrete mapping using full-waveform
  inversion of GPR data": https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf
- Jazayeri 2019 dissertation: https://digitalcommons.usf.edu/etd/7815/
- Giannakis et al. 2020/2021, ML diameter estimation: https://www.pure.ed.ac.uk/ws/portalfiles/portal/139152639/IEEE_GRLS_FinalSubmission.pdf
- Park et al. 2021, YOLO-v3 rebar diameter estimation: https://www.mdpi.com/2072-4292/13/10/2011
- Zhou et al. 2018, GPR+EMI dual sensor: https://www.mdpi.com/1424-8220/18/9/2969
- Cheng et al. 2023, UWB MIMO GPR array: https://haihan-sun.github.io/files/GPR9.pdf
- Zatar et al. 2024, detecting reinforced concrete rebars: https://www.mdpi.com/2076-3417/14/13/5808
- Liu et al. 2025, dual-polarization GPR rebar characterization: https://doi.org/10.1016/j.ndteint.2025.103391
- Xiang et al. 2020, theoretical database matching: https://arxiv.org/abs/2005.09643
- Patsia et al. 2023, DL forward model plus FWI: https://doi.org/10.1109/TGRS.2023.3303683
- Xia et al. 2025, prior-guided discrete global optimization FWI: https://doi.org/10.21741/9781644903513-28
- Liu/Zeng et al. 2025, DeepMask-GPR: https://www.mdpi.com/2079-9292/14/24/4799
- Zhou et al. 2021, progressively expanded bandwidths: https://onlinelibrary.wiley.com/doi/10.1002/nsg.12154
- Feng et al. 2022, WRI cumulative frequency strategy: https://www.mdpi.com/2072-4292/14/9/2162
- Feng et al. 2023, source-independent common-offset GPR FWI: https://www.sciencedirect.com/science/article/pii/S0926985122003627
- Lu et al. 2024, quadratic Wasserstein GPR FWI: https://www.mdpi.com/2072-4292/16/22/4146
- Sun et al. 2025, implicit multiparameter GPR FWI: https://academic.oup.com/gji/article/240/2/904/7908524
- Hunziker et al. 2025, OT+LS crosshole GPR FWI: https://www.sciencedirect.com/science/article/pii/S0926985125000369
- Wang et al. 2025, source-independent field GPR FWI: https://doi.org/10.1190/geo2024-0283.1
- Xia et al. 2025, noisy FWI: https://www.sciencedirect.com/science/article/pii/S0926985125003519
- Xie et al. 2022, GPR depth uncertainty: https://www.sciencedirect.com/science/article/abs/pii/S0886779822000426
