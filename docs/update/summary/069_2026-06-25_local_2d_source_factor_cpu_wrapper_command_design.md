# Local 2D Source-Factor CPU Wrapper Command Design

Date: 2026-06-25

## Scope

This checkpoint records output `173`, a CPU-only command design for the nine
missing source-factor counterfactual diagnostics from run `172`.

## Output

```text
outputs/summary_tables/173_local_2d_source_factor_cpu_wrapper_command_design
```

Tracked note:

```text
docs/experiments/885_local_2d_source_factor_cpu_wrapper_command_design.md
```

## Result

```text
commands generated:                     9
unique source runs:                     2
CPU only:                               true
no-fit amplitude:                       true
one variant per command:                true
commands executed:                      false
bounded CPU smoke ready:                true
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Decision

Run `173` provides a CPU-only command plan, not executed evidence. The next
step is a bounded CPU smoke check on one command before full nine-command
execution. GPU work, field transfer, broad source robustness, and time-zero-only
explanation remain blocked.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_wrapper_command_design.py
sha256: 768f0012a70cf201970824317d5d1beee8923b1ad7c452f9d5999340a99d7ba8

test_local_2d_source_factor_cpu_wrapper_command_design.py
sha256: 851c75b0901f87507dd9eb97af36900f92179a821c5867116326bb3a550ed8a8
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_wrapper_command_design.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_wrapper_command_design.py: pass
tests/test_local_2d_source_factor_cpu_wrapper_command_design.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_wrapper_command_design.png
1492x771, dynamic range=255
```

Marathon status: active. The next branch should smoke-test command parsing or
execute the smallest CPU-only dry run before launching any full command batch.
