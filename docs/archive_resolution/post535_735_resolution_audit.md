# Post-535 Archive Resolution Audit

## Purpose

This audit responds to the post-crash run inflation problem. It does not allocate a numbered experiment ID. It classifies runs 535-735 and tracker docs 100-271 so admin/checkpoint churn can be consolidated without breaking substantive experiment evidence or canonical references.

## Generated Evidence

```text
outputs/archive_resolution/post535_735_resolution_audit/post535_735_output_classification.csv
outputs/archive_resolution/post535_735_resolution_audit/tracker_doc_100_271_classification.csv
outputs/archive_resolution/post535_735_resolution_audit/post535_735_resolution_summary.json
outputs/archive_resolution/post535_735_resolution_audit/admin_output_reference_counts.csv
outputs/archive_resolution/post535_735_resolution_audit/move_admin_outputs_with_symlinks.py
docs/experiments_consolidated/README.md
docs/experiments_consolidated/admin_tracker_bundle_manifest.json
docs/experiments_consolidated/admin_tracker_bundle_101_140.md
docs/experiments_consolidated/admin_tracker_bundle_141_180.md
docs/experiments_consolidated/admin_tracker_bundle_181_220.md
docs/experiments_consolidated/admin_tracker_bundle_221_271.md
```

## Output Run Classification

Runs inspected: 201

- `keep_substantive_experiment_or_diagnostic`: 2
- `relocate_or_consolidate_admin_churn`: 158
- `keep_report_dev_or_analysis`: 41

Recommended output action counts:

- `keep_in_main_experiment_archive`: 2
- `candidate_move_to_outputs/experiment_admin_archive/535_735_with_compatibility_link`: 158
- `keep_in_place_or_link_from_report_dev_index`: 41

Reference scan:

```text
files scanned: 4339
admin candidates: 158
admin candidates with references: 158
admin candidates without references: 0
```

Therefore admin output folders should not be moved by plain `mv` alone. Any
relocation must leave a compatibility symlink at the original
`outputs/experiments/NNN_name` path or update every reference first.

A dry-run relocation helper is provided:

```text
outputs/archive_resolution/post535_735_resolution_audit/move_admin_outputs_with_symlinks.py
```

Default mode is dry-run. It only performs moves if called with `--execute`.
The intended destination is `outputs/experiment_admin_archive/535_735/`, with
the original `outputs/experiments/NNN_name` path replaced by a relative symlink
to preserve existing references.

Admin/churn examples:

- `537_marathon_checkpoint_reporting_handoff`
- `550_archive_status_checkpoint`
- `551_commit_archive_inventory`
- `553_post_hardening_resume_checkpoint`
- `556_post_archive_resume_checkpoint`
- `557_commit_pr_summary_draft`
- `558_next_action_queue`
- `561_next_action_queue_refresh`
- `564_post_imrad_resume_checkpoint`
- `566_next_action_queue_manuscript_refresh`

Keep examples:

- `535_source_shape_center_interval_reporting_handoff` -> `keep_substantive_experiment_or_diagnostic`
- `536_single_rebar_shallow_r4_reporting_handoff` -> `keep_substantive_experiment_or_diagnostic`
- `538_current_evidence_synthesis` -> `keep_report_dev_or_analysis`
- `539_results_section_draft` -> `keep_report_dev_or_analysis`
- `540_results_methods_evidence_table` -> `keep_report_dev_or_analysis`
- `541_combined_report_draft` -> `keep_report_dev_or_analysis`
- `542_decision_figure_map` -> `keep_report_dev_or_analysis`
- `543_compact_objective_summary_figure` -> `keep_report_dev_or_analysis`
- `544_decision_figure_readiness_audit` -> `keep_report_dev_or_analysis`
- `545_report_figure_caption_package` -> `keep_report_dev_or_analysis`

## Tracker Doc Classification

Tracker docs inspected: 172

- `append_verbatim_to_report_dev_tracker_bundle_review_first`: 21
- `append_verbatim_to_admin_tracker_bundle_then_replace_with_stub_or_index_link`: 151

The tracker consolidation plan is append-only: concatenate the original markdown bodies into larger bundle files with separators and source-path headers. Do not summarize or rewrite the source text during consolidation. Original paths should either remain in place until references are updated, or become small compatibility stubs pointing to the bundle section.

Created append-only admin bundles:

- `docs/experiments_consolidated/admin_tracker_bundle_101_140.md`: 34 source docs
- `docs/experiments_consolidated/admin_tracker_bundle_141_180.md`: 34 source docs
- `docs/experiments_consolidated/admin_tracker_bundle_181_220.md`: 34 source docs
- `docs/experiments_consolidated/admin_tracker_bundle_221_271.md`: 49 source docs

Validation confirms each listed source header and source body is present
verbatim in its bundle. Original `docs/experiments/` files remain untouched.

## Safe Reorganization Policy

1. Keep substantive experiment/diagnostic outputs in `outputs/experiments`.
2. Keep useful report/dev artifacts in place until report references are checked; optionally add a report/dev index later.
3. Move admin/churn output folders only with compatibility links or stubs, because manifests, handoff matrices, and tracker docs reference canonical paths.
4. Consolidate short tracker docs by appending verbatim into bundle files. Do not rewrite their content.
5. Stop allocating numbered experiment IDs for commit summaries, queues, resume checkpoints, or archive pointer refreshes unless crash recovery absolutely requires it.

## Proposed Next Step

Before moving output folders, run a reference check over docs, manifests, and
reports for every admin/churn candidate. Then either leave originals plus the
bundle index, or move admin output directories to
`outputs/experiment_admin_archive/535_735/` while preserving compatibility
links at the original paths.
