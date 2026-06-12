# Experiment 223: Next-Action Queue Current Manuscript/Archive Audit Refresh

## Purpose

Refresh the next-action queue after run 689 made run 688 the current state
audit context.

## 690: Next-Action Queue Current Manuscript/Archive Audit Refresh

Output:

```text
outputs/experiments/690_next_action_queue_current_manuscript_archive_audit_refresh
```

Command:

```text
Update the next-action queue from run 687 so state audit points to run 688 and
commit preparation points to run 689.
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
git diff --check: clean after run 690
```

## Interpretation

Run 690 is now the current next-action queue. It points local validation to run
675, aggregate CLI smokes to runs 609 and 676, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 682, manuscript validation to run
685, state audit to run 688, commit preparation to run 689, restart to run
648, and archive handoff to run 633.

## Next Decision

Default to code/docs review. If a commit/export is imminent, run a fresh
precommit validation checkpoint; archive rebuild remains gated to external
handoff needs.

