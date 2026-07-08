# Local 2D Source-Factor CPU Wrapper Parse Smoke

Date: 2026-06-25

## Scope

This checkpoint records output `174`, a static parse/gate smoke for the CPU
wrapper command design from run `173`.

## Output

```text
outputs/summary_tables/174_local_2d_source_factor_cpu_wrapper_parse_smoke
```

Tracked note:

```text
docs/experiments/886_local_2d_source_factor_cpu_wrapper_parse_smoke.md
```

## Result

```text
commands parsed:                         9
parse passes:                            9
parse failures:                          0
output collisions:                       0
parse smoke pass:                        true
commands executed:                       false
single-command execution ready:          true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

The generated CPU commands are internally consistent and collision-free. The
next execution step should be a single bounded CPU command smoke, not the full
nine-command batch. Full source robustness, GPU work, and field transfer remain
blocked.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_wrapper_parse_smoke.py
sha256: 0ac03221f932d61c7ffcd0a46e7fa842dbadf17fb4c8fc50a1219e0e3ab859f1

test_local_2d_source_factor_cpu_wrapper_parse_smoke.py
sha256: 8c26dc9fccd502c07a1e17e008237d8e8469b2df8b5f5275d54144b991ff7dc3
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_wrapper_parse_smoke.py
4 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_wrapper_parse_smoke.py: pass
tests/test_local_2d_source_factor_cpu_wrapper_parse_smoke.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_wrapper_parse_smoke.png
1276x738, dynamic range=255
```

Marathon status: active. The next branch should run or further preflight one
bounded CPU command before any full batch.
