# Field Experiment 003: GSSI 51600S Hyperbola Calibration QC

## Purpose

CPU-only velocity/time-zero and hyperbola-template overlay run for the two
short local GSSI 51600S profiles:

```text
PROJECT001C__014.DZT
PROJECT001C__016.DZT
```

This run follows field experiment 002. It uses the repeated shallow reflector
cues from the preprocessing stage and fits simple hyperbola templates for
visual calibration. The output is a calibration hypothesis, not a field
inversion result.

## Data Source

```text
data/2026-06-09_GSSI_model_51600S
```

Dataset family:

```text
local_gssi_51600s_2026_06_09
```

## Command

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_gssi_field_hyperbola_calibration.py \
  --input-dir data/2026-06-09_GSSI_model_51600S \
  --field-root outputs/field_experiments \
  --dataset-id local_gssi_51600s_2026_06_09 \
  --outdir outputs/field_experiments/local_gssi_51600s_2026_06_09/003_gssi51600s_hyperbola_calibration_qc
```

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/003_gssi51600s_hyperbola_calibration_qc
```

Artifacts:

```text
data/field_hyperbola_calibration_summary.csv
data/field_hyperbola_apex_fits.csv
data/field_hyperbola_score_surface.csv
data/field_hyperbola_calibration_summary.json
data/figure_validation.csv
figures/field_hyperbola_calibration_summary.png
figures/PROJECT001C__014_hyperbola_overlay.png
figures/PROJECT001C__014_score_surface.png
figures/PROJECT001C__016_hyperbola_overlay.png
figures/PROJECT001C__016_score_surface.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Method

The script imports DZT profiles with `readgssi` 0.0.22, applies the same
median-background-removal and Hilbert-envelope cue map used in field experiment
002, then keeps shallow reflector cues with two-way time at or below 1.25 ns.

Multiple cue picks at the same lateral position are clustered, and the earliest
high-envelope maximum in each lateral cluster is treated as the hyperbola apex
cue. The fitting model is:

```text
t(x) = t_zero + sqrt((t_apex - t_zero)^2 + (2 * (x - x0) / v)^2)
```

where `v` is template velocity and `t_zero` is a time-zero offset. This is a
simple zero-offset point-scatterer approximation. It does not model the real
51600S transmitter/receiver offset, antenna coupling, or 3D survey geometry.

## Results

The corrected run fit six apex cues, three in each short profile.

| File | Apex cues | Best velocity | Implied epsr | Time-zero | Median display depth | Median cue spacing | Boundary warning |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `PROJECT001C__014.DZT` | 3 | 0.176 m/ns | 2.90 | -0.05 ns | 66.6 mm | 281.6 mm | yes |
| `PROJECT001C__016.DZT` | 3 | 0.100 m/ns | 8.99 | -0.05 ns | 40.8 mm | 296.7 mm | yes |

Fitted apex positions:

```text
PROJECT001C__014: x ~= 0.130, 0.403, 0.693 m
PROJECT001C__016: x ~= 0.113, 0.433, 0.707 m
```

The fitted overlays align visually with the obvious shallow hyperbola-like
responses in both short profiles. The repeated lateral spacing is consistent
with the field experiment 002 cue spacing estimate of roughly 0.28-0.30 m.

## Interpretation

This run gives useful visual calibration support: the short profiles contain
repeatable shallow hyperbola-like events at three lateral positions. The
profile-level spacing evidence is stronger than the absolute velocity/depth
calibration.

However, the velocity/depth numbers are not stable enough to call calibrated
cover depth. Both profiles selected the lower time-zero grid boundary
(-0.05 ns), and the score surfaces are broad rather than sharply peaked.
That means the current zero-offset template is missing enough real acquisition
physics that velocity, dielectric, and depth should remain hypotheses.

The profiles disagree strongly in fitted velocity:

```text
014: v ~= 0.176 m/ns, epsr ~= 2.90
016: v ~= 0.100 m/ns, epsr ~= 8.99
```

This disagreement may reflect profile orientation, real material variation,
antenna-offset effects, time-zero ambiguity, or the limitations of using a
zero-offset approximation on measured GSSI data.

## Figure Validation

Five figures were validated as nonblank:

```text
minimum nonwhite fraction: 0.4867
minimum sampled unique colors: 809
```

## Next Decision

Do not move directly to field FWI from this result. The next useful field step
is to add a more realistic common-offset/hyperbola template or a manually
anchored time-zero calibration:

1. Add the 51600S effective Tx/Rx offset if it can be found from documentation
   or estimated from calibration data.
2. Refit profiles 014 and 016 with a common-offset model.
3. Compare whether the fitted velocity becomes more consistent across the two
   short profiles.
4. Only after that, consider field-to-synthetic waveform comparison on one
   manually selected short-profile event.
