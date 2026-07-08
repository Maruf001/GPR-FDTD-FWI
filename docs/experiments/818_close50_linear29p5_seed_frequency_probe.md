# Experiment 818: Close50 Linear 29.5 mm Seed-Frequency Probe

Date: 2026-06-18

## Purpose

Close the remaining close50 target2 sub-30 mm seed-frequency question after
the post-close14 claim refresh. This branch tests whether the linear-receiver
29.5 mm result is a repeated ambiguity or a seed13-specific caveat.

The decision rule was fixed before launching the only missing GPU run:

```text
If seed34 is strict-clean:
  report seed13 as a 1/3 x-ambiguity case.

If seed34 is x-ambiguous:
  report x ambiguity in 2/3 seeds.

In both cases:
  do not promote a clean sub-30 threshold because seed13 is already ambiguous.
```

## Outputs

```text
1300_synthetic_2d_next_question_matrix_post_claim_refresh
1301_close50_linear29p5_seed_frequency_contract
1302_coordinate_optimizer_close50_seed34_sources4_txrx29p5_linear_receiver_objectives
1303_close50_linear29p5_three_seed_frequency_policy
```

Key artifacts:

```text
outputs/experiments/1300_synthetic_2d_next_question_matrix_post_claim_refresh/data/synthetic_2d_next_question_matrix_summary.json
outputs/experiments/1301_close50_linear29p5_seed_frequency_contract/data/close50_linear29p5_seed_frequency_contract_summary.json
outputs/experiments/1302_coordinate_optimizer_close50_seed34_sources4_txrx29p5_linear_receiver_objectives/data/multi_rebar_coordinate_optimizer_summary.json
outputs/experiments/1303_close50_linear29p5_three_seed_frequency_policy/data/close50_linear_receiver_policy_summary.json
outputs/experiments/1303_close50_linear29p5_three_seed_frequency_policy/figures/close50_linear_receiver_policy.png
```

## Result

Run 1300 ranked the post-claim-refresh close50 seed-frequency contract as the
top synthetic question, but with no immediate GPU priority:

```text
policy label:                 synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate count:              8
top question:                 close50_sub30_seed_frequency_contract
conditional GPU candidates:   1
gpu priority:                 none_now
```

Run 1301 converted that question into a skip-existing contract:

```text
policy label:                 close50_linear29p5_seed_frequency_contract_skip_existing_cpu_no_gpu
existing seeds:               13,21
missing seeds:                34
gpu priority:                 low_conditional_not_launched
resource policy:              run only seed34, GPU <=90%, RAM <=80%
```

Run 1302 executed the single missing seed34 probe:

```text
runtime:                      1536.1 s
target index:                 2
sources:                      4
Tx/Rx offset:                 29.5 mm
receiver sampling:            linear
truth geometry selected:      2 / 2 cases
strong confidence rows:       2 / 2 cases
x-ambiguity rows:             0 / 2 cases
highband truth rows:          2 / 2 cases
observed GPU utilization:     about 85-86%
observed RAM use:             about 14 GiB
```

Run 1303 synthesized the three-seed policy:

```text
policy label:                 close50_linear29p5_three_seed_exact_strong_not_clean_replicated
seeds:                        seed13,seed21,seed34
truth geometry rows:          6 / 6
strong confidence rows:       6 / 6
strict-clean rows:            5 / 6
x-ambiguity rows:             1 / 6
strict-clean seeds:           seed21,seed34
ambiguous seeds:              seed13
highband truth rows:          6 / 6
```

## Interpretation

The seed34 result is strict-clean, so the close50 linear 29.5 mm branch is not
a robust repeated ambiguity. It is a seed-frequency caveat:

```text
seed13: x-ambiguous in one nominal row
seed21: strict-clean
seed34: strict-clean
```

This supports reporting 29.5 mm as exact and strong but not clean-replicated.
The nearest-sampled first clean replicated offset remains 30 mm for paper-safe
threshold language. Do not claim a clean sub-30 threshold from this branch.

## Validation

Focused tests:

```text
tests/test_close50_linear_receiver_policy.py
tests/test_close50_linear29p5_seed_frequency_contract.py
tests/test_synthetic_2d_next_question_matrix.py
14 passed
```

Figure validation:

```text
1300 synthetic_2d_next_question_matrix.png: 2501x903, dynamic range=255
1301 close50_linear29p5_seed_frequency_contract.png: 2195x835, dynamic range=255
1303 close50_linear_receiver_policy.png: 2263x835, dynamic range=255
```
