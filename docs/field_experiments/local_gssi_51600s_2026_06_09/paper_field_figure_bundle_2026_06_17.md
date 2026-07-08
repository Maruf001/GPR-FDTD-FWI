# Paper Field-Figure Bundle

Date: 2026-06-18

## Scope

This bundle lists the field-data figures that are currently defensible for a
paper or supplement from the local GSSI 51600S dataset. The dataset remains
independent 2D line-profile QC evidence, not a 3D survey or measured-data FWI
benchmark.

Structured bundle:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/059_gssi51600s_field_publication_claim_bundle/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/059_gssi51600s_field_publication_claim_bundle/data/field_publication_claim_boundaries.csv
```

Previous acquisition-readiness structured bundle:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness/data/field_publication_claim_boundaries.csv
```

Previous depth/degen refreshed structured bundle:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc/data/field_publication_claim_boundaries.csv
```

Previous early-time refreshed structured bundle:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/091_gssi51600s_field_publication_claim_bundle_post_early_time_anchor_qc/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/091_gssi51600s_field_publication_claim_bundle_post_early_time_anchor_qc/data/field_publication_claim_boundaries.csv
```

Previous cue-spacing refreshed structured bundle:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context/data/field_publication_claim_boundaries.csv
```

Current timing-anchor refreshed structured bundle:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/098_gssi51600s_field_publication_claim_bundle_post_timing_anchor_conflict/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/098_gssi51600s_field_publication_claim_bundle_post_timing_anchor_conflict/data/field_publication_claim_boundaries.csv
```

Run 098 supersedes 095 for manuscript organization because it keeps the long
profile sensitivity rows, relaxed-anchor negative QC, band-limited
repeatability, measured-event support tiers, the 075 relative time-zero
uncertainty budget, the 078 time-zero perturbation sensitivity figure, the 081
field acquisition/HPC-readiness audit, and the 084-086 apparent-depth and
hyperbola/time-zero degeneracy guardrails, then adds the 090 early-time
common-mode negative-control boundary and the 094 cue-spacing threshold
sensitivity context, and promotes the 097 timing-anchor conflict synthesis as
a structured timing-scope boundary.

## Recommended Figures

### Short-Profile Content-Backed Waveform QC

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/035_gssi51600s_content_backed_waveform_panels/figures/content_backed_waveform_panels.png
```

Use:

```text
Short 014/016 content-backed field-to-synthetic visual QC.
```

Key metrics:

```text
valid panels:                 4 / 4
content-backed pairs:         2
minimum absolute correlation: 0.819494
mean absolute correlation:    0.856643
```

Caption draft:

```text
Content-backed waveform QC for the local GSSI 51600S short-profile pair
014/016. Panels show only repeat-content events selected by the short-profile
content policy. The comparison supports visual timing/QC consistency for these
events, not field inversion, radius, cover-depth, 3D geometry, or FWI
validation.
```

### Short-Profile Supported Corrected-Stack Intervals

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/049_gssi51600s_supported_interval_visual_qc/figures/supported_interval_visual_qc.png
```

Use:

```text
Preferred corrected-stack visual endpoint for the short 014/016 pair.
```

Key metrics:

```text
selected all-window intervals:    3
supported intervals:              3 / 3
total selected length:            0.166650 m
minimum corrected abs corr:       0.909285
minimum abs-correlation gain:     0.363612
```

Caption draft:

```text
Supported-interval corrected-stack QC for the local GSSI 51600S short-profile
pair 014/016. Panels are restricted to profile intervals supported by all
tested shallow windows, avoiding unsupported columns. The result supports
relative timing/repeatability QC only and is not an absolute time-zero,
geometry, radius, cover-depth, 3D, or measured-data FWI result.
```

