# Experiment 1501: Fine Offset-Transition Margin Audit

Date: 2026-06-29

## Purpose

Audit saved per-objective misfit margins around the 40-45 mm acquisition-layout
transition.

Runs `1495-1500` localize and guard the 45 mm acquisition-layout transition.
This run checks whether that transition is visible in the saved
wrong-minus-truth misfit margins, not only in binary pass/fail labels.

This run uses saved run `1495` artifacts only. It does not run new FDTD
simulations, launch GPU work, transfer claims to field evidence, run field FWI,
or start 3D/HPC work.

## Output

```text
outputs/experiments/1501_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_model_margin_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_transition_margin_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
fine claim boundary guarded:          true
models audited:                       90
objective rows audited:               540
all-objectives truth models:          58
any-failure models:                   32
all-objective failure models:         12
transition stress models:             24
pre-45 stress models all fail any:    true
45 mm stress models all clear:        true
max min-margin before 45:             -0.000374885
min margin at 45:                     0.00022905
margin sign flip:                     true
broad radius promoted:                false
physical claim ready:                 false
GPU work ready:                       false
field transfer ready:                 false
3D/HPC ready:                         false
figure size:                          3582x918
figure dynamic range:                 255
```

## Interpretation

The saved margins confirm that the tested far-error stress cases have negative
minimum margins before 45 mm and positive minimum margins at 45 mm. The 45 mm
clearing is therefore visible in the misfit margin, not only in the binary
pass/fail label.

This strengthens the local 2D acquisition-layout mechanism description, but it
does not make a broad physical claim. The result remains a tested-grid result
for the current synthetic setup.

## Decision

Use run `1501` as the margin audit for the guarded fine acquisition-layout
transition. Broad physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
remain blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit.py
3 passed
```
