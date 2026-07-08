# Experiment 852: Local 2D Detector Refreshed Selector Gap Audit

Date: 2026-06-18

## Purpose

Explain the remaining rank gap after experiment `851` / summary table `107`
found the best robust detector selector policy: `component_only` with the
`branch` strategy, dominated by `score_component_balanced`.

This audit joins the saved run `107` selected-policy rows back to the run `105`
feature-separability rows. It reports the selected all-truth rank, the top
false geometry signature, the per-case best-feature oracle rank, and the rank
penalty from using the robust selector instead of the per-case best feature.

This is CPU-only synthesis. It does not run FDTD, FWI, detector scoring, GPU
kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/108_local_2d_detector_refreshed_selector_gap_audit_post_feature_family
```

Key artifacts:

```text
data/local_2d_detector_refreshed_selector_gap_summary.json
data/local_2d_detector_refreshed_selector_gap_cases.csv
data/local_2d_detector_refreshed_selector_gap_branch_summary.csv
figures/local_2d_detector_refreshed_selector_gap_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_detector_refreshed_selector_gap_audit_cpu_no_fwi
source selector policy label:          local_2d_detector_selector_feature_family_audit_cpu_no_fwi
case count:                            12
branch rows:                           2
selected feature family:               component_only
selected selector strategy:            branch
dominant selected feature:             score_component_balanced
selected top-1 cases:                  0 / 12
selected top-10 cases:                 3 / 12
selected top-50 cases:                 10 / 12
selected top-100 cases:                11 / 12
selected top-200 cases:                12 / 12
selected deeper-than-top200 cases:     0 / 12
case-oracle top-1 cases:               0 / 12
case-oracle top-50 cases:              11 / 12
case-oracle top-200 cases:             12 / 12
selected matches case-best feature:    3 / 12
rank-penalty cases:                    9 / 12
median selected all-truth rank:        23.5
max selected all-truth rank:           151
median case-best all-truth rank:       5.5
max case-best all-truth rank:          60
median rank penalty vs case best:      7
max rank penalty vs case best:         91
positive false-minus-truth gap cases:  12 / 12
dominant top missing targets:          target0,target1
ready for rank-gated selector claim:   true
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Branch summary:

```text
target2_close14:
  top50 = 6/6, top200 = 6/6, median selected rank = 23.5,
  max selected rank = 50, median rank penalty = 15.5,
  dominant top miss = target0,target1

target2_close50_linear29p5:
  top50 = 4/6, top200 = 6/6, median selected rank = 18.5,
  max selected rank = 151, median rank penalty = 2,
  dominant top miss = target0,target1
```

## Interpretation

This result strengthens the detector-baseline boundary rather than opening a
GPU/FWI launch path. The refreshed robust selector is good enough for a
rank-gated candidate-list claim: all 12 cases contain an all-truth triple
within the top 200, and 10/12 are within the top 50.

It is still not a detector-seeded FWI gate. Top-1 all-truth recovery is 0/12,
and even the per-case feature oracle has 0/12 top-1 cases. All 12 selected
cases have a positive best-false-minus-best-truth score gap, meaning the top
false geometry scores above the best all-truth geometry under the selected
feature. The dominant top-row failure is missing the left/middle targets
(`target0,target1`), so the detector is systematically selecting partial or
wrong branches before the complete truth triple.

The practical manuscript statement is:

```text
The detector baseline supplies useful candidate lists but cannot by itself
select the correct multi-rebar geometry. In the tested close-spacing cases,
truth is present but not top-ranked; ambiguity must be reported as a
rank-gated resolution/identifiability result rather than promoted to an
automatic inversion initializer.
```

## Validation

Focused test:

```text
tests/test_local_2d_detector_refreshed_selector_gap_audit.py
4 passed
```

Figure validation:

```text
local_2d_detector_refreshed_selector_gap_audit.png: 2773x1005,
nonwhite=0.1435, dynamic range=255
```
