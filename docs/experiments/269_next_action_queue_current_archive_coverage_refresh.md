# Experiment 269: Next-Action Queue Current Archive Coverage Refresh

## Purpose

Refresh the next-action queue after run 734 made archive coverage current and
run 735 made commit preparation current.

## 736: Next-Action Queue Current Archive Coverage Refresh

Output:

```text
outputs/experiments/736_next_action_queue_current_archive_coverage_refresh
```

Command:

```text
Update the queue from run 732 so it points archive coverage to run 734 and
commit preparation to run 735.
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
queue points archive coverage to run 734
queue points commit preparation to run 735
queue points manuscript validation to run 730
queue points local validation to run 726
queue points code self-review to run 718
queue points state audit to run 733
queue pointer checks: 11/11
git diff --check: clean after run 736
```

## Interpretation

The current next-action queue is now run 736. It supersedes run 732 while
preserving run 726 local validation, run 718 code self-review, run 730
manuscript validation, run 733 state audit, run 734 archive coverage, run 735
commit preparation, run 648 restart, and run 633 as the checksum-valid but
stale archive.

## Next Decision

Audit the run 734-736 archive-coverage refresh chain if more bookkeeping is
needed before handoff. Rebuild the archive only for explicit external handoff.
