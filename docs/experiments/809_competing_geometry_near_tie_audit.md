# Experiment 809: Competing Geometry Near-Tie Audit

Date: 2026-06-17

## Purpose

CPU-only audit of exact-strong archive rows using the raw near-best competing
geometry, not only the reported ambiguity-width fields. This checks whether
zero-width objective near-ties still have nonzero geometry deltas.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1287_competing_geometry_near_tie_audit
```

Artifacts:

```text
data/competing_geometry_near_tie_rows.csv
data/competing_geometry_near_tie_summary_rows.csv
data/competing_geometry_near_tie_summary.json
data/figure_validation.csv
figures/competing_geometry_near_tie_audit.png
run_manifest.json
```

## Result

Policy label:

```text
competing_geometry_near_tie_zero_width_metric_gap_cpu_no_gpu
```

Summary:

```text
exact-strong rows:                         323
reported-width near-tie rows:              21
zero-width competing-geometry near ties:   18
zero-width duplicate objective near ties:  0
competitor-separated rows:                 284
hidden near-tie targets:                   1;2
objective-unique eligible fraction:        0.879257
gpu priority:                              none_now
```

Target table:

```text
target0: exact-strong 3,   hidden near ties 0, competitor separated 3
target1: exact-strong 53,  hidden near ties 9, competitor separated 44, geometry deltas z+radius
target2: exact-strong 267, reported near ties 21, hidden near ties 9, competitor separated 237, geometry deltas x;z+radius
```

Recommended metric:

```text
objective_unique_candidate = exact_strong and not competitor_within_ambiguity_threshold
```

## Interpretation

The ambiguity-width-only reporting metric is not sufficient for
objective-uniqueness wording. It misses 18 zero-width rows where the raw
near-best competitor is still inside the ambiguity threshold and has nonzero
geometry deltas.

Keep geometry-clean and objective-unique claims separate. No broad GPU run is
justified by this audit.

## Validation

Focused tests:

```text
tests/test_competing_geometry_near_tie_audit.py: 4 passed
```

Figure validation:

```text
competing_geometry_near_tie_audit.png: 2263x835,
nonwhite=0.3944, dynamic range=255
```
