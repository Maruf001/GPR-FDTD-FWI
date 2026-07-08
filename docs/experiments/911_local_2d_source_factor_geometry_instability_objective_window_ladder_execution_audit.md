# Experiment 911: Local 2D Source-Factor Geometry-Instability Objective-Window Ladder Execution Audit

Date: 2026-06-25

## Purpose

Execute the six-objective ladder command designed in run `232`.

Run `230` showed that corrected `base` plus `highband` did not move the
geometry-instability case from `x=188 mm` to the `x=190 mm` truth. This run
tests whether the broader established objective ladder can recover truth x.

This is a bounded CPU-only optimizer execution. It does not launch a broad
source-factor batch, GPU work, field transfer, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/summary_tables/234_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit
outputs/experiments/1370_local_2d_source_factor_geomxdisc_objective_window_ladder_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_geometry_instability_objective_window_ladder_execution_summary.json
data/local_2d_source_factor_geometry_instability_objective_window_ladder_execution_objectives.csv
data/local_2d_source_factor_geometry_instability_objective_window_ladder_execution_confidence.csv
data/local_2d_source_factor_geometry_instability_objective_window_ladder_execution_required_artifacts.csv
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_OBJECTIVE_WINDOW_LADDER_EXECUTION_AUDIT.md
figures/local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.png
scripts/run_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
scripts/test_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
commands executed:                  true
timed out:                          false
exit code:                          0
elapsed seconds:                    471.871
complete optimizer output:          true
usable evidence ready:              true
required artifacts present:         6 / 6
candidate CSV count:                1
figure file count:                  4
confidence best x:                  188.0 mm
confidence truth x selected:        false
objective row count:                6
truth-x objective count:            0
lower-x objective count:            6
any objective truth x selected:     false
all objectives select lower x:      true
full batch ready:                   false
GPU work ready:                     false
field transfer ready:               false
```

Objective diagnostics for the update case:

| Objective | Best x mm | Best z mm | Best radius mm | Best misfit | Truth x | Truth xyz |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `base` | 188.0 | 90.0 | 5.0 | 0.7270403815749271 | false | false |
| `highband` | 188.0 | 90.0 | 5.0 | 0.5538109095852684 | false | false |
| `late` | 188.0 | 90.0 | 5.0 | 0.7886942776468757 | false | false |
| `late_high` | 188.0 | 90.0 | 5.0 | 0.8823877763972461 | false | false |
| `veryhigh` | 188.0 | 90.0 | 5.0 | 0.42294365040380777 | false | false |
| `early_high` | 188.0 | 90.0 | 5.0 | 0.2248946538450012 | false | false |

## Interpretation

The lower-x preference is not isolated to the base objective, highband
weighting, late-time windowing, or high-frequency windowing. All six objective
windows select the same lower x candidate.

This makes an objective-window repair unlikely for this branch. The remaining
root cause is more likely in the geometry/state setup, interaction with
neighbor rebars, rasterization/material discretization, or source/receiver
observable definition than in the current objective-window selection.

## Decision

Do not promote objective-window selection as a fix for the geometry-instability
case. Keep broad source-factor batch execution, GPU work, field transfer, and
claim-making blocked.

The next useful local 2D branch should be a geometry/state interaction audit:
compare whether the lower-x preference survives when neighbor rebar positions
or initial-state offsets are changed while target z and radius stay fixed.

## Milestone Snapshot

This is a result-driven local 2D execution milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
sha256: fee41868503f1d29f203d6e04f0b58a4fe05fefe716c9eaca4d88a10b2bc5159

test_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
sha256: cd0f64f3414e46468734401ede5dbd7fed3efd73f0c46748a74fc384ac746e1e
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
3 passed
```

Compile check:

```text
run_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py: pass
tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py: pass
```

Figure check:

```text
1671x738, dynamic range=255
```
