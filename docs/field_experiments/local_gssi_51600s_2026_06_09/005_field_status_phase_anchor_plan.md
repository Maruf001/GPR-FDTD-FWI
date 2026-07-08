# Field Experiment 005: Status Synthesis And Phase-Anchor Plan

Date: 2026-06-17

## Purpose

Consolidate the local GSSI 51600S field stream after field experiments 001-004
and define the next meaningful field-data step. This is a CPU-side synthesis
note only. No new parser run, figure generation, FDTD, FWI, or GPU command was
launched while preparing it.

The goal is to decide what the field data can support now and what is still
missing before any field-to-synthetic waveform comparison.

## Inputs Read

Trackers:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/000_dataset_context.md
docs/field_experiments/local_gssi_51600s_2026_06_09/001_gssi51600s_dzt_qc.md
docs/field_experiments/local_gssi_51600s_2026_06_09/002_gssi51600s_preprocess_feature_qc.md
docs/field_experiments/local_gssi_51600s_2026_06_09/003_gssi51600s_hyperbola_calibration_qc.md
docs/field_experiments/local_gssi_51600s_2026_06_09/004_gssi51600s_common_offset_sweep.md
```

Output summaries:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/001_gssi51600s_dzt_qc/data/gssi_dzt_inventory.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/002_gssi51600s_preprocess_feature_qc/data/field_profile_feature_summary.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/002_gssi51600s_preprocess_feature_qc/data/field_reflector_cue_candidates.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/003_gssi51600s_hyperbola_calibration_qc/data/field_hyperbola_calibration_summary.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/004_gssi51600s_common_offset_sweep/data/field_common_offset_profile_summary.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/004_gssi51600s_common_offset_sweep/data/field_common_offset_best_by_offset.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/004_gssi51600s_common_offset_sweep/data/field_common_offset_apex_fits.csv
```

## Current Field State

The dataset contains four one-channel GSSI DZT profiles with DZX sidecars:

| File | Traces | Length | Role in current field stream |
| --- | ---: | ---: | --- |
| `PROJECT001C__013.DZT` | 807 | 2.686 m | long profile, deeper sparse cues |
| `PROJECT001C__014.DZT` | 274 | 0.910 m | short profile, strongest shallow repeated cues |
| `PROJECT001C__015.DZT` | 814 | 2.710 m | long profile, mixed/deeper cues |
| `PROJECT001C__016.DZT` | 274 | 0.910 m | short profile, strongest shallow repeated cues |

Available metadata are enough for profile-level QC:

```text
antenna name: 51600S
nominal frequency: 1600 MHz
time range: 5.0 ns
scan spacing: about 3.333 mm
header dielectric: 2.25
DZX present: yes for all four DZT files
```

The metadata are not enough for calibrated inversion:

- no `.DZG` GPS/position sidecar;
- no complete survey layout or scan-line ordering;
- no independent rebar cover, diameter, spacing, slab thickness, or dielectric;
- no confirmed 51600S Tx/Rx geometry or time-zero convention;
- no manual phase/apex labels.

## What The Field Runs Establish

### Import and QC

Field experiment 001 proves that the four DZT files import cleanly with
`readgssi` 0.0.22 and that the output/metadata path is usable.

### Reflector-Cue Screening

Field experiment 002 establishes that preprocessing can produce useful
envelope cue maps and sparse candidate tables. The short profiles are the most
useful for near-term calibration:

| File | Cue count | Cue time range | Median cue spacing |
| --- | ---: | ---: | ---: |
| `PROJECT001C__014.DZT` | 3 | 0.697-0.707 ns | 0.2816 m |
| `PROJECT001C__016.DZT` | 6 raw / 3 unique x groups | 0.727-0.992 ns | 0.2966 m |

The repeated shallow short-profile cue positions are:

```text
PROJECT001C__014: x ~= 0.130, 0.403, 0.693 m
PROJECT001C__016: x ~= 0.113, 0.433, 0.707 m
```

The pairwise spacings are:

```text
PROJECT001C__014: 0.2733 m, 0.2900 m
PROJECT001C__016: 0.3200 m, 0.2733 m
```

This is useful pattern evidence. It is not confirmed rebar spacing.

### Zero-Offset Hyperbola Calibration

Field experiment 003 shows visually plausible overlays but unstable velocity:

| File | Best velocity | Implied epsr | Median depth | Boundary warning |
| --- | ---: | ---: | ---: | --- |
| `PROJECT001C__014.DZT` | 0.176 m/ns | 2.90 | 66.6 mm | yes |
| `PROJECT001C__016.DZT` | 0.100 m/ns | 8.99 | 40.8 mm | yes |

