# Local 2D Source-Factor CPU X/Z/Radius Local Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records output `188`, the execution audit for the x/z/radius
local source-factor CPU smoke designed in run `187`.

## Output

```text
outputs/summary_tables/188_local_2d_source_factor_cpu_xzradius_local_execution_audit
outputs/experiments/1363_local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
```

Tracked note:

```text
docs/experiments/897_local_2d_source_factor_cpu_xzradius_local_execution_audit.md
```

## Result

```text
cap seconds:                            3600
audit elapsed seconds:                  748.947
optimizer elapsed seconds:              597.056
exit code:                              0
timed out:                              false
expected candidate count per case:      8
required artifacts present:             6 / 6
complete optimizer output:              true
usable evidence ready:                  true
double prefix detected:                 false
best x mm, nominal:                     189.0
best z mm, nominal:                     90.0
best radius mm, nominal:                5.0
radius margin rel, nominal:             0.101490
confidence, nominal:                    strong
best x mm, time-shift-only:             189.0
best z mm, time-shift-only:             90.0
best radius mm, time-shift-only:        5.0
radius margin rel, time-shift-only:     0.009782
confidence, time-shift-only:            moderate
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Decision

The local x/z/radius neighborhood selected the local truth candidate in both
source cases. The source perturbation weakened the radius margin from strong to
moderate but did not change the winner.

This supports bounded replication, not full batch/GPU/field escalation.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
sha256: 9bfe375d520a2284336c1daa6e53fdc69c642445585cc80088d87f9a09bf8991

test_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
sha256: 67222e50f5ecb2c28f1d818e0283072a1d26e3619a65fcc1f329e9308163def1
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_xzradius_local_execution_audit.py: pass
tests/test_local_2d_source_factor_cpu_xzradius_local_execution_audit.py: pass
```

Figure checks:

```text
audit figure:       1420x738, dynamic range=255
optimizer figures:  4 files, dynamic range 238-255
```

Marathon status: active. Continue with bounded replication or another
single-target local neighborhood; do not stop at this checkpoint.
