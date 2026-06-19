# Experiment 849: Local 2D Detector Feature-Separability Audit

Date: 2026-06-18

## Purpose

Audit whether the saved detector/component-gate candidate triples contain a
truth-free feature that can rank the all-truth triple high enough to justify a
detector-seeded FWI handoff.

This is a CPU-only analysis of saved detector rows. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/105_local_2d_detector_feature_separability_audit_post_upper_bound
```

Key artifacts:

```text
data/local_2d_detector_feature_separability_summary.json
data/local_2d_detector_feature_separability_objective_summary.csv
data/local_2d_detector_feature_separability_case_summary.csv
data/local_2d_detector_feature_separability_cv_summary.csv
figures/local_2d_detector_feature_separability_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_detector_feature_separability_audit_cpu_no_fwi
case count:                           12
candidate triples:                    12180
all-truth triples:                    49
all-truth triple fraction:            0.004023
features tested:                      22
best top-1 feature:                   score_component_balanced
best top-1 all-truth cases:           0 / 12
best in-sample top-50 cases:          10 / 12
best in-sample top-200 cases:         12 / 12
minimal all-case rank-gated budget:   200
minimal all-case feature:             score_component_balanced
leave-one-case top-1 all-truth cases: 0 / 12
leave-one-case top-50 cases:          7 / 12
leave-one-case top-200 cases:         9 / 12
ready for rank-gated upper bound:     true
ready for detector-seeded FWI:        false
gpu priority:                         none
```

## Interpretation

The detector candidate space does contain all-truth triples, but they are rare:
49 out of 12,180 saved component-gate triples. No tested truth-free feature
selects an all-truth triple at top 1 for any case. In-sample rank-gated
coverage reaches 12/12 only at top 200 candidate triples per case, while
leave-one-case feature selection reaches only 9/12 at top 200.

This strengthens the detector-baseline boundary: the detector is useful as a
rank-gated upper-bound and candidate-list context result, but it is not ready
for detector-seeded FWI or GPU launch under the current selector evidence.

## Validation

Focused test:

```text
tests/test_local_2d_detector_feature_separability_audit.py
3 passed
```

Figure validation:

```text
local_2d_detector_feature_separability_audit.png: 2569x937,
nonwhite=0.0613, dynamic range=255
```
