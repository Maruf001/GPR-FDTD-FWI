# Experiment 802: Close50 X-Ambiguity Metric Design

Date: 2026-06-17

## Purpose

CPU-only reporting-metric design for the close50 sub-30 mm linear receiver
branch. This implements the top recommendation from experiment 801:
define an ambiguity-aware reporting rule on existing rows before considering
any new GPU run.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1280_close50_x_ambiguity_metric_design
```

Artifacts:

```text
data/close50_x_ambiguity_metric_rows.csv
data/close50_x_ambiguity_metric_summary.json
data/figure_validation.csv
figures/close50_x_ambiguity_metric.png
run_manifest.json
```

## Result

Policy label:

```text
close50_sub30_x_ambiguity_reporting_metric_ready_cpu_no_gpu
```

Summary:

```text
rows:                         6
exact strong rows:            6
paper-clean candidate rows:   4
x-ambiguous rows:             2
radius-ambiguous rows:        0
nominal x-ambiguous rows:     2
source-mismatch ambiguous:    0
max x-ambiguity width:        1.000 mm
gpu priority:                 none_now
```

Recommended reporting metric:

```text
paper_clean_candidate =
  truth_geometry_match
  and strong_confidence
  and x_ambiguity_width_mm == 0
  and radius_ambiguity_width_mm == 0
```

## Interpretation

The sub-30 close50 linear receiver branch should be reported as exact and
strong but not strict-clean under the ambiguity-aware paper metric. The two
failing rows are seed13 nominal cases at 29.5 and 29.75 mm. Radius separation
is not the issue; the caveat is location degeneracy.

This supports reporting an x-ambiguity caveat, not launching another GPU run.

## Validation

Focused tests:

```text
tests/test_close50_x_ambiguity_metric_design.py: 3 passed
```

Figure validation:

```text
close50_x_ambiguity_metric.png: 2535x835,
nonwhite=0.3373, dynamic range=255
```
