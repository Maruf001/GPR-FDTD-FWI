# Local 2D Source-Factor Numbered CPU Command Design

Date: 2026-06-25

## Scope

This checkpoint records output `175`, a numbered refresh of the CPU wrapper
command design for source-factor counterfactual diagnostics.

## Output

```text
outputs/summary_tables/175_local_2d_source_factor_numbered_cpu_command_design
```

Tracked note:

```text
docs/experiments/887_local_2d_source_factor_numbered_cpu_command_design.md
```

## Result

```text
commands generated:                     9
assigned experiment ID start:           1359
assigned experiment ID end:             1367
numbered command passes:                9
numbered command failures:              0
output collisions:                      0
commands executed:                      false
single-command execution ready:         true
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Decision

Run `175` supersedes run `173` for actual execution because it allocates fresh
synthetic experiment IDs `1359` through `1367`. The next step should be one
bounded CPU smoke command, not the full batch.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_numbered_cpu_command_design.py
sha256: f8da0a52628fd9370676b77e97f25b98cc7f3970c01b51cdfb7564df11e5a654

test_local_2d_source_factor_numbered_cpu_command_design.py
sha256: ad393cec26adfc78f6e9318dd332e30749a262157babc85c894eadf3ca6647a9
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_numbered_cpu_command_design.py
4 passed
```

Python compile check:

```text
run_local_2d_source_factor_numbered_cpu_command_design.py: pass
tests/test_local_2d_source_factor_numbered_cpu_command_design.py: pass
```

Figure check:

```text
local_2d_source_factor_numbered_cpu_command_design.png
1600x736, dynamic range=255
```

Marathon status: active. The next branch should execute or preflight one
numbered CPU command before any full batch.
