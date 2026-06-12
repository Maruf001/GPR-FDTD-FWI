# Experiment 211: Next-Action Queue Coordinate Aggregate Smoke Refresh

## Purpose

Refresh the next-action queue after run 677 made the coordinate aggregate
row-sanitization smoke the current commit-preparation context.

## 678: Next-Action Queue Coordinate Aggregate Smoke Refresh

Output:

```text
outputs/experiments/678_next_action_queue_coordinate_aggregate_smoke_refresh
```

Command:

```text
Update the next-action queue from run 674 so aggregate CLI smokes include run
676 and commit preparation points to run 677.
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
git diff --check: clean after run 678
```

## Interpretation

Run 678 is now the current next-action queue. It points local validation to run
675, aggregate CLI smokes to runs 609 and 676, objective CLI smokes to runs
611, 642, and 669, commit preparation to run 677, state audit to run 672,
archive coverage to run 654, restart to run 648, manuscript validation to run
636, and archive handoff to run 633.

## Next Decision

Run a state audit over runs 675-678 before starting any larger reporting or
archive refresh.

