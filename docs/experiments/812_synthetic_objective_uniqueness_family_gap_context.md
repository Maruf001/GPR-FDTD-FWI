# Experiment 812: Synthetic Objective-Uniqueness Family Gap Context

Date: 2026-06-17

## Purpose

CPU-only family-context audit for the objective-uniqueness caveats from
experiment 809 / run 1287 and the acquisition actionability map from experiment
811 / run 1289. This separates close-spacing x-resolution caveats from
variable-depth/radius and archive-metadata caveats before any future 2D GPU
decision.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1290_synthetic_objective_uniqueness_family_gap_context
```

Artifacts:

```text
data/synthetic_objective_uniqueness_family_gap_rows.csv
data/synthetic_objective_uniqueness_family_gap_summary.json
data/figure_validation.csv
figures/synthetic_objective_uniqueness_family_gap_context.png
run_manifest.json
```

## Result

Policy label:

```text
objective_uniqueness_family_context_close14_target2_cpu_no_gpu
```

Summary:

```text
family cells:                         13
near-tie rows:                        39
known close14 target2 x near ties:     4
known target2 depth/radius near ties:  2
target1 legacy archive near ties:      9
target2 close50 known near ties:       0
gpu priority:                          none_now
```

Known-acquisition target2 x-resolution caveats come from the close14 family,
not close50. The variable-depth/radius caveat is separate and should not be
mixed into close-spacing x-resolution claims. Target1 remains an archive
metadata caveat.

## Interpretation

The next synthetic 2D GPU question, if the manuscript later requires one,
should be a narrow target2 close14 x-resolution probe around the existing
Tx/Rx=45 mm family after CPU objective scope is fixed. This audit argues
against broad close50 reruns and against treating target1 archive caveats as
new acquisition-priority work.

## Validation

Focused tests:

```text
tests/test_synthetic_objective_uniqueness_family_gap_context.py: 3 passed
```

Figure validation:

```text
synthetic_objective_uniqueness_family_gap_context.png: 2569x903,
nonwhite=0.1706, dynamic range=255
```
