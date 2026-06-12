# Experiment 130: Next-Action Queue Current Archive Refresh

## Purpose

Refresh the current action queue after the run 595 handoff archive refresh and
run 596 commit/PR summary refresh.

## 597: Next-Action Queue Current Archive Refresh

Output:

```text
outputs/experiments/597_next_action_queue_current_archive_refresh
```

Command:

```text
Create a refreshed next_action_queue.md from run 593, updating optional archive
handoff from run 580 to run 595 and commit preparation from run 592 to run 596.
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
git diff --check: clean after run 597
```

## Interpretation

Run 597 is the current action queue. It keeps restart on run 588, local code
validation on run 584, manuscript validation on run 591, commit preparation on
run 596, and the packaged archive on run 595.

## Next Decision

Continue manuscript, archive-handoff, or commit-preparation work. Do not start
GPU work unless a bounded evidence gap is selected deliberately.
