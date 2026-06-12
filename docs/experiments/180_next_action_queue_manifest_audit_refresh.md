# Experiment 180: Next-Action Queue Manifest-Audit Refresh

## Purpose

Refresh the current action queue after the run 645 state audit and run 646
commit/PR summary refresh.

## 647: Next-Action Queue Manifest-Audit Refresh

Output:

```text
outputs/experiments/647_next_action_queue_manifest_audit_refresh
```

Command:

```text
Create a refreshed next_action_queue.md from run 644, updating state audit from
run 629 to run 645 and commit preparation from run 643 to run 646.
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
git diff --check: clean after run 647
```

## Interpretation

Run 647 is the current action queue. It keeps restart on run 626, local code
validation on run 639, CLI smokes on runs 609, 611, and 642, state audit on
run 645, manuscript validation on run 636, archive handoff on run 633, and
commit preparation on run 646.

## Next Decision

Continue manuscript, archive-handoff, or commit-preparation work. Do not start
GPU work unless a bounded evidence gap is selected deliberately.
