• Yes. Initial evidence-backed read: you are not simply inventing FWI for rebar sizing from
  scratch. That has been done. But there may still be a paperable niche if framed narrowly
  around confidence-aware, source-profiled, geometry-parameterized FWI for multiple close rebars
  under source mismatch and ambiguity, especially if you add stronger validation.

  What Is Already In The Literature

  - FWI for rebar diameter already exists. The key missing paper for your local paper set is
    Jazayeri et al. 2019, Reinforced concrete mapping using full-waveform inversion of GPR data.
    They use common-offset surface GPR, sparse blind deconvolution for source-wavelet
    estimation, ray-based initialization, and FWI, reporting rebar diameter errors under 11% for
    covers <= 7.5 cm. This directly overlaps the broad claim “GPR FWI can estimate rebar
    diameter.”
    Source: Jazayeri et al. 2019 PDF
    (https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf)

  - Source wavelet uncertainty is already known as central. Jazayeri’s dissertation says the
    source wavelet is “the most challenging component” for common-offset GPR FWI and uses sparse
    blind deconvolution.
    Source: Jazayeri dissertation (https://digitalcommons.usf.edu/etd/7815/)

  - Diameter estimation is an active problem beyond FWI. There are ML, YOLO, database-matching,
    MIMO-array, GPR+EMI, and dual-polarization approaches. Examples:
      - ML diameter estimation: Giannakis et al. 2020/2021

        (https://www.pure.ed.ac.uk/ws/portalfiles/portal/139152639/IEEE_GRLS_FinalSubmission.pdf)

      - YOLO-v3 rebar diameter estimation: Park et al. 2021
        (https://www.mdpi.com/2072-4292/13/10/2011)

      - MIMO UWB array sizing: Cheng et al. 2023 (https://haihan-sun.github.io/files/GPR9.pdf)
      - GPR+EMI dual sensor: Zhou et al. 2018 (https://www.mdpi.com/1424-8220/18/9/2969)
      - dual-polarization GPR: Liu et al. 2025
        (https://colab.ws/articles/10.1016%2Fj.ndteint.2025.103391)

  - Modern GPR-FWI literature is pushing robustness, not just inversion. Current work includes
    progressive bandwidth, Wasserstein/optimal-transport objectives, source-independent
    objectives, implicit neural representations, noise-model FWI, and learned forward models.
    Sources: PEBDD bandwidth FWI (https://onlinelibrary.wiley.com/doi/10.1002/nsg.12154),
    quadratic Wasserstein GPR FWI (https://www.mdpi.com/2072-4292/16/22/4146), OT+LS crosshole
    GPR FWI (https://www.sciencedirect.com/science/article/pii/S0926985125000369), implicit
    multiparameter GPR FWI (https://academic.oup.com/gji/article/240/2/904/7908524), DL
    forward-model FWI for reinforced slabs

    (https://www.research.ed.ac.uk/en/publications/gpr-full-waveform-inversion-with-deep-learning-forward-modelling-)

  Where Your Work May Still Be Novel
  The broad contribution should not be framed as “we use GPR FWI to estimate rebar size/
  location.” That is already taken.

  The more defensible niche is something like:

  > A confidence-aware, source-profiled, low-dimensional geometric FWI workflow for resolving
  > and sizing multiple nearby rebars from controlled common-offset/Tx-Rx GPR data, with
  > explicit ambiguity intervals and source-mismatch diagnostics.

  That niche is more plausible because your project appears to emphasize things many papers
  either omit or treat lightly:

  - multi-rebar coordinate/radius recovery, not just one isolated bar,
  - close-spacing ambiguity,
  - detector-to-FWI staged workflow,
  - target-specific source/ringdown profiling,
  - repeated seed/optimizer reliability checks,
  - confidence intervals, top-k alternatives, ambiguity margins,
  - explicit distinction between “exact recovery,” “moderate confidence,” and “unresolved.”

  Current Weakness
  Right now, the strongest limitation is that your evidence is still mostly controlled
  synthetic. Several competing papers already include lab or field validation. That means your
  paper is probably not viable as a strong applied NDT paper unless you add one of:

  - lab slab data,
  - gprMax/realistic antenna benchmark,
  - public benchmark comparison,
  - direct comparison against hyperbola fitting, Jazayeri-style SBD+FWI, ML/database baselines,
    or MIMO/dual-pol limitations.

  My Judgment
  You are partly reinventing known components: FWI, source estimation, diameter sizing, staged
  bandwidth, and robustness objectives are all established. But you may not be reinventing the
  workflow-level contribution if you can show that your system handles multiple nearby rebars
  with quantified ambiguity under source mismatch better or more transparently than prior
  methods.

  The next useful artifact is a literature-positioning matrix: rows as papers, columns as
  single/multiple rebars, close spacing, diameter, depth, source uncertainty, real data, UQ/
  confidence, optimizer robustness, and hardware assumptions. That would directly tell us where
  the publishable gap is.