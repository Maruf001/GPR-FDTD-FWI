# Experiment 846: Branch-Preservation Actionability Triage

Date: 2026-06-18

## Purpose

Triage the 13 missed-but-retained truth-lateral candidate surfaces from run
`094` by reopening the saved candidate CSVs and comparing full x/z coordinate
error for the greedy best row against the retained truth-lateral row.

This is CPU-only analysis of saved candidate surfaces. It does not run FDTD,
FWI, GPU kernels, field work, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/095_local_2d_branch_preservation_actionability
```

Key artifacts:

```text
data/local_2d_branch_preservation_actionability_summary.json
data/local_2d_branch_preservation_actionability_rows.csv
data/local_2d_branch_preservation_actionability_label_rows.csv
data/local_2d_branch_preservation_actionability_gates.csv
data/figure_validation.csv
figures/local_2d_branch_preservation_actionability.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_branch_preservation_actionability_cpu_no_gpu
missed-retained rows:                 13
truth-lateral improves L-inf:          7
truth-lateral same L-inf:              6
truth-lateral worse L-inf:             0
narrow coupled-probe candidates:       3
already coupled follow-up:             1
max L-inf improvement:                 1 mm
mean L-inf improvement:                0.538 mm
branch-preservation actionability:     true
narrow GPU probe ready:                false
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Actionability classes:

```text
candidate_for_narrow_coupled_probe:          3
candidate_surface_selectable_improvement:    4
objective_near_tie_same_coordinate_error:    6
```

The unprobed coupled-probe candidates are older close50 target2 archive rows:

```text
1221 target2 close50 seed21 sources4 Tx/Rx25
274  target2 close50 seed34 sources3 Tx/Rx40
285  target2 close50 seed34 sources4 Tx/Rx25
```

Each has a saved-surface 1 mm to 0 mm L-infinity improvement if the retained
truth-lateral branch is selected. Run `1341` is the already-followed coupled
case; run `1343` tested it directly.

## Interpretation

Run `095` sharpens the branch-preservation story. The archive near-tie issue is
not only bookkeeping: in 7/13 missed-retained rows, the retained truth-lateral
candidate improves full x/z coordinate error, and none of the retained
truth-lateral candidates worsen coordinate error.

The result still does not justify launching a GPU queue. The three unprobed
coupled candidates are older close50 target2 archive cases, not the current
detector/FWI launch path. A GPU follow-up would need a separate case-specific
coupled-search design, skip-existing checks, and a clear reason why that old
branch changes the manuscript claim.

## Validation

Focused test for the new actionability script:

```text
tests/test_local_2d_branch_preservation_actionability.py
2 passed
```

Focused detector/field regression:

```text
66 passed
```

Full suite:

```text
881 passed
```

Figure validation:

```text
local_2d_branch_preservation_actionability.png: 2263x835,
nonwhite=0.3023, dynamic range=255
```
