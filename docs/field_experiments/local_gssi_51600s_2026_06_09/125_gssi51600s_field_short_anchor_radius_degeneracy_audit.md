# Field Experiment 125: GSSI 51600S Short-Anchor Radius-Degeneracy Audit

Date: 2026-06-18

## Purpose

Audit whether the saved content-backed short-anchor field/synthetic waveform
evidence supports a calibrated radius seed. This directly follows run `124`,
which found strong waveform coherence but 0/2 radius matches.

This was a CPU saved-artifact audit. It read the existing run `011` radius
sweep, run `033` content-backed event matches, and run `124` waveform
coherence summary. It did not run DZT preprocessing, FDTD, FWI, GPU kernels,
3D/HPC jobs, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/125_gssi51600s_field_short_anchor_radius_degeneracy_audit
```

Key artifacts:

```text
data/field_short_anchor_radius_degeneracy_side_rows.csv
data/field_short_anchor_common_radius_rows.csv
data/field_short_anchor_radius_degeneracy_gates.csv
data/field_short_anchor_radius_degeneracy_summary.json
figures/field_short_anchor_radius_degeneracy_audit.png
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_radius_degeneracy_audit_qc_only
content-backed pairs:                 2
content sides:                        4
selected best-radius sides:           4 / 4
weak radius sides:                    4 / 4
weak radius gap threshold:            0.03
min best-second radius corr gap:      0.006066
max best-second radius corr gap:      0.018674
max radius correlation span:          0.035246
selected radius mismatch pairs:       2 / 2
common-radius rows:                   6
common-radius near-tie pairs:         2 / 2
best common-radius max min loss:      0.000000
best common-radius max mean loss:     0.017623
waveform morphology QC ready:         true
radius seed ready:                    false
radius recovery ready:                false
geometry seed ready:                  false
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: the selected side-wise radii are locally best in the saved
field/synthetic waveform grid, but the margins are too small to treat them as
calibrated radius evidence. The selected radii disagree between repeated
profiles, and forcing a common radius across both sides of each content-backed
pair produces near-tied pair support. In both content pairs, a common-radius
candidate loses no pair-min correlation relative to the selected mixed-radius
pair.

## Claim Boundary

Use this result to strengthen the field boundary:

```text
The measured GSSI data support short-profile relative timing and waveform
morphology QC, but not radius seeding, radius recovery, geometry seeding,
field FWI, 3D/HPC, or heavy field work.
```

The useful publication role is negative/guardrail evidence. It explains why
field waveform resemblance should not be over-promoted into a field inversion
or calibrated radius result.

## Validation

```text
tests/test_gssi_field_short_anchor_radius_degeneracy_audit.py
3 passed
```

Figure validation:

```text
field_short_anchor_radius_degeneracy_audit.png: 2263x835,
nonwhite=0.2006, dynamic range=255
```
