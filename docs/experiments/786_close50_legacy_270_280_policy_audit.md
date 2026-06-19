# Experiment 786: Close50 Legacy 270/280 Policy Audit

Date: 2026-06-17

## Purpose

CPU-only audit of the old close50 experiment 270/280 area against the later
close50 target2 threshold evidence. This addresses whether the 270/280 branch
needs more local GPU work, or whether later runs already resolved the useful
question.

No FDTD, FWI, GPU kernels, or new synthetic inversion runs were launched.

## Output

```text
outputs/experiments/1264_close50_legacy_270_280_policy_audit
```

Artifacts:

```text
data/close50_legacy_branch_evidence.csv
data/close50_threshold_by_txrx.csv
data/close50_legacy_tracker_output_alignment.csv
data/close50_legacy_policy_audit_summary.json
data/figure_validation.csv
figures/close50_legacy_policy_audit.png
run_manifest.json
```

## Inputs

```text
outputs/experiments/270_coordinate_optimizer_close50_seed21_sources5_txrx40_objectives
outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates
outputs/experiments/1222_coordinate_confidence_close50_sources4_txrx25_30_35_40_seed_replicates
docs/experiments/270_current_archive_coverage_refresh_state_audit.md
docs/experiments/280_seed89_fitted_ringdown_all_target_summary.md
```

## Result

Policy label:

```text
close50_target2_threshold_resolved_no_gpu_repeat
```

Threshold evidence for the later close50 target2 sources4 aggregate:

| Tx/Rx | Rows | Truth rows | X ambiguity rows | Min margin | Branch label |
| ---: | ---: | ---: | ---: | ---: | --- |
| 25 mm | 12 | 4 | 12 | 6.06e-05 | `mixed_or_ambiguous` |
| 30 mm | 6 | 6 | 0 | 1.70e-03 | `clean_replicated` |
| 35 mm | 6 | 6 | 0 | 4.27e-03 | `clean_replicated` |
| 40 mm | 6 | 6 | 0 | 4.82e-03 | `clean_replicated` |

Legacy branch checks:

```text
run 270 output: exact 2/2 rows, min margin 2.55e-03, target2-only, sources5, Tx/Rx 40.
run 280 output: exact 6/6 rows, min margin 4.82e-03, target2-only, sources4, Tx/Rx 40.
first clean tested threshold in later aggregate: Tx/Rx 30 mm.
ambiguous tested threshold: Tx/Rx 25 mm.
```

Tracker/output alignment issue:

```text
docs/experiments/270_current_archive_coverage_refresh_state_audit.md
  does not describe outputs/experiments/270_coordinate_optimizer_close50_seed21_sources5_txrx40_objectives

docs/experiments/280_seed89_fitted_ringdown_all_target_summary.md
  does not describe outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates
```

## Interpretation

The old close50 270/280 branch was limited, not failed. It is target2-only and
should not be framed as an all-target, field-data, or general resolution-limit
result. But later close50 threshold evidence already answers the useful target2
question:

```text
Tx/Rx 25 mm is ambiguous.
Tx/Rx 30 mm is the first tested clean replicated offset.
Tx/Rx 35-40 mm are clean and stronger.
```

Do not repeat the old Tx/Rx 40 target2 branch. A new GPU run is only justified
if the paper needs a finer bracket between Tx/Rx 25 and 30 mm, or if the
question changes to another target/geometry.

## Validation

Focused tests:

```text
tests/test_close50_legacy_policy_audit.py: 3 passed
```

The audit figure was validated as nonblank:

```text
close50_legacy_policy_audit.png nonwhite=0.2279, dynamic range=255
```
