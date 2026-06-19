# Field Experiment 016: GSSI 51600S Long-Profile Phase Anchor QC

Date: 2026-06-17

## Purpose

CPU-only phase/time-zero anchoring sensitivity run for the two longer local
GSSI 51600S profiles:

```text
PROJECT001C__013.DZT
PROJECT001C__015.DZT
```

This extends the short-profile phase-anchor work from experiment 006 without
running FDTD, FWI, or GPU kernels. The run uses a wider `--max-anchor-time-ns`
of 2.5 ns because the short-profile 1.25 ns cutoff produced no usable long
profile picks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/016_gssi51600s_long_profiles_phase_anchor_qc
```

Artifacts:

```text
data/field_phase_anchor_picks.csv
data/field_phase_anchor_summary.json
data/field_phase_convention_aggregate_summary.csv
data/field_phase_convention_fit_summary.csv
data/field_phase_convention_apex_fits.csv
data/field_phase_convention_score_surface.csv
data/figure_validation.csv
figures/PROJECT001C__015_phase_anchor_panel.png
figures/phase_convention_depth_velocity_summary.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Result

Requested profiles:

```text
PROJECT001C__013.DZT
PROJECT001C__015.DZT
```

Usable phase-anchor profiles:

```text
PROJECT001C__015.DZT only
```

Skipped profile:

```text
PROJECT001C__013.DZT: 4 cue candidates before the 2.5 ns filter, 0 after it
```

Profile 015 produced two phase-anchor picks. The best screening phase was
`cue_time`, but every phase convention landed on a grid-boundary solution:

| Phase convention | Rank | Mean score | Median depth | Tx/Rx | Velocity | Boundary? |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `cue_time` | 1 | 1.5161 | 98.4 mm | 0 mm | 0.120 m/ns | yes |
| `nearest_zero_crossing` | 2 | 1.5143 | 97.5 mm | 0 mm | 0.120 m/ns | yes |
| `signed_positive_peak` | 3 | 1.4533 | 72.8 mm | 100 mm | 0.085 m/ns | yes |
| `envelope_max` | 4 | 1.4235 | 53.0 mm | 100 mm | 0.085 m/ns | yes |
| `top_envelope_35pct` | 5 | 1.4235 | 53.0 mm | 100 mm | 0.085 m/ns | yes |
| `signed_negative_peak` | 6 | 1.3735 | 96.4 mm | 0 mm | 0.120 m/ns | yes |

## Interpretation

The long-profile extension does not make the field dataset inversion-ready.
Profile 013 has no retained phase-anchor events under the widened timing
window, and profile 015 produces only two low-score picks with boundary-constrained
fits. The result is useful as a field-data boundary:

```text
Long profiles 013/015 should not be used for field FWI or geometry claims
without stronger event picking, survey metadata, and independent target
validation.
```

The short-profile `top_envelope_35pct` +0.2 ns timing policy remains the better
controlled field-to-synthetic calibration branch.

## Code Note

This run also hardened `run_gssi_field_phase_anchor_qc.py`:

```text
--max-anchor-time-ns controls the retained cue window.
Profiles with no retained phase-anchor picks are skipped and reported instead
of crashing during figure generation.
```

## Validation

Both generated figures were validated as nonblank:

```text
PROJECT001C__015_phase_anchor_panel.png nonwhite=0.7383
phase_convention_depth_velocity_summary.png nonwhite=0.3538
```
