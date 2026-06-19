# Field Experiment 009: GSSI 51600S Shifted Waveform Epsr Probe

## Purpose

Follow-up to field experiment 008. The shifted waveform probe showed that a
small positive synthetic time shift can make simple single-rebar snippets match
the field waveform shape much better. This run asks whether that match actually
discriminates the fitted field dielectric/velocity hypothesis from the default
project concrete permittivity.

This run repeats the experiment 008 shift grid and adds config-epsr candidates:

```text
fitted epsr from phase-anchor/common-offset fit
config epsr = 6.0
synthetic time shifts = -0.3 to +0.3 ns
```

This is field calibration/QC, not field FWI.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/009_gssi51600s_field_synthetic_waveform_shift_epsr_probe
```

Artifacts:

```text
data/field_synthetic_waveform_probe.csv
data/field_synthetic_waveform_shift_surface.csv
data/field_synthetic_waveform_probe_summary.json
data/figure_validation.csv
figures/field_synthetic_waveform_probe_summary.png
figures/field_synthetic_waveform_best_panel.png
run_manifest.json
```

## Result

The run evaluated 24 candidate snippets:

```text
valid synthetic geometries: 18
invalid shallow geometries: 6
```

Best candidate:

```text
file: PROJECT001C__016.DZT
phase convention: cue_time
radius: 6.0 mm
epsr source: fitted
epsr: 12.44
synthetic time shift: +0.1 ns
absolute normalized correlation: 0.8639
normalized residual RMS: 0.5267
```

Best-candidate summaries by epsr source:

| Epsr source | Valid rows | Mean best `|corr|` | Min best `|corr|` | Max best `|corr|` |
| --- | ---: | ---: | ---: | ---: |
| fitted | 9 | 0.8443 | 0.8215 | 0.8639 |
| config | 9 | 0.8218 | 0.7955 | 0.8428 |

Shift-surface summaries:

| Epsr source | Shift | Mean `|corr|` | Min `|corr|` | Max `|corr|` |
| --- | ---: | ---: | ---: | ---: |
| fitted | +0.1 ns | 0.5621 | 0.3724 | 0.8639 |
| fitted | +0.2 ns | 0.8131 | 0.7180 | 0.8586 |
| config | +0.1 ns | 0.6345 | 0.4036 | 0.8343 |
| config | +0.2 ns | 0.7684 | 0.6367 | 0.8428 |

## Interpretation

Fitted epsr is slightly better than config epsr, but not by enough to treat this
probe as material or velocity identification. The default epsr=6.0 snippets can
also reach high shifted correlations after a +0.1 to +0.2 ns adjustment.

The useful conclusion is:

```text
The field waveform shape is time-shift sensitive and not yet epsr-discriminating.
The data remains useful for calibration/QC, but not for field FWI.
```

## Validation

Both figures were validated as nonblank:

```text
field_synthetic_waveform_probe_summary.png nonwhite=0.4308
field_synthetic_waveform_best_panel.png nonwhite=0.3643
```

The run used the default coarse project grid and 5 synthetic sources. No broad
field inversion or 3D experiment was launched.

## Next Decision

Do not escalate this local field dataset to FWI yet. If field work continues,
the next bounded step should estimate a single global time-zero/source-phase
correction and then test whether candidate ranking remains stable under that
global correction. Without independent geometry or cover-depth metadata, the
current waveform correlations are not unique enough for inversion claims.