### Short-Profile Relative Time-Zero Uncertainty Budget

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/075_gssi51600s_field_time_zero_uncertainty_budget/figures/field_time_zero_uncertainty_budget.png
```

Use:

```text
Manuscript uncertainty budget for the short 014/016 relative time-zero QC.
```

Key metrics:

```text
relative anchor offset:            0.127701 ns
bootstrap observed median offset:  0.117878 ns
bootstrap CI:                      0.108055 to 0.147348 ns
conservative half-width:           0.058939 ns
content-anchor support:            2 / 3 event pairs
trace-window support:              6 / 6
short supported bands:             low, mid_low, mid_high, broad
```

Caption draft:

```text
Relative time-zero uncertainty budget for the local GSSI 51600S short-profile
pair 014/016. The supported timing estimate is bounded by phase-convention and
bootstrap evidence, then stress-tested with content anchors, trace alignment,
corrected-stack windows, spatial support, and band-limited repeatability. The
budget supports relative timing QC only and is not absolute time-zero
calibration, geometry, radius, cover-depth, 3D, or measured-data FWI evidence.
```

### Short-Profile Time-Zero Perturbation Sensitivity

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/078_gssi51600s_field_time_zero_perturbation_sensitivity/figures/field_time_zero_perturbation_sensitivity.png
```

Use:

```text
Perturbation sensitivity for the short 014/016 relative time-zero uncertainty budget.
```

Key metrics:

```text
tested offsets:                      7
tested windows:                      3
raw/no-correction support:           0 / 3
nominal support:                     3 / 3
bootstrap-CI support:                9 / 9
conservative-envelope support:       6 / 6
minimum nonraw matrix improvement:   0.125152
minimum nonraw corrected abs corr:   0.661316
minimum nonraw improved-column frac: 0.570281
```

Caption draft:

```text
Time-zero perturbation sensitivity for the local GSSI 51600S short-profile pair
014/016. The B-scan stack QC remains supported for the nominal relative offset,
all bootstrap-CI offsets, and both conservative uncertainty-envelope endpoints
across the tested shallow windows. This figure supports uncertainty robustness
for relative timing QC only and is not absolute time-zero calibration, field
FWI, 3D geometry, radius, or cover-depth evidence.
```

### Early-Time Common-Mode Negative QC

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/090_gssi51600s_field_early_time_anchor_audit/figures/field_early_time_anchor_audit.png
```

Use:

```text
Negative-control evidence that the early direct/ringdown component is not an
absolute time-zero calibration or replacement for content-backed timing.
```

Key metrics:

```text
primary early window:                 0.00-0.55 ns
early peak median time:               0.235756 ns
early peak time span across profiles: 0.000000 ns
short 014/016 early lag:              0.000000 ns
short 014/016 early correlation:      0.999798
content-backed short offset:          0.127701 ns
conservative half-width:              0.058939 ns
early/content delta:                  0.127701 ns
absolute time-zero ready:             false
```

Caption draft:

```text
Early-time common-mode audit for the local GSSI 51600S profiles. The
direct/ringdown component is repeatable and aligns near zero lag for the
short-profile 014/016 pair, but it does not reproduce the content-backed
0.127701 ns relative offset. The early-time component is therefore an
instrument/common-mode QC negative control only, not absolute time-zero
calibration, field FWI, 3D geometry, radius, or cover-depth evidence.
```

### Field Cue-Spacing Context

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/094_gssi51600s_field_cue_spacing_sensitivity_audit/figures/field_cue_spacing_threshold_sensitivity.png
```

Use:

```text
Measured-field cue-spacing context only, not known-truth close-rebar resolution validation.
```

Key metrics:

```text
thresholds:                         0.050, 0.100, 0.150, 0.200, 0.300, 0.500, 1.000 ns
minimum same-time spacing:          96.657 mm
maximum same-time lateral pairs:    32
ready for field context:            true
ready for resolution benchmark:     false
ready for field FWI:                false
```

Caption draft:

