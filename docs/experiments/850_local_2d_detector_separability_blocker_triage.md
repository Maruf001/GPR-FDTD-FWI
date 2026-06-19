# Experiment 850: Local 2D Detector Separability Blocker Triage

Date: 2026-06-18

## Purpose

Turn the run `105` detector feature-separability audit into an actionable
failure taxonomy: which cases are only rank-gated, which cases are deeper, and
which cases fail because truth-free feature choice does not generalize.

This is CPU-only synthesis of saved run `105` outputs. It does not run FDTD,
FWI, detector scoring, GPU kernels, field FWI, 3D/HPC work, or neural-network
training.

## Output

```text
outputs/summary_tables/106_local_2d_detector_separability_blocker_triage_post_feature_audit
```

Key artifacts:

```text
data/local_2d_detector_separability_blocker_summary.json
data/local_2d_detector_separability_blocker_cases.csv
data/local_2d_detector_separability_blocker_branch_summary.csv
figures/local_2d_detector_separability_blocker_triage.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                       local_2d_detector_separability_blocker_triage_cpu_no_fwi
case count:                         12
all-truth triples:                  49
best per-case top-10 cases:          8 / 12
best per-case top-50 cases:         11 / 12
best per-case top-200 cases:        12 / 12
leave-one-case top-1 cases:          0 / 12
leave-one-case top-50 cases:         7 / 12
leave-one-case top-200 cases:        9 / 12
feature-generalization failures:     3
ready for rank-gated upper bound:    true
ready for detector-seeded FWI:       false
gpu priority:                        none
```

The three feature-generalization failures are:

```text
target2_close50_linear29p5|seed13|source_mismatch
target2_close50_linear29p5|seed21|source_mismatch
target2_close50_linear29p5|seed34|source_mismatch
```

Branch-level result:

```text
target2_close14:              leave-one top50 = 6/6, top200 = 6/6, feature failures = 0
target2_close50_linear29p5:   leave-one top50 = 1/6, top200 = 3/6, feature failures = 3
```

## Interpretation

The detector candidate space is not the primary blocker: per-case features put
truth inside top 200 for all cases and inside top 50 for 11/12 cases. The
blocker is feature generalization. In the close50 source-mismatch family, the
best per-case feature can rank truth inside top 10, but leave-one-case feature
selection pushes truth deeper than top 200.

This supports a rank-gated upper-bound detector-baseline claim, but it blocks
detector-seeded FWI. The useful CPU next step, if needed, is a
branch-conditioned selector or holdout-robustness audit, not a GPU optimizer
launch.

## Validation

Focused test:

```text
tests/test_local_2d_detector_separability_blocker_triage.py
3 passed
```

Figure validation:

```text
local_2d_detector_separability_blocker_triage.png: 2654x971,
nonwhite=0.1723, dynamic range=255
```
