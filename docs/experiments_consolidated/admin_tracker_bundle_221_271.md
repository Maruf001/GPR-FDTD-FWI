# Admin Tracker Bundle 221-271

This append-only bundle consolidates short admin/checkpoint tracker docs. Source bodies below are copied verbatim and originals are left untouched for compatibility until references are checked.

## Included Sources

- `docs/experiments/221_current_manuscript_archive_state_audit.md` (165 words)
- `docs/experiments/222_commit_pr_summary_current_manuscript_archive_audit_refresh.md` (160 words)
- `docs/experiments/223_next_action_queue_current_manuscript_archive_audit_refresh.md` (172 words)
- `docs/experiments/224_current_precommit_validation_after_manuscript_archive_refresh.md` (140 words)
- `docs/experiments/225_commit_pr_summary_current_validation_refresh.md` (150 words)
- `docs/experiments/226_next_action_queue_current_validation_refresh.md` (176 words)
- `docs/experiments/229_commit_pr_summary_coordinate_default_smoke_refresh.md` (176 words)
- `docs/experiments/230_next_action_queue_coordinate_default_smoke_refresh.md` (179 words)
- `docs/experiments/231_current_coordinate_default_smoke_state_audit.md` (201 words)
- `docs/experiments/232_commit_pr_summary_coordinate_default_audit_refresh.md` (163 words)
- `docs/experiments/233_next_action_queue_coordinate_default_audit_refresh.md` (184 words)
- `docs/experiments/234_current_coordinate_default_audit_refresh_state_audit.md` (167 words)
- `docs/experiments/235_current_precommit_validation_after_coordinate_default_audit_refresh.md` (118 words)
- `docs/experiments/236_commit_pr_summary_current_validation_after_coordinate_default_audit_refresh.md` (169 words)
- `docs/experiments/237_next_action_queue_current_validation_after_coordinate_default_audit_refresh.md` (193 words)
- `docs/experiments/238_current_validation_after_coordinate_default_audit_state_audit.md` (168 words)
- `docs/experiments/239_code_self_review_current_validation_checkpoint.md` (172 words)
- `docs/experiments/240_commit_pr_summary_current_review_refresh.md` (156 words)
- `docs/experiments/241_next_action_queue_current_review_refresh.md` (189 words)
- `docs/experiments/242_current_review_refresh_state_audit.md` (165 words)
- `docs/experiments/243_current_state_archive_coverage_audit_refresh.md` (192 words)
- `docs/experiments/244_commit_pr_summary_current_archive_coverage_refresh.md` (178 words)
- `docs/experiments/245_next_action_queue_current_archive_coverage_refresh.md` (189 words)
- `docs/experiments/246_current_archive_coverage_refresh_state_audit.md` (184 words)
- `docs/experiments/247_current_precommit_validation_after_archive_coverage_refresh.md` (120 words)
- `docs/experiments/248_commit_pr_summary_current_validation_refresh.md` (168 words)
- `docs/experiments/249_next_action_queue_current_validation_refresh.md` (187 words)
- `docs/experiments/250_current_validation_refresh_state_audit.md` (179 words)
- `docs/experiments/251_code_self_review_current_validation_refresh.md` (149 words)
- `docs/experiments/252_commit_pr_summary_current_review_refresh.md` (161 words)
- `docs/experiments/253_next_action_queue_current_review_refresh.md` (186 words)
- `docs/experiments/254_current_review_refresh_state_audit.md` (171 words)
- `docs/experiments/255_current_state_archive_coverage_audit_refresh.md` (192 words)
- `docs/experiments/256_commit_pr_summary_current_archive_coverage_refresh.md` (178 words)
- `docs/experiments/257_next_action_queue_current_archive_coverage_refresh.md` (189 words)
- `docs/experiments/258_current_archive_coverage_refresh_state_audit.md` (178 words)
- `docs/experiments/259_current_precommit_validation_after_archive_coverage_audit_refresh.md` (122 words)
- `docs/experiments/260_commit_pr_summary_current_validation_refresh.md` (160 words)
- `docs/experiments/261_next_action_queue_current_validation_refresh.md` (187 words)
- `docs/experiments/262_current_validation_refresh_state_audit.md` (179 words)
- `docs/experiments/263_imrad_manuscript_current_validation_refresh.md` (170 words)
- `docs/experiments/264_commit_pr_summary_current_manuscript_validation_refresh.md` (178 words)
- `docs/experiments/265_next_action_queue_current_manuscript_validation_refresh.md` (212 words)
- `docs/experiments/266_current_manuscript_validation_refresh_state_audit.md` (185 words)
- `docs/experiments/267_current_state_archive_coverage_audit_refresh.md` (190 words)
- `docs/experiments/268_commit_pr_summary_current_archive_coverage_refresh.md` (178 words)
- `docs/experiments/269_next_action_queue_current_archive_coverage_refresh.md` (207 words)
- `docs/experiments/270_current_archive_coverage_refresh_state_audit.md` (185 words)
- `docs/experiments/271_post_archive_coverage_audit_resume_checkpoint.md` (163 words)

---

## Source: `docs/experiments/221_current_manuscript_archive_state_audit.md`

# Experiment 221: Current Manuscript/Archive State Audit

## Purpose

Audit the archive coverage and manuscript validation refresh chain after runs
682-687.

## 688: Current Manuscript/Archive State Audit

Output:

```text
outputs/experiments/688_current_manuscript_archive_state_audit
```

Command:

```text
Audit runs 682-687 for manifest, declared artifact, docs tracker, symlink,
validation, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_manuscript_archive_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 682 archive coverage status: pass
run 682 missing base paths: 0
run 685 lint status: pass
run 685 balance status: pass
run 687 queue pointer checks: 10/10
run 686 summary pointer checks: 3/3
planning doc pointer checks: 3/3
git diff --check: clean after run 688
```

## Interpretation

Runs 682-687 are internally consistent. The current queue correctly points
manuscript validation to run 685, archive coverage to run 682, and commit
preparation to run 686.

## Next Decision

Refresh commit-preparation and next-action queue pointers so the current state
audit points to run 688.

---

## Source: `docs/experiments/222_commit_pr_summary_current_manuscript_archive_audit_refresh.md`

# Experiment 222: Commit/PR Summary Current Manuscript/Archive Audit Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 688
state audit of the manuscript/archive refresh chain.

## 689: Commit/PR Summary Current Manuscript/Archive Audit Refresh

Output:

```text
outputs/experiments/689_commit_pr_summary_current_manuscript_archive_audit_refresh
```

Command:

```text
Update the commit/PR summary from run 686 so it records run 688 as the current
state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_current_manuscript_archive_audit_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 689
```

