# Experiment 844: Coupled Middle-Right Branch-Preserving Search

Date: 2026-06-18

## Purpose

Run the narrow GPU diagnostic authorized by experiment `843`: keep every
target1 middle-bar branch inside the proposed 0.01 absolute / 10% relative
misfit preservation window, then re-evaluate the target2 right-bar local grid
for each retained middle branch.

This tests whether the repaired close14 seed residual from run `1341` is a
one-path greedy artifact or whether the coupled objective itself still prefers
the wrong right-bar branch. It is a single-case diagnostic, not a broad GPU
queue, detector-seeded FWI, field-data run, 3D/HPC run, or neural-network run.

## Output

```text
outputs/experiments/1343_local2d_coupled_middle_right_branch_preserving_search
```

Key artifacts:

```text
data/coupled_middle_right_summary.json
data/coupled_middle_right_branch_rows.csv
data/coupled_middle_right_candidates.csv
data/coupled_middle_right_gates.csv
data/figure_validation.csv
figures/coupled_middle_right_branch_preserving_search.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local2d_coupled_middle_right_branch_preserving_search
source greedy run:                    1341
retained target1 branches:             3
target2 candidates evaluated:         55
objective-best branch rank:            3
objective-best target1:               x=250 mm, z=91 mm
objective-best target2:               x=264 mm, z=89 mm
objective-best coupled misfit:         0.0647758716
greedy final L-inf error:              2 mm
objective-best final L-inf error:      1 mm
oracle-best final L-inf error:         1 mm
objective improvement:                 1 mm
target2 true lateral selected:         true
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
elapsed time:                          320.77 s
```

Branch summary:

```text
rank  target1 x/z   gap rel     target2 best x/z   final L-inf
1     252 / 89      0.000000    266 / 91           2 mm
2     250 / 89      0.092165    264 / 91           1 mm
3     250 / 91      0.095236    264 / 89           1 mm
```

## Interpretation

Run `1343` confirms that the residual in run `1341` is a greedy
branch-lock / coupled-assignment issue. The locally best middle branch
`x=252,z=89` preserves the 2 mm final error, but both retained near-tie
middle branches unlock a 1 mm solution for target2. The coupled objective
does not merely contain the correct branch as an oracle-only option: the
objective-best and oracle-best rows are the same branch-preserving solution
`target1=(250,91), target2=(264,89)`.

This supports a branch-preserving selector claim for the repaired close14
diagnostic. It does not support a broad GPU queue or detector-seeded FWI,
because the evidence is still one repaired seed and still uses controlled
exact-radius synthetic priors.

## Validation

Focused test for the new coupled-search script:

```text
tests/test_local_2d_detector_coupled_middle_right_search.py
2 passed
```

Focused detector/field regression:

```text
60 passed
```

Full suite:

```text
875 passed
```

Figure validation:

```text
coupled_middle_right_branch_preserving_search.png: 2127x784,
nonwhite=0.4325, dynamic range=255
```