```text
Cue-spacing threshold sensitivity for the local GSSI 51600S field data. Across
the tested same-time thresholds, visible measured cue spacings remain wider
than the synthetic close-spacing stress scale. This figure provides
measured-field context only; it is not known-truth rebar separation,
resolution validation, cover-depth/radius recovery, field FWI, 3D geometry, or
synthetic-policy relabeling evidence.
```

### Timing-Anchor Conflict Synthesis

This figure is produced by run 097 and is now included in the current
structured run 098 publication bundle.

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/097_gssi51600s_field_timing_anchor_conflict_synthesis/figures/field_timing_anchor_conflict.png
```

Use:

```text
Quantitative boundary showing that the field timing anchors have distinct scopes.
```

Key metrics:

```text
short content-backed offset:         0.127701 ns
short conservative half-width:       0.058939 ns
early/common-mode shift:             0.000000 ns
long pattern-only offset:            0.060000 ns
early vs short delta / half-width:   2.167
long vs short delta / half-width:    1.149
absolute time-zero ready:            false
field FWI ready:                     false
```

Caption draft:

```text
Timing-anchor conflict synthesis for the local GSSI 51600S field data. The
short 014/016 content-backed timing offset, early/common-mode direct-ringdown
alignment, and long 015/013 pattern-only shift are distinct QC anchors with
different scopes. The figure supports relative timing and claim-boundary
wording only; it is not absolute time-zero calibration, cover-depth/radius
recovery, field FWI, 3D geometry, or synthetic-policy relabeling evidence.
```

### Long-Profile Pattern-Only Visual QC

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/057_gssi51600s_long_profile_pattern_visual_qc/figures/long_profile_pattern_visual_qc.png
```

Use:

```text
Long-profile pattern-QC visualization for the 015/013 pair.
```

Key metrics:

```text
pattern shift:                 +0.060000 ns
selected anchor windows:        6
supported anchor windows:       6 / 6
minimum shifted abs corr:       0.889509
mean shifted abs corr:          0.956439
minimum pattern-shift gain:     0.019532
```

Caption draft:

```text
Pattern-only visual QC for the local GSSI 51600S long-profile pair 015/013
after applying the robust +0.06 ns pattern alignment. The shift is stable
across the tested shallow windows and improves all six stable anchor windows.
Because profile 013 lacks phase-anchor picks, this figure is not phase-time
calibration, field inversion, 3D geometry, radius, cover-depth, or measured-data
FWI evidence.
```

Supporting holdout figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/058_gssi51600s_long_profile_pattern_holdout_qc/figures/long_profile_pattern_holdout_qc.png
```

Time-window sensitivity figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/060_gssi51600s_long_profile_pattern_holdout_sensitivity/figures/long_profile_pattern_holdout_sensitivity.png
```

Spatial-width sensitivity figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/061_gssi51600s_long_profile_pattern_holdout_width_sensitivity/figures/long_profile_pattern_holdout_width_sensitivity.png
```

Use:

```text
Supplemental holdout check for all eight long-profile stack-anchor candidates.
```

Key metrics:

```text
candidate anchor windows:         8
stable supported windows:         6 / 6
repeat-limited supported windows: 2 / 2
minimum stable gain:              0.019532
minimum repeat-limited gain:      0.172819
time-window supported rows:       24 / 24
minimum sensitivity gain:         0.001818
minimum sensitivity shifted corr: 0.873226
spatial-width supported rows:     24 / 24
minimum width-sensitivity gain:   0.019532
minimum width shifted corr:       0.888491
```

Caption draft:

```text
Holdout stress QC for the long-profile 015/013 pattern-only +0.06 ns
alignment. The two repeat-limited anchor candidates, excluded from the
claim-bearing stable-anchor visual panel, also improve under the same shift.
This strengthens the pattern-QC interpretation but remains diagnostic only and
does not create phase-anchor, absolute time-zero, 3D, radius, cover-depth, or
measured-data FWI evidence.
```

### Long-Profile Relaxed Phase-Anchor Negative QC

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/064_gssi51600s_long_profiles_relaxed_phase_anchor_audit/figures/phase_convention_depth_velocity_summary.png
```

