# Experiment 851: Local 2D Detector Selector Feature-Family Audit

Date: 2026-06-18

## Purpose

Test whether the detector selector failure isolated in run `106` is caused by
allowing span-target features to overfit the saved benchmark cases. The audit
compares leave-one-case selector policies over feature families and grouping
strategies, using only saved run `105` feature-rank outputs.

This is CPU-only synthesis. It does not run FDTD, FWI, detector scoring, GPU
kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/107_local_2d_detector_selector_feature_family_audit_post_blocker_triage
```

Key artifacts:

```text
data/local_2d_detector_selector_feature_family_summary.json
data/local_2d_detector_selector_feature_family_policy_summary.csv
data/local_2d_detector_selector_feature_family_cases.csv
data/local_2d_detector_selector_feature_family_best_branch_summary.csv
figures/local_2d_detector_selector_feature_family_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_detector_selector_feature_family_audit_cpu_no_fwi
selector policies tested:             20
case count:                           12
best feature family:                  component_only
best selector strategy:               branch
best top-1 cases:                     0 / 12
best top-10 cases:                    3 / 12
best top-50 cases:                    10 / 12
best top-200 cases:                   12 / 12
best deeper-than-top200 cases:        0
median first all-truth rank:          23.5
max first all-truth rank:             151
all-feature global top-50 cases:       7 / 12
all-feature global top-200 cases:      9 / 12
top-50 gain over all-feature global:   +3
top-200 gain over all-feature global:  +3
ready for rank-gated selector claim:   true
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Best-policy branch summary:

```text
target2_close14:              top50 = 6/6, top200 = 6/6
target2_close50_linear29p5:   top50 = 4/6, top200 = 6/6
```

## Interpretation

The earlier all-feature selector failed because span-target features overfit
the benchmark geometry and pushed the close50 source-mismatch truth triples
deeper than top 200. Restricting the selector to component/waveform score
features removes those deep failures: all 12 cases are within top 200 and
10/12 are within top 50.

This improves the detector baseline claim. The detector can be reported as a
rank-gated candidate-list baseline with a robust component-score selector, but
it still cannot be used as a detector-seeded FWI launch gate because top-1
all-truth recovery remains 0/12.

## Validation

Focused test:

```text
tests/test_local_2d_detector_selector_feature_family_audit.py
3 passed
```

Figure validation:

```text
local_2d_detector_selector_feature_family_audit.png: 2739x1005,
nonwhite=0.2225, dynamic range=255
```
