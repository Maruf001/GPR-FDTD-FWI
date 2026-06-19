# Field Experiment 012: GSSI 51600S Field-Family Global Shift Policy

## Purpose

CPU-only policy reduction of the expanded experiment 011 shift surface. This
run asks whether one shared synthetic time shift still explains the larger
field waveform-family comparison.

This run reads the experiment 011 CSV only. It does not run FDTD, FWI, or GPU
kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/012_gssi51600s_field_family_global_shift_policy
```

Artifacts:

```text
data/global_shift_summary.csv
data/global_shift_by_epsr.csv
data/global_shift_by_phase.csv
data/event_specific_best_candidates.csv
data/global_vs_event_specific_shift.csv
data/global_shift_policy_summary.json
data/figure_validation.csv
figures/global_shift_policy.png
figures/global_shift_penalty.png
run_manifest.json
```

## Result

Best global shift over the expanded surface:

```text
global synthetic time shift: +0.2 ns
valid shift-surface rows:    378
candidate count:             54
mean |corr|:                 0.6953
min |corr|:                  0.1177
same-polarity fraction:      0.8889
```

Event-specific best shifts are stronger:

```text
event-specific mean |corr|: 0.8240
global-shift mean |corr|:   0.6953
mean global penalty:        -0.1287
worst global penalty:       -0.6673
best global penalty:         0.0000
```

Phase-specific behavior explains the weaker global result:

| Phase convention | Best shared shift within phase | Mean `|corr|` at that shift | Min `|corr|` at that shift | Same-polarity rows |
| --- | ---: | ---: | ---: | ---: |
| `cue_time` | +0.1 ns | 0.7256 | 0.3901 | 18/18 |
| `top_envelope_35pct` | +0.2 ns | 0.8241 | 0.7319 | 36/36 |

Epsr-source behavior remains non-discriminating:

| Epsr source | Mean `|corr|` at +0.2 ns | Min `|corr|` at +0.2 ns | Max `|corr|` at +0.2 ns |
| --- | ---: | ---: | ---: |
| fitted | 0.7052 | 0.1177 | 0.8895 |
| config | 0.6854 | 0.2492 | 0.8575 |

## Interpretation

The larger field-family surface keeps +0.2 ns as the best global timing
hypothesis, but the policy is not uniformly stable across phase conventions.
Top-envelope anchoring is coherent at +0.2 ns; cue-time anchoring is better
explained by +0.1 ns and contains the largest penalties under the global
policy.

The practical field policy should now be:

```text
Use +0.2 ns only as a top-envelope timing hypothesis.
Do not use cue_time anchoring for field inversion.
Do not treat waveform correlation as geometry, radius, or epsr identification.
Do not run field FWI without external cover-depth/geometry metadata.
```

## Validation

Both figures were validated as nonblank:

```text
global_shift_policy.png nonwhite=0.0759
global_shift_penalty.png nonwhite=0.3704
```
