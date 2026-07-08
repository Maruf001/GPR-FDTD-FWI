# Experiment 1676: 84-Grid Pilot Real Executor Input-Contract Writer Audit

Date: 2026-06-30

## Purpose

Materialize non-evidence input contracts for the revised five-row 84-grid pilot
real executor.

Run `1675` showed that the real executor shell exists but the solver-binding
layer still has eight blockers. This run closes one implementation gap by
adding an input-contract writer for the revised pilot payloads
`1;23;46;68;72`.

This run does not bind observed data, scan positions, time values, or a mute
mask; does not run FDTD; does not write real solver logs or real result JSON;
and does not promote GPU, field, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1676_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_audit
```

Key artifacts:

```text
data/input_contracts/payload_001_input_contract.json
data/input_contracts/payload_023_input_contract.json
data/input_contracts/payload_046_input_contract.json
data/input_contracts/payload_068_input_contract.json
data/input_contracts/payload_072_input_contract.json
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source solver-binding gap ready:        true
input-contract writer available:        true
pilot payloads:                         5
input contracts written:                5
writer exits successful:                5
payload 68 included:                    true
stale payload 86 included:              false
unresolved solver bindings total:       20
prior blocking bindings:                8
bindings closed by this run:            1
remaining blocking bindings:            7
solver binding ready:                   false
commands executed:                      false
new FDTD executed:                      false
GPU work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
audit ready:                            true
```

Remaining blockers:

| Binding | Status |
| --- | --- |
| observed_by_case | unresolved |
| scan_positions | unresolved |
| time_values | unresolved |
| mute | unresolved |
| solver_log_writer | unresolved |
| result_json_writer | unresolved |
| post_write_command_runner | unresolved |

## Interpretation

The revised pilot now has a structured input contract for every payload. The
contracts preserve the payload identity, objective profile, transition bin,
candidate transmitter-receiver offset, template path, staged output path, and
validation command. They explicitly mark the solver-array bindings as
unresolved.

This is implementation progress, not execution evidence. The writer closes the
input-contract-writing gap only. Real FDTD remains blocked until the solver
arrays, solver log writer, result JSON writer, and post-write validation runner
exist and pass validation.

## Decision

Use run `1676` as the current 2D real-executor input-contract checkpoint. Do
not enable real FDTD execution until the seven remaining bindings are
implemented and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_audit.py
7 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
