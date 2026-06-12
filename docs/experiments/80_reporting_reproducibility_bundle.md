# Experiment 80: Reporting Reproducibility Bundle

## Purpose

Create a lightweight final reporting bundle that points to the current report
draft, figure/caption package, claim-consistency audit, figure-readiness audit,
evidence synthesis, handoff matrix, and master plan.

## 547: Reporting Reproducibility Bundle

Output:

```text
outputs/experiments/547_reporting_reproducibility_bundle
```

Command:

```text
Manual CPU-only reporting bundle. The links directory contains symlinks to
canonical report, figure, audit, and planning artifacts.
```

Artifacts:

```text
README.md
data/reporting_reproducibility_manifest.json
links/report_draft.md
links/figure_caption_package.md
links/report_figures/
links/claim_consistency_audit.md
links/figure_readiness_audit.json
links/current_evidence_synthesis.json
links/handoff_matrix.md
links/master_plan.md
run_manifest.json
```

Validation state:

```text
full pytest: 255 passed in 24.16 s
git diff --check: clean after run 546
run 543-546 JSON manifests: valid
run 545 package figures: all symlinked PNGs open through package paths
claim consistency audit: status=consistent, issues=0
```

## Interpretation

The reporting branch is packaged for assembly. The bundle preserves the same
claim boundaries as the claim-consistency audit: interval-aware variable-depth
/radius reporting, branch-specific veryhigh diagnostic use, source-shape center
r=6.0-6.2 mm reporting, and shallow r=4 mm nuisance-aware interval reporting.

## Next Decision

Use the bundle for final report assembly. No GPU experiment is queued.
