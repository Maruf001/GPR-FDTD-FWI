# Field Experiment 004: GSSI 51600S Common-Offset Hyperbola Sweep

## Purpose

CPU-only common-offset sensitivity run for the two short local GSSI 51600S
profiles:

```text
PROJECT001C__014.DZT
PROJECT001C__016.DZT
```

Field experiment 003 used a zero-offset hyperbola approximation and found
visually useful overlays but inconsistent fitted velocities. This run asks
whether allowing an effective transmitter/receiver offset changes the
calibration picture.

This is still a field quality-control and model-sensitivity experiment, not a
field FWI run and not a confirmed rebar-cover estimate.

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
/home/lam001/miniforge3/envs/FNO/bin/python run_gssi_field_common_offset_sweep.py \
  --input-dir data/2026-06-09_GSSI_model_51600S \
  --field-root outputs/field_experiments \
  --dataset-id local_gssi_51600s_2026_06_09 \
  --outdir outputs/field_experiments/local_gssi_51600s_2026_06_09/004_gssi51600s_common_offset_sweep
```

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/004_gssi51600s_common_offset_sweep
```

Artifacts:

```text
data/field_common_offset_profile_summary.csv
data/field_common_offset_apex_fits.csv
data/field_common_offset_best_by_offset.csv
data/field_common_offset_score_surface.csv
data/field_common_offset_sweep_summary.json
data/figure_validation.csv
figures/common_offset_sensitivity.png
figures/PROJECT001C__014_common_offset_overlay.png
figures/PROJECT001C__016_common_offset_overlay.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Method

The script reuses the shallow apex cues from field experiment 003 and sweeps
assumed effective Tx/Rx offsets:

```text
0, 20, 40, 60, 80, 100, 120 mm
```

For each offset it searches template velocity and time-zero values, then scores
the hyperbola curves against the envelope cue map. The trace coordinate is
treated as an antenna midpoint. This is a sensitivity approximation, not a
known instrument geometry.

## Results

Both short profiles selected 60 mm as the best offset in this sweep.

| File | Apex cues | Best offset | Best velocity | Implied epsr | Time-zero | Median fitted depth | Boundary warning |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `PROJECT001C__014.DZT` | 3 | 60 mm | 0.0975 m/ns | 9.45 | 0.0775 ns | 6.5 mm | no |
| `PROJECT001C__016.DZT` | 3 | 60 mm | 0.0900 m/ns | 11.10 | -0.0500 ns | 21.2 mm | yes |

The best-by-offset curve shows a clear score maximum near 60 mm for both
profiles. Relative to the zero-offset run, the fitted velocities become more
consistent:

```text
zero-offset experiment 003:
  014: 0.176 m/ns
  016: 0.100 m/ns

common-offset experiment 004:
  014: 0.0975 m/ns
  016: 0.0900 m/ns
```

## Interpretation

The offset sweep is useful because it suggests that the shallow hyperbola
curvature is not well described by a zero-offset model. A roughly 60 mm
effective offset makes the two short profiles more internally consistent in
velocity.

However, the fitted depths become implausibly shallow, especially 6.5 mm for
profile 014. That means the templates are likely fitting the top/phase of the
shallow response rather than a calibrated rebar-cover apex. The result should
therefore be interpreted as:

```text
60 mm effective offset is a useful overlay/modeling hypothesis.
The absolute depth numbers are not yet reliable cover estimates.
```

The next field model needs either a known 51600S antenna geometry or a manually
anchored time-zero/phase convention before using these profiles for
field-to-synthetic waveform comparison.

## Figure Validation

Three figures were validated as nonblank:

```text
minimum nonwhite fraction: 0.2962
minimum sampled unique colors: 1788
```

## Next Decision

The next field step should not be FWI yet. Recommended next action:

1. Treat 60 mm effective Tx/Rx offset as the current field-template hypothesis.
2. Add manual phase/apex picking for the short profiles to distinguish top
   envelope, red/blue phase peak, and true hyperbola apex convention.
3. Recompute depth estimates under those phase conventions.
4. Only then choose one event for a field-to-synthetic waveform comparison.
