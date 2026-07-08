# Experiment 768: Target0 Objective-Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only diagnostic-objective synthesis for the 18 target0 rows aggregated in
experiment 765. This checks whether the target1/target2 late-high diagnostic
pattern generalizes to target0.

No FDTD, FWI, or GPU command was run for this synthesis.

## Output

```text
outputs/experiments/1231_coordinate_objective_diagnostic_target0_policy
```

Artifacts:

```text
data/coordinate_objective_diagnostic_ratios.csv
data/coordinate_objective_confidence_rows.csv
data/coordinate_objective_diagnostic_report.json
figures/coordinate_objective_diagnostic_ratios.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Result

The report compares five diagnostic objectives against the matching base row
for each of the 18 target0 summaries.

Ratio summary:

| Objective | Rows | Truth-preserving rows | Geometry changes | Mean margin ratio | Min ratio | Max ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `early_high` | 18 | 18 | 0 | 1.1251 | 1.0443 | 1.2848 |
| `highband` | 18 | 18 | 0 | 1.3327 | 1.2546 | 1.4616 |
| `late` | 18 | 18 | 0 | 0.7659 | 0.6603 | 0.8900 |
| `late_high` | 18 | 18 | 0 | 0.8611 | 0.6900 | 1.0267 |
| `veryhigh` | 18 | 18 | 0 | 1.2982 | 1.1264 | 1.5476 |

Objective-specific confidence rows:

| Objective | Truth rows | Rows clearing `5.0e-4` | Weak rows | Mean margin | Min margin | Max margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `base` | 18 | 5 | 13 | 4.871635e-4 | 4.384714e-4 | 5.583698e-4 |
| `early_high` | 18 | 13 | 5 | 5.481026e-4 | 4.807441e-4 | 6.558477e-4 |
| `highband` | 18 | 18 | 0 | 6.495129e-4 | 5.680446e-4 | 7.519866e-4 |
| `late` | 18 | 0 | 18 | 3.727977e-4 | 3.194032e-4 | 4.579559e-4 |
| `late_high` | 18 | 1 | 17 | 4.191154e-4 | 3.076531e-4 | 5.121683e-4 |
| `veryhigh` | 18 | 18 | 0 | 6.334062e-4 | 5.095716e-4 | 8.057408e-4 |

Every objective row preserves exact target0 geometry. The only nonzero
ambiguity width is in the `late` objective, where the max radius ambiguity
width is 0.25 mm.

## Interpretation

Target0 does not follow the target1/target2 late-window pattern. Highband and
veryhigh strengthen every audited target0 row while preserving exact geometry;
late and late_high generally weaken the target0 radius margin.

Current target-specific diagnostic policy:

```text
target0: use highband/veryhigh as secondary confirmation evidence; do not use
         late or late_high as a target0 rescue rule.
target1: late_high is the strongest secondary confirmation in the audited weak
         exact branches.
target2: highband/late/late_high all clear the audited exact branches, with
         late_high strongest on average.
```

This prevents overgeneralizing one objective variant across all targets. The
diagnostic objectives remain reporting/confirmation evidence, not replacements
for the base production acceptance gate.

## Validation

The diagnostic-ratio figure was validated as nonblank:

```text
coordinate_objective_diagnostic_ratios.png nonwhite=0.2774
```
