# Experiment 1675: 84-Grid Pilot Real-Executor Solver-Binding Gap Audit

Date: 2026-06-30

## Purpose

Audit what remains before the real-executor shell can bind to the CPU FDTD
solver route.

Run `1674` added the executor shell and proved that it can validate the revised
payload contracts while refusing real mode. This run inspects the low-level
CPU probe interface and lists the runtime inputs and output-writing pieces that
are still missing.

This run does not execute FDTD, accept pilot evidence, launch GPU work,
transfer to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1675_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_binding_gap_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_binding_gap_audit_binding_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_binding_gap_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_binding_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source shell ready:                  true
run_candidate_family callable:       true
binding rows:                        12
function-parameter bindings:         8
executor I/O bindings:               4
ready bindings:                      4
blocking bindings:                   8
solver binding ready:                false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
3D/HPC ready:                        false
gap audit ready:                     true
```

Blocking bindings:

```text
observed_by_case
scan_positions
time_values
mute
input_contract_writer
solver_log_writer
result_json_writer
post_write_command_runner
```

## Interpretation

The real-executor shell is a valid entry point, but it is not yet connected to
the solver. The remaining work is concrete: construct the observed data bundle,
scan positions, time axis, mute mask, input-contract writer, solver-log writer,
result JSON writer, and post-write command runner.

## Decision

Do not enable real FDTD mode until those eight bindings are implemented and
tested. The next executor task should be a bounded solver-binding design or
implementation step, still guarded by the five JSON output and command-check
requirements.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_binding_gap_audit.py
3 passed
```

Figure check:

```text
2105x847, dynamic range=255
```