## Interpretation

The current commit-preparation artifact is now run 689. It supersedes run 686
for review/commit planning while preserving run 675 as local validation, run
676 as aggregate non-finite row CLI smoke, run 682 as archive coverage audit,
run 685 as manuscript validation, run 688 as state audit, and run 648 as
restart.

## Next Decision

Refresh the next-action queue so state audit points to run 688 and commit
preparation points to run 689.

---

## Source: `docs/experiments/223_next_action_queue_current_manuscript_archive_audit_refresh.md`

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

---

## Source: `docs/experiments/224_current_precommit_validation_after_manuscript_archive_refresh.md`

# Experiment 224: Current Precommit Validation After Manuscript/Archive Refresh

## Purpose

Refresh the local precommit validation checkpoint after the manuscript/archive
refresh chain and current queue run 690.

## 691: Current Precommit Validation After Manuscript/Archive Refresh

Output:

```text
outputs/experiments/691_current_precommit_validation_after_manuscript_archive_refresh
```

Commands:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
git diff --check
```

Artifacts:

```text
README.md
data/current_precommit_validation_after_manuscript_archive_refresh.json
run_manifest.json
```

Validation:

```text
pytest: 266 passed in 24.28 s
git diff --check: clean
GPU: NVIDIA GB10, utilization 0%, memory used/total N/A from nvidia-smi
RAM: 119 GiB total, 17 GiB used, 101 GiB available
Swap: 15 GiB total, 463 MiB used
```

## Interpretation

The current code and reporting worktree passes the full test suite after the
manuscript/archive refresh chain. Run 691 supersedes run 675 as the local
precommit validation checkpoint.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 691.

---

## Source: `docs/experiments/225_commit_pr_summary_current_validation_refresh.md`

# Experiment 225: Commit/PR Summary Current Validation Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 691 became
the current local precommit validation checkpoint.

## 692: Commit/PR Summary Current Validation Refresh

Output:

```text
outputs/experiments/692_commit_pr_summary_current_validation_refresh
```

Command:

```text
Update the commit/PR summary from run 689 so it records run 691 as the current
local validation checkpoint.
```

Artifacts:

```text
README.md
commit_pr_summary_current_validation_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 692
```

## Interpretation

The current commit-preparation artifact is now run 692. It supersedes run 689
for review/commit planning while preserving run 691 as local validation, run
685 as manuscript validation, run 688 as state audit, run 682 as archive
coverage audit, and run 648 as restart.

## Next Decision

Refresh the next-action queue so local validation points to run 691 and commit
preparation points to run 692.

---

## Source: `docs/experiments/226_next_action_queue_current_validation_refresh.md`

# Experiment 226: Next-Action Queue Current Validation Refresh

## Purpose

Refresh the next-action queue after run 692 made run 691 the current local
validation checkpoint.

## 693: Next-Action Queue Current Validation Refresh

Output:

```text
outputs/experiments/693_next_action_queue_current_validation_refresh
```

Command:

```text
Update the next-action queue from run 690 so local validation points to run 691
and commit preparation points to run 692.
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
git diff --check: clean after run 693
```

## Interpretation

Run 693 is now the current next-action queue. It points local validation to run
691, aggregate CLI smokes to runs 609 and 676, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 682, manuscript validation to run
685, state audit to run 688, commit preparation to run 692, restart to run
648, and archive handoff to run 633.

## Next Decision

Default to code/docs review or commit preparation. If more autonomous work is
needed, run a lightweight self-review of the reporting hardening for remaining
JSON-safety, manifest-artifact, and sparse/non-finite edge cases.

---

## Source: `docs/experiments/229_commit_pr_summary_coordinate_default_smoke_refresh.md`

# Experiment 229: Commit/PR Summary Coordinate Default Smoke Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 695
aggregate invalid-default CLI smoke.

## 696: Commit/PR Summary Coordinate Default Smoke Refresh

Output:

```text
outputs/experiments/696_commit_pr_summary_coordinate_default_smoke_refresh
```

Command:

```text
Update the commit/PR summary from run 692 so it records run 694 as the current
local validation/code hardening checkpoint and run 695 as the latest aggregate
CLI smoke.
```

Artifacts:

```text
README.md
commit_pr_summary_coordinate_default_smoke_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 696
```

## Interpretation

The current commit-preparation artifact is now run 696. It supersedes run 692
for review/commit planning while preserving run 694 as local validation and
metadata/default hardening, run 695 as aggregate invalid-default CLI smoke, run
688 as state audit, run 685 as manuscript validation, run 682 as archive
coverage audit, and run 648 as restart.

## Next Decision

Refresh the next-action queue so local validation points to run 694, aggregate
CLI smokes include run 695, and commit preparation points to run 696.

---

## Source: `docs/experiments/230_next_action_queue_coordinate_default_smoke_refresh.md`

# Experiment 230: Next-Action Queue Coordinate Default Smoke Refresh

## Purpose

Refresh the next-action queue after run 696 made run 694 and run 695 the current
metadata/default hardening and aggregate smoke context.

## 697: Next-Action Queue Coordinate Default Smoke Refresh

Output:

```text
outputs/experiments/697_next_action_queue_coordinate_default_smoke_refresh
```

Command:

```text
Update the next-action queue from run 693 so local validation points to run
694, aggregate CLI smokes include run 695, and commit preparation points to run
696.
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
git diff --check: clean after run 697
```

## Interpretation

Run 697 is now the current next-action queue. It points local validation and
metadata/default hardening to run 694, aggregate CLI smokes to runs 609, 676,
and 695, objective CLI smokes to runs 611, 642, and 669, archive coverage to
run 682, manuscript validation to run 685, state audit to run 688, commit
preparation to run 696, restart to run 648, and archive handoff to run 633.

## Next Decision

Run a state audit over runs 694-697 before starting another reporting or
archive refresh.

---

## Source: `docs/experiments/231_current_coordinate_default_smoke_state_audit.md`

# Experiment 231: Current Coordinate Default Smoke State Audit

## Purpose

Audit the coordinate confidence metadata/default hardening chain after runs
694-697.

## 698: Current Coordinate Default Smoke State Audit

Output:

```text
outputs/experiments/698_current_coordinate_default_smoke_state_audit
```

Command:

```text
Audit runs 694-697 for manifest, declared artifact, docs tracker, symlink,
validation, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_coordinate_default_smoke_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 694 status: pass
run 694 full pytest: 268 passed in 24.43 s
run 695 status: pass
run 695 invalid defaults rejected: 3/3
run 695 invalid output dirs created: 0
run 695 valid-control non-finite numerics: 0
run 695 valid-control plots nonblank: 2/2
run 697 queue pointer checks: 13/13
run 696 summary pointer checks: 4/4
planning doc pointer checks: 3/3
git diff --check: clean after run 698
```

## Interpretation

Runs 694-697 are internally consistent. The aggregate default Tx/Rx offset
hardening has focused-test coverage, full-suite validation, and a real CLI
smoke showing `nan`, `inf`, and negative defaults fail before output
allocation while a finite default still produces strict aggregate artifacts.

## Next Decision

Refresh commit-preparation and next-action queue pointers so the current state
audit points to run 698.

---

## Source: `docs/experiments/232_commit_pr_summary_coordinate_default_audit_refresh.md`

# Experiment 232: Commit/PR Summary Coordinate Default Audit Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 698
state audit of the coordinate metadata/default hardening chain.

## 699: Commit/PR Summary Coordinate Default Audit Refresh

Output:

```text
outputs/experiments/699_commit_pr_summary_coordinate_default_audit_refresh
```

Command:

```text
Update the commit/PR summary from run 696 so it records run 698 as the current
state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_coordinate_default_audit_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 699
```

## Interpretation

The current commit-preparation artifact is now run 699. It supersedes run 696
for review/commit planning while preserving run 694 as local validation and
metadata/default hardening, run 695 as aggregate invalid-default CLI smoke, run
698 as state audit, run 685 as manuscript validation, run 682 as archive
coverage audit, and run 648 as restart.

## Next Decision

Refresh the next-action queue so state audit points to run 698 and commit
preparation points to run 699.

---

## Source: `docs/experiments/233_next_action_queue_coordinate_default_audit_refresh.md`

# Experiment 233: Next-Action Queue Coordinate Default Audit Refresh

## Purpose

Refresh the next-action queue after run 699 made run 698 the current
state-audit context and run 699 the current commit-preparation artifact.

## 700: Next-Action Queue Coordinate Default Audit Refresh

Output:

```text
outputs/experiments/700_next_action_queue_coordinate_default_audit_refresh
```

Command:

```text
Update the next-action queue from run 697 so state audit points to run 698 and
commit preparation points to run 699.
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
git diff --check: clean after run 700
```

## Interpretation

Run 700 is now the current next-action queue. It points local validation and
metadata/default hardening to run 694, aggregate CLI smokes to runs 609, 676,
and 695, objective CLI smokes to runs 611, 642, and 669, archive coverage to
run 682, manuscript validation to run 685, state audit to run 698, commit
preparation to run 699, restart to run 648, and archive handoff to run 633.

## Next Decision

Use run 699 for code/docs review or commit preparation, or run a small pointer
audit over runs 698-700 if more bookkeeping is needed before handoff.

---

## Source: `docs/experiments/234_current_coordinate_default_audit_refresh_state_audit.md`

# Experiment 234: Current Coordinate Default Audit Refresh State Audit

## Purpose

Audit the coordinate default audit/commit/queue refresh chain after runs
698-700.

## 701: Current Coordinate Default Audit Refresh State Audit

Output:

```text
outputs/experiments/701_current_coordinate_default_audit_refresh_state_audit
```

Command:

```text
Audit runs 698-700 for manifest, declared artifact, docs tracker, symlink,
validation, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_coordinate_default_audit_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 698 status: pass
run 699 inventory status: inventory_ready
run 700 queue pointer checks: 13/13
run 699 summary pointer checks: 4/4
planning doc pointer checks: 3/3
git diff --check: clean after run 701
```

## Interpretation

Runs 698-700 are internally consistent. The current queue points state audit to
run 698 and commit preparation to run 699 while preserving run 694 local
validation and run 695 aggregate invalid-default CLI smoke.

## Next Decision

Use run 699 for code/docs review or commit preparation. Rebuild the external
archive only if handoff packaging is requested.

---

## Source: `docs/experiments/235_current_precommit_validation_after_coordinate_default_audit_refresh.md`

# Experiment 235: Current Precommit Validation After Coordinate Default Audit Refresh

## Purpose

Refresh local validation after the coordinate default audit/commit/queue refresh
chain through run 701.

## 702: Current Precommit Validation After Coordinate Default Audit Refresh

Output:

```text
outputs/experiments/702_current_precommit_validation_after_coordinate_default_audit_refresh
```

Commands:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
git diff --check
```

