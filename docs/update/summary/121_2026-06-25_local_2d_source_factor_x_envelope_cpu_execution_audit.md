# Local 2D Source-Factor X-Envelope CPU Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records run `220`, which executed the two bounded CPU commands
designed by run `218`.

This was targeted CPU optimizer work only. It did not launch a full batch, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/220_local_2d_source_factor_x_envelope_cpu_execution_audit
```

Tracked note:

```text
docs/experiments/904_local_2d_source_factor_x_envelope_cpu_execution_audit.md
```

Optimizer outputs:

```text
outputs/experiments/1365_local_2d_source_factor_xenvelope_max_amplitude_stress_ff_max_amplitude_stress_time_shift_only_cpu
outputs/experiments/1366_local_2d_source_factor_xenvelope_max_geometry_instability_ff_max_geometry_instability_time_shift_only_cpu
```

## Result

```text
commands executed:                2 / 2
timed out:                        0
nonzero exits:                    0
complete optimizer outputs:       2 / 2
required artifacts present:       12 / 12
candidate CSV count:              2
figure file count:                8
total elapsed seconds:            845.85
truth x selected count:           1 / 2
truth xyz selected count:         1 / 2
x-envelope evidence ready:        true
x-envelope truth x supported:     false
x-envelope truth xyz supported:   false
full batch ready:                 false
GPU work ready:                   false
field transfer ready:             false
```

Per-case result:

| Family | Best x | Best z | Best r | Truth x selected |
| --- | ---: | ---: | ---: | --- |
| `max_amplitude_stress` | 190.0 | 90.0 | 5.0 | true |
| `max_geometry_instability` | 188.0 | 90.0 | 5.0 | false |

## Decision

The x-envelope branch is now executed and evidence-ready, but it does not
support promotion. The amplitude-stress case resolves when truth x is included;
the geometry-instability case still prefers `x=188`.

The next useful local 2D task is a geometry-instability discriminant audit.
Full source-factor batch execution, GPU work, field transfer, and source-factor
claims remain blocked.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_x_envelope_cpu_execution_audit.py
sha256: d58847980a3790ba4f46c5f3824fd620813fd7c8e5bef885cbe9b2aaebe303e6

test_local_2d_source_factor_x_envelope_cpu_execution_audit.py
sha256: 63d85699c0bd22c2327d404480e6f1672da27649b12dd0c41c94af09c0cd2131
```

Future related local 2D work should start from a duplicated run-specific
script rather than editing this milestone script in place.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_x_envelope_cpu_execution_audit.py -q
4 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_x_envelope_cpu_execution_audit.py tests/test_local_2d_source_factor_x_envelope_cpu_execution_audit.py
pass
```

Figure check:

```text
1852x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with a snapshot-audit refresh, then a
geometry-instability discriminant audit.
