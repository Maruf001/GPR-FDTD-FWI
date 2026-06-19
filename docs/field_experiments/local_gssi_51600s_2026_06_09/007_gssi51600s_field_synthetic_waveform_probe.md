# Field Experiment 007: GSSI 51600S Field-to-Synthetic Waveform Probe

## Purpose

Bounded field-to-synthetic waveform sanity check for the two short local GSSI
51600S profiles after phase-anchor experiment 006. This compares selected field
event windows with simple single-rebar 2D FDTD snippets under two phase
conventions:

```text
cue_time
top_envelope_35pct
```

This is not field FWI and not a calibrated cover/radius estimate.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/007_gssi51600s_field_synthetic_waveform_probe
```

Artifacts:

```text
data/field_synthetic_waveform_probe.csv
data/field_synthetic_waveform_probe_summary.json
data/figure_validation.csv
figures/field_synthetic_waveform_probe_summary.png
figures/field_synthetic_waveform_best_panel.png
run_manifest.json
```

## Result

The probe compared 12 candidate snippets:

```text
selected field events: 4
valid synthetic geometries: 9
invalid shallow geometries: 3
```

The best candidate was:

```text
file: PROJECT001C__016.DZT
phase convention: cue_time
apex group: 1
radius: 5.0 mm
fitted depth: 22.8 mm
fitted epsr: 12.44
absolute normalized correlation: 0.3440
polarity: same
normalized residual RMS: 0.9390
```

Profile 014 cue-time candidates were geometrically invalid because the fitted
depth was only about 4.1 mm, shallower than the tested 5-8 mm rebar radii.
Top-envelope candidates were physically valid but mostly opposite polarity and
lower-correlation.

## Interpretation

The field data has coherent shallow events, but a simple single-rebar synthetic
snippet does not yet match the field waveform strongly. The best same-polarity
case is only a modest match, and the plausible-depth top-envelope convention
does not improve waveform agreement.

The useful conclusion is:

```text
The local GSSI data should remain in field QC / field-to-synthetic calibration.
It is not ready for field FWI or a 3D interpretation.
```

## Validation

Both figures were validated as nonblank:

```text
field_synthetic_waveform_probe_summary.png nonwhite=0.1312
field_synthetic_waveform_best_panel.png nonwhite=0.3961
```

The run used one bounded GPU job at the default coarse project grid with 5
synthetic sources. No broad GPU field inversion was launched.

## Next Decision

The next useful field step is not FWI. Recommended options are:

1. Add an explicit source/wavelet polarity and time-shift sensitivity check for
   the best profile 016 cue-time event.
2. Compare fitted-epsr snippets against config-epsr snippets only if the
   waveform-shape question remains useful.
3. Defer any field inversion until a known target, survey geometry, antenna
   geometry, or external cover-depth measurement is available.
