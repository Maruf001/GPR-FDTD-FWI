# Experiment 910: Local 2D Source-Factor Geometry-Instability Objective-Window Ladder Design

Date: 2026-06-25

## Purpose

Design a bounded CPU command to test whether any established diagnostic
objective window selects the truth x for the geometry-instability case.

Run `230` executed the corrected base-plus-highband command successfully, but
both objectives still selected `x=188 mm` instead of the `x=190 mm` truth. This
run keeps the same geometry, source timing, material setup, target, and
candidate x values, then expands the objective diagnostics to the historical
six-objective ladder:

```text
base
highband
late
late_high
veryhigh
early_high
```

This is command design only. It does not execute FDTD, optimizer commands, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/232_local_2d_source_factor_geometry_instability_objective_window_ladder_design
```

Key artifacts:

```text
data/local_2d_source_factor_geometry_instability_objective_window_ladder_command.csv
data/local_2d_source_factor_geometry_instability_objective_window_ladder_validation.csv
data/local_2d_source_factor_geometry_instability_objective_window_ladder_summary.json
commands/run_local_2d_source_factor_geometry_instability_objective_window_ladder.sh
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_OBJECTIVE_WINDOW_LADDER_DESIGN.md
figures/local_2d_source_factor_geometry_instability_objective_window_ladder_design.png
scripts/run_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
scripts/test_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source execution run:             230
source highband truth x selected: false
commands generated:               1
predicted runner experiment ID:   1370
expected runner output:           1370_local_2d_source_factor_geomxdisc_objective_window_ladder_cpu
first objective label:            base
objective count:                  6
x candidate count:                3
estimated candidate-objectives:   18
ladder design pass:               true
execution ready:                  true
full batch ready:                 false
GPU work ready:                   false
field transfer ready:             false
```

Objective ladder:

```text
base:1.0,7.0,0.3,none,none,0.0
highband:1.0,7.0,0.3,1.1,3.4,0.15
late:1.5,5.5,0.2,none,none,0.0
late_high:1.5,5.5,0.2,1.1,3.4,0.15
veryhigh:1.0,7.0,0.3,1.8,4.2,0.15
early_high:0.8,3.5,0.2,1.1,3.4,0.15
```

## Interpretation

This is the right next discriminant because it does not broaden geometry or
launch a new source-factor batch. It asks a narrower question: is the lower-x
preference tied to a particular time/frequency window, or does it persist
across the established objective ladder?

## Decision

Use run `232` as the source for the next single-command CPU execution audit.
Do not launch broad source-factor batches, GPU work, field transfer, or claims
from the current evidence.

## Milestone Snapshot

This is a result-driven local 2D command-design milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
sha256: b6e403ffa583180a658bbb5259b403e1420971f7bca52ccae9693458c02fa607

test_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
sha256: e027e35789ce656e7a89650b56329a669eee48eb2f8cff386b794420b0269240
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
2 passed
```

Compile check:

```text
run_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py: pass
tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py: pass
```

Figure check:

```text
1673x738, dynamic range=255
```
