# Experiment 276: Seed21 Fitted-Ringdown All-Target Summary

## Purpose

Run 743 summarizes the restored GPU sequence from runs 740-742. Those runs
added a fourth source-mismatch/ringdown noise seed, seed21, to the established
Tx/Rx=50 mm variable-depth/radius final-state fitted-ringdown branch.

This run is a decision-grade analysis artifact: it converts three substantive
GPU diagnostics into one compact table, one JSON summary, and two figures.

## 743: Seed21 Fitted-Ringdown All-Target Summary

Output:

```text
outputs/experiments/743_seed21_fitted_ringdown_all_target_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_seed21_fitted_ringdown_summary.py --run-name seed21_fitted_ringdown_all_target_summary
```

Inputs:

```text
run 740 target 0 summary
run 742 target 1 summary
run 741 target 2 summary
```

Artifacts:

```text
README.md
data/seed21_fitted_ringdown_summary.json
data/seed21_objective_confidence_rows.csv
data/seed21_objective_ratios.csv
data/seed21_target_summary.csv
figures/seed21_base_margins_by_target.png
figures/seed21_objective_ratios_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

All three base production rows are truth-geometry rows:

| Target | Truth x/z/r mm | Base margin | Base confidence | Strongest truth-preserving diagnostic | Ratio |
| ---: | --- | ---: | --- | --- | ---: |
| 0 | 150 / 80 / 5.0 | 5.385658e-04 | moderate | veryhigh | 1.250 |
| 1 | 250 / 100 / 6.0 | 7.175881e-04 | moderate | late_high | 1.279 |
| 2 | 350 / 120 / 8.0 | 8.000475e-04 | moderate | late_high | 1.506 |

Aggregate:

```text
target count: 3
base truth count: 3
base confidence labels: moderate=3
best truth-preserving objectives: veryhigh=1, late_high=2
objective ratio rows: 15
objective confidence rows: 18
diagnostic geometry changes: 0
```

## Interpretation

The additional seed21 stress does not expose a new failure in the
fitted-ringdown Tx/Rx=50 final-state branch. Base remains exact and moderate
on all targets.

The diagnostic objective pattern remains target-specific:

```text
target 0: veryhigh is strongest
targets 1 and 2: late_high is strongest
```

This strengthens the conservative rule rather than replacing it:

```text
Use base for coordinate updates.
Use diagnostic objective variants as reporting evidence.
Do not promote a single global diagnostic objective without a separate
branch-specific update-rule study.
```

## Validation

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_seed21_fitted_ringdown_summary.py
3 passed

JSON parse:
run_manifest.json pass
seed21_fitted_ringdown_summary.json pass

CSV row counts:
seed21_target_summary.csv: 3
seed21_objective_ratios.csv: 15
seed21_objective_confidence_rows.csv: 18

Figure validation:
seed21_base_margins_by_target.png: 1243x733, dynamic range 255
seed21_objective_ratios_by_target.png: 1515x835, dynamic range 255

git diff --check: clean after run 743
```

## Next Decision

Continue with bounded GPU diagnostics while resources are healthy. Candidate
next steps are:

```text
1. another added seed on the same all-target fitted-ringdown branch
2. a different concrete physics stress, not a broad all-parameter sweep
3. a decision-grade archive/report artifact outside the numbered experiment
   stream only when it is not pointer churn
```
