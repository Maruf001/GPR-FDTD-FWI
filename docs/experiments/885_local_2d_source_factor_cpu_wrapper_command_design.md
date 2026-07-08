# Experiment 885: Local 2D Source-Factor CPU Wrapper Command Design

Date: 2026-06-25

## Purpose

Turn the nine missing source-factor counterfactual diagnostics from run `172`
into CPU-only coordinate-optimizer command designs.

This is a command-design run only. It does not execute the commands, run new
FDTD, use GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/173_local_2d_source_factor_cpu_wrapper_command_design
```

Key artifacts:

```text
data/local_2d_source_factor_cpu_wrapper_commands.csv
data/local_2d_source_factor_cpu_wrapper_gates.csv
data/local_2d_source_factor_cpu_wrapper_command_summary.json
commands/run_local_2d_source_factor_counterfactual_cpu_commands.sh
docs/LOCAL_2D_SOURCE_FACTOR_CPU_WRAPPER_COMMAND_DESIGN.md
figures/local_2d_source_factor_cpu_wrapper_command_design.png
scripts/run_local_2d_source_factor_cpu_wrapper_command_design.py
scripts/test_local_2d_source_factor_cpu_wrapper_command_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
commands generated:                     9
unique source runs:                     2
gates:                                  4
passing gates:                          4
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

## Interpretation

The nine missing source-factor diagnostics can be expressed as CPU-only wrapper
commands against the existing coordinate optimizer. Each command fixes one
variant's source-frequency and source-time grid, uses a controlled
replication-case pair, and disables amplitude fitting.

This is not evidence yet. The commands are an execution design and must pass a
bounded CPU smoke check before full nine-command execution.

## Decision

Use these commands as the input to a bounded CPU smoke check. Do not use them as
counterfactual evidence until generated runs exist and pass the matched 1 mm
geometry/radius gate. Do not launch GPU work or field transfer from this
command design.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_wrapper_command_design.py
sha256: 768f0012a70cf201970824317d5d1beee8923b1ad7c452f9d5999340a99d7ba8

test_local_2d_source_factor_cpu_wrapper_command_design.py
sha256: 851c75b0901f87507dd9eb97af36900f92179a821c5867116326bb3a550ed8a8
```

Subsequent local 2D source-factor execution runs should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_wrapper_command_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_cpu_wrapper_command_design.png
1492x771, dynamic range=255
```