Use:

```text
Negative evidence that relaxed long-profile late-window picks do not upgrade
the 015/013 pair to absolute time-zero or measured-data FWI evidence.
```

Key metrics:

```text
relaxed phase-anchor picks:       10
low-SNR relaxed picks:            10 / 10
best phase convention:            cue_time
best boundary solution count:     1
median display depth:             102.5 mm
```

Caption draft:

```text
Relaxed late-window phase-anchor audit for the long-profile 015/013 pair. The
best relaxed hypothesis is depth-plausible, but all relaxed picks are low-SNR
and one fitted branch remains boundary-limited. This supports the negative
claim boundary: the long pair remains pattern-only QC, not absolute time-zero,
cover-depth, radius, 3D, or measured-data FWI evidence.
```

### Field Band-Limited Repeatability QC

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/068_gssi51600s_field_bandlimited_repeatability_audit/figures/field_bandlimited_repeatability.png
```

Use:

```text
Band-limited measured-repeatability QC for short and long profile pairs.
```

Key metrics:

```text
short supported bands:        low, mid_low, mid_high, broad
short raw/corrected abs corr: 0.545551 -> 0.771287
long pattern bands:           mid_low, mid_high, high, broad
long raw/pattern abs corr:    0.789502 -> 0.905584
```

Caption draft:

```text
Band-limited repeatability audit for the local GSSI 51600S field data. The
short 014/016 relative correction is supported in low through mid-high and
broad bands, while the long 015/013 support remains pattern-only. This figure
supports field QC band choices only, not absolute time-zero, radius,
cover-depth, 3D, or measured-data FWI.
```

### Measured Event-Support Tier Table

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/072_gssi51600s_field_event_support_tiers/figures/field_event_support_tiers.png
```

Use:

```text
Compact measured-event support and blocker table for the field supplement.
```

Key metrics:

```text
tier rows:                      9
short content-backed anchors:   2 / 3 event pairs
short timing-only cues:         1
long pattern-supported anchors: 8 total
blocked rows:                   1
```

Caption draft:

```text
Measured-event support tiers for the local GSSI 51600S field data. The table
separates short-profile content-backed relative time-zero QC, a limited
short-profile timing-only cue, long-profile pattern-only support, band-limited
repeatability, and explicit blockers for field FWI or 3D inversion claims.
```

### Field Acquisition/HPC Readiness Audit

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/081_gssi51600s_field_acquisition_readiness_audit/figures/field_acquisition_readiness_audit.png
```

Use:

```text
Acquisition-readiness boundary for using the local GSSI dataset as measured 2D
line-profile QC, not field FWI or 3D HPC input.
```

Key metrics:

```text
scan spacing:                    3.333 mm
nominal in-medium wavelength:    124.914 mm
samples per wavelength:          37.478
time-zero half-width:            0.058939 ns
two-way depth equivalent:        5.890 mm
all-window spatial support:      70 / 249 columns
ready for 3D HPC:                false
ready for field FWI:             false
```

Caption draft:

```text
Acquisition-readiness audit for the local GSSI 51600S field dataset. The traces
are densely sampled along each 2D line relative to the nominal in-medium
wavelength, supporting measured line-profile timing and repeatability QC.
However, missing crossline/grid metadata, relative-only time-zero support,
sparse all-window spatial support, and long-profile pattern-only evidence block
3D inversion, field FWI, radius, and cover-depth claims from this dataset.
```

### Supplemental Apparent-Depth Scale QC

These supplemental field guardrail figures from runs 084-086 are now part of
the current structured run 098 publication bundle.

Figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/084_gssi51600s_field_apparent_depth_qc/figures/field_apparent_depth_qc.png
```

Use:

```text
Depth-equivalent scale check for short-pair relative timing QC, not calibrated
cover-depth recovery.
```

