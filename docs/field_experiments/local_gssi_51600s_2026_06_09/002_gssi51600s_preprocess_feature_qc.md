# Field Experiment 002: GSSI 51600S Preprocessing And Reflector-Cue QC

## Purpose

CPU-only field-data preprocessing and feature screening for the local GSSI
model 51600S reinforced-concrete profiles. This run follows the import/QC
baseline in field experiment 001 and asks a narrower question:

Can the imported DZT profiles support stable B-scan preprocessing, envelope
feature maps, and sparse reflector cues that are useful for visual triage?

This is not a rebar-identification run, not a radius-estimation run, and not a
2D or 3D full-waveform inversion run.

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
/home/lam001/miniforge3/envs/FNO/bin/python run_gssi_field_preprocess_feature_qc.py \
  --input-dir data/2026-06-09_GSSI_model_51600S \
  --field-root outputs/field_experiments \
  --dataset-id local_gssi_51600s_2026_06_09 \
  --outdir outputs/field_experiments/local_gssi_51600s_2026_06_09/002_gssi51600s_preprocess_feature_qc
```

The explicit `--outdir` was used after an initial NumPy 2 compatibility patch
so this completed run stayed in field experiment `002`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/002_gssi51600s_preprocess_feature_qc
```

Artifacts:

```text
data/field_preprocess_feature_qc_summary.json
data/field_profile_feature_summary.csv
data/field_reflector_cue_candidates.csv
data/figure_validation.csv
figures/field_preprocessing_mosaic.png
figures/field_candidate_summary.png
figures/field_energy_summary.png
figures/*_feature_screen.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Method

Each DZT profile was imported with `readgssi` 0.0.22 through the existing QC
reader. The preprocessing stack was:

1. Median background removal at each two-way-time sample.
2. Hilbert-envelope calculation.
3. Gaussian smoothing of the envelope.
4. Robust per-time-sample normalization across lateral trace position.
5. Sparse local-maximum picking in the cue map.

The sparse picks are called reflector cues because they identify high-energy
places worth visual inspection. They are not confirmed rebars.

Approximate depths use the DZX/DZT dielectric value of 2.25 and should be
treated as metadata-derived display depths, not measured cover truth.

## Results

Imported four profile channel records and wrote 19 sparse reflector cues.

| File | Traces | Length | DZX | Cues | Unique x cues | Cue time range | Median x spacing |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `PROJECT001C__013.DZT` | 807 | 2.686 m | yes | 4 | 4 | 2.692-2.770 ns | 0.893 m |
| `PROJECT001C__014.DZT` | 274 | 0.910 m | yes | 3 | 3 | 0.697-0.707 ns | 0.282 m |
| `PROJECT001C__015.DZT` | 814 | 2.710 m | yes | 6 | 6 | 1.650-2.721 ns | 0.600 m |
| `PROJECT001C__016.DZT` | 274 | 0.910 m | yes | 6 | 3 | 0.727-0.992 ns | 0.297 m |

The strongest short-line cue positions are:

```text
PROJECT001C__014: x ~= 0.130, 0.403, 0.693 m; t ~= 0.70 ns
PROJECT001C__016: x ~= 0.113, 0.433, 0.707 m; t ~= 0.73-0.99 ns
```

Using the metadata dielectric value, those early cue times correspond roughly
to 70-100 mm display depth. This is plausible for shallow reinforced concrete
features, but it is not enough to identify cover depth without calibration.

## Interpretation

The field import path is now more than a file inventory: it can produce
preprocessed B-scans, envelope anomaly maps, energy summaries, and sparse
candidate tables.

The short profiles `PROJECT001C__014.DZT` and `PROJECT001C__016.DZT` show
strong, repeated shallow hyperbola-like responses at three lateral positions
with approximately 0.28-0.30 m spacing. That pattern is potentially useful for
manual inspection and later calibration.

The long profiles `PROJECT001C__013.DZT` and `PROJECT001C__015.DZT` contain
many near-surface periodic responses. The current sparse local-maximum picker
selects deeper cue points for these lines, which is useful for triage but not a
final detector policy. A later field detector should explicitly separate strong
periodic shallow ringing/direct-wave effects from physical hyperbola apexes.

The 2026-06-11 refresh includes the `PROJECT001C__016.DZX` sidecar, so all
four profiles now have same-stem DZX metadata. No `.DZG` GPS/position file is
available, so the survey-layout caveat remains.

## Figure Validation

Seven figures were validated as nonblank:

```text
minimum nonwhite fraction: 0.2718
minimum sampled unique colors: 943
```

## Next Decision

Recommended next field-data step:

1. Build a manual/semiautomatic time-zero and velocity calibration note for the
   short profiles 014 and 016.
2. Use the repeated cue spacing around 0.28-0.30 m as a field hypothesis, not a
   confirmed rebar spacing.
3. Add a cautious hyperbola-template overlay for 014 and 016 before attempting
   any measured-data FWI comparison.
4. Keep all field outputs under
   `outputs/field_experiments/local_gssi_51600s_2026_06_09/` and all trackers
   under `docs/field_experiments/local_gssi_51600s_2026_06_09/`.
