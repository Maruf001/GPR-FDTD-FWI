# Experiment 887: Local 2D Source-Factor Numbered CPU Command Design

Date: 2026-06-25

## Purpose

Refresh the CPU wrapper command design from run `173` with fresh synthetic
experiment IDs before any execution.

This avoids creating confusing duplicate-prefix output folders based on the
source runs `221` and `233`.

This is a command-design run only. It does not execute the commands, run new
FDTD, use GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/175_local_2d_source_factor_numbered_cpu_command_design
```

Key artifacts:

```text
data/local_2d_source_factor_numbered_cpu_commands.csv
data/local_2d_source_factor_numbered_cpu_command_validation.csv
data/local_2d_source_factor_numbered_cpu_command_summary.json
commands/run_local_2d_source_factor_numbered_cpu_commands.sh
docs/LOCAL_2D_SOURCE_FACTOR_NUMBERED_CPU_COMMAND_DESIGN.md
figures/local_2d_source_factor_numbered_cpu_command_design.png
scripts/run_local_2d_source_factor_numbered_cpu_command_design.py
scripts/test_local_2d_source_factor_numbered_cpu_command_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
commands generated:                     9
assigned experiment ID start:           1359
assigned experiment ID end:             1367
numbered command passes:                9
numbered command failures:              0
output collisions:                      0
CPU only:                               true
no-fit amplitude:                       true
commands executed:                      false
single-command execution ready:         true
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Interpretation

The CPU wrapper commands now allocate fresh synthetic experiment IDs instead of
reusing source-run numeric prefixes. The numbered commands supersede the
unnumbered run `173` command script for future execution.

## Decision

Use this numbered command set for any future bounded CPU smoke. Keep full batch
execution, GPU work, field transfer, and source-robustness claims blocked until
a single numbered command has been executed and inspected.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_numbered_cpu_command_design.py
sha256: f8da0a52628fd9370676b77e97f25b98cc7f3970c01b51cdfb7564df11e5a654

test_local_2d_source_factor_numbered_cpu_command_design.py
sha256: ad393cec26adfc78f6e9318dd332e30749a262157babc85c894eadf3ca6647a9
```

Subsequent local 2D source-factor execution runs should start from a duplicated
run-specific script or from the numbered command artifact, not from the
superseded unnumbered command script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_numbered_cpu_command_design.py
4 passed
```

Figure check:

```text
local_2d_source_factor_numbered_cpu_command_design.png
1600x736, dynamic range=255
```