Artifacts:

```text
README.md
data/current_precommit_validation_after_coordinate_default_audit_refresh.json
run_manifest.json
```

Validation:

```text
full pytest: 268 passed in 24.60 s
git diff --check: clean
GPU utilization: 1%
RAM available: 101 GiB
```

## Interpretation

Run 702 supersedes run 694 as the current local validation checkpoint. The code
and docs remain clean after the run698-701 audit/commit/queue refresh chain.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 702.

---

## Source: `docs/experiments/236_commit_pr_summary_current_validation_after_coordinate_default_audit_refresh.md`

# Experiment 236: Commit/PR Summary Current Validation After Coordinate Default Audit Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 702 made
the full precommit validation current.

## 703: Commit/PR Summary Current Validation After Coordinate Default Audit Refresh

Output:

```text
outputs/experiments/703_commit_pr_summary_current_validation_after_coordinate_default_audit_refresh
```

Command:

```text
Update the commit/PR summary from run 699 so it records run 702 as the current
local validation checkpoint.
```

Artifacts:

```text
README.md
commit_pr_summary_current_validation_after_coordinate_default_audit_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 703
```

## Interpretation

The current commit-preparation artifact is now run 703. It supersedes run 699
for review/commit planning while preserving run 702 as local validation, run
694 as metadata/default hardening, run 695 as aggregate invalid-default CLI
smoke, run 701 as state audit, run 685 as manuscript validation, run 682 as
archive coverage audit, and run 648 as restart.

## Next Decision

Refresh the next-action queue so local validation points to run 702 and commit
preparation points to run 703.

---

## Source: `docs/experiments/237_next_action_queue_current_validation_after_coordinate_default_audit_refresh.md`

# Experiment 237: Next-Action Queue Current Validation After Coordinate Default Audit Refresh

## Purpose

Refresh the next-action queue after run 703 made run 702 the current local
validation checkpoint and run 703 the current commit-preparation artifact.

## 704: Next-Action Queue Current Validation After Coordinate Default Audit Refresh

Output:

```text
outputs/experiments/704_next_action_queue_current_validation_after_coordinate_default_audit_refresh
```

Command:

```text
Update the next-action queue from run 700 so local validation points to run
702 and commit preparation points to run 703.
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
git diff --check: clean after run 704
```

## Interpretation

