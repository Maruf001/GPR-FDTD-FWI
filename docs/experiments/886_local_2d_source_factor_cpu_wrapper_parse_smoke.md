# Experiment 886: Local 2D Source-Factor CPU Wrapper Parse Smoke

Date: 2026-06-25

## Purpose

Statically validate the CPU wrapper command design from run `173` before any
optimizer execution.

This is a parse/gate smoke only. It does not execute the commands, run new FDTD,
use GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/174_local_2d_source_factor_cpu_wrapper_parse_smoke
```

Key artifacts:

```text
data/local_2d_source_factor_cpu_wrapper_parse_smoke.csv
data/local_2d_source_factor_cpu_wrapper_parse_smoke_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_WRAPPER_PARSE_SMOKE.md
figures/local_2d_source_factor_cpu_wrapper_parse_smoke.png
scripts/run_local_2d_source_factor_cpu_wrapper_parse_smoke.py
scripts/test_local_2d_source_factor_cpu_wrapper_parse_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
commands parsed:                         9
parse passes:                            9
parse failures:                          0
output collisions:                       0
CPU gate passes:                         9
no-fit-amplitude gate passes:            9
update-label matches:                    9
scalar source-grid commands:             9
parse smoke pass:                        true
commands executed:                       false
single-command execution ready:          true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Interpretation

All nine generated CPU wrapper commands pass static parse gates and have no
output-folder collisions. This still does not execute the optimizer.

## Decision

A single bounded CPU command smoke is technically ready. Keep full nine-command
execution, GPU work, field transfer, broad source robustness, and time-zero-only
explanation blocked until an executed smoke run is inspected.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_wrapper_parse_smoke.py
sha256: 0ac03221f932d61c7ffcd0a46e7fa842dbadf17fb4c8fc50a1219e0e3ab859f1

test_local_2d_source_factor_cpu_wrapper_parse_smoke.py
sha256: 8c26dc9fccd502c07a1e17e008237d8e8469b2df8b5f5275d54144b991ff7dc3
```

Subsequent local 2D source-factor execution runs should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_wrapper_parse_smoke.py
4 passed
```

Figure check:

```text
local_2d_source_factor_cpu_wrapper_parse_smoke.png
1276x738, dynamic range=255
```