The disagreement means the zero-offset model is not sufficient for calibrated
depth or material interpretation.

### Common-Offset Sensitivity

Field experiment 004 sweeps effective Tx/Rx offsets from 0 to 120 mm. Both
short profiles select 60 mm as the best offset:

| File | Best offset | Best velocity | Implied epsr | Time-zero | Median fitted depth | Boundary warning |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `PROJECT001C__014.DZT` | 60 mm | 0.0975 m/ns | 9.45 | 0.0775 ns | 6.5 mm | no |
| `PROJECT001C__016.DZT` | 60 mm | 0.0900 m/ns | 11.10 | -0.0500 ns | 21.2 mm | yes |

The 60 mm score preference is meaningful but not decisive:

| File | Best offset | Best score | Second offset | Second score | Score gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| `PROJECT001C__014.DZT` | 60 mm | 3.0703 | 80 mm | 2.9954 | 0.0750 |
| `PROJECT001C__016.DZT` | 60 mm | 3.1236 | 40 mm | 3.0572 | 0.0664 |

The common-offset model improves velocity consistency between the two short
profiles, but its depth estimates become too shallow to accept as cover depth.
The result should be interpreted as:

```text
60 mm effective offset is a useful overlay/modeling hypothesis.
Absolute field depth remains uncalibrated.
```

## Current Scientific Use Of Field Data

Allowed now:

- parser and metadata validation;
- profile-level QC and preprocessing;
- repeated shallow cue documentation;
- visual hyperbola overlay hypotheses;
- common-offset sensitivity analysis;
- manual phase/time-zero anchoring plan;
- eventual one-event field-to-synthetic waveform comparison after anchoring.

Not allowed yet:

- field FWI;
- radius or cover-depth claims;
- treating 60 mm as confirmed antenna geometry;
- treating cue spacing as confirmed rebar spacing;
- mixing field outputs with `outputs/experiments`;
- using field profiles to change synthetic known-truth confidence labels.

## Phase-Anchor Plan

The next field experiment should be a manual/semiautomatic phase-anchor note for
profiles 014 and 016. It should not run FWI. It should define which visible
feature in the measured waveform is being treated as the apex:

1. top of envelope lobe;
2. signed-amplitude positive peak;
3. signed-amplitude negative peak;
4. envelope maximum;
5. phase-consistent zero crossing, if stable.

For each of the six short-profile apex groups, record:

```text
file
apex_group
x_m
trace_index
current cue time_ns
manual top-envelope time_ns
manual signed-positive time_ns
manual signed-negative time_ns
manual envelope-maximum time_ns
recommended phase convention
quality flag
notes
```

Then recompute the common-offset fit under each phase convention. A useful
phase convention should:

- keep the three apex groups visible in both short profiles;
- avoid grid-boundary time-zero solutions where possible;
- produce plausible depth ranges for reinforced concrete;
- keep profile 014 and 016 velocities in the same material range;
- preserve the repeated spacing evidence without forcing absolute depth.

## Recommended Field Experiment 006

Name:

```text
006_gssi51600s_phase_anchor_qc.md
```

Expected output root:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/006_gssi51600s_phase_anchor_qc
```

Minimum artifacts:

```text
data/field_phase_anchor_picks.csv
data/field_phase_convention_fit_summary.csv
figures/PROJECT001C__014_phase_anchor_panel.png
figures/PROJECT001C__016_phase_anchor_panel.png
figures/phase_convention_depth_velocity_summary.png
figures/FIGURE_NOTES.md
run_manifest.json
```

Acceptance criteria:

- Figures are nonblank and show the picked phase markers over the measured
  B-scans.
- The pick CSV includes all six short-profile apex groups.
- The chosen convention is documented as a hypothesis, not as ground truth.
- The note explicitly says whether one event is ready for field-to-synthetic
  waveform comparison.

Stop criteria:

- If phase markers are visually unstable across neighboring traces, stop at
  QC and do not run waveform comparison.
- If every convention still produces implausible depth or grid-boundary
  time-zero fits, require external antenna/time-zero calibration before
  proceeding.

## Bottom-Line Decision

The field stream is useful and should continue, but it is not ready for FWI.
The next meaningful work is phase/time-zero anchoring on the two short profiles,
followed by at most one carefully documented field-to-synthetic waveform
comparison. The current strongest field result is repeated shallow structure
with roughly 0.27-0.32 m cue spacing; the weakest result is absolute depth.