Run 704 is now the current next-action queue. It points local validation to run
702, metadata/default hardening to run 694, aggregate CLI smokes to runs 609,
676, and 695, objective CLI smokes to runs 611, 642, and 669, archive coverage
to run 682, manuscript validation to run 685, state audit to run 701, commit
preparation to run 703, restart to run 648, and archive handoff to run 633.

## Next Decision

Use run 703 for code/docs review or commit preparation, or run a small pointer
audit over runs 702-704 if more bookkeeping is needed before handoff.

---

## Source: `docs/experiments/238_current_validation_after_coordinate_default_audit_state_audit.md`

# Experiment 238: Current Validation After Coordinate Default Audit State Audit

## Purpose

Audit the validation/commit/queue refresh chain after runs 702-704.

## 705: Current Validation After Coordinate Default Audit State Audit

Output:

```text
outputs/experiments/705_current_validation_after_coordinate_default_audit_state_audit
```

Command:

```text
Audit runs 702-704 for manifest, declared artifact, docs tracker, symlink,
validation, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_validation_after_coordinate_default_audit_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 702 status: pass
run 702 full pytest: 268 passed in 24.60 s
run 703 inventory status: inventory_ready
run 704 queue pointer checks: 14/14
run 703 summary pointer checks: 4/4
planning doc pointer checks: 3/3
git diff --check: clean after run 705
```

## Interpretation

Runs 702-704 are internally consistent. The current queue points local
validation to run 702, state audit to run 701, and commit preparation to run
703.

## Next Decision

Use run 703 for code/docs review or commit preparation. Rebuild the external
archive only if handoff packaging is requested.

---

## Source: `docs/experiments/239_code_self_review_current_validation_checkpoint.md`

# Experiment 239: Code Self-Review Current Validation Checkpoint

## Purpose

Perform a focused code review of the current runtime diffs after the fresh run
702 full-suite validation and run 705 pointer audit.

## 706: Code Self-Review Current Validation Checkpoint

Output:

```text
outputs/experiments/706_code_self_review_current_validation_checkpoint
```

Command:

```text
Focused code review of the candidate-confidence, coordinate aggregate, and
objective diagnostic reporting diffs after run 702 validation and run 705
audit.
```

Artifacts:

```text
README.md
data/code_self_review_current_validation_checkpoint.json
run_manifest.json
```

Validation:

```text
status: pass
blocking findings: 0
code edits made by this run: 0
run_manifest.json parses as JSON
data/code_self_review_current_validation_checkpoint.json parses as JSON
git diff --check: clean after run 706
```

## Interpretation

No blocking runtime defects were found in the reviewed diffs. The remaining
risk is the existing global manifest helper still uses default JSON dumping,
but the changed reporting paths have focused tests and CLI smokes confirming
non-finite values are sanitized before serialization.

## Next Decision

Refresh commit-preparation and next-action queue pointers if this review should
become the current review checkpoint; otherwise use run 703 for commit
preparation.

---

## Source: `docs/experiments/240_commit_pr_summary_current_review_refresh.md`

# Experiment 240: Commit/PR Summary Current Review Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 706
recorded the current focused code self-review checkpoint.

## 707: Commit/PR Summary Current Review Refresh

Output:

```text
outputs/experiments/707_commit_pr_summary_current_review_refresh
```

Command:

```text
Update the commit/PR summary from run 703 so it records run 706 as the current
focused code self-review checkpoint.
```

Artifacts:

```text
README.md
commit_pr_summary_current_review_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 707
```

## Interpretation

The current commit-preparation artifact is now run 707. It supersedes run 703
for review/commit planning while preserving run 702 as local validation, run
706 as code self-review, run 705 as state audit, run 685 as manuscript
validation, run 682 as archive coverage audit, and run 648 as restart.

## Next Decision

Refresh the next-action queue so code self-review points to run 706 and commit
preparation points to run 707.

---

## Source: `docs/experiments/241_next_action_queue_current_review_refresh.md`

# Experiment 241: Next-Action Queue Current Review Refresh

## Purpose

Refresh the next-action queue after run 707 made run 706 the current code-review
checkpoint and run 707 the current commit-preparation artifact.

## 708: Next-Action Queue Current Review Refresh

Output:

```text
outputs/experiments/708_next_action_queue_current_review_refresh
```

Command:

```text
Update the next-action queue from run 704 so code self-review points to run 706
and commit preparation points to run 707.
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
git diff --check: clean after run 708
```

## Interpretation

Run 708 is now the current next-action queue. It points local validation to run
702, code self-review to run 706, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 682, manuscript validation to run
685, state audit to run 705, commit preparation to run 707, restart to run 648,
and archive handoff to run 633.

## Next Decision

Use run 707 for code/docs review or commit preparation, or run a small pointer
audit over runs 706-708 if more bookkeeping is needed before handoff.

---

## Source: `docs/experiments/242_current_review_refresh_state_audit.md`

# Experiment 242: Current Review Refresh State Audit

## Purpose

Audit the review/commit/queue refresh chain after runs 706-708.

## 709: Current Review Refresh State Audit

Output:

```text
outputs/experiments/709_current_review_refresh_state_audit
```

Command:

```text
Audit runs 706-708 for manifest, declared artifact, docs tracker, symlink,
review, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_review_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 706 status: pass
run 706 blocking findings: 0
run 707 inventory status: inventory_ready
run 708 queue pointer checks: 15/15
run 707 summary pointer checks: 5/5
planning doc pointer checks: 3/3
git diff --check: clean after run 709
```

## Interpretation

Runs 706-708 are internally consistent. The current queue points code
self-review to run 706 and commit preparation to run 707 while preserving run
702 local validation and run 705 state audit.

## Next Decision

Use run 707 for code/docs review or commit preparation. Rebuild the external
archive only if handoff packaging is requested.

---

## Source: `docs/experiments/243_current_state_archive_coverage_audit_refresh.md`

# Experiment 243: Current State Archive Coverage Audit Refresh

## Purpose

Refresh the archive coverage audit for the current local state through run 709
without building a new archive.

## 710: Current State Archive Coverage Audit Refresh

Output:

```text
outputs/experiments/710_current_state_archive_coverage_audit_refresh
```

Command:

```text
Compare the run 633 archive file list and tarball contents against the current
base path list through outputs/experiments/709 and docs/experiments/242.
```

Artifacts:

```text
README.md
data/current_state_archive_coverage_audit_refresh.json
data/current_state_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 371
archive input paths: 372
base files: 947
base total size: 262.0 MiB
missing paths: 0
paths not covered by run 633 archive: 156
files missing from run 633 archive: 364
files changed since run 633 archive: 8
run 633 archive SHA-256: verified
run 633 archive entry count: 805
archive recommended for external handoff: true
git diff --check: clean after run 710
```

## Interpretation

