# Experiment 908: Local 2D Source-Factor Geometry-Instability Highband/Base Corrected Design

Date: 2026-06-25

## Purpose

Correct the invalid highband-only command from run `226`.

`run_multi_rebar_coordinate_optimizer.py` requires the first diagnostic
objective variant to be labelled `base`. Run `226` showed that a highband-only
command exits before producing output. This run keeps the highband discriminant
but prepends the required base objective.

This is a command-design milestone. It does not execute FDTD, optimizer
commands, GPU work, field transfer, field FWI, 3D/HPC, or neural-network
training.

## Output

```text
outputs/summary_tables/228_local_2d_source_factor_geometry_instability_highband_base_corrected_design
```

Key artifacts:

```text
data/local_2d_source_factor_geometry_instability_highband_base_corrected_command.csv
data/local_2d_source_factor_geometry_instability_highband_base_corrected_validation.csv
data/local_2d_source_factor_geometry_instability_highband_base_corrected_summary.json
commands/run_local_2d_source_factor_geometry_instability_highband_base_corrected.sh
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_HIGHBAND_BASE_CORRECTED_DESIGN.md
figures/local_2d_source_factor_geometry_instability_highband_base_corrected_design.png
scripts/run_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
scripts/test_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source execution run:             226
commands generated:               1
predicted runner experiment ID:   1369
expected runner output:           1369_local_2d_source_factor_geomxdisc_shifted_source_base_highband_cpu
first objective label:            base
objective count:                  2
contains highband:                true
estimated evaluations:            6
corrected design pass:            true
corrected execution ready:        true
full batch ready:                 false
GPU work ready:                   false
field transfer ready:             false
```

## Interpretation

The previous highband test failed for command-interface reasons, not because
the highband physics was tested. This corrected design creates the valid
objective sequence:

```text
base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15
```

The command remains bounded: target 0 only, x offsets `0,1,2`, z offset `-10`,
radius offset `-1`, shifted source timing `-50 ps`.

## Decision

Use run `228` as the source for the next single-command corrected highband CPU
execution audit. Do not run a broad source-factor batch, GPU work, field
transfer, or source-factor claims from the current evidence.

## Milestone Snapshot

This is a result-driven local 2D command-design milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
sha256: 294023a253f48fa3dfeed93542fd5efa34936fb40ec6edc4201883348bc126e7

test_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
sha256: 0c1cc5fa4535b2569d2d3b6b3f937d16f2a15319aa3f649ed4ee1731939edc3d
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_highband_base_corrected_design.py
2 passed
```

Figure check:

```text
local_2d_source_factor_geometry_instability_highband_base_corrected_design.png
1673x738, dynamic range=255
```
