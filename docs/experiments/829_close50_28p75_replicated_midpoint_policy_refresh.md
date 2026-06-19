# Experiment 829: Close50 28.75 mm Replicated-Midpoint Policy Refresh

Date: 2026-06-18

## Purpose

Run one bounded close50 target2 GPU replicate at nearest-sampled Tx/Rx 28.75 mm
and refresh the synthetic 2D policy stack from that result. This addresses the
old 270/280 concern without reopening a broad sweep.

This tracker covers runs 1316-1319 as one research slice.

Superseded endpoint note: experiment 830 / runs 1320-1321 keep this close50
replicated-midpoint evidence but add the current target1 policy figures to the
paper-facing synthetic 2D publication bundle. Run 1321 is the current synthetic
next-question matrix.

## Outputs

```text
outputs/experiments/1316_coordinate_optimizer_close50_seed13_sources4_txrx28p75_objectives
outputs/experiments/1317_close50_legacy_270_280_policy_audit_post_28p75_seed13_replicate
outputs/experiments/1318_synthetic_2d_publication_figure_bundle_post_28p75_replicated_midpoint_refresh
outputs/experiments/1319_synthetic_2d_next_question_matrix_post_28p75_replicated_midpoint_bundle
```

## Result

Run 1316 is exact and strong for seed13:

```text
target:              close50 target2
sources:             4
Tx/Rx offset:         28.75 mm, nearest receiver sampling
final x/z/r:          300 / 90 / 8.0 mm
nominal margin:       1.8985e-03, strong
source-mismatch margin: 1.7138e-03, strong
highband diagnostic:  truth geometry for both cases
strict clean:         no; nominal row retains x=300-301 mm ambiguity
elapsed:              1527.5 s
```

Combined with the earlier seed21 28.75 mm pilot, this creates replicated
non-clean immediate-below-threshold support:

```text
1317 policy label:     close50_target2_threshold_refined_replicated_midpoint_not_clean
first clean Tx/Rx:     30 mm
non-clean offsets:     25, 27.5, 28.75 mm
clean offsets:         30, 35, 40 mm
replicated non-clean midpoint: 28.75 mm
threshold scope:       target2 only
```

Run 1318 refreshes the paper-facing synthetic publication bundle to use run
1317 instead of the older run 1308 close50 legacy refresh:

```text
figure count:           7
validated figure count: 7
claim boundaries:       5
gpu priority:           none
ready for draft:        true
```

Run 1319 refreshes the synthetic next-question matrix:

```text
policy label:                 synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:               10
immediate GPU candidates:     0
conditional GPU candidates:   0
top question:                 synthetic_publication_bundle_current
gpu priority:                 none_now
```

## Interpretation

The old close50 Tx/Rx 40 branch should not be repeated. It was clean for its
target2-only purpose. The more useful publication statement is now sharper:
nearest-sampled 28.75 mm has replicated non-clean support, while 30 mm remains
the first clean replicated offset in the tested close50 target2 branch.

Do not promote 28.75 mm, 29.5 mm, or 29.75 mm to a clean sub-30 threshold. The
useful claim is an acquisition- and objective-specific threshold boundary:
below 30 mm the branch is exact/strong in some cases but still has lateral
ambiguity; at 30 mm and above the tested replicated nearest-sampled rows are
strict-clean.

Seed34 at 28.75 mm is not a current GPU priority. Seed21 plus seed13 are enough
to establish replicated non-clean immediate-below-threshold evidence, and run
1319 returns zero immediate or conditional GPU candidates.

## Validation

Focused tests:

```text
tests/test_close50_legacy_policy_audit.py
tests/test_synthetic_2d_publication_figure_bundle.py
tests/test_synthetic_2d_next_question_matrix.py
24 passed
```

Figure validation:

```text
1316 coordinate_confidence_margins.png: 1804x665, dynamic range=238
1317 close50_legacy_policy_audit.png: 2365x801, dynamic range=255
1318 synthetic_2d_publication_figure_bundle.png: 2738x903, dynamic range=255
```

Resource envelope:

```text
GPU utilization during run 1316: 84-86%, below the 90% cap
RAM during run 1316: about 15 GiB used, far below the 80% cap
```