Run 633 remains checksum-valid but stale. A refreshed archive is justified only
when an external handoff is needed; otherwise keep run 633 as the current
packaged archive and avoid repeated 128M archive churn.

## Next Decision

Refresh commit-preparation and next-action queue pointers so archive coverage
points to run 710.

---

## Source: `docs/experiments/244_commit_pr_summary_current_archive_coverage_refresh.md`

# Experiment 244: Commit/PR Summary Current Archive Coverage Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 710
recorded current archive coverage without rebuilding the archive.

## 711: Commit/PR Summary Current Archive Coverage Refresh

Output:

```text
outputs/experiments/711_commit_pr_summary_current_archive_coverage_refresh
```

Command:

```text
Update the commit/PR summary from run 707 so it records run 710 as the current
archive coverage audit while keeping run 633 as the checksum-valid but stale
external handoff archive.
```

Artifacts:

```text
README.md
commit_pr_summary_current_archive_coverage_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 711
```

## Interpretation

The current commit-preparation artifact is now run 711. It supersedes run 707
for commit planning while preserving run 702 as local validation, run 706 as
code self-review, run 709 as state audit, run 710 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so archive coverage points to run 710 and commit
preparation points to run 711.

---

## Source: `docs/experiments/245_next_action_queue_current_archive_coverage_refresh.md`

# Experiment 245: Next-Action Queue Current Archive Coverage Refresh

## Purpose

Refresh the next-action queue after run 711 made run 710 the current archive
coverage checkpoint and run 711 the current commit-preparation artifact.

## 712: Next-Action Queue Current Archive Coverage Refresh

Output:

```text
outputs/experiments/712_next_action_queue_current_archive_coverage_refresh
```

Command:

```text
Update the next-action queue from run 708 so archive coverage points to run
710 and commit preparation points to run 711.
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
git diff --check: clean after run 712
```

## Interpretation

Run 712 is now the current next-action queue. It points local validation to run
702, code self-review to run 706, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 710, manuscript validation to run
685, state audit to run 709, commit preparation to run 711, restart to run 648,
and archive handoff to run 633.

## Next Decision

Run a small pointer audit over runs 710-712 if more bookkeeping is needed
before handoff; otherwise use run 711 for commit preparation.

---

## Source: `docs/experiments/246_current_archive_coverage_refresh_state_audit.md`

# Experiment 246: Current Archive Coverage Refresh State Audit

## Purpose

Audit the archive-coverage/commit/queue refresh chain after runs 710-712.

## 713: Current Archive Coverage Refresh State Audit

Output:

```text
outputs/experiments/713_current_archive_coverage_refresh_state_audit
```

Command:

```text
Audit runs 710-712 for manifest, declared artifact, docs tracker, symlink,
archive coverage, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_archive_coverage_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 710 archive audit status: pass
run 710 archive checksum match: true
run 711 inventory status: inventory_ready
run 712 queue pointer checks: 15/15
run 711 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 713
```

## Interpretation

Runs 710-712 are internally consistent. The current queue points archive
coverage to run 710 and commit preparation to run 711 while preserving run 702
local validation, run 706 code self-review, and run 633 as the checksum-valid
but stale handoff archive.

## Next Decision

Use run 711 for commit preparation, or refresh full-suite validation if the
next handoff needs a newer local validation timestamp than run 702.

---

## Source: `docs/experiments/247_current_precommit_validation_after_archive_coverage_refresh.md`

# Experiment 247: Current Precommit Validation After Archive Coverage Refresh

## Purpose

Refresh local validation after the archive-coverage refresh audit/commit/queue
chain through run 713.

## 714: Current Precommit Validation After Archive Coverage Refresh

Output:

```text
outputs/experiments/714_current_precommit_validation_after_archive_coverage_refresh
```

