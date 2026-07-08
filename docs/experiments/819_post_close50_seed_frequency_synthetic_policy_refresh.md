# Experiment 819: Post-Close50 Seed-Frequency Synthetic Policy Refresh

Date: 2026-06-18

## Purpose

Refresh the synthetic 2D manuscript decision surface after the close50 linear
29.5 mm three-seed policy. This is a CPU-side reporting step: it moves the
completed close50 caveat into the claim-boundary table and then confirms
whether any immediate local synthetic GPU work remains justified.

## Outputs

```text
1304_synthetic_2d_next_question_matrix_post_close50_seed_frequency
1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency
1306_synthetic_2d_next_question_matrix_post_close50_claim_refresh
```

Key artifacts:

```text
outputs/experiments/1304_synthetic_2d_next_question_matrix_post_close50_seed_frequency/data/synthetic_2d_next_question_matrix_summary.json
outputs/experiments/1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/synthetic_2d_publication_claim_boundary_refresh_summary.json
outputs/experiments/1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/synthetic_2d_publication_claim_boundaries_refreshed.csv
outputs/experiments/1306_synthetic_2d_next_question_matrix_post_close50_claim_refresh/data/synthetic_2d_next_question_matrix_summary.json
```

## Result

Run 1304 ranked the needed CPU-side refresh:

```text
policy label:                 synthetic_2d_next_question_matrix_cpu_first_no_gpu
top question:                 post_close50_claim_boundary_refresh
conditional GPU candidates:   0
gpu priority:                 none_now
decision:                     close50 29.5 mm is exact/strong across three seeds, but seed13 remains an x-ambiguity caveat
```

Run 1305 refreshed the manuscript claim boundaries:

```text
policy label:                 synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu
claim boundaries:             9
close14 probe included:       true
close50 seed policy included: true
close50 seeds:                3
close50 ambiguous seeds:      seed13
gpu priority:                 none
```

Run 1306 confirmed the current synthetic local policy endpoint:

```text
policy label:                 synthetic_2d_next_question_matrix_cpu_first_no_gpu
top question:                 synthetic_claim_boundaries_current
cpu-first candidates:         0
conditional GPU candidates:   0
gpu priority:                 none_now
decision:                     no immediate or broad GPU run is justified
```

## Interpretation

The close14 objective-limit branch and close50 linear 29.5 mm seed-frequency
caveat are now both represented in the synthetic claim-boundary CSV. The
paper-safe close50 threshold language should remain conservative:

```text
29.5 mm: exact/strong across three seeds, not clean-replicated
30.0 mm: nearest-sampled paper-safe clean threshold
```

The local 2D synthetic queue is not closed permanently. It is closed only for
the already-posed close14 and close50 policy questions. Any future GPU work
should introduce a genuinely new objective, geometry, acquisition design, or
exception hypothesis before consuming GPU time.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py
tests/test_synthetic_2d_publication_claim_boundary_refresh.py
14 passed
```

Figure validation:

```text
1304 synthetic_2d_next_question_matrix.png: 2501x903, dynamic range=255
1305 synthetic_2d_publication_claim_boundary_refresh.png: 2127x835, dynamic range=255
1306 synthetic_2d_next_question_matrix.png: 2501x903, dynamic range=255
```
