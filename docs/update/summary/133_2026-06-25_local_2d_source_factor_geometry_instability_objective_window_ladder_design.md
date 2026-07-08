# Local 2D Source-Factor Geometry-Instability Objective-Window Ladder Design

Date: 2026-06-25

## Scope

This checkpoint records run `232`, a bounded CPU command design that expands
the corrected highband branch into the established six-objective diagnostic
ladder.

This was command design only. It did not execute FDTD, optimizer commands, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/232_local_2d_source_factor_geometry_instability_objective_window_ladder_design
```

Tracked note:

```text
docs/experiments/910_local_2d_source_factor_geometry_instability_objective_window_ladder_design.md
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
estimated candidate-objectives:   18
ladder design pass:               true
execution ready:                  true
full batch ready:                 false
GPU work ready:                   false
field transfer ready:             false
```

## Decision

Run `232` is the next executable local 2D objective/observable branch. It is
one bounded CPU command that tests whether `base`, `highband`, `late`,
`late_high`, `veryhigh`, or `early_high` can select truth x for the
geometry-instability case.

Broad source-factor batch execution, GPU work, field transfer, and claims
remain blocked.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
sha256: b6e403ffa583180a658bbb5259b403e1420971f7bca52ccae9693458c02fa607

test_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
sha256: e027e35789ce656e7a89650b56329a669eee48eb2f8cff386b794420b0269240
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py -q
2 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_design.py
pass
```

Figure check:

```text
1673x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then execute the single ladder
CPU command if resources remain safe.
