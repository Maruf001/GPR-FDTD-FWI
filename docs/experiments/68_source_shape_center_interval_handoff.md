# Experiment 68: Source-Shape Center Interval Handoff

## Purpose

Package the same-depth multi-rebar source-shape center-target radius decision
into a small reporting artifact. This makes the interval-supported result easy
to cite without rerunning the expensive source-shape sweeps.

## 535: Source-Shape Center Interval Reporting Handoff

Output:

```text
outputs/experiments/535_source_shape_center_interval_reporting_handoff
```

Artifacts:

```text
README.md
data/source_shape_center_interval_handoff.json
run_manifest.json
```

Decision:

```text
reported radius interval: 6.0-6.2 mm
point-radius claim: rejected
global veryhigh promotion: rejected
```

Evidence summary:

| Evidence | Geometry | Confidence |
| --- | --- | --- |
| Run 506 base | x=250 mm, z=90 mm, r=6.0 mm selected | weak, margin 1.006e-04, ambiguity 6.0-6.2 mm |
| Run 507 late_high | truth geometry preserved | weak, margin 1.632e-04, ratio 1.622 |
| Run 507 veryhigh | truth geometry preserved | weak, margin 6.388e-05, ratio 0.635 |

Interpretation:

```text
The source-shape center branch is truth-geometry correct but radius-interval
supported. Late_high is the best tested diagnostic, but it remains weak.
Veryhigh does not transfer from the variable-depth/radius branch.
```

## Next Decision

Keep the source-shape center target reported as a 6.0-6.2 mm interval unless a
new physics lever appears. Do not spend GPU time on dense coupled sweeps for
this branch under the current objective set.
