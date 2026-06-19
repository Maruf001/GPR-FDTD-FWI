# Field Experiment 008: GSSI 51600S Waveform Time-Shift Probe

## Purpose

Follow-up to field experiment 007. The first field-to-synthetic waveform probe
found only a modest best match without extra alignment, so this run asks whether
the mismatch is mainly a small time-anchor/source-phase error.

This run reuses the same selected field events, phase conventions, radii,
5-source synthetic snippets, and 60 mm Tx/Rx offset as experiment 007, but
searches a small post-simulation synthetic time-shift grid:

```text
-0.3, -0.2, -0.1, 0.0, +0.1, +0.2, +0.3 ns
```

This is a bounded waveform QC run, not field FWI.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/008_gssi51600s_field_synthetic_waveform_shift_probe
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

The run evaluated the same 12 candidate snippets as experiment 007:

```text
selected field events: 4
valid synthetic geometries: 9
invalid shallow geometries: 3
```

The best shifted candidate was:

```text
file: PROJECT001C__016.DZT
phase convention: cue_time
apex group: 1
radius: 6.0 mm
fitted depth: 22.8 mm
fitted epsr: 12.44
synthetic time shift: +0.1 ns
absolute normalized correlation: 0.8639
polarity: same
normalized residual RMS: 0.5267
```

Without this shift search, the best experiment 007 match was only
`|corr|=0.3440`. The +0.1 to +0.2 ns shifted candidates produce much stronger
same-polarity matches.

## Interpretation

The shifted result is important but not a geometry solution. It says the local
field events can resemble simple single-rebar FDTD snippets after a small timing
adjustment, but the high correlations are not unique:

```text
valid shifted candidates cluster around |corr| = 0.82-0.86
```

That means the next field bottleneck is time-zero/source-wavelet calibration and
candidate discrimination, not running FWI. The current field data still does
not support a defensible radius/depth inversion claim.

The full shift surface adds one useful policy detail:

| Synthetic shift | Valid rows | Mean `|corr|` | Min `|corr|` | Max `|corr|` | Same-polarity rows |
| ---: | ---: | ---: | ---: | ---: | ---: |
| -0.3 ns | 9 | 0.1679 | 0.0186 | 0.3971 | 0 |
| -0.2 ns | 9 | 0.3385 | 0.1900 | 0.5421 | 0 |
| -0.1 ns | 9 | 0.3548 | 0.2755 | 0.4365 | 0 |
| 0.0 ns | 9 | 0.2000 | 0.1181 | 0.3440 | 3 |
| +0.1 ns | 9 | 0.5621 | 0.3724 | 0.8639 | 9 |
| +0.2 ns | 9 | 0.8131 | 0.7180 | 0.8586 | 9 |
| +0.3 ns | 9 | 0.4249 | 0.0113 | 0.7143 | 8 |

The single best candidate uses +0.1 ns, but the best shared shift over all
valid candidates is +0.2 ns. That favors testing a global field time shift
before any event-specific interpretation.

## Validation

Both figures were validated as nonblank:

```text
field_synthetic_waveform_probe_summary.png nonwhite=0.4505
field_synthetic_waveform_best_panel.png nonwhite=0.3637
```

The run used the default coarse project grid and 5 synthetic sources. No broad
field inversion or 3D experiment was launched.

## Next Decision

The next field work should estimate a single global field time shift and
source polarity convention across profiles before any inversion. A useful
bounded next step would compare:

```text
fitted-epsr vs config-epsr snippets
global shift shared across all selected events
event-specific shift
```

If a global shift explains most of the waveform agreement, keep the field data
as calibration/QC evidence. If only event-specific shifts work, the current
profiles are too underconstrained for inversion.
