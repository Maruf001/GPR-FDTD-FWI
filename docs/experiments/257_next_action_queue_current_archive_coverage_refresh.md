# Experiment 257: Next-Action Queue Current Archive Coverage Refresh

## Purpose

Refresh the next-action queue after run 723 made run 722 the current archive
coverage checkpoint and run 723 the current commit-preparation artifact.

## 724: Next-Action Queue Current Archive Coverage Refresh

Output:

```text
outputs/experiments/724_next_action_queue_current_archive_coverage_refresh
```

Command:

```text
Update the next-action queue from run 720 so archive coverage points to run
722 and commit preparation points to run 723.
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
git diff --check: clean after run 724
```

## Interpretation

Run 724 is now the current next-action queue. It points local validation to run
714, code self-review to run 718, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 722, manuscript validation to run
685, state audit to run 721, commit preparation to run 723, restart to run 648,
and archive handoff to run 633.

## Next Decision

Run a small pointer audit over runs 722-724 if more bookkeeping is needed
before handoff; otherwise use run 723 for commit preparation.
