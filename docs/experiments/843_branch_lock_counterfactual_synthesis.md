# Experiment 843: Branch-Lock Counterfactual Synthesis

Date: 2026-06-18

## Purpose

Synthesize the repaired-seed run `1341` and counterfactual run `1342` into a
CPU-side branch-lock policy result.

The question is whether the remaining `target2_close14|seed21|nominal`
residual is just a failed local waveform search, or whether it is caused by a
greedy branch choice for the middle bar that blocks the right bar under exact
non-overlap geometry.

## Output

```text
outputs/summary_tables/093_local_2d_detector_branch_lock_counterfactual_synthesis
```

Key artifacts:

```text
data/local_2d_detector_branch_lock_counterfactual_synthesis_summary.json
data/local_2d_detector_branch_lock_counterfactual_synthesis_rows.csv
data/local_2d_detector_branch_lock_counterfactual_synthesis_gates.csv
data/figure_validation.csv
figures/local_2d_detector_branch_lock_counterfactual_synthesis.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_detector_branch_lock_counterfactual_synthesis_cpu_no_fwi
target1 selected branch:               x=252 mm, z=89 mm
target1 near-tie branch:               x=250 mm, z=89 mm
near-tie misfit gap:                   0.006101703
near-tie relative gap:                 0.092164510
branch-preservation cutoff:            abs<=0.01 and rel<=0.10
near-tie retained by rule:             true
target2 true-x available after greedy: false
target2 true-x unlocked counterfact.:  true
greedy final L-inf error:              2 mm
counterfactual final L-inf error:      1 mm
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
```

## Interpretation

Run `093` makes the mechanism explicit: the repaired exact-radius one-pass
residual is a greedy branch-lock / coupled-assignment issue. The middle branch
selected by run `1341` has the best local target1 misfit, but the near-tie
truth-lateral branch is close enough to retain under a 10% relative-gap rule.
When that near-tie middle branch is retained, run `1342` shows target2 can move
to the true lateral position.

The next meaningful 2D design is therefore a branch-preserving selector or a
small coupled middle-right search. Repeating a one-path greedy coordinate pass
is not the right next step, and this result still does not authorize a broad
GPU queue or detector-seeded FWI.

## Validation

Focused test for the new synthesis script:

```text
tests/test_local_2d_detector_branch_lock_counterfactual_synthesis.py
2 passed
```

Figure validation:

```text
local_2d_detector_branch_lock_counterfactual_synthesis.png: 2144x801,
nonwhite=0.4995, dynamic range=255
```