Key metrics:

```text
reflector cue count:                 19
apparent depth scale:                69.696 to 276.822 mm
content-backed short pairs:           2 / 3
corrected rows inside depth budget:   3 / 3
mean raw depth residual:             13.743 mm
mean corrected depth residual:        2.290 mm
max corrected depth residual:         4.908 mm
conservative depth-equivalent budget: 5.890 mm
```

Caption draft:

```text
Apparent-depth scale QC for the local GSSI 51600S field dataset. The short
014/016 relative time-zero correction reduces paired phase residuals to within
the conservative depth-equivalent uncertainty budget. This supports measured
relative timing and depth-scale QC only; it is not calibrated cover-depth,
radius, 3D, or field-FWI evidence.
```

Sensitivity figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/085_gssi51600s_field_apparent_depth_sensitivity/figures/field_apparent_depth_sensitivity.png
```

Use:

```text
Sensitivity guardrail showing why apparent-depth scale QC must not be reported
as calibrated cover-depth recovery.
```

Key metrics:

```text
sensitivity scenarios:              5
epsr range:                         2.25 to 11.10
max apparent cue depth range:       126.906 to 276.822 mm
max apparent cue depth span:        149.916 mm
max apparent cue depth factor:      2.18x
residual support across scenarios:  5 / 5
```

Caption draft:

```text
Dielectric/time-zero sensitivity of the local GSSI apparent-depth scale. The
relative short-pair residual support survives the tested scale assumptions, but
the absolute apparent cue-depth scale shifts by about 150 mm. This figure
supports the no-cover-depth boundary and should not be used as a calibrated
depth, radius, 3D, or field-FWI result.
```

Degeneracy figure:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/086_gssi51600s_field_hyperbola_timezero_degeneracy_audit/figures/field_hyperbola_timezero_degeneracy.png
```

Use:

```text
Score-surface degeneracy guardrail showing why hyperbola/common-offset overlays
remain QC overlays, not calibrated inversion.
```

Key metrics:

```text
surface summary rows:               4
boundary best-fit surfaces:         3 / 4
max near-top epsr span:             4.085
max near-top time-zero span:        0.300 ns
max near-top offset count, 5% gate: 5
```

Caption draft:

```text
Hyperbola/time-zero degeneracy audit for the local GSSI 51600S field overlays.
Near-top score regions span multiple dielectric/time-zero choices, common-offset
scores keep several Tx/Rx offsets plausible, and most best fits sit on grid
boundaries. This supports using the overlays as field QC only, not calibrated
cover-depth, radius, 3D, or field-FWI recovery.
```

## Claim Boundary

Allowed:

```text
The field data provide measured 2D line-profile QC, relative timing evidence for
the short 014/016 pair, supported corrected-stack visual intervals for 014/016,
an uncertainty budget and perturbation sensitivity audit for the short-pair
relative time-zero correction, pattern-only visual alignment for the long
015/013 pair, and a repeat-limited holdout stress check for that long-profile
pattern alignment. The relaxed long-profile phase-anchor audit can be used as
negative evidence that the long pair should remain pattern-only. The
band-limited repeatability, event-support tier, time-zero uncertainty, and
time-zero perturbation figures can be used to organize measured-field QC
support and blockers. The acquisition-readiness audit can be used to justify
dense along-line 2D QC while explicitly ruling out current field FWI or 3D HPC
submission from this dataset. Runs 084-086 can be used as structured
supplemental guardrail figures for apparent-depth scale QC, apparent-depth
sensitivity, and score-surface degeneracy.
```

Not allowed:

```text
Do not use this dataset to claim recovered 3D survey geometry, measured-data
FWI validation, field radius/depth estimates, absolute time-zero calibration,
or a transferable long-profile time-zero correction. Do not use the dense
along-line scan spacing alone as evidence for volumetric survey coverage. Do
not report the apparent-depth figures as calibrated cover-depth recovery.
```
