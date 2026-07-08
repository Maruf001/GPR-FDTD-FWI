# Experiment 904: Local 2D Source-Factor X-Envelope CPU Execution Audit

Date: 2026-06-25

## Purpose

Execute the two bounded CPU commands from run `218` and audit whether including
truth x resolves the two local 2D source-factor update cases.

This run performs CPU FDTD/optimizer work only for the two targeted commands.
It does not launch a full source-factor batch, GPU work, field transfer, field
FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/220_local_2d_source_factor_x_envelope_cpu_execution_audit
```

Optimizer outputs:

```text
outputs/experiments/1365_local_2d_source_factor_xenvelope_max_amplitude_stress_ff_max_amplitude_stress_time_shift_only_cpu
outputs/experiments/1366_local_2d_source_factor_xenvelope_max_geometry_instability_ff_max_geometry_instability_time_shift_only_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_x_envelope_cpu_execution_rows.csv
data/local_2d_source_factor_x_envelope_cpu_execution_results.csv
data/local_2d_source_factor_x_envelope_cpu_execution_required_artifacts.csv
data/local_2d_source_factor_x_envelope_cpu_execution_audit_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_X_ENVELOPE_CPU_EXECUTION_AUDIT.md
figures/local_2d_source_factor_x_envelope_cpu_execution_audit.png
scripts/run_local_2d_source_factor_x_envelope_cpu_execution_audit.py
scripts/test_local_2d_source_factor_x_envelope_cpu_execution_audit.py
scripts/script_snapshot_manifest.json
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

| Family | Candidate count | Best x | Best z | Best radius | Truth x | Truth xyz |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `max_amplitude_stress` | 2 | 190.0 | 90.0 | 5.0 | true | true |
| `max_geometry_instability` | 3 | 188.0 | 90.0 | 5.0 | false | false |

## Interpretation

The targeted x-envelope run produced complete evidence, but it did not resolve
the source-factor branch. Including truth x is sufficient for the amplitude
stress update case, where the optimizer selects `x=190, z=90, r=5`. It is not
sufficient for the geometry-instability update case, where the optimizer still
selects `x=188, z=90, r=5` even though `x=190` was in the candidate set.

This means the previous decision boundary remains: do not promote the current
source-factor branch to a full batch, GPU work, or field transfer. The remaining
issue is not merely that truth x was outside the candidate envelope; the
geometry-instability case prefers the lower-x candidate under the current
source/noise/objective settings.

## Decision

Use run `220` as the current local 2D source-factor execution checkpoint. The
next useful local 2D task is a geometry-instability discriminant audit, not a
broader compute promotion.

## Milestone Snapshot

This is a result-driven local 2D execution milestone. It froze:

```text
run_local_2d_source_factor_x_envelope_cpu_execution_audit.py
sha256: d58847980a3790ba4f46c5f3824fd620813fd7c8e5bef885cbe9b2aaebe303e6

test_local_2d_source_factor_x_envelope_cpu_execution_audit.py
sha256: 63d85699c0bd22c2327d404480e6f1672da27649b12dd0c41c94af09c0cd2131
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_x_envelope_cpu_execution_audit.py
4 passed
```

Figure check:

```text
local_2d_source_factor_x_envelope_cpu_execution_audit.png
1852x738, dynamic range=255
```
