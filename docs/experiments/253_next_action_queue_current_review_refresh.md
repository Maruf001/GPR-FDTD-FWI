# Experiment 253: Next-Action Queue Current Review Refresh

## Purpose

Refresh the next-action queue after run 719 made run 718 the current code-review
checkpoint and run 719 the current commit-preparation artifact.

## 720: Next-Action Queue Current Review Refresh

Output:

```text
outputs/experiments/720_next_action_queue_current_review_refresh
```

Command:

```text
Update the next-action queue from run 716 so code self-review points to run 718
and commit preparation points to run 719.
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
git diff --check: clean after run 720
```

## Interpretation

Run 720 is now the current next-action queue. It points local validation to run
714, code self-review to run 718, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 710, manuscript validation to run
685, state audit to run 717, commit preparation to run 719, restart to run 648,
and archive handoff to run 633.

## Next Decision

Run a small pointer audit over runs 718-720 if more bookkeeping is needed
before handoff; otherwise use run 719 for commit preparation.
