# Experiment 201: Next-Action Queue Candidate Row-Sanitization Audit Refresh

## Purpose

Refresh the current action queue after the run 666 state audit and run 667
commit/PR summary refresh.

## 668: Next-Action Queue Candidate Row-Sanitization Audit Refresh

Output:

```text
outputs/experiments/668_next_action_queue_candidate_row_sanitization_audit_refresh
```

Command:

```text
Create a refreshed next_action_queue.md from run 665, updating state audit from
run 660 to run 666 and commit preparation from run 664 to run 667.
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
git diff --check: clean after run 668
```

## Interpretation

Run 668 is the current action queue. It keeps restart on run 648, local code
validation on run 663, CLI smokes on runs 609, 611, and 642, state audit on
run 666, manuscript validation on run 636, archive handoff on run 633, archive
coverage audit on run 654, and commit preparation on run 667.

## Next Decision

Continue manuscript, archive-handoff, or commit-preparation work. Rebuild the
archive only if an external handoff is needed.

