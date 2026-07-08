# BEM Experiment 132: 2D Ladder Bridge Decision Refresh

Date: 2026-06-27

## Purpose

Refresh the decision boundary between the validated BEM-side 2D ladder and the
project-core FDTD comparison path.

Run `131` showed that the BEM track has a coherent 2D validation ladder through
matched dielectric, PEC, and half-space cases. This run asks the next narrower
question:

```text
Does that 2D ladder currently bridge into the project-core FDTD rebar-scattered
comparison path?
```

This is a CPU-only synthesis. It does not run FDTD, BEM solvers, GPU/HPC work,
3D validation, field FWI, or neural-network training.

## Output

```text
outputs/bem_experiments/132_project_core_bem_2d_ladder_bridge_decision_refresh
```

Key artifacts:

```text
data/project_core_bem_2d_ladder_bridge_decision_rows.csv
data/project_core_bem_2d_ladder_bridge_decision_refresh_summary.json
figures/project_core_bem_2d_ladder_bridge_decision_refresh.png
docs/PROJECT_CORE_BEM_2D_LADDER_BRIDGE_DECISION_REFRESH.md
scripts/script_snapshot_manifest.json
```

## Result

```text
decision items:                         4
decision passes:                        2
decision failures:                      2
BEM 2D validation ladder ready:         true
best ladder matched FDTD/BEM L2:        0.02330746966791303
project direct/background L2:           0.03170696405248453
project scattered symmetric L2:         1.3943651626310445
bridge gap vs best ladder:              59.82481936040623
project-core bridge ready:              false
project archive comparison ready:       false
real 3D validation ready:               false
field FWI ready:                        false
gpu/hpc ready:                          false
```

Decision rows:

| Decision item | Metric | Threshold | Status | Ready |
| --- | ---: | ---: | --- | --- |
| BEM 2D validation ladder | 0.02330746966791303 |  | pass | true |
| project-core direct/background calibration | 0.03170696405248453 | 0.05 | pass | true |
| project-core scattered transfer | 1.3943651626310445 | 0.1 | fail | false |
| project-core archive comparison | 0 |  | fail | false |

## Interpretation

The BEM-owned 2D validation ladder remains strong. The best matched FDTD/BEM
case has relative L2 error about `0.0233`, and the project-core direct/background
source-normalization check also passes at about `0.0317`.

The blocker is the scattered rebar transfer. Its symmetric relative L2 remains
about `1.394`, which is roughly `59.8x` larger than the best matched BEM/FDTD
ladder error and far outside the provisional `0.1` comparison gate.

This separates the problem cleanly:

- BEM method validation is not the current blocker.
- Direct/background source normalization is not the current blocker.
- The project-core scattered-field adapter remains the blocker.

## Decision

Keep BEM as a validated parallel 2D forward-model track. Do not promote
project-core FDTD/BEM agreement, older project archive comparison, 3D
validation, GPU/HPC, or field FWI until the scattered-field bridge is repaired
and passes a factorized comparison gate.

The next useful BEM branch is a scattered-field adapter audit that decomposes
the project-core mismatch by sign, timing, normalization, receiver ordering,
background subtraction, and observable definition.

## Validation

Focused test:

```text
tests/test_project_core_bem_2d_ladder_bridge_decision_refresh.py
3 passed
```

Figure validation:

```text
project_core_bem_2d_ladder_bridge_decision_refresh.png
2769x847, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_2d_ladder_bridge_decision_refresh.py
sha256=0d81360d79c713e1f9de6d09e7042adb312a6ca26146a874d5058e4e24a81042

tests/test_project_core_bem_2d_ladder_bridge_decision_refresh.py
sha256=7168896ab5f3807dda0190f2aef53f7d95514256030232218dfdf4567dd33776
```
