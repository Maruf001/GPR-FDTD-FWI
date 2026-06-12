# Experiment 214: Next-Action Queue Coordinate Aggregate Audit Refresh

## Purpose

Refresh the next-action queue after run 680 made the run 679 state audit the
current commit-preparation context.

## 681: Next-Action Queue Coordinate Aggregate Audit Refresh

Output:

```text
outputs/experiments/681_next_action_queue_coordinate_aggregate_audit_refresh
```

Command:

```text
Update the next-action queue from run 678 so state audit points to run 679 and
commit preparation points to run 680.
```

Artifacts:

```text
README.md
next_action_queue.md
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
git diff --check: clean after run 681
```

## Interpretation

Run 681 is now the current next-action queue. It points local validation to run
675, aggregate CLI smokes to runs 609 and 676, objective CLI smokes to runs
611, 642, and 669, state audit to run 679, commit preparation to run 680,
archive coverage to run 654, restart to run 648, manuscript validation to run
636, and archive handoff to run 633.

## Next Decision

Default to code/docs review or manuscript work. Run a current archive coverage
refresh only if an external handoff package is likely.

