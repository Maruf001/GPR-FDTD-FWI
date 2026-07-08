# Local 2D Source-Factor X-Envelope CPU Command Design

Date: 2026-06-25

## Scope

This checkpoint records the conversion of the run `216` source-factor
x-envelope design into executable local 2D CPU optimizer commands.

This was CPU-side command design only. It did not run FDTD, GPU work, field
transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/218_local_2d_source_factor_x_envelope_cpu_command_design
```

Tracked note:

```text
docs/experiments/903_local_2d_source_factor_x_envelope_cpu_command_design.md
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

The generated commands are:

| Expected output | Family | Offsets |
| --- | --- | --- |
| `1365_local_2d_source_factor_xenvelope_max_amplitude_stress_ff_max_amplitude_stress_time_shift_only_cpu` | `max_amplitude_stress` | x=`1,2`, z=`5`, r=`-1` |
| `1366_local_2d_source_factor_xenvelope_max_geometry_instability_ff_max_geometry_instability_time_shift_only_cpu` | `max_geometry_instability` | x=`0,1,2`, z=`-10`, r=`-1` |

## Decision

Run `218` is the current executable local 2D source-factor branch. The next
defensible task is an execution audit that runs these two bounded CPU commands
and checks whether they produce complete optimizer evidence.

The branch still does not justify a full batch, GPU run, field transfer, or
source-factor claim.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_x_envelope_cpu_command_design.py
sha256: c071e36e5e24219177a730e0b3f609d048c20aa460160267537373c47e479e02

test_local_2d_source_factor_x_envelope_cpu_command_design.py
sha256: 1d271ac6c57bee3384a1078c04a29bf2a6de0331f33d9d86545d597e096b7a0d
```

Future related local 2D execution work should start from a duplicated
run-specific script rather than editing this milestone script in place.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_x_envelope_cpu_command_design.py -q
3 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_x_envelope_cpu_command_design.py tests/test_local_2d_source_factor_x_envelope_cpu_command_design.py
pass
```

Figure check:

```text
1852x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with the execution-audit branch from a duplicated
run-specific script.
