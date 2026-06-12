# Experiment 230: Next-Action Queue Coordinate Default Smoke Refresh

## Purpose

Refresh the next-action queue after run 696 made run 694 and run 695 the current
metadata/default hardening and aggregate smoke context.

## 697: Next-Action Queue Coordinate Default Smoke Refresh

Output:

```text
outputs/experiments/697_next_action_queue_coordinate_default_smoke_refresh
```

Command:

```text
Update the next-action queue from run 693 so local validation points to run
694, aggregate CLI smokes include run 695, and commit preparation points to run
696.
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
git diff --check: clean after run 697
```

## Interpretation

Run 697 is now the current next-action queue. It points local validation and
metadata/default hardening to run 694, aggregate CLI smokes to runs 609, 676,
and 695, objective CLI smokes to runs 611, 642, and 669, archive coverage to
run 682, manuscript validation to run 685, state audit to run 688, commit
preparation to run 696, restart to run 648, and archive handoff to run 633.

## Next Decision

Run a state audit over runs 694-697 before starting another reporting or
archive refresh.

