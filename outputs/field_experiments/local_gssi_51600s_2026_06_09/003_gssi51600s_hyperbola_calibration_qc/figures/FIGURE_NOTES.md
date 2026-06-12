# Figure Notes

## `field_hyperbola_calibration_summary.png`

Summary chart for the two short GSSI 51600S profiles. Dashed reference lines
show the metadata dielectric value of 2.25 and its corresponding velocity.
These are not ground-truth values; they are context for the fitted templates.

## Hyperbola Overlay Figures

- `PROJECT001C__014_hyperbola_overlay.png`: median-background-removed B-scan with fitted hyperbola templates and approximate display-depth labels.
- `PROJECT001C__016_hyperbola_overlay.png`: median-background-removed B-scan with fitted hyperbola templates and approximate display-depth labels.

The overlays use a simple zero-offset point-scatterer formula. They are useful
for visual calibration and velocity/time-zero triage, but they do not include
the actual 51600S transmitter/receiver offset or antenna coupling.

The current fits prefer the lower time-zero grid boundary, so the velocity and
depth numbers should be read as overlay hypotheses rather than calibrated cover
measurements.

## Score Surfaces

- `PROJECT001C__014_score_surface.png`: velocity/time-zero score surface; a sharp peak would support a more stable calibration than a broad plateau.
- `PROJECT001C__016_score_surface.png`: velocity/time-zero score surface; a sharp peak would support a more stable calibration than a broad plateau.

Ground-penetrating radar (GPR) B-scans are profile images with profile distance
on the horizontal axis and two-way travel time on the vertical axis.
