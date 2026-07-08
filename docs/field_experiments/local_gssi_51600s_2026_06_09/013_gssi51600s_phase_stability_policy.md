# Field Experiment 013: GSSI 51600S Phase-Stability Policy

## Purpose

CPU-only policy reduction of the expanded field waveform shift surface from
experiment 011. Experiments 011 and 012 showed that a shared positive synthetic
time shift is useful, but the larger event family exposed phase-convention
differences. This run asks which phase convention is stable enough to use as a
field calibration anchor.

This run reads the experiment 011 CSV only. It does not run FDTD, FWI, or GPU
kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/013_gssi51600s_phase_stability_policy
```

Artifacts:

```text
data/phase_shift_summary.csv
data/phase_policy_summary.csv
data/phase_event_stability.csv
data/phase_stability_policy_summary.json
data/figure_validation.csv
figures/phase_shift_stability.png
figures/phase_event_stability.png
run_manifest.json
```

## Result

Phase-level policy summary:

| Phase convention | Events | Best shared shift | Mean `|corr|` | Min `|corr|` | Same-polarity fraction |
| --- | ---: | ---: | ---: | ---: | ---: |
| `cue_time` | 3 | +0.1 ns | 0.7256 | 0.3901 | 1.0 |
| `top_envelope_35pct` | 6 | +0.2 ns | 0.8241 | 0.7319 | 1.0 |

Event-level stability under the global +0.2 ns hypothesis:

```text
stable events at +0.2 ns: 6 of 9
stable top-envelope events: 6 of 6
stable cue-time events: 0 of 3
```

All six top-envelope event families choose +0.2 ns as their event-specific
best shift, with same polarity and `|corr| >= 0.8103`.

Cue-time anchoring is event-specific:

| Event | Event-specific shift | Best `|corr|` | Global +0.2 ns `|corr|` | Penalty |
| --- | ---: | ---: | ---: | ---: |
| `016 cue_time group1` | +0.1 ns | 0.8639 | 0.8070 | -0.0569 |
| `016 cue_time group2` | +0.1 ns | 0.8836 | 0.4661 | -0.4175 |
| `016 cue_time group3` | +0.3 ns | 0.8273 | 0.3347 | -0.4926 |

## Interpretation

The field timing policy should now be narrowed:

```text
Use top_envelope_35pct with a +0.2 ns synthetic time shift as the current
profile-level timing hypothesis.
Do not use cue_time anchoring for field inversion.
Do not treat waveform correlation as geometry, radius, or epsr identification.
```

This result improves the field calibration story but does not make the local
GSSI dataset FWI-ready. The dataset still lacks independent cover-depth,
diameter, material, and survey-layout metadata.

## Validation

Both figures were validated as nonblank:

```text
phase_shift_stability.png nonwhite=0.0812
phase_event_stability.png nonwhite=0.3843
```
