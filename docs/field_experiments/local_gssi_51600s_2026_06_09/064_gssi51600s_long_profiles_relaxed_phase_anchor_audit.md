# Field Experiment 064: GSSI 51600S Long-Profile Relaxed Phase-Anchor Audit

Date: 2026-06-18

## Purpose

CPU-only feasibility audit for the open long-profile question: profile 013 had
four reflector cues before filtering, but zero phase-anchor picks under the
nominal 2.50 ns cutoff. This run relaxes the cutoff to 2.90 ns for profiles
015 and 013 to test whether the late candidates support time-zero anchoring.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/064_gssi51600s_long_profiles_relaxed_phase_anchor_audit
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
figures/PROJECT001C__013_phase_anchor_panel.png
figures/PROJECT001C__015_phase_anchor_panel.png
figures/phase_convention_depth_velocity_summary.png
run_manifest.json
```

## Result

Summary:

```text
requested profiles:                 2
profiles with relaxed picks:        2
phase-anchor picks:                 10
low-SNR picks:                      10 / 10
best phase convention:              cue_time
best median depth:                  102.5 mm
best boundary solution count:       1
plausible 15-120 mm depth range:    true
```

## Interpretation

Relaxing the time cutoff admits profile 013 late candidates, but every relaxed
pick is flagged low-SNR and the best relaxed hypothesis still has a boundary
solution. This is useful negative/feasibility evidence: the long pair remains
pattern-only QC, not absolute field time-zero, measured-data FWI, cover-depth,
radius, or 3D evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_phase_anchor_qc.py: 2 passed
```

Figure validation:

```text
PROJECT001C__013_phase_anchor_panel.png: 2479x1005, nonwhite=0.7377
PROJECT001C__015_phase_anchor_panel.png: 2479x1005, nonwhite=0.7379
phase_convention_depth_velocity_summary.png: 2569x835, nonwhite=0.4589
```
