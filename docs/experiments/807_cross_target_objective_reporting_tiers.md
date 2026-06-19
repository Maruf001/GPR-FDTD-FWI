# Experiment 807: Cross-Target Objective Reporting Tiers

Date: 2026-06-17

## Purpose

CPU-only cross-target audit of exact-strong archive rows using the reporting
tiers introduced by the target2 objective-margin work. This checks whether
geometry ambiguity and zero-width objective near-ties are target-specific or
cross-target.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1285_cross_target_objective_reporting_tiers
```

Artifacts:

```text
data/cross_target_objective_reporting_tier_rows.csv
data/cross_target_objective_reporting_tier_summary_rows.csv
data/cross_target_objective_reporting_tiers_summary.json
data/figure_validation.csv
figures/cross_target_objective_reporting_tiers.png
run_manifest.json
```

## Result

Policy label:

```text
cross_target_reporting_tiers_target2_geometry_target1_target2_zero_width_cpu_no_gpu
```

Summary:

```text
exact-strong rows:                  323
target count:                       3
geometry-ambiguous rows:            21
zero-width objective near-tie rows: 18
strict-clean separated rows:        284
geometry-ambiguous targets:         2
zero-width near-tie targets:        1;2
gpu priority:                       none_now
```

Target table:

```text
target0: exact-strong 3,   strict clean 3,   geometry ambiguous 0, zero-width near ties 0
target1: exact-strong 53,  strict clean 53,  geometry ambiguous 0, zero-width near ties 9
target2: exact-strong 267, strict clean 246, geometry ambiguous 21, zero-width near ties 9
```

## Interpretation

Target2 is the only target with geometry ambiguity in exact-strong archive
rows. Target1 and target2 both contain zero-width objective near-ties, which
limit objective-uniqueness wording but do not undermine location-clean geometry
claims.

Use this tiering in manuscript tables:

```text
strict location-clean geometry
zero-width objective near-tie
geometry-ambiguous near-tie
```

No broad GPU run is justified by this audit.

## Validation

Focused tests:

```text
tests/test_cross_target_objective_reporting_tiers.py: 3 passed
```

Figure validation:

```text
cross_target_objective_reporting_tiers.png: 2263x835,
nonwhite=0.4120, dynamic range=255
```
