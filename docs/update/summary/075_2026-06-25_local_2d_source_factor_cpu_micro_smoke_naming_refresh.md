# Local 2D Source-Factor CPU Micro-Smoke Naming Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `180`, the corrected source-factor CPU
micro-smoke command design after the runner auto-prefix behavior was detected.

## Output

```text
outputs/summary_tables/180_local_2d_source_factor_cpu_micro_smoke_naming_refresh
```

Tracked note:

```text
docs/experiments/890_local_2d_source_factor_cpu_micro_smoke_naming_refresh.md
```

## Result

```text
predicted runner experiment ID:          1360
requested run name:                      local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1360_local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
micro validation pass:                   true
recommended cap seconds:                 300
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
single geometry offset:                  true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands generated:                      true
commands executed:                       false
micro-smoke execution ready:             true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

Run `180` supersedes the run `178` micro-smoke command. The next bounded
execution smoke should use the numeric-free `--run-name` and a five-minute cap.

Do not run the full source-factor CPU batch yet. Do not escalate to GPU or
field transfer from this design-only milestone.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
sha256: 88996a07f9484f11c24f84302fbca04b2cbc8b116705fd2d083200a7365ca4a1

test_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
sha256: 017c4dd3b5de7e8f9fc13d312d50f8835dd59f78d848da00895efa2f41a8598e
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py: pass
tests/test_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_micro_smoke_naming_refresh.png
1420x738, dynamic range=255
```

Marathon status: active. The next branch is a bounded execution smoke using the
corrected command, followed by an output-completeness audit before any broader
CPU batch.
