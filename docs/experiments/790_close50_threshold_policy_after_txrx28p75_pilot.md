# Experiment 790: Close50 Threshold Policy After Tx/Rx 28.75 mm Pilot

Date: 2026-06-17

## Purpose

CPU-only policy refresh after the close50 Tx/Rx 28.75 mm seed21 pilot in
experiment 789. This folds both midpoint pilots, 27.5 mm and 28.75 mm, into the
existing close50 target2 threshold table.

No FDTD, FWI, GPU kernels, or new synthetic inversion runs were launched.

## Output

```text
outputs/experiments/1268_close50_threshold_policy_after_txrx28p75_pilot
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
outputs/experiments/1267_coordinate_optimizer_close50_seed21_sources4_txrx28p75_objectives
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
| 28.75 mm | single-seed pilot | 2 | 2 | 2 | 1.25e-03 | `single_seed_exact_but_nonclean` |
| 30 mm | replicated aggregate | 6 | 6 | 0 | 1.70e-03 | `clean_replicated` |
| 35 mm | replicated aggregate | 6 | 6 | 0 | 4.27e-03 | `clean_replicated` |
| 40 mm | replicated aggregate | 6 | 6 | 0 | 4.82e-03 | `clean_replicated` |

Decision:

```text
Tx/Rx 25 mm is ambiguous.
Tx/Rx 27.5 mm and 28.75 mm refine the below-threshold bracket but remain non-clean.
Tx/Rx 30 mm remains the first clean replicated offset.
```

## Interpretation

The 28.75 mm pilot narrowed the transition region: it is strong and exact for
seed21, unlike the weaker 27.5 mm pilot. However, it still has one-grid-cell x
ambiguity in both confidence rows, and it is only a single-seed pilot. The
paper-safe statement remains that the first clean replicated close50 target2
offset is 30 mm under the current sources4 confidence policy.

Under the current 1 mm grid with `receiver_sampling=nearest`, the requested
28.75 mm run is effectively a 29 mm Tx/Rx receiver-index run. Sub-millimeter
requested-offset bisection should not be treated as new physical acquisition
evidence unless the receiver sampling is changed, for example to linear
interpolation, or the grid is refined.

## Validation

Focused tests:

```text
tests/test_close50_legacy_policy_audit.py: 7 passed
```

The policy figure was validated as nonblank:

```text
close50_legacy_policy_audit.png nonwhite=0.2698, dynamic range=255
```
