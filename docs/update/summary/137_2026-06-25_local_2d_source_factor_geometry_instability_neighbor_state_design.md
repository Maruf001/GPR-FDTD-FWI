# Local 2D Source-Factor Geometry-Instability Neighbor-State Design

Date: 2026-06-25

## Scope

This checkpoint records run `236`, a bounded CPU command design that tests
whether the geometry-instability lower-x preference is caused by the non-target
neighbor state.

This was command design only. It did not execute FDTD, optimizer commands, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/236_local_2d_source_factor_geometry_instability_neighbor_state_design
```

Tracked note:

```text
docs/experiments/912_local_2d_source_factor_geometry_instability_neighbor_state_design.md
```

## Result

```text
source execution run:             234
source all objectives lower x:    true
commands generated:               3
commands passing gates:           3
predicted runner experiment IDs:  1371, 1372, 1373
estimated candidate-objectives:   9
execution ready:                  true
full batch ready:                 false
GPU work ready:                   false
field transfer ready:             false
```

## Decision

Run `236` is the next executable local 2D geometry/state branch. It contains
three bounded CPU commands:

```text
truth_neighbor_positions_base
truth_neighbor_radii_base
truth_neighbor_full_base
```

Broad source-factor batch execution, GPU work, field transfer, and claims
remain blocked.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_neighbor_state_design.py
sha256: 25186e022f8098d7ee342007a9170935212f522d934f3e0726ed0718c7860200

test_local_2d_source_factor_geometry_instability_neighbor_state_design.py
sha256: 5cb1b5819488297b3095d22926198bcdd017bce6d15056bb12a6cc1255177876
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_neighbor_state_design.py -q
3 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_neighbor_state_design.py tests/test_local_2d_source_factor_geometry_instability_neighbor_state_design.py
pass
```

Figure check:

```text
1817x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then execute the three
neighbor-state CPU commands if resources remain safe.
