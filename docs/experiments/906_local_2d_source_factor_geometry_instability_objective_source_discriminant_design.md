# Experiment 906: Local 2D Source-Factor Geometry-Instability Objective/Source Discriminant Design

Date: 2026-06-25

## Purpose

Design the next bounded CPU commands after run `222` showed that the
geometry-instability family has a persistent lower-x preference even when truth
x is included and z/radius are fixed to truth.

This is a command-design milestone. It does not execute FDTD, optimizer
commands, GPU work, field transfer, field FWI, 3D/HPC, or neural-network
training.

## Output

```text
outputs/summary_tables/224_local_2d_source_factor_geometry_instability_objective_source_discriminant_design
```

Key artifacts:

```text
data/local_2d_source_factor_geometry_instability_objective_source_discriminant_commands.csv
data/local_2d_source_factor_geometry_instability_objective_source_discriminant_validation.csv
data/local_2d_source_factor_geometry_instability_objective_source_discriminant_summary.json
commands/run_local_2d_source_factor_geometry_instability_objective_source_discriminants.sh
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_OBJECTIVE_SOURCE_DISCRIMINANT_DESIGN.md
figures/local_2d_source_factor_geometry_instability_objective_source_discriminant_design.png
scripts/run_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
scripts/test_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source audit run:                     222
source command run:                   218
commands generated:                   3
predicted runner experiment start:    1367
predicted runner experiment end:      1369
command design passes:                3
command design failures:              0
estimated candidate/profile/objective evaluations: 12
output collisions:                    0
geometry discriminant execution ready: true
full batch ready:                     false
GPU work ready:                       false
field transfer ready:                 false
```

Designed commands:

| Expected output | Discriminant | Source times ps | Objective | Estimated evals |
| --- | --- | --- | --- | ---: |
| `1367_local_2d_source_factor_geomxdisc_matched_nominal_source_base_cpu` | matched nominal source | `0.0` | base | 3 |
| `1368_local_2d_source_factor_geomxdisc_shifted_source_highband_cpu` | shifted source highband | `-50.0` | highband | 3 |
| `1369_local_2d_source_factor_geomxdisc_time_grid_base_cpu` | time grid base | `0.0,-50.0` | base | 6 |

## Interpretation

Run `222` ruled out the simple explanation that geometry-instability failed
only because truth x was absent. This design separates three hypotheses:

1. Matched nominal source timing may remove the lower-x preference.
2. High-band objective weighting may change the x ordering.
3. Allowing both nominal and shifted source timing may expose whether timing
   mismatch is driving the preference.

## Decision

Use run `224` as the source for the next bounded geometry-instability CPU
execution audit. Do not run a broad source-factor batch, GPU work, or field
transfer from the current evidence.

## Milestone Snapshot

This is a result-driven local 2D command-design milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
sha256: afe5d2822d53558561a1f48281fa01e40287cc30b556d4f53671a70873e60a1f

test_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
sha256: 92c15c43a01785603647e0615db290a0f7b13b37219e2440499740dce867b67a
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
2 passed
```

Figure check:

```text
local_2d_source_factor_geometry_instability_objective_source_discriminant_design.png
2032x770, dynamic range=255
```
