# Experiment 803: Archive Location-Clean Metric Audit

Date: 2026-06-17

## Purpose

CPU-only application of the strict location-clean reporting metric from
experiment 802 across existing non-smoke coordinate-confidence aggregate CSVs.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1281_archive_location_clean_metric_audit
```

Artifacts:

```text
data/archive_location_clean_metric_rows.csv
data/archive_location_clean_metric_summary.json
data/figure_validation.csv
figures/archive_location_clean_metric_audit.png
run_manifest.json
```

## Result

Policy label:

```text
archive_location_clean_metric_x_ambiguity_present_cpu_no_gpu
```

Summary:

```text
aggregate files audited:              67
rows audited:                         687
exact rows:                           543
exact strong rows:                    323
strict location-clean strong rows:    302
exact strong x-ambiguous rows:        19
exact strong z-ambiguous rows:        2
exact strong radius-ambiguous rows:   2
location-clean fraction:              0.934985
max x-ambiguity width:                1.000 mm
gpu priority:                         none_now
```

## Interpretation

The strict location-clean metric should be used as an archive reporting audit:
rows that are exact and strong but have nonzero x, z, or radius ambiguity
should not be presented as strict clean thresholds.

The ambiguity caveat is broader than the close50 sub-30 branch, but the audit
does not justify immediate GPU work. It supports better reporting discipline
and targeted CPU-side review of ambiguous aggregate rows.

## Validation

Focused tests:

```text
tests/test_archive_location_clean_metric_audit.py: 3 passed
```

Figure validation:

```text
archive_location_clean_metric_audit.png: 2195x835,
nonwhite=0.3497, dynamic range=255
```
