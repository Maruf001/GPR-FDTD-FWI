# Experiment 65: Variable-Depth/Radius Objective Cross-Condition Report

## Purpose

Compare the Tx/Rx=50 mm objective diagnostics across the final-state
non-ringdown package and the fitted-ringdown stress package. This is a
CPU-only reporting check over existing JSON summaries, not a new FDTD sweep.

## Inputs

Non-ringdown Tx/Rx=50 mm objective packages:

```text
outputs/experiments/499_coordinate_optimizer_variable_depth_radius_target0_txrx50_three_seed_objective_variants/data/multi_rebar_coordinate_optimizer_summary.json
outputs/experiments/504_coordinate_optimizer_variable_depth_radius_target1_txrx50_three_seed_objective_variants/data/multi_rebar_coordinate_optimizer_summary.json
outputs/experiments/501_coordinate_optimizer_variable_depth_radius_target2_txrx50_three_seed_objective_variants/data/multi_rebar_coordinate_optimizer_summary.json
```

Fitted-ringdown Tx/Rx=50 mm objective packages:

```text
target 0: runs 515, 518, 508
target 1: runs 526, 528, 512
target 2: runs 521, 523, 510
```

## 532: All-Condition Objective Confidence Report

Output:

```text
outputs/experiments/532_variable_depth_radius_txrx50_all_condition_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/499_coordinate_optimizer_variable_depth_radius_target0_txrx50_three_seed_objective_variants/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/504_coordinate_optimizer_variable_depth_radius_target1_txrx50_three_seed_objective_variants/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/501_coordinate_optimizer_variable_depth_radius_target2_txrx50_three_seed_objective_variants/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/515_coordinate_optimizer_variable_depth_radius_seed13_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/518_coordinate_optimizer_variable_depth_radius_seed34_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/526_coordinate_optimizer_variable_depth_radius_seed13_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/528_coordinate_optimizer_variable_depth_radius_seed34_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/512_coordinate_optimizer_variable_depth_radius_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/521_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/523_coordinate_optimizer_variable_depth_radius_seed34_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/510_coordinate_optimizer_variable_depth_radius_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_txrx50_all_condition_objective_confidence_report \
  --outdir outputs/experiments/532_variable_depth_radius_txrx50_all_condition_objective_confidence_report
```

Runtime:

```text
0.85 s
```

Diagnostic ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Ratio min/mean/max |
| --- | ---: | ---: | ---: | --- |
| early_high | 27 | 27 | 0 | 0.512 / 0.617 / 0.748 |
| highband | 27 | 27 | 0 | 0.828 / 0.981 / 1.089 |
| late | 27 | 27 | 0 | 0.510 / 1.294 / 2.136 |
| late_high | 27 | 27 | 0 | 0.420 / 1.306 / 2.133 |
| veryhigh | 27 | 27 | 0 | 1.058 / 1.612 / 2.563 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Margin min/mean/max | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- | --- |
| base | 27 | 27 | weak=16, moderate=10, strong=1 | 1.777e-04 / 4.823e-04 / 1.040e-03 | 0 / 0 / 0.25 |
| early_high | 27 | 27 | weak=25, moderate=2 | 1.146e-04 / 2.932e-04 / 6.280e-04 | 0 / 0 / 0 |
| highband | 27 | 27 | weak=16, moderate=10, strong=1 | 1.849e-04 / 4.754e-04 / 1.109e-03 | 0 / 0 / 0 |
| late | 27 | 27 | weak=12, moderate=10, strong=5 | 1.779e-04 / 6.263e-04 / 1.635e-03 | 0 / 0 / 0.25 |
| late_high | 27 | 27 | weak=12, moderate=10, strong=5 | 1.520e-04 / 6.397e-04 / 1.715e-03 | 0 / 0 / 0 |
| veryhigh | 27 | 27 | weak=5, moderate=17, strong=5 | 2.689e-04 / 7.221e-04 / 1.325e-03 | 0 / 0 / 0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
14248x1005 px, dynamic range 255, grayscale std 65.8432
```

## Interpretation

Every objective variant preserves truth geometry across the selected 27
coordinate-confidence rows, so the comparison is about margin quality rather
than branch failure.

Veryhigh is the only tested diagnostic with margin ratio above 1.0 on every
row. It also gives the strongest aggregate objective-confidence summary:
weak=5, moderate=17, strong=5, mean absolute margin 7.221e-04, and zero x/z/r
ambiguity width. Base remains exact but has weak=16, moderate=10, strong=1 and
a 0.25 mm maximum radius ambiguity.

Late and late_high have useful high-end gains and are strongest for targets 1
and 2 under fitted ringdown, but their minima are below 1.0 because they weaken
target-0 rows. They should remain per-target diagnostics rather than the
branch-level reporting default.

## Next Decision

Use veryhigh as the branch-level reporting diagnostic for the Tx/Rx=50 mm
variable-depth/variable-radius final-state package, while keeping the base
objective as the production coordinate update rule. The next work should be a
lightweight summary artifact that makes this distinction explicit; do not run
more GPU sweeps until that handoff is clear.
