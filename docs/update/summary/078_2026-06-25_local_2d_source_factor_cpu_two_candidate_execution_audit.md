# Local 2D Source-Factor CPU Two-Candidate Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records output `183`, the execution audit for the
two-candidate source-factor CPU smoke designed in run `182`.

## Output

```text
outputs/summary_tables/183_local_2d_source_factor_cpu_two_candidate_execution_audit
outputs/experiments/1361_local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
```

Tracked note:

```text
docs/experiments/893_local_2d_source_factor_cpu_two_candidate_execution_audit.md
```

## Result

```text
cap seconds:                            900
audit elapsed seconds:                  319.838
optimizer elapsed seconds:              179.415
exit code:                              0
timed out:                              false
expected candidate count per case:      2
required artifacts present:             6 / 6
complete optimizer output:              true
usable evidence ready:                  true
double prefix detected:                 false
best x mm, nominal:                     189.0
best x mm, time-shift-only:             189.0
confidence labels:                      missing
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Decision

The two-candidate smoke validates a small CPU neighborhood and gives a first
ranking signal: both cases prefer x `189.0` mm over x `188.0` mm. It still does
not test radius competition, so confidence labels remain `missing`.

The next useful branch is a duplicated-script x/radius mini-neighborhood smoke.
The full source-factor batch, GPU work, and field transfer remain blocked.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_two_candidate_execution_audit.py
sha256: a7c169477d69ccbb2c7a0fcba6bbc08a04b003c4f842adb095b136f30a3cf294

test_local_2d_source_factor_cpu_two_candidate_execution_audit.py
sha256: 6343f28b568ae776ab9ec652f8ad49a016d03777e0f95786f894448e172927d2
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_two_candidate_execution_audit.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_two_candidate_execution_audit.py: pass
tests/test_local_2d_source_factor_cpu_two_candidate_execution_audit.py: pass
```

Figure checks:

```text
audit figure:       1420x738, dynamic range=255
optimizer figures:  4 files, dynamic range 238-255
```

Marathon status: active. The next branch should add a minimal radius competitor
while keeping the command bounded.
