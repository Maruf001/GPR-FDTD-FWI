# Experiment 797: Close50 Linear Sub-30 mm Bracket Policy

Date: 2026-06-17

## Purpose

CPU-only synthesis of the close50 target2 linearly sampled sub-30 mm branch:

```text
1271: seed21, linear 29.5 mm
1272: seed13, linear 29.5 mm
1274: seed13, linear 29.75 mm
```

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1275_close50_linear_sub30_bracket_policy
```

Artifacts:

```text
data/close50_linear_sub30_bracket_summary.json
data/close50_linear_sub30_bracket_run_rows.csv
data/close50_linear_sub30_bracket_confidence_rows.csv
data/close50_linear_sub30_bracket_objective_diagnostics.csv
data/figure_validation.csv
figures/close50_linear_sub30_bracket_policy.png
run_manifest.json
```

## Result

Policy label:

```text
close50_linear_sub30_seed13_x_ambiguity_persists
```

Summary:

```text
tested offsets:                 29.5, 29.75 mm
sub-30 confidence rows:          6
truth geometry rows:             6
strong-confidence rows:          6
strict clean rows:               4
x-ambiguity rows:                2
radius-ambiguity rows:           0
seed13 x-ambiguous offsets:      29.5, 29.75 mm
minimum primary radius margin:   1.4692e-03
highband truth rows:             6 / 6
```

Per-run policy rows:

| Run | Result |
| --- | --- |
| seed21 linear 29.5 | `single_seed_clean` |
| seed13 linear 29.5 | `single_seed_exact_strong_x_ambiguous` |
| seed13 linear 29.75 | `single_seed_exact_strong_x_ambiguous` |

## Interpretation

The sub-30 linear branch is exact and strong, but it is not clean under the
strict no-x-ambiguity policy. The seed13 nominal row remains x-ambiguous at
both 29.5 and 29.75 mm.

Stop sub-30 linear receiver bracketing for clean-threshold claims under the
current objective. The nearest-sampled close50 target2 result remains the
paper-safe clean threshold:

```text
first clean replicated nearest-sampled Tx/Rx offset: 30 mm
```

Further GPU work on this branch should require a new question, such as a new
objective definition or a seed-frequency estimate. It should not continue as
another midpoint bisection.

## Validation

Focused tests:

```text
tests/test_close50_linear_sub30_bracket_policy.py: 2 passed
```

Figure validation:

```text
close50_linear_sub30_bracket_policy.png: 2331x835,
nonwhite=0.4693, dynamic range=255
```