Commands:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
git diff --check
```

Artifacts:

```text
README.md
data/current_precommit_validation_after_archive_coverage_refresh.json
data/git_diff_check.log
data/gpu_snapshot.csv
data/memory_snapshot.txt
data/pytest_q.log
run_manifest.json
```

Validation:

```text
full pytest: 268 passed in 24.41 s
git diff --check: clean
GPU utilization: 1%
RAM available: 101 GiB
```

## Interpretation

Run 714 supersedes run 702 as the current local validation checkpoint. The code
and docs remain clean after the run710-713 archive-coverage audit refresh
chain.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 714.

---

## Source: `docs/experiments/248_commit_pr_summary_current_validation_refresh.md`

# Experiment 248: Commit/PR Summary Current Validation Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 714 made
local validation current.

## 715: Commit/PR Summary Current Validation Refresh

Output:

```text
outputs/experiments/715_commit_pr_summary_current_validation_refresh
```

Command:

```text
Update the commit/PR summary from run 711 so it records run 714 as the current
local validation checkpoint and run 713 as the current state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_current_validation_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 715
```

## Interpretation

The current commit-preparation artifact is now run 715. It supersedes run 711
for commit planning while preserving run 714 as local validation, run 706 as
code self-review, run 713 as state audit, run 710 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so local validation points to run 714 and commit
preparation points to run 715.

---

## Source: `docs/experiments/249_next_action_queue_current_validation_refresh.md`

# Experiment 249: Next-Action Queue Current Validation Refresh

## Purpose

Refresh the next-action queue after run 715 made run 714 the current local
validation checkpoint and run 715 the current commit-preparation artifact.

## 716: Next-Action Queue Current Validation Refresh

Output:

```text
outputs/experiments/716_next_action_queue_current_validation_refresh
```

Command:

```text
Update the next-action queue from run 712 so local validation points to run
714 and commit preparation points to run 715.
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
git diff --check: clean after run 716
```

## Interpretation

Run 716 is now the current next-action queue. It points local validation to run
714, code self-review to run 706, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 710, manuscript validation to run
685, state audit to run 713, commit preparation to run 715, restart to run 648,
and archive handoff to run 633.

## Next Decision

Run a small pointer audit over runs 714-716 if more bookkeeping is needed
before handoff; otherwise use run 715 for commit preparation.

---

## Source: `docs/experiments/250_current_validation_refresh_state_audit.md`

# Experiment 250: Current Validation Refresh State Audit

## Purpose

Audit the validation/commit/queue refresh chain after runs 714-716.

## 717: Current Validation Refresh State Audit

Output:

```text
outputs/experiments/717_current_validation_refresh_state_audit
```

Command:

```text
Audit runs 714-716 for manifest, declared artifact, docs tracker, symlink,
validation, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_validation_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 714 validation status: pass
run 714 pytest passed: 268
run 714 git diff check status: clean
run 715 inventory status: inventory_ready
run 716 queue pointer checks: 15/15
run 715 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 717
```

## Interpretation

Runs 714-716 are internally consistent. The current queue points local
validation to run 714 and commit preparation to run 715 while preserving run
706 code self-review, run 710 archive coverage, and run 633 as the
checksum-valid but stale handoff archive.

## Next Decision

Use run 715 for commit preparation. Rebuild the external archive only if
handoff packaging is requested.

---

## Source: `docs/experiments/251_code_self_review_current_validation_refresh.md`

# Experiment 251: Code Self-Review Current Validation Refresh

## Purpose

Review the current code/test diff after run 714 full validation and run 717
pointer audit.

## 718: Code Self-Review Current Validation Refresh

Output:

```text
outputs/experiments/718_code_self_review_current_validation_refresh
```

Command:

```text
Review current code/test diffs after run 714 validation and run 717 state
audit; rerun focused tests.
```

Artifacts:

```text
README.md
data/code_self_review_current_validation_refresh.json
run_manifest.json
```

Validation:

```text
focused tests: 32 passed in 0.30 s
current full suite: run 714 pass, 268/268 in 24.41 s
current state audit: run 717 pass
blocking findings: 0
git diff --check: clean after run 718
```

## Interpretation

No blocking runtime defects were found in the current code/test diff. The
remaining required truth-coordinate casts match the existing reporting summary
contract, and optional/non-finite reporting values are covered by focused tests
and CLI smokes.

## Next Decision

Refresh commit-preparation and next-action queue pointers so code self-review
points to run 718.

---

## Source: `docs/experiments/252_commit_pr_summary_current_review_refresh.md`

# Experiment 252: Commit/PR Summary Current Review Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 718 made
code self-review current.

## 719: Commit/PR Summary Current Review Refresh

Output:

```text
outputs/experiments/719_commit_pr_summary_current_review_refresh
```

Command:

```text
Update the commit/PR summary from run 715 so it records run 718 as the current
focused code self-review checkpoint.
```

Artifacts:

```text
README.md
commit_pr_summary_current_review_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 719
```

## Interpretation

The current commit-preparation artifact is now run 719. It supersedes run 715
for commit planning while preserving run 714 as local validation, run 718 as
code self-review, run 717 as state audit, run 710 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so code self-review points to run 718 and commit
preparation points to run 719.

---

## Source: `docs/experiments/253_next_action_queue_current_review_refresh.md`

# Experiment 253: Next-Action Queue Current Review Refresh

## Purpose

Refresh the next-action queue after run 719 made run 718 the current code-review
checkpoint and run 719 the current commit-preparation artifact.

## 720: Next-Action Queue Current Review Refresh

Output:

```text
outputs/experiments/720_next_action_queue_current_review_refresh
```

Command:

```text
Update the next-action queue from run 716 so code self-review points to run 718
and commit preparation points to run 719.
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
git diff --check: clean after run 720
```

## Interpretation

Run 720 is now the current next-action queue. It points local validation to run
714, code self-review to run 718, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 710, manuscript validation to run
685, state audit to run 717, commit preparation to run 719, restart to run 648,
and archive handoff to run 633.

## Next Decision

Run a small pointer audit over runs 718-720 if more bookkeeping is needed
before handoff; otherwise use run 719 for commit preparation.

---

## Source: `docs/experiments/254_current_review_refresh_state_audit.md`

# Experiment 254: Current Review Refresh State Audit

## Purpose

Audit the review/commit/queue refresh chain after runs 718-720.

## 721: Current Review Refresh State Audit

Output:

```text
outputs/experiments/721_current_review_refresh_state_audit
```

Command:

```text
Audit runs 718-720 for manifest, declared artifact, docs tracker, symlink,
review, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_review_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 718 status: pass
run 718 blocking findings: 0
run 719 inventory status: inventory_ready
run 720 queue pointer checks: 15/15
run 719 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 721
```

## Interpretation

Runs 718-720 are internally consistent. The current queue points code
self-review to run 718 and commit preparation to run 719 while preserving run
714 local validation, run 717 state audit, and run 633 as the checksum-valid
but stale handoff archive.

## Next Decision

Use run 719 for commit preparation. Rebuild the external archive only if
handoff packaging is requested.

---

## Source: `docs/experiments/255_current_state_archive_coverage_audit_refresh.md`

# Experiment 255: Current State Archive Coverage Audit Refresh

## Purpose

Refresh the archive coverage audit for the current local state through run 721
without building a new archive.

## 722: Current State Archive Coverage Audit Refresh

Output:

```text
outputs/experiments/722_current_state_archive_coverage_audit_refresh
```

Command:

```text
Compare the run 633 archive file list and tarball contents against the current
base path list through outputs/experiments/721 and docs/experiments/254.
```

Artifacts:

```text
README.md
data/current_state_archive_coverage_audit_refresh.json
data/current_state_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 395
archive input paths: 396
base files: 1003
base total size: 262.4 MiB
missing paths: 0
paths not covered by run 633 archive: 180
files missing from run 633 archive: 420
files changed since run 633 archive: 8
run 633 archive SHA-256: verified
run 633 archive entry count: 805
archive recommended for external handoff: true
git diff --check: clean after run 722
```

## Interpretation

Run 633 remains checksum-valid but stale. A refreshed archive is justified only
when an external handoff is needed; otherwise keep run 633 as the current
packaged archive and avoid repeated 128M archive churn.

## Next Decision

Refresh commit-preparation and next-action queue pointers so archive coverage
points to run 722.

---

## Source: `docs/experiments/256_commit_pr_summary_current_archive_coverage_refresh.md`

# Experiment 256: Commit/PR Summary Current Archive Coverage Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 722
recorded current archive coverage without rebuilding the archive.

## 723: Commit/PR Summary Current Archive Coverage Refresh

Output:

```text
outputs/experiments/723_commit_pr_summary_current_archive_coverage_refresh
```

Command:

```text
Update the commit/PR summary from run 719 so it records run 722 as the current
archive coverage audit while keeping run 633 as the checksum-valid but stale
external handoff archive.
```

Artifacts:

```text
README.md
commit_pr_summary_current_archive_coverage_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 723
```

## Interpretation

The current commit-preparation artifact is now run 723. It supersedes run 719
for commit planning while preserving run 714 as local validation, run 718 as
code self-review, run 721 as state audit, run 722 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so archive coverage points to run 722 and commit
preparation points to run 723.

---

## Source: `docs/experiments/257_next_action_queue_current_archive_coverage_refresh.md`

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

---

## Source: `docs/experiments/258_current_archive_coverage_refresh_state_audit.md`

# Experiment 258: Current Archive Coverage Refresh State Audit

## Purpose

Audit the archive-coverage/commit/queue refresh chain after runs 722-724.

## 725: Current Archive Coverage Refresh State Audit

Output:

```text
outputs/experiments/725_current_archive_coverage_refresh_state_audit
```

Command:

```text
Audit runs 722-724 for manifest, declared artifact, docs tracker, symlink,
archive coverage, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_archive_coverage_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 722 archive audit status: pass
run 722 archive checksum match: true
run 723 inventory status: inventory_ready
run 724 queue pointer checks: 15/15
run 723 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 725
```

## Interpretation

Runs 722-724 are internally consistent. The current queue points archive
coverage to run 722 and commit preparation to run 723 while preserving run 714
local validation, run 718 code self-review, and run 633 as the checksum-valid
but stale handoff archive.

## Next Decision

Use run 723 for commit preparation, or refresh local validation if a newer
full-suite timestamp is needed.

---

## Source: `docs/experiments/259_current_precommit_validation_after_archive_coverage_audit_refresh.md`

# Experiment 259: Current Precommit Validation After Archive Coverage Audit Refresh

## Purpose

Refresh local validation after the archive-coverage refresh audit/commit/queue
chain through run 725.

## 726: Current Precommit Validation After Archive Coverage Audit Refresh

Output:

```text
outputs/experiments/726_current_precommit_validation_after_archive_coverage_audit_refresh
```

Commands:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
git diff --check
```

