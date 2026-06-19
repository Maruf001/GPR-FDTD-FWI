# Field Experiment 011: GSSI 51600S Waveform-Family Shift/Epsr Probe

## Purpose

Bounded field-to-synthetic waveform-family expansion for the two short local
GSSI 51600S profiles:

```text
PROJECT001C__014.DZT
PROJECT001C__016.DZT
```

Experiments 008 and 009 tested only the top event per profile and phase
convention. This run tests all three repeated shallow events per short profile
for the two current phase conventions, while keeping the same small shift grid,
three radius hypotheses, fitted/config epsr comparison, 60 mm effective Tx/Rx
offset, and 5-source synthetic aperture.

This is field calibration/QC only. It is not field FWI, not a 3D experiment,
and not a confirmed rebar geometry result.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe
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

The run evaluated:

```text
selected events:          12
candidate snippets:       72
valid synthetic snippets: 54
invalid shallow snippets: 18
```

Best candidate:

```text
file: PROJECT001C__014.DZT
phase convention: top_envelope_35pct
apex group: 2
radius: 8.0 mm
epsr source: fitted
epsr: 9.96
synthetic time shift: +0.2 ns
absolute normalized correlation: 0.8895
normalized residual RMS: 0.5016
```

Best event-level matches:

| Event family | Best shift | Best `|corr|` | Best radius | Best epsr source | Polarity |
| --- | ---: | ---: | ---: | --- | --- |
| `014 top_envelope_35pct group1` | +0.2 ns | 0.8586 | 6 mm | fitted | same |
| `014 top_envelope_35pct group2` | +0.2 ns | 0.8895 | 8 mm | fitted | same |
| `014 top_envelope_35pct group3` | +0.2 ns | 0.8836 | 8 mm | fitted | same |
| `016 cue_time group1` | +0.1 ns | 0.8639 | 6 mm | fitted | same |
| `016 cue_time group2` | +0.1 ns | 0.8836 | 8 mm | fitted | same |
| `016 cue_time group3` | +0.3 ns | 0.8273 | 5 mm | config | opposite |
| `016 top_envelope_35pct group1` | +0.2 ns | 0.8340 | 5 mm | fitted | same |
| `016 top_envelope_35pct group2` | +0.2 ns | 0.8195 | 5 mm | fitted | same |
| `016 top_envelope_35pct group3` | +0.2 ns | 0.8103 | 5 mm | fitted | same |

Shift-surface mean `|corr|` over all valid rows:

| Synthetic shift | Mean `|corr|` | Min `|corr|` | Max `|corr|` |
| ---: | ---: | ---: | ---: |
| -0.3 ns | 0.2428 | 0.0186 | 0.5196 |
| -0.2 ns | 0.2773 | 0.0197 | 0.5421 |
| -0.1 ns | 0.2899 | 0.0018 | 0.5363 |
| 0.0 ns | 0.2574 | 0.0109 | 0.8016 |
| +0.1 ns | 0.5899 | 0.3724 | 0.8836 |
| +0.2 ns | 0.6953 | 0.1177 | 0.8895 |
| +0.3 ns | 0.4469 | 0.0084 | 0.8273 |

## Interpretation

The expanded event family supports a positive synthetic timing correction, and
the `top_envelope_35pct` convention is especially coherent at +0.2 ns. All six
top-envelope event families prefer +0.2 ns with same polarity and high
correlations.

The `cue_time` convention is less stable. Two cue-time event families prefer
+0.1 ns, and one prefers +0.3 ns with opposite polarity. This makes cue-time
anchoring a poor basis for measured-data inversion.

Fitted epsr is not uniquely identified. Config epsr remains competitive across
the expanded surface, and radius choices vary by event family. The field data
therefore remain calibration/QC evidence rather than geometry, radius, or epsr
recovery evidence.

## Validation

Both figures were validated as nonblank:

```text
field_synthetic_waveform_probe_summary.png nonwhite=0.4352
field_synthetic_waveform_best_panel.png nonwhite=0.4244
```

The run used GPU FDTD for a bounded waveform-family probe. Sampled resource
checks stayed below the requested caps.
