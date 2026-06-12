# Experiment 198: Next-Action Queue Candidate Row-Sanitization Refresh

## Purpose

Refresh the current action queue after the run 663 row-sanitization hardening
and run 664 commit/PR summary refresh.

## 665: Next-Action Queue Candidate Row-Sanitization Refresh

Output:

```text
outputs/experiments/665_next_action_queue_candidate_row_sanitization_refresh
```

Command:

```text
Create a refreshed next_action_queue.md from run 662, updating local validation
from run 657 to run 663 and commit preparation from run 661 to run 664.
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
git diff --check: clean after run 665
```

## Interpretation

Run 665 is the current action queue. It keeps restart on run 648, local code
validation on run 663, CLI smokes on runs 609, 611, and 642, state audit on
run 660, manuscript validation on run 636, archive handoff on run 633, archive
coverage audit on run 654, and commit preparation on run 664.

## Next Decision

Continue manuscript, archive-handoff, or commit-preparation work. Rebuild the
archive only if an external handoff is needed.

