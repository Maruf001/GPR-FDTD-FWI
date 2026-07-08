# Field Experiment 006: GSSI 51600S Phase Anchor QC

## Purpose

CPU-only phase/time-zero anchoring sensitivity run for the two short local GSSI
51600S profiles:

```text
PROJECT001C__014.DZT
PROJECT001C__016.DZT
```

Field experiment 004 found that a common-offset template, especially near
60 mm effective Tx/Rx offset, gave more consistent shallow hyperbola curvature
than the zero-offset approximation but produced implausibly shallow absolute
depths. This run tests whether the problem is mainly phase convention: cue time,
top-envelope onset, envelope maximum, signed phase peaks, or nearest zero
crossing.

This remains field QC and field-to-synthetic preparation. It is not a field FWI
run, not a confirmed rebar-cover estimate, and not a 3D experiment.

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
conda run -n gpr-fdtd-fwi python run_gssi_field_phase_anchor_qc.py \
  --input-dir data/2026-06-09_GSSI_model_51600S \
  --field-root outputs/field_experiments \
  --dataset-id local_gssi_51600s_2026_06_09 \
  --outdir outputs/field_experiments/local_gssi_51600s_2026_06_09/006_gssi51600s_phase_anchor_qc
```

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/006_gssi51600s_phase_anchor_qc
```

Artifacts:

```text
data/field_phase_anchor_picks.csv
data/field_phase_anchor_summary.json
data/field_phase_convention_aggregate_summary.csv
data/field_phase_convention_apex_fits.csv
data/field_phase_convention_fit_summary.csv
data/field_phase_convention_score_surface.csv
data/figure_validation.csv
figures/PROJECT001C__014_phase_anchor_panel.png
figures/PROJECT001C__016_phase_anchor_panel.png
figures/phase_convention_depth_velocity_summary.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

The script evaluated six phase conventions across six shallow event picks. The
best screening convention was `cue_time`, but it still produced shallow and
partly boundary-constrained depths:

| Phase convention | Rank | Mean score | Velocity gap | Median depth | Depth plausible | Boundary solutions |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| `cue_time` | 1 | 3.0994 | 0.010 m/ns | 16.1 mm | no | 1 |
| `nearest_zero_crossing` | 2 | 3.0745 | 0.010 m/ns | 6.7 mm | no | 1 |
| `top_envelope_35pct` | 3 | 2.8399 | 0.010 m/ns | 30.7 mm | yes | 2 |
| `signed_negative_peak` | 4 | 3.0359 | 0.010 m/ns | 14.7 mm | no | 2 |
| `envelope_max` | 5 | 2.9910 | 0.015 m/ns | 7.6 mm | no | 2 |
| `signed_positive_peak` | 6 | 1.7300 | 0.010 m/ns | 6.8 mm | no | 2 |

Figure validation passed for all three figures:

```text
minimum nonwhite fraction: 0.4168
minimum sampled unique colors: 1907
```

## Interpretation

The phase-anchor experiment did not rescue a reliable field depth estimate. The
highest scoring convention, `cue_time`, keeps the two short profiles internally
consistent in velocity but implies depths as shallow as about 6.7 mm and still
hits one time-zero boundary solution. The most physically plausible median
depths came from `top_envelope_35pct`, around 27-34 mm, but that convention had
lower scores and two boundary solutions.

The useful conclusion is therefore a boundary condition:

```text
The local GSSI profiles contain coherent shallow events, but the current
time-zero/phase convention is not calibrated well enough for field FWI.
```

The files should also be treated as 2D profile data, not 3D data. There are four
DZT scan files and no defensible crossline grid, survey layout, or 3D position
metadata in the local extraction. They can support profile-level calibration,
B-scan waveform comparison, and field-to-synthetic sanity checks, but not a 3D
inversion claim.

## Next Decision

The next meaningful field step is a small field-to-synthetic waveform comparison
for one or two picked shallow events:

1. Use the 60 mm effective Tx/Rx offset from experiment 004 as the current
   field-template hypothesis.
2. Compare synthetic B-scan snippets under `cue_time` and `top_envelope_35pct`
   anchoring, because they bracket best score versus plausible depth.
3. Score waveform shape, polarity/phase, apex timing, and lateral curvature
   before any FWI attempt.
4. Keep this field tracker separate from `docs/experiments/`, which remains for
   synthetic simulation and infrastructure trackers.