Artifacts:

```text
README.md
data/current_precommit_validation_after_archive_coverage_audit_refresh.json
data/git_diff_check.log
data/gpu_snapshot.csv
data/memory_snapshot.txt
data/pytest_q.log
run_manifest.json
```

Validation:

```text
full pytest: 268 passed in 24.43 s
git diff --check: clean
GPU utilization: 1%
RAM available: 101 GiB
```

## Interpretation

Run 726 supersedes run 714 as the current local validation checkpoint. The code
and docs remain clean after the run722-725 archive-coverage audit refresh
chain.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 726.

---

## Source: `docs/experiments/260_commit_pr_summary_current_validation_refresh.md`

# Experiment 260: Commit/PR Summary Current Validation Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 726 made
local validation current.

## 727: Commit/PR Summary Current Validation Refresh

Output:

```text
outputs/experiments/727_commit_pr_summary_current_validation_refresh
```

Command:

```text
Update the commit/PR summary from run 723 so it records run 726 as the current
local validation checkpoint.
```

Artifacts:

```text
README.md
commit_pr_summary_current_validation_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 727
```

## Interpretation

The current commit-preparation artifact is now run 727. It supersedes run 723
for commit planning while preserving run 726 as local validation, run 718 as
code self-review, run 725 as state audit, run 722 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so local validation points to run 726 and commit
preparation points to run 727.

---

## Source: `docs/experiments/261_next_action_queue_current_validation_refresh.md`

# Experiment 261: Next-Action Queue Current Validation Refresh

## Purpose

Refresh the next-action queue after run 727 made run 726 the current local
validation checkpoint and run 727 the current commit-preparation artifact.

## 728: Next-Action Queue Current Validation Refresh

Output:

```text
outputs/experiments/728_next_action_queue_current_validation_refresh
```

Command:

```text
Update the next-action queue from run 724 so local validation points to run
726 and commit preparation points to run 727.
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
git diff --check: clean after run 728
```

## Interpretation

Run 728 is now the current next-action queue. It points local validation to run
726, code self-review to run 718, metadata/default hardening to run 694,
aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to runs
611, 642, and 669, archive coverage to run 722, manuscript validation to run
685, state audit to run 725, commit preparation to run 727, restart to run 648,
and archive handoff to run 633.

## Next Decision

Run a small pointer audit over runs 726-728 if more bookkeeping is needed
before handoff; otherwise use run 727 for commit preparation.

---

## Source: `docs/experiments/262_current_validation_refresh_state_audit.md`

# Experiment 262: Current Validation Refresh State Audit

## Purpose

Audit the validation/commit/queue refresh chain after runs 726-728.

## 729: Current Validation Refresh State Audit

Output:

```text
outputs/experiments/729_current_validation_refresh_state_audit
```

Command:

```text
Audit runs 726-728 for manifest, declared artifact, docs tracker, symlink,
validation, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_validation_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 726 validation status: pass
run 726 pytest passed: 268
run 726 git diff check status: clean
run 727 inventory status: inventory_ready
run 728 queue pointer checks: 15/15
run 727 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 729
```

## Interpretation

Runs 726-728 are internally consistent. The current queue points local
validation to run 726 and commit preparation to run 727 while preserving run
718 code self-review, run 722 archive coverage, and run 633 as the
checksum-valid but stale handoff archive.

## Next Decision

Use run 727 for commit preparation. Rebuild the external archive only if
handoff packaging is requested.

---

## Source: `docs/experiments/263_imrad_manuscript_current_validation_refresh.md`

# Experiment 263: IMRAD Manuscript Current Validation Refresh

## Purpose

Refresh the IMRAD manuscript validation pointers from the run 685
archive-coverage state to the current validation, review, archive-coverage,
commit, queue, and audit state.

## 730: IMRAD Manuscript Current Validation Refresh

Output:

```text
outputs/experiments/730_imrad_manuscript_current_validation_refresh
```

Command:

```text
Update the manuscript validation/archive section and Data And Code Availability
block to the current run 718/722/726/727/728/729 state, then lint references,
images, markers, and guardrail prose.
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint_current_validation_refresh.json
data/manuscript_balance_audit_current_validation_refresh.json
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint: pass
referenced runs: 68
missing referenced runs: 0
embedded images resolved: 7
unresolved editing markers: 0
manuscript balance/guardrail audit: pass
word count: 1673
required guardrails present: 5/5
duplicate interval-supported sentence: false
git diff --check: clean after run 730
```

## Interpretation

The manuscript now points to the current local validation, code self-review,
aggregate/objective CLI smokes, state audit, archive coverage, commit summary,
resume checkpoint, and action queue. No scientific claim changed.

## Next Decision

Refresh commit-preparation and next-action queue pointers so manuscript
validation points to run 730.

---

## Source: `docs/experiments/264_commit_pr_summary_current_manuscript_validation_refresh.md`

# Experiment 264: Commit/PR Summary Current Manuscript Validation Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 730 made
manuscript validation current.

## 731: Commit/PR Summary Current Manuscript Validation Refresh

Output:

```text
outputs/experiments/731_commit_pr_summary_current_manuscript_validation_refresh
```

Command:

```text
Update the commit/PR summary from run 727 so it records run 730 as the current
manuscript validation checkpoint and run 729 as the current state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_current_manuscript_validation_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
inventory status: inventory_ready
manuscript validation pointer: run 730
git diff --check: clean after run 731
```

