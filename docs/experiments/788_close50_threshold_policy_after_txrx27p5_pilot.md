# Experiment 788: Close50 Threshold Policy After Tx/Rx 27.5 mm Pilot

Date: 2026-06-17

## Purpose

CPU-only policy refresh after the close50 Tx/Rx 27.5 mm seed21 pilot in
experiment 787. This run folds the midpoint pilot into the existing close50
target2 threshold table without promoting a single-seed result to a replicated
threshold.

No FDTD, FWI, GPU kernels, or new synthetic inversion runs were launched.

## Output

```text
outputs/experiments/1266_close50_threshold_policy_after_txrx27p5_pilot
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
outputs/experiments/1265_coordinate_optimizer_close50_seed21_sources4_txrx27p5_objectives
```

## Result

Policy label:

```text
close50_target2_threshold_refined_midpoint_not_clean
```

Threshold table:

| Tx/Rx | Scope | Rows | Truth rows | X ambiguity rows | Min margin | Branch label |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 25 mm | replicated aggregate | 12 | 4 | 12 | 6.06e-05 | `mixed_or_ambiguous` |
| 27.5 mm | single-seed pilot | 4 | 4 | 4 | 4.78e-04 | `single_seed_exact_but_nonclean` |
| 30 mm | replicated aggregate | 6 | 6 | 0 | 1.70e-03 | `clean_replicated` |
| 35 mm | replicated aggregate | 6 | 6 | 0 | 4.27e-03 | `clean_replicated` |
| 40 mm | replicated aggregate | 6 | 6 | 0 | 4.82e-03 | `clean_replicated` |

Decision:

```text
Tx/Rx 25 mm is ambiguous.
Tx/Rx 27.5 mm is exact for seed21 but non-clean under confidence/ambiguity policy.
Tx/Rx 30 mm remains the first clean replicated offset.
```

## Interpretation

The 27.5 mm pilot improves the threshold bracket without requiring more GPU
work. It shows that the midpoint is not a clean confidence-policy result: all
four confidence rows have x/r ambiguity, the nominal case is weak, and the
high-band diagnostic selected the nearby wrong branch in experiment 787.

Do not run seed13/34 at Tx/Rx 27.5 mm unless the paper specifically needs a
replicated non-clean midpoint bracket. For the current policy, 30 mm remains
the first tested clean replicated close50 target2 offset.

## Validation

Focused tests:

```text
tests/test_close50_legacy_policy_audit.py: 6 passed
```

The policy figure was validated as nonblank:

```text
close50_legacy_policy_audit.png nonwhite=0.2656, dynamic range=255
```
