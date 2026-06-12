# Experiment 195: Next-Action Queue Candidate-Confidence Audit Refresh

## Purpose

Refresh the current action queue after the run 660 state audit and run 661
commit/PR summary refresh.

## 662: Next-Action Queue Candidate-Confidence Audit Refresh

Output:

```text
outputs/experiments/662_next_action_queue_candidate_confidence_audit_refresh
```

Command:

```text
Create a refreshed next_action_queue.md from run 659, updating state audit from
run 651 to run 660 and commit preparation from run 658 to run 661.
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
git diff --check: clean after run 662
```

## Interpretation

Run 662 is the current action queue. It keeps restart on run 648, local code
validation on run 657, CLI smokes on runs 609, 611, and 642, state audit on
run 660, manuscript validation on run 636, archive handoff on run 633, archive
coverage audit on run 654, and commit preparation on run 661.

## Next Decision

Continue manuscript, archive-handoff, or commit-preparation work. Rebuild the
archive only if an external handoff is needed.

