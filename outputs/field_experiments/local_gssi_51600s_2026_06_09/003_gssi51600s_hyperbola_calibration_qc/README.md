# GSSI 51600S Hyperbola Calibration QC

CPU-only field-data calibration run for:

```text
data/2026-06-09_GSSI_model_51600S
```

This run fits simple zero-offset hyperbola templates to the short profiles
`PROJECT001C__014.DZT` and `PROJECT001C__016.DZT`. The fitted velocity,
time-zero, dielectric, and depth values are calibration hypotheses for visual
quality control. They are not ground-truth cover measurements and not
full-waveform inversion outputs.

Profile summaries:

- `PROJECT001C__014.DZT`: v=0.176 m/ns, epsr=2.90, median depth=66.6 mm, boundary warning=True
- `PROJECT001C__016.DZT`: v=0.100 m/ns, epsr=8.99, median depth=40.8 mm, boundary warning=True

Boundary warning means the best grid point lies on the edge of the searched
velocity/time-zero grid. In that case, the overlay can still be visually useful,
but the fitted velocity, dielectric, and depth should not be treated as stable
calibration values.
