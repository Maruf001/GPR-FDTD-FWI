# BEM Experiment 018: Project-Core Bridge Checkpoint Pack

Date: 2026-06-24

## Purpose

Condense the current BEM validation ladder and project-core bridge result into
a compact checkpoint for discussion and presentation planning.

This pack summarizes runs `013` through `017`. It does not run a new solver.

## Output

```text
outputs/bem_experiments/018_bem_project_core_bridge_checkpoint_pack
```

Key artifacts:

```text
data/bem_project_core_bridge_checkpoint_summary.json
data/bem_project_core_bridge_ladder.csv
figures/bem_project_core_bridge_checkpoint_ladder.png
docs/BEM_PROJECT_CORE_BRIDGE_CHECKPOINT.md
```

## Result

```text
runs summarized:                013, 014, 015, 016, 017
BEM-owned ladder ready:         true
project-core bridge ready:      false
presentation checkpoint ready:  true
validated BEM-owned endpoint:   016_2d_halfspace_pec_bem_fdtd_matched_adapter
current project-core gate:      017_project_core_fdtd_source_normalization_adapter
```

| Run | Stage | Metric | Ready |
| ---: | --- | ---: | --- |
| 013 | 2D CPU BEM analytic scan | 0.0028625612719971973 | yes |
| 014 | matched dielectric BEM/FDTD | 0.024754323796019783 | yes |
| 015 | matched PEC cylinder | 0.0343267003276678 | yes |
| 016 | matched half-space PEC | 0.030998297443390457 | yes |
| 017 | project-core FDTD bridge gate | 1.3943651626310445 | no |

## Interpretation

The BEM-owned 2D ladder is coherent through analytic dielectric, homogeneous
PEC, and concrete half-space PEC cases. The project-core FDTD bridge does not
pass: direct-wave source calibration is good, but the rebar-scattered transfer
fails by a large margin.

## Presentation Position

Present BEM as a validated parallel forward-model track. Do not present it as
a drop-in replacement for the existing project FDTD stream yet. The strongest
current result is run `016`; run `017` is a useful negative gate that prevents
an overclaim.

## Next Marathon Branch

Run a factorized project-core diagnostic ladder:

1. homogeneous dielectric cylinder;
2. homogeneous PEC cylinder;
3. half-space PEC with controlled source injection.

Only promote project-core/BEM comparison after those narrower gates pass.

## Validation

```text
python -m py_compile run_bem_project_core_bridge_checkpoint_pack.py
conda run -n gpr-fdtd-fwi python run_bem_project_core_bridge_checkpoint_pack.py
```

Figure check:

```text
1 PNG figure, nonblank dynamic range, 1822x803
```
