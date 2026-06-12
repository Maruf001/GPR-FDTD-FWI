# Experiment 220: Next-Action Queue Current Manuscript Validation Refresh

## Purpose

Refresh the next-action queue after run 686 made run 685 the current manuscript
validation context.

## 687: Next-Action Queue Current Manuscript Validation Refresh

Output:

```text
outputs/experiments/687_next_action_queue_current_manuscript_validation_refresh
```

Command:

```text
Update the next-action queue from run 684 so manuscript validation points to
run 685 and commit preparation points to run 686.
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
git diff --check: clean after run 687
```

## Interpretation

Run 687 is now the current next-action queue. It points local validation to run
675, aggregate CLI smokes to runs 609 and 676, objective CLI smokes to runs
611, 642, and 669, state audit to run 679, archive coverage to run 682,
manuscript validation to run 685, commit preparation to run 686, restart to
run 648, and archive handoff to run 633.

## Next Decision

Run a state audit over runs 682-687 before starting another reporting or
archive refresh.

