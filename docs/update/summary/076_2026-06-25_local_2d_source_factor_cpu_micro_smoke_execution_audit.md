# Local 2D Source-Factor CPU Micro-Smoke Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records output `181`, the execution audit for the corrected
source-factor CPU micro-smoke command from run `180`.

## Output

```text
outputs/summary_tables/181_local_2d_source_factor_cpu_micro_smoke_execution_audit
outputs/experiments/1360_local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
```

Tracked note:

```text
docs/experiments/891_local_2d_source_factor_cpu_micro_smoke_execution_audit.md
```

## Result

```text
cap seconds:                            300
audit elapsed seconds:                  262.859
optimizer elapsed seconds:              85.753
exit code:                              0
timed out:                              false
candidate CSV count:                    1
figure file count:                      4
required artifacts present:             6 / 6
complete optimizer output:              true
usable evidence ready:                  true
double prefix detected:                 false
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Decision

The corrected micro-smoke validates the execution path and naming contract. It
does not validate source-factor robustness because the grid has only one
candidate and therefore no meaningful ranking margin.

The next useful branch is a duplicated-script bounded CPU smoke with a small
candidate neighborhood. Keep the full nine-command batch, GPU work, and field
transfer blocked until that wider smoke completes.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
sha256: d6a08bcc2f5d190eca6f4ac920da13d80988e208a6fae345e92f098500258d02

test_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
sha256: 3dd5b0846b8ad818d4667428771f2d46c5c4a6b9552f471147e6f7eef7391151
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_micro_smoke_execution_audit.py: pass
tests/test_local_2d_source_factor_cpu_micro_smoke_execution_audit.py: pass
```

Figure checks:

```text
audit figure:       1420x738, dynamic range=255
optimizer figures:  4 files, dynamic range 238-255
```

Marathon status: active. The next branch should widen the CPU smoke minimally
while preserving the validated numeric-free `--run-name` convention.
