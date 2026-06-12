# Experiment 217: Next-Action Queue Current Archive Coverage Refresh

## Purpose

Refresh the next-action queue after run 683 made run 682 the current archive
coverage context.

## 684: Next-Action Queue Current Archive Coverage Refresh

Output:

```text
outputs/experiments/684_next_action_queue_current_archive_coverage_refresh
```

Command:

```text
Update the next-action queue from run 681 so archive coverage points to run 682
and commit preparation points to run 683.
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
git diff --check: clean after run 684
```

## Interpretation

Run 684 is now the current next-action queue. It points local validation to run
675, aggregate CLI smokes to runs 609 and 676, objective CLI smokes to runs
611, 642, and 669, state audit to run 679, archive coverage to run 682, commit
preparation to run 683, restart to run 648, manuscript validation to run 636,
and archive handoff to run 633.

## Next Decision

Default to code/docs review or a fresh manuscript validation refresh. Archive
rebuild remains gated to external handoff needs.

