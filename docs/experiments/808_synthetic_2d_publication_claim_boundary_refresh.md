# Experiment 808: Synthetic 2D Publication Claim Boundary Refresh

Date: 2026-06-17

## Purpose

CPU-only manuscript-claim refresh for the synthetic 2D publication bundle after
the reporting-tier audits in experiments 807 and 806. This preserves the older
publication figure bundle and writes a new claim-boundary table.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1286_synthetic_2d_publication_claim_boundary_refresh
```

Artifacts:

```text
data/synthetic_2d_publication_claim_boundaries_refreshed.csv
data/synthetic_2d_publication_claim_boundary_refresh_summary.json
data/figure_validation.csv
figures/synthetic_2d_publication_claim_boundary_refresh.png
run_manifest.json
```

## Result

Policy label:

```text
synthetic_2d_publication_claim_boundaries_refreshed_cpu_no_gpu
```

Summary:

```text
claim boundary count:              7
reporting-tier policy:             cross_target_reporting_tiers_target2_geometry_target1_target2_zero_width_cpu_no_gpu
geometry-ambiguous targets:        2
zero-width near-tie targets:       1;2
gpu priority:                      none
ready for manuscript claim table:  true
```

Refreshed claim areas:

```text
resolution_limit
confidence_policy
field_separation
reporting_tiers
objective_uniqueness
target_specificity
gpu_next_step
```

## Interpretation

Use the refreshed claim-boundary CSV when drafting synthetic 2D results. It
adds the needed distinctions between exact-strong, strict location-clean,
zero-width objective near-tie, and geometry-ambiguous near-tie rows.

The no-broad-GPU posture remains unchanged: a GPU run should only follow a new
objective, geometry, or acquisition question.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_publication_claim_boundary_refresh.py: 3 passed
```

Figure validation:

```text
synthetic_2d_publication_claim_boundary_refresh.png: 2127x835,
nonwhite=0.5544, dynamic range=255
```
