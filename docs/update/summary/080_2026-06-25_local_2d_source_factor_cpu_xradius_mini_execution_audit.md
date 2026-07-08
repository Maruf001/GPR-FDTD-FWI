# Local 2D Source-Factor CPU X/Radius Mini Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records output `185`, the execution audit for the x/radius
mini-neighborhood source-factor CPU smoke designed in run `184`.

## Output

```text
outputs/summary_tables/185_local_2d_source_factor_cpu_xradius_mini_execution_audit
outputs/experiments/1362_local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
```

Tracked note:

```text
docs/experiments/895_local_2d_source_factor_cpu_xradius_mini_execution_audit.md
```

## Result

```text
cap seconds:                            1800
audit elapsed seconds:                  426.060
optimizer elapsed seconds:              284.008
exit code:                              0
timed out:                              false
expected candidate count per case:      4
required artifacts present:             6 / 6
complete optimizer output:              true
usable evidence ready:                  true
double prefix detected:                 false
best x mm, nominal:                     189.0
best radius mm, nominal:                5.0
radius margin abs, nominal:             0.108855
radius margin rel, nominal:             0.128188
best x mm, time-shift-only:             189.0
best radius mm, time-shift-only:        5.0
radius margin abs, time-shift-only:     0.075729
radius margin rel, time-shift-only:     0.067690
confidence labels:                      strong, strong
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Decision

The x/radius mini-neighborhood validates a useful bounded CPU path. Both source
cases select x `189.0` mm and radius `5.0` mm with strong radius margins.

This is still single-target, single-family evidence. The next useful branch is
bounded replication or a slightly wider local neighborhood, not full batch,
GPU, or field transfer.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
sha256: 7add5722dc040e4e27a66a4126e6f382c4dc13fbf0061727c8782b8356a9d8c9

test_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
sha256: f18b60a0f625dc71f5670a65c6293cce64be1c22113fd05b7b9ae7dc1b71d27d
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_xradius_mini_execution_audit.py: pass
tests/test_local_2d_source_factor_cpu_xradius_mini_execution_audit.py: pass
```

Figure checks:

```text
audit figure:       1420x738, dynamic range=255
optimizer figures:  4 files, dynamic range 238-255
```

Marathon status: active. Continue with bounded replication or a slightly wider
local neighborhood before any broader batch or GPU work.
