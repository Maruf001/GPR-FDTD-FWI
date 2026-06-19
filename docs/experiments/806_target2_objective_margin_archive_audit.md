# Experiment 806: Target2 Objective-Margin Archive Audit

Date: 2026-06-17

## Purpose

CPU-only audit of target2 exact-strong objective margins across existing
non-smoke coordinate-confidence aggregate CSVs. This extends experiment 805
from geometry-ambiguous rows to all exact-strong target2 rows.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1284_target2_objective_margin_archive_audit
```

Artifacts:

```text
data/target2_objective_margin_archive_rows.csv
data/target2_objective_margin_archive_summary.json
data/figure_validation.csv
figures/target2_objective_margin_archive_audit.png
run_manifest.json
```

## Result

Policy label:

```text
target2_objective_margin_geometry_clean_but_near_ties_present_cpu_no_gpu
```

Summary:

```text
aggregate files audited:                 67
target2 exact-strong rows:               267
strict location-clean rows:              246
geometry-ambiguous rows:                 21
zero-width objective near-tie rows:       9
strict-clean margin-separated rows:      237
competitors within ambiguity threshold:  30
strict location-clean fraction:          0.921348
minimum competitor objective gap:        2.210812e-05
minimum separated competitor gap:        1.083986e-03
gpu priority:                            none_now
```

## Interpretation

Target2 exact-strong rows need two reporting tiers:

```text
1. strict location-clean geometry
2. objective-margin separation
```

The 21 geometry-ambiguous rows should be excluded from strict location-clean
claims. The 9 zero-width objective near-tie rows do not undermine
location-clean claims, but they should prevent stronger wording that implies a
uniquely isolated objective basin.

This is a reporting and objective-margin diagnostic. It does not justify a
broad GPU sweep.

## Validation

Focused tests:

```text
tests/test_target2_objective_margin_archive_audit.py: 3 passed
```

Figure validation:

```text
target2_objective_margin_archive_audit.png: 2297x835,
nonwhite=0.2087, dynamic range=255
```
