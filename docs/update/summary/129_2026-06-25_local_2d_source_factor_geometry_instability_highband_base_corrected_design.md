# Local 2D Source-Factor Geometry-Instability Highband/Base Corrected Design

Date: 2026-06-25

## Scope

This checkpoint records run `228`, which corrects the invalid highband-only
command from run `226` by prepending the required `base` objective.

This was command design only. It did not execute FDTD, optimizer commands, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/228_local_2d_source_factor_geometry_instability_highband_base_corrected_design
```

Tracked note:

```text
docs/experiments/908_local_2d_source_factor_geometry_instability_highband_base_corrected_design.md
```

## Result

```text
commands generated:               1
predicted runner experiment ID:   1369
expected runner output:           1369_local_2d_source_factor_geomxdisc_shifted_source_base_highband_cpu
first objective label:            base
objective count:                  2
estimated evaluations:            6
corrected design pass:            true
corrected execution ready:        true
full batch ready:                 false
GPU work ready:                   false
field transfer ready:             false
```

## Decision

Run `228` is the next executable local 2D highband branch. It is one bounded
CPU command. Full source-factor batch execution, GPU work, field transfer, and
claims remain blocked.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
sha256: 294023a253f48fa3dfeed93542fd5efa34936fb40ec6edc4201883348bc126e7

test_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
sha256: 0c1cc5fa4535b2569d2d3b6b3f937d16f2a15319aa3f649ed4ee1731939edc3d
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py -q
2 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py tests/test_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
pass
```

Figure check:

```text
1673x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then execute the single
corrected highband/base CPU command if resources remain safe.
