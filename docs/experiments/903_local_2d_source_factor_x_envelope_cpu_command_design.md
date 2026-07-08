# Experiment 903: Local 2D Source-Factor X-Envelope CPU Command Design

Date: 2026-06-25

## Purpose

Convert the run `216` x-envelope design into executable local 2D CPU optimizer
commands.

Run `216` expressed the next source-factor question in absolute millimeters:
include target-0 truth x for the two update cases while keeping the supported
truth z/radius fixed. This run translates those absolute candidate values into
the offset-based command interface used by `run_multi_rebar_coordinate_optimizer.py`.

This is a command-design milestone. It does not execute FDTD, GPU work, field
transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/218_local_2d_source_factor_x_envelope_cpu_command_design
```

Key artifacts:

```text
data/local_2d_source_factor_x_envelope_cpu_command_rows.csv
data/local_2d_source_factor_x_envelope_cpu_command_validation.csv
data/local_2d_source_factor_x_envelope_cpu_command_summary.json
commands/run_local_2d_source_factor_x_envelope_cpu_commands.sh
docs/LOCAL_2D_SOURCE_FACTOR_X_ENVELOPE_CPU_COMMAND_DESIGN.md
figures/local_2d_source_factor_x_envelope_cpu_command_design.png
scripts/run_local_2d_source_factor_x_envelope_cpu_command_design.py
scripts/test_local_2d_source_factor_x_envelope_cpu_command_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source design run:                  216
source command run:                 175
commands generated:                 2
predicted runner experiment start:  1365
predicted runner experiment end:    1366
command design passes:              2
command design failures:            0
candidate evaluations:              5
output collisions:                  0
small CPU execution ready:          true
full batch ready:                   false
GPU work ready:                     false
field transfer ready:               false
```

Designed commands:

| Index | Expected output | Family | X offsets | Z offsets | Radius offsets | Candidates |
| ---: | --- | --- | --- | --- | --- | ---: |
| 1 | `1365_local_2d_source_factor_xenvelope_max_amplitude_stress_ff_max_amplitude_stress_time_shift_only_cpu` | `max_amplitude_stress` | `1,2` | `5` | `-1` | 2 |
| 2 | `1366_local_2d_source_factor_xenvelope_max_geometry_instability_ff_max_geometry_instability_time_shift_only_cpu` | `max_geometry_instability` | `0,1,2` | `-10` | `-1` | 3 |

## Interpretation

The branch now has an executable next step. The prior x/z/radius evidence was
blocked because truth x was outside the tested envelope. This run closes the
command-design part of that gap by generating two bounded CPU commands that
include truth x and hold z/radius at the values that previously passed.

The commands intentionally use run names without numeric prefixes because the
optimizer runner adds the experiment ID prefix. This avoids the double-prefix
problem seen in the earlier source-factor command stream.

## Decision

Use run `218` as the source for the next local 2D x-envelope CPU execution
audit. Do not promote to full batch, GPU work, field transfer, or source-factor
claims until those two commands are actually executed and inspected.

## Milestone Snapshot

This is a result-driven local 2D command-design milestone. It froze:

```text
run_local_2d_source_factor_x_envelope_cpu_command_design.py
sha256: c071e36e5e24219177a730e0b3f609d048c20aa460160267537373c47e479e02

test_local_2d_source_factor_x_envelope_cpu_command_design.py
sha256: 1d271ac6c57bee3384a1078c04a29bf2a6de0331f33d9d86545d597e096b7a0d
```

Subsequent local 2D source-factor execution experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_x_envelope_cpu_command_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_x_envelope_cpu_command_design.png
1852x738, dynamic range=255
```
