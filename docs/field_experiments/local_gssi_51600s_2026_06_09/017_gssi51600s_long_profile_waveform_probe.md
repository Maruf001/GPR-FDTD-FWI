# Field Experiment 017: GSSI 51600S Long-Profile Waveform Probe

Date: 2026-06-17

## Purpose

Bounded field-to-synthetic waveform sanity check for the long-profile phase
anchors from experiment 016. This run tests whether the only usable long-profile
phase-anchor profile, `PROJECT001C__015.DZT`, has waveform snippets that
resemble simple single-rebar 2D FDTD snippets.

This is not field FWI and not a calibrated cover/radius estimate.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/017_gssi51600s_long_profile_waveform_probe
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

## Command Scope

```text
profile stems:       PROJECT001C__015
phase conventions:   cue_time, top_envelope_35pct
events per profile:  2
radius values:       5, 6, 8 mm
epsr sources:        fitted and config
synthetic shifts:    -0.2, -0.1, 0.0, +0.1, +0.2 ns
sources:             5
Tx/Rx offset:        60 mm
backend:             gpu-cpml
```

Sampled resource checks during the run stayed below the requested caps:

```text
GPU utilization: 61-64%
host RAM:        about 12.5 GB used
```

## Result

The run evaluated:

```text
selected field events:       4
candidate snippets:         24
valid synthetic snippets:   18
invalid geometries:          6
shift-surface rows:         90
```

Best candidate:

```text
file: PROJECT001C__015.DZT
phase convention: cue_time
apex group: 2
radius: 5.0 mm
epsr source: fitted
epsr: 6.24
synthetic time shift: +0.2 ns
absolute normalized correlation: 0.5811
polarity: opposite
normalized residual RMS: 0.5886
```

Top same-polarity candidates were weaker:

| Event | Phase | Radius | Epsr source | Shift | `|corr|` | Polarity |
| --- | --- | ---: | --- | ---: | ---: | --- |
| g2 | `top_envelope_35pct` | 8 mm | config | +0.1 ns | 0.5185 | same |
| g2 | `top_envelope_35pct` | 5 mm | config | 0.0 ns | 0.5130 | same |
| g2 | `top_envelope_35pct` | 6 mm | config | 0.0 ns | 0.5078 | same |
| g1 | `cue_time` | 5 mm | fitted | +0.2 ns | 0.4966 | same |

## Interpretation

The long-profile waveform probe is a negative/limiting result. The strongest
absolute match is opposite polarity, and the same-polarity top-envelope matches
remain only moderate. This does not support moving the long profiles into field
FWI or geometry/radius claims.

Current field policy:

```text
Use long profiles 013/015 for QC context only.
Keep the controlled field-to-synthetic calibration branch focused on short
profiles 014/016 unless external survey/target metadata becomes available.
```

## Code Note

This run also generalized `run_gssi_field_synthetic_waveform_probe.py`:

```text
--profile-stems selects which DZT profiles are processed.
```

## Validation

Both figures were validated as nonblank:

```text
field_synthetic_waveform_probe_summary.png nonwhite=0.2820
field_synthetic_waveform_best_panel.png nonwhite=0.4350
```
