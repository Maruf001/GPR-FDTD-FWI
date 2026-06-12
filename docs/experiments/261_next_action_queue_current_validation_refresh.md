# Experiment 261: Next-Action Queue Current Validation Refresh

## Purpose

Refresh the next-action queue after run 727 made run 726 the current local
validation checkpoint and run 727 the current commit-preparation artifact.

## 728: Next-Action Queue Current Validation Refresh

Output:

```text
outputs/experiments/728_next_action_queue_current_validation_refresh
```

Command:

```text
Update the next-action queue from run 724 so local validation points to run
726 and commit preparation points to run 727.
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
git diff --check: clean after run 728
```

## Interpretation

Run 728 is now the current next-action queue. It points local validation to run
726, code self-review to run 718, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 722, manuscript validation to run
685, state audit to run 725, commit preparation to run 727, restart to run 648,
and archive handoff to run 633.

## Next Decision

Run a small pointer audit over runs 726-728 if more bookkeeping is needed
before handoff; otherwise use run 727 for commit preparation.
