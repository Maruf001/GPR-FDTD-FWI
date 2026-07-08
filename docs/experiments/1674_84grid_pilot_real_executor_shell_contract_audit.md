# Experiment 1674: 84-Grid Pilot Real-Executor Shell Contract Audit

Date: 2026-06-30

## Purpose

Record the first real-executor shell for the revised five-row pilot.

Runs `1671`-`1673` prepared the historical no-executor audits so the executor
file could be added without invalidating older results. This run validates the
new executor shell: it can check revised payload contracts but still refuses
real FDTD execution because solver binding is not implemented yet.

This run does not execute FDTD, accept pilot evidence, launch GPU work,
transfer to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1674_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_shell_contract_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_shell_contract_audit_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_shell_contract_audit_refusal_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_shell_contract_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_shell_contract_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract checks:                     5
contract checks passed:              5
required payload IDs:                1;23;46;68;72
contains payload 68:                 true
contains stale payload 86:           false
real-mode refusals:                  1
unknown-payload refusals:            1
new FDTD executions:                 0
real FDTD enabled rows:              0
real executor shell available:       true
bounded pilot execution ready:       false
GPU work ready:                      false
field transfer ready:                false
3D/HPC ready:                        false
shell contract audit ready:          true
```

## Interpretation

The real-executor entry point now exists. It reads the run `1670` design
contract, validates the five revised payload rows, accepts payload `68` in
contract-check mode, and rejects stale payload `86`.

The shell is not an FDTD executor yet. Real mode returns an explicit refusal,
and no real result JSON files are produced.

## Decision

Use the shell as the future real-executor entry point. The next 2D executor
task is implementing and validating the solver-binding layer while preserving
the rule that no FDTD result is accepted until all five JSON outputs and their
command checks pass.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_cpu_screen_executor.py
5 passed

tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_shell_contract_audit.py
3 passed
```

Figure check:

```text
2141x847, dynamic range=255
```
