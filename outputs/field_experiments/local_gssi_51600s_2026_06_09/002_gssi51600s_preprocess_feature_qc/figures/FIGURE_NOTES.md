# Figure Notes

## `field_preprocessing_mosaic.png`

Ground-penetrating radar (GPR) preprocessing overview for the four imported
GSSI 51600S lines. Each panel shows the median-background-removed B-scan. A
B-scan is a profile image whose horizontal axis is profile distance and whose
vertical axis is two-way travel time.

## `field_candidate_summary.png`

Sparse reflector-cue map. The markers are high-envelope local maxima after
background removal and robust normalization. They are useful places to inspect,
but they are not confirmed rebar detections.

## `field_energy_summary.png`

Profile-level feature summary: number of sparse cue points, early-to-mid time
energy ratio, and cue-map dynamic range. These metrics help decide whether a
line is useful for later calibration or too dominated by ringing/background.

## Per-Profile Screens

- `PROJECT001C__013_ch0_feature_screen.png`: four-panel preprocessing, envelope cue, lateral energy, and time-energy summary for `PROJECT001C__013.DZT`.
- `PROJECT001C__014_ch0_feature_screen.png`: four-panel preprocessing, envelope cue, lateral energy, and time-energy summary for `PROJECT001C__014.DZT`.
- `PROJECT001C__015_ch0_feature_screen.png`: four-panel preprocessing, envelope cue, lateral energy, and time-energy summary for `PROJECT001C__015.DZT`.
- `PROJECT001C__016_ch0_feature_screen.png`: four-panel preprocessing, envelope cue, lateral energy, and time-energy summary for `PROJECT001C__016.DZT`.

These figures support field-data quality control only. They do not imply that
the current synthetic 2D FDTD/FWI inversion pipeline can already invert this
measured dataset.
