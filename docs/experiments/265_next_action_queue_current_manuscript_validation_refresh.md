# Experiment 265: Next-Action Queue Current Manuscript Validation Refresh

## Purpose

Refresh the next-action queue after run 730 made manuscript validation current
and run 731 made commit preparation current.

## 732: Next-Action Queue Current Manuscript Validation Refresh

Output:

```text
outputs/experiments/732_next_action_queue_current_manuscript_validation_refresh
```

Command:

```text
Update the queue from run 728 so it points manuscript validation to run 730,
state audit to run 729, and commit preparation to run 731.
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
queue points manuscript validation to run 730
queue points local validation to run 726
queue points code self-review to run 718
queue points state audit to run 729
queue points archive coverage to run 722
queue points commit preparation to run 731
queue pointer checks: 11/11
git diff --check: clean after run 732
```

## Interpretation

The current next-action queue is now run 732. It supersedes run 728 while
preserving run 726 local validation, run 718 code self-review, run 730
manuscript validation, run 729 state audit, run 722 archive coverage, run 731
commit preparation, run 648 restart, and run 633 as the checksum-valid but
stale archive.

## Next Decision

Audit the run 730-732 manuscript-validation refresh chain if more bookkeeping
is needed before handoff. Rebuild the archive only for explicit external
handoff.