## Interpretation

The current commit-preparation artifact is now run 731. It supersedes run 727
for commit planning while preserving run 726 as local validation, run 718 as
code self-review, run 729 as state audit, run 722 as archive coverage audit,
run 730 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so manuscript validation points to run 730 and
commit preparation points to run 731.

---

## Source: `docs/experiments/265_next_action_queue_current_manuscript_validation_refresh.md`

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

---

## Source: `docs/experiments/266_current_manuscript_validation_refresh_state_audit.md`

# Experiment 266: Current Manuscript Validation Refresh State Audit

## Purpose

Audit the manuscript-validation, commit-summary, and next-action queue refresh
chain after runs 730-732.

## 733: Current Manuscript Validation Refresh State Audit

Output:

```text
outputs/experiments/733_current_manuscript_validation_refresh_state_audit
```

Command:

```text
Check run 730-732 manifests, declared artifacts, docs trackers, infrastructure
symlinks, manuscript validation metrics, commit-summary pointers, queue
pointers, and planning-doc pointers.
```

Artifacts:

```text
README.md
data/current_manuscript_validation_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 730 manuscript checks: 7/7
run 731 summary checks: 5/5
run 732 queue pointer checks: 11/11
planning doc pointer checks: 3/3
git diff --check: clean after run 733
```

## Interpretation

Runs 730-732 are internally consistent. The current queue points manuscript
validation to run 730 and commit preparation to run 731 while preserving run
726 local validation, run 718 code self-review, run 729 state audit, run 722
archive coverage, and run 633 as the checksum-valid but stale handoff archive.

## Next Decision

Use run 731 for commit preparation and run 732 as the live queue. Rebuild the
archive only for explicit external handoff.

---

## Source: `docs/experiments/267_current_state_archive_coverage_audit_refresh.md`

# Experiment 267: Current State Archive Coverage Audit Refresh

## Purpose

Refresh the archive-coverage audit after the run 730-733 manuscript-validation
refresh chain without rebuilding the handoff archive.

## 734: Current State Archive Coverage Audit Refresh

Output:

```text
outputs/experiments/734_current_state_archive_coverage_audit_refresh
```

Command:

```text
Compare the run 633 archive file list and tarball contents against the current
base path list through outputs/experiments/733 and docs/experiments/266.
```

Artifacts:

```text
README.md
data/current_state_archive_coverage_audit_refresh.json
data/current_state_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 419
archive input paths: 420
base files: 1060
base total size: 262.9 MiB
missing paths: 0
paths not covered by run 633 archive: 204
files missing from run 633 archive: 477
files changed since run 633 archive: 8
run 633 archive SHA-256: verified
run 633 archive entry count: 805
archive recommended for external handoff: true
git diff --check: clean after run 734
```

## Interpretation

Run 633 remains checksum-valid but stale for current local state through run
733 and docs/experiments/266. Rebuild the archive only for explicit external
handoff; otherwise continue local reporting/commit work.

## Next Decision

Refresh commit-preparation and next-action queue pointers only if archive
coverage must be made current in the live queue.

---

## Source: `docs/experiments/268_commit_pr_summary_current_archive_coverage_refresh.md`

# Experiment 268: Commit/PR Summary Current Archive Coverage Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 734 made
archive coverage current.

## 735: Commit/PR Summary Current Archive Coverage Refresh

Output:

```text
outputs/experiments/735_commit_pr_summary_current_archive_coverage_refresh
```

Command:

```text
Update the commit/PR summary from run 731 so it records run 734 as the current
archive coverage checkpoint and run 733 as the current state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_current_archive_coverage_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
inventory status: inventory_ready
archive coverage pointer: run 734
git diff --check: clean after run 735
```

## Interpretation

The current commit-preparation artifact is now run 735. It supersedes run 731
for commit planning while preserving run 726 as local validation, run 718 as
code self-review, run 733 as state audit, run 734 as archive coverage audit,
run 730 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so archive coverage points to run 734 and commit
preparation points to run 735.

---

## Source: `docs/experiments/269_next_action_queue_current_archive_coverage_refresh.md`

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

---

## Source: `docs/experiments/270_current_archive_coverage_refresh_state_audit.md`

# Experiment 270: Current Archive Coverage Refresh State Audit

## Purpose

Audit the archive-coverage, commit-summary, and next-action queue refresh chain
after runs 734-736.

## 737: Current Archive Coverage Refresh State Audit

Output:

```text
outputs/experiments/737_current_archive_coverage_refresh_state_audit
```

Command:

```text
Check run 734-736 manifests, declared artifacts, docs trackers,
infrastructure symlinks, archive coverage metrics, commit-summary pointers,
queue pointers, and planning-doc pointers.
```

Artifacts:

```text
README.md
data/current_archive_coverage_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 734 archive checks: 9/9
run 735 summary checks: 5/5
run 736 queue pointer checks: 11/11
planning doc pointer checks: 3/3
git diff --check: clean after run 737
```

## Interpretation

Runs 734-736 are internally consistent. The current queue points archive
coverage to run 734 and commit preparation to run 735 while preserving run 726
local validation, run 718 code self-review, run 730 manuscript validation, run
733 state audit, and run 633 as the checksum-valid but stale handoff archive.

## Next Decision

Use run 735 for commit preparation and run 736 as the live queue. Rebuild the
archive only for explicit external handoff.

---

## Source: `docs/experiments/271_post_archive_coverage_audit_resume_checkpoint.md`

# Experiment 271: Post-Archive-Coverage Audit Resume Checkpoint

## Purpose

Record a compact crash-recovery checkpoint after the manuscript validation and
archive coverage refresh chain.

## 738: Post-Archive-Coverage Audit Resume Checkpoint

Output:

```text
outputs/experiments/738_post_archive_coverage_audit_resume_checkpoint
```

Command:

```text
Record current pointers to validation, review, manuscript validation, archive
coverage, state audit, commit preparation, next-action queue, and handoff
archive.
```

Artifacts:

```text
README.md
data/post_archive_coverage_audit_resume_checkpoint.json
run_manifest.json
```

Validation:

```text
checkpoint status: ready
pointer count: 8
full pytest pointer: run 726
code self-review pointer: run 718
manuscript validation pointer: run 730
archive coverage pointer: run 734
state audit pointer: run 737
commit preparation pointer: run 735
queue pointer: run 736
handoff archive pointer: run 633
git diff --check: clean after run 738
```

## Interpretation

Run 738 supersedes run 648 as the current crash-recovery checkpoint while
preserving run 633 as the checksum-valid but stale external archive.

## Next Decision

Use run 735 for commit preparation and run 736 as the live queue. Rebuild the
archive only for explicit external handoff.
