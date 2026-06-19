# Experiment 821: Close50 Legacy 270/280 Policy Audit Refresh

Date: 2026-06-18

## Purpose

Refresh the old close50 270/280 branch audit after the later sub-30 mm midpoint
pilots became available. This is a CPU-only synthesis of existing outputs; it
does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

This tracker supersedes the narrow conclusion in experiment 786 for the
specific 270/280 question because it includes the 27.5 mm and 28.75 mm
single-seed midpoint pilots.

## Output

```text
outputs/experiments/1308_close50_legacy_270_280_policy_audit_post_midpoint_refresh
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

Summary:

```text
first clean replicated Tx/Rx offset: 30 mm
ambiguous replicated offsets:        25 mm
non-clean offsets:                   25, 27.5, 28.75 mm
clean replicated offsets:            30, 35, 40 mm
single-seed midpoint offsets:         27.5, 28.75 mm
single-seed non-clean midpoints:      27.5, 28.75 mm
threshold rows:                       36
single-seed midpoint rows:            6
run 270 truth fraction:               1.0
run 270 min margin:                   2.5465e-03
run 280 Tx/Rx 40 truth fraction:      1.0
run 280 Tx/Rx 40 min margin:          4.8172e-03
tracker/output mismatch count:        2
```

## Interpretation

The old 270/280 close50 branch should not be treated as failed. It was a
limited target2 Tx/Rx 40 mm branch, and it was clean there. The current evidence
says something more useful for the paper:

```text
Tx/Rx 25 mm is ambiguous.
Tx/Rx 27.5 and 28.75 mm single-seed midpoint pilots remain non-clean.
Tx/Rx 30 mm is the first clean replicated nearest-sampled offset.
Tx/Rx 35-40 mm are clean and stronger.
```

Do not repeat the old Tx/Rx 40 target2 branch. More midpoint seeds are only
justified if the manuscript needs a replicated non-clean bracket below 30 mm;
they are not justified as a default continuation of the 270/280 work.

## Validation

Figure validation:

```text
close50_legacy_policy_audit.png: 2365x801,
nonwhite=0.2698, dynamic range=255
```
