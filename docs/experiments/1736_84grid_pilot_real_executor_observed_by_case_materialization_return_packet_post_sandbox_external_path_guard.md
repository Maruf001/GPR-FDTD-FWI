# Experiment 1736: 84-Grid Observed-by-Case Materialization Return-Packet Post-Sandbox External-Path Guard

Date: 2026-06-30

## Purpose

Guard the locked external-return paths after run `1733` completed the
21-item materialization return-packet contract inside an output-local sandbox.

Run `1733` proved that the file, parse, and load mechanics can pass when the
packet is complete. This run checks that the sandbox completion did not create
external return files, materialize observed data, or execute FDTD.

## Output

```text
outputs/experiments/1736_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard.png
scripts/
```

## Result

```text
source sandbox smoke ready:         true
source validator ready:             true
source sensitivity ready:           true
guard rows:                         21
guard roles:                        3
external paths under return root:   21
external items present now:         0
source external items present:      0
sandbox items present:              21
sandbox nonempty items:             21
sandbox accepted items:             21
sandbox/external path overlaps:     0
sandbox under external return root: 0
synthetic-only items:               21
observed data materialized:         0
new FDTD executions:                0
ready for materialization:          false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The completed sandbox packet stayed output-local. All 21 expected external
return paths are still empty, and none of the sandbox items overlap those
paths or sit under the external return root.

This preserves the distinction between a positive intake-mechanics smoke and a
real materialization result.

## Decision

Keep real materialization, FDTD execution, GPU work, field transfer, field
FWI, and 3D/HPC blocked until real external return items are accepted through
the locked contract.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard.py

3 passed
```

Figure check:

```text
2609x845, dynamic range=255
```
