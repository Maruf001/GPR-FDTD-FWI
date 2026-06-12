# Experiment 64: Variable-Depth/Radius Ringdown Seed Replication

## Goal

Replicate the fitted-ringdown target-0 guardrail from experiment 63 on another
noise seed:

```text
target 0 at x=150 mm, z=80 mm, r=5 mm
source_mismatch_ringdown025_noise10_seed13
fit source primary and ringdown coefficients
Tx/Rx offset 50 mm
same diagnostic objective variants as experiment 63
```

Experiment 63 closed the seed55 all-target guardrail. This experiment starts
seed replication with target 0 because it was the most sensitive radius row in
the earlier variable-depth/radius branch.

## 515: Seed13 Target-0 Ringdown Objective Sweep

Output:

```text
outputs/experiments/515_coordinate_optimizer_variable_depth_radius_seed13_target0_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 508, but replication case source_mismatch_ringdown025_noise10_seed13.
target index 0 only, z offsets 0:1:1 from z=80 mm, radius offsets 0:1.25:0.25
from r=5 mm, and top-k 12.
```

Runtime:

```text
387.4 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-0 point: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
radius margin: 4.836e-04
confidence label: weak
ambiguity interval: x=150 mm, z=80 mm, r=5.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.0992
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2490
fitted combined source_ringdown_coefficient column: 0.2737
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 150 / 80 / 5.0 | 5.25 | 4.836e-04 | 1.000 | weak | 5.0 |
| highband | 150 / 80 / 5.0 | 5.25 | 4.712e-04 | 0.974 | weak | 5.0 |
| late | 150 / 80 / 5.0 | 5.25 | 3.454e-04 | 0.714 | weak | 5.0-5.25 |
| late_high | 150 / 80 / 5.0 | 5.25 | 3.382e-04 | 0.699 | weak | 5.0 |
| veryhigh | 150 / 80 / 5.0 | 5.25 | 6.397e-04 | 1.323 | moderate | 5.0 |
| early_high | 150 / 80 / 5.0 | 5.25 | 3.617e-04 | 0.748 | weak | 5.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 69.4500
```

## 516: Seed13 Target-0 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/516_variable_depth_radius_seed13_target0_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/515_coordinate_optimizer_variable_depth_radius_seed13_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_seed13_target0_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/516_variable_depth_radius_seed13_target0_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
veryhigh margin ratio: 1.323x
all other diagnostic variants reduce the margin
veryhigh confidence label: moderate
base confidence label: weak
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2055x1005 px, dynamic range 255, grayscale std 72.2984
```

## 517: Target-0 Seed13/Seed55 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/517_variable_depth_radius_target0_seed13_seed55_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/515_coordinate_optimizer_variable_depth_radius_seed13_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_target0_seed13_seed55_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/517_variable_depth_radius_target0_seed13_seed55_txrx50_ringdown025_objective_confidence_report
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Ratio min/mean/max |
| --- | ---: | ---: | ---: | --- |
| early_high | 2 | 2 | 0 | 0.698 / 0.723 / 0.748 |
| highband | 2 | 2 | 0 | 0.965 / 0.969 / 0.974 |
| late | 2 | 2 | 0 | 0.556 / 0.635 / 0.714 |
| late_high | 2 | 2 | 0 | 0.640 / 0.670 / 0.699 |
| veryhigh | 2 | 2 | 0 | 1.283 / 1.303 / 1.323 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 2 | 2 | weak=1, moderate=1 | 0 / 0 / 0 |
| early_high | 2 | 2 | weak=2 | 0 / 0 / 0 |
| highband | 2 | 2 | weak=1, moderate=1 | 0 / 0 / 0 |
| late | 2 | 2 | weak=2 | 0 / 0 / 0.25 |
| late_high | 2 | 2 | weak=2 | 0 / 0 / 0 |
| veryhigh | 2 | 2 | moderate=2 | 0 / 0 / 0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2058x1005 px, dynamic range 255, grayscale std 71.3183
```

## 518: Seed34 Target-0 Ringdown Objective Sweep

Output:

```text
outputs/experiments/518_coordinate_optimizer_variable_depth_radius_seed34_target0_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 515, but replication case source_mismatch_ringdown025_noise10_seed34.
```

Runtime:

```text
393.0 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-0 point: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
radius margin: 5.476e-04
confidence label: moderate
ambiguity interval: x=150 mm, z=80 mm, r=5.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.0994
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2509
fitted combined source_ringdown_coefficient column: 0.2758
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 150 / 80 / 5.0 | 5.25 | 5.476e-04 | 1.000 | moderate | 5.0 |
| highband | 150 / 80 / 5.0 | 5.25 | 5.228e-04 | 0.955 | moderate | 5.0 |
| late | 150 / 80 / 5.0 | 5.25 | 3.249e-04 | 0.593 | weak | 5.0-5.25 |
| late_high | 150 / 80 / 5.0 | 5.25 | 2.937e-04 | 0.536 | weak | 5.0 |
| veryhigh | 150 / 80 / 5.0 | 5.25 | 6.928e-04 | 1.265 | moderate | 5.0 |
| early_high | 150 / 80 / 5.0 | 5.25 | 4.050e-04 | 0.740 | weak | 5.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 66.8113
```

## 519: Seed34 Target-0 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/519_variable_depth_radius_seed34_target0_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/518_coordinate_optimizer_variable_depth_radius_seed34_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_seed34_target0_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/519_variable_depth_radius_seed34_target0_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
veryhigh margin ratio: 1.265x
all other diagnostic variants reduce the margin
veryhigh confidence label: moderate
base confidence label: moderate
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2055x1005 px, dynamic range 255, grayscale std 71.4423
```

## 520: Target-0 Three-Seed Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/520_variable_depth_radius_target0_three_seed_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/515_coordinate_optimizer_variable_depth_radius_seed13_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/518_coordinate_optimizer_variable_depth_radius_seed34_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_target0_three_seed_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/520_variable_depth_radius_target0_three_seed_txrx50_ringdown025_objective_confidence_report
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Ratio min/mean/max |
| --- | ---: | ---: | ---: | --- |
| early_high | 3 | 3 | 0 | 0.698 / 0.728 / 0.748 |
| highband | 3 | 3 | 0 | 0.955 / 0.965 / 0.974 |
| late | 3 | 3 | 0 | 0.556 / 0.621 / 0.714 |
| late_high | 3 | 3 | 0 | 0.536 / 0.625 / 0.699 |
| veryhigh | 3 | 3 | 0 | 1.265 / 1.290 / 1.323 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 3 | 3 | weak=1, moderate=2 | 0 / 0 / 0 |
| early_high | 3 | 3 | weak=3 | 0 / 0 / 0 |
| highband | 3 | 3 | weak=1, moderate=2 | 0 / 0 / 0 |
| late | 3 | 3 | weak=3 | 0 / 0 / 0.25 |
| late_high | 3 | 3 | weak=3 | 0 / 0 / 0 |
| veryhigh | 3 | 3 | moderate=3 | 0 / 0 / 0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2058x1005 px, dynamic range 255, grayscale std 71.6576
```

## 521: Seed13 Target-2 Ringdown Objective Sweep

Output:

```text
outputs/experiments/521_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 510, but replication case source_mismatch_ringdown025_noise10_seed13.
target index 2 only, z offsets -1:0:1 from z=120 mm, radius offsets -1:0:0.25
from r=8 mm, and top-k 10.
```

Runtime:

```text
323.7 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-2 point: x=350 mm, z=120 mm, r=8.0 mm
next radius: 7.25 mm
radius margin: 8.106e-04
confidence label: moderate
ambiguity interval: x=350 mm, z=120 mm, r=8.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.0992
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2490
fitted combined source_ringdown_coefficient column: 0.2737
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 350 / 120 / 8.0 | 7.25 | 8.106e-04 | 1.000 | moderate | 8.0 |
| highband | 350 / 120 / 8.0 | 7.25 | 8.677e-04 | 1.070 | moderate | 8.0 |
| late | 350 / 120 / 8.0 | 7.25 | 1.203e-03 | 1.484 | strong | 8.0 |
| late_high | 350 / 120 / 8.0 | 7.25 | 1.310e-03 | 1.616 | strong | 8.0 |
| veryhigh | 350 / 120 / 8.0 | 7.25 | 1.137e-03 | 1.403 | strong | 8.0 |
| early_high | 350 / 120 / 8.0 | 7.25 | 4.977e-04 | 0.614 | weak | 8.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 72.6259
```

## 522: Seed13 Target-2 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/522_variable_depth_radius_seed13_target2_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/521_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_seed13_target2_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/522_variable_depth_radius_seed13_target2_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
late_high margin ratio: 1.616x
late margin ratio: 1.484x
veryhigh margin ratio: 1.403x
late/late_high/veryhigh confidence labels: strong
base/highband confidence labels: moderate
early_high confidence label: weak
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2059x1005 px, dynamic range 255, grayscale std 74.8286
```

## 523: Seed34 Target-2 Ringdown Objective Sweep

Output:

```text
outputs/experiments/523_coordinate_optimizer_variable_depth_radius_seed34_target2_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 521, but replication case source_mismatch_ringdown025_noise10_seed34.
```

Runtime:

```text
325.5 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-2 point: x=350 mm, z=120 mm, r=8.0 mm
next radius: 7.25 mm
radius margin: 1.040e-03
confidence label: strong
ambiguity interval: x=350 mm, z=120 mm, r=8.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.0994
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2509
fitted combined source_ringdown_coefficient column: 0.2758
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 350 / 120 / 8.0 | 7.25 | 1.040e-03 | 1.000 | strong | 8.0 |
| highband | 350 / 120 / 8.0 | 7.25 | 1.109e-03 | 1.067 | strong | 8.0 |
| late | 350 / 120 / 8.0 | 7.25 | 1.635e-03 | 1.572 | strong | 8.0 |
| late_high | 350 / 120 / 8.0 | 7.25 | 1.715e-03 | 1.649 | strong | 8.0 |
| veryhigh | 350 / 120 / 8.0 | 7.25 | 1.325e-03 | 1.274 | strong | 8.0 |
| early_high | 350 / 120 / 8.0 | 7.25 | 6.280e-04 | 0.604 | moderate | 8.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 83.8665
```

## 524: Seed34 Target-2 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/524_variable_depth_radius_seed34_target2_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/523_coordinate_optimizer_variable_depth_radius_seed34_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_seed34_target2_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/524_variable_depth_radius_seed34_target2_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
late_high margin ratio: 1.649x
late margin ratio: 1.572x
veryhigh margin ratio: 1.274x
base/highband/late/late_high/veryhigh confidence labels: strong
early_high confidence label: moderate
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2059x1005 px, dynamic range 255, grayscale std 74.3584
```

## 525: Target-2 Three-Seed Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/525_variable_depth_radius_target2_three_seed_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/521_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/523_coordinate_optimizer_variable_depth_radius_seed34_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/510_coordinate_optimizer_variable_depth_radius_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_target2_three_seed_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/525_variable_depth_radius_target2_three_seed_txrx50_ringdown025_objective_confidence_report
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Ratio min/mean/max |
| --- | ---: | ---: | ---: | --- |
| early_high | 3 | 3 | 0 | 0.604 / 0.608 / 0.614 |
| highband | 3 | 3 | 0 | 1.038 / 1.058 / 1.070 |
| late | 3 | 3 | 0 | 1.484 / 1.522 / 1.572 |
| late_high | 3 | 3 | 0 | 1.559 / 1.608 / 1.649 |
| veryhigh | 3 | 3 | 0 | 1.274 / 1.325 / 1.403 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 3 | 3 | moderate=2, strong=1 | 0 / 0 / 0 |
| early_high | 3 | 3 | weak=1, moderate=2 | 0 / 0 / 0 |
| highband | 3 | 3 | moderate=2, strong=1 | 0 / 0 / 0 |
| late | 3 | 3 | strong=3 | 0 / 0 / 0 |
| late_high | 3 | 3 | strong=3 | 0 / 0 / 0 |
| veryhigh | 3 | 3 | strong=3 | 0 / 0 / 0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2058x1005 px, dynamic range 255, grayscale std 74.5585
```

## 526: Seed13 Target-1 Ringdown Objective Sweep

Output:

```text
outputs/experiments/526_coordinate_optimizer_variable_depth_radius_seed13_target1_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 512, but replication case source_mismatch_ringdown025_noise10_seed13.
target index 1 only, z offsets -1:1:1 from z=100 mm, radius offsets -1:1:0.25
from r=6 mm, and top-k 27.
```

Runtime:

```text
874.9 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-1 point: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
radius margin: 6.009e-04
confidence label: moderate
ambiguity interval: x=250 mm, z=100 mm, r=6.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.0992
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2490
fitted combined source_ringdown_coefficient column: 0.2737
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 250 / 100 / 6.0 | 6.25 | 6.009e-04 | 1.000 | moderate | 6.0 |
| highband | 250 / 100 / 6.0 | 6.25 | 6.039e-04 | 1.005 | moderate | 6.0 |
| late | 250 / 100 / 6.0 | 6.25 | 7.182e-04 | 1.195 | moderate | 6.0 |
| late_high | 250 / 100 / 6.0 | 6.25 | 7.513e-04 | 1.250 | moderate | 6.0 |
| veryhigh | 250 / 100 / 6.0 | 6.25 | 6.596e-04 | 1.098 | moderate | 6.0 |
| early_high | 250 / 100 / 6.0 | 6.25 | 3.608e-04 | 0.601 | weak | 6.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 68.4026
```

## 527: Seed13 Target-1 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/527_variable_depth_radius_seed13_target1_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/526_coordinate_optimizer_variable_depth_radius_seed13_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_seed13_target1_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/527_variable_depth_radius_seed13_target1_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
late_high margin ratio: 1.250x
late margin ratio: 1.195x
veryhigh margin ratio: 1.098x
base/highband/late/late_high/veryhigh confidence labels: moderate
early_high confidence label: weak
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2055x1005 px, dynamic range 255, grayscale std 76.2528
```

## 528: Seed34 Target-1 Ringdown Objective Sweep

Output:

```text
outputs/experiments/528_coordinate_optimizer_variable_depth_radius_seed34_target1_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 526, but replication case source_mismatch_ringdown025_noise10_seed34.
target index 1 only, z offsets -1:1:1 from z=100 mm, radius offsets -1:1:0.25
from r=6 mm, and top-k 27.
```

Runtime:

```text
884.6 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-1 point: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
radius margin: 6.002e-04
confidence label: moderate
ambiguity interval: x=250 mm, z=100 mm, r=6.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.0994
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2509
fitted combined source_ringdown_coefficient column: 0.2758
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 250 / 100 / 6.0 | 6.25 | 6.002e-04 | 1.000 | moderate | 6.0 |
| highband | 250 / 100 / 6.0 | 6.25 | 6.112e-04 | 1.018 | moderate | 6.0 |
| late | 250 / 100 / 6.0 | 6.25 | 7.889e-04 | 1.314 | moderate | 6.0 |
| late_high | 250 / 100 / 6.0 | 6.25 | 8.663e-04 | 1.443 | moderate | 6.0 |
| veryhigh | 250 / 100 / 6.0 | 6.25 | 6.444e-04 | 1.074 | moderate | 6.0 |
| early_high | 250 / 100 / 6.0 | 6.25 | 3.474e-04 | 0.579 | weak | 6.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 68.4036
```

## 529: Seed34 Target-1 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/529_variable_depth_radius_seed34_target1_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/528_coordinate_optimizer_variable_depth_radius_seed34_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_seed34_target1_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/529_variable_depth_radius_seed34_target1_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
late_high margin ratio: 1.443x
late margin ratio: 1.314x
veryhigh margin ratio: 1.074x
base/highband/late/late_high/veryhigh confidence labels: moderate
early_high confidence label: weak
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2055x1005 px, dynamic range 255, grayscale std 74.5189
```

## 530: Target-1 Three-Seed Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/530_variable_depth_radius_target1_three_seed_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/526_coordinate_optimizer_variable_depth_radius_seed13_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/528_coordinate_optimizer_variable_depth_radius_seed34_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/512_coordinate_optimizer_variable_depth_radius_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_target1_three_seed_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/530_variable_depth_radius_target1_three_seed_txrx50_ringdown025_objective_confidence_report
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Ratio min/mean/max |
| --- | ---: | ---: | ---: | --- |
| early_high | 3 | 3 | 0 | 0.579 / 0.599 / 0.618 |
| highband | 3 | 3 | 0 | 1.005 / 1.023 / 1.046 |
| late | 3 | 3 | 0 | 1.146 / 1.219 / 1.314 |
| late_high | 3 | 3 | 0 | 1.250 / 1.338 / 1.443 |
| veryhigh | 3 | 3 | 0 | 1.058 / 1.077 / 1.098 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 3 | 3 | moderate=3 | 0 / 0 / 0 |
| early_high | 3 | 3 | weak=3 | 0 / 0 / 0 |
| highband | 3 | 3 | moderate=3 | 0 / 0 / 0 |
| late | 3 | 3 | moderate=3 | 0 / 0 / 0 |
| late_high | 3 | 3 | moderate=3 | 0 / 0 / 0 |
| veryhigh | 3 | 3 | moderate=3 | 0 / 0 / 0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2058x1005 px, dynamic range 255, grayscale std 74.1161
```

## 531: All-Target Three-Seed Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/531_variable_depth_radius_all_targets_three_seed_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/515_coordinate_optimizer_variable_depth_radius_seed13_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/518_coordinate_optimizer_variable_depth_radius_seed34_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/526_coordinate_optimizer_variable_depth_radius_seed13_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/528_coordinate_optimizer_variable_depth_radius_seed34_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/512_coordinate_optimizer_variable_depth_radius_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/521_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/523_coordinate_optimizer_variable_depth_radius_seed34_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/510_coordinate_optimizer_variable_depth_radius_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_all_targets_three_seed_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/531_variable_depth_radius_all_targets_three_seed_txrx50_ringdown025_objective_confidence_report
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Ratio min/mean/max |
| --- | ---: | ---: | ---: | --- |
| early_high | 9 | 9 | 0 | 0.579 / 0.645 / 0.748 |
| highband | 9 | 9 | 0 | 0.955 / 1.015 / 1.070 |
| late | 9 | 9 | 0 | 0.556 / 1.120 / 1.572 |
| late_high | 9 | 9 | 0 | 0.536 / 1.190 / 1.649 |
| veryhigh | 9 | 9 | 0 | 1.058 / 1.231 / 1.403 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 9 | 9 | weak=1, moderate=7, strong=1 | 0 / 0 / 0 |
| early_high | 9 | 9 | weak=7, moderate=2 | 0 / 0 / 0 |
| highband | 9 | 9 | weak=1, moderate=7, strong=1 | 0 / 0 / 0 |
| late | 9 | 9 | weak=3, moderate=3, strong=3 | 0 / 0 / 0.25 |
| late_high | 9 | 9 | weak=3, moderate=3, strong=3 | 0 / 0 / 0 |
| veryhigh | 9 | 9 | moderate=6, strong=3 | 0 / 0 / 0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
4762x1005 px, dynamic range 255, grayscale std 73.2677
```

## Interpretation

The three-seed target-0 replication passes the point-geometry guardrail and
strengthens the target-0 case for veryhigh:

```text
base: exact on all three rows, weak=1 and moderate=2
veryhigh: exact and moderate on all three rows
target-0 three-seed aggregate: veryhigh is the only diagnostic with consistent
margin improvement, ratio 1.265-1.323x.
```

This is a useful replication because seed13 was the weakest target-0 row in
the earlier Tx/Rx=50 final-state package, and it still becomes moderate under
the veryhigh diagnostic.

The first target-2 seed replication also passes:

```text
base: exact and moderate, margin 8.106e-04
late_high: exact and strong, margin 1.310e-03, ratio 1.616x
veryhigh: exact and strong, margin 1.137e-03, ratio 1.403x.
```

The target-2 three-seed replication is now closed:

```text
base: exact on all three rows, moderate=2 and strong=1
late_high: exact and strong on all three rows, ratio 1.559-1.649x
veryhigh: exact and strong on all three rows, ratio 1.274-1.403x.
```

The first target-1 seed replication passes:

```text
base: exact and moderate, margin 6.009e-04
late_high: exact and moderate, margin 7.513e-04, ratio 1.250x
veryhigh: exact and moderate, margin 6.596e-04, ratio 1.098x.
```

The target-1 three-seed replication is now closed:

```text
base: exact and moderate on all three rows
late_high: exact and moderate on all three rows, ratio 1.250-1.443x
veryhigh: exact and moderate on all three rows, ratio 1.058-1.098x.
```

The all-target fitted-ringdown package is also closed:

```text
base: exact on all nine target/seed rows, weak=1, moderate=7, strong=1
veryhigh: exact on all nine rows, moderate=6, strong=3, ratio 1.058-1.403x
late_high: largest mean ratio on targets 1 and 2, but weakens all target-0 rows.
```

Veryhigh is therefore the only tested diagnostic objective that improves every
row in the variable-depth/variable-radius Tx/Rx=50 fitted-ringdown branch. It
should still remain reporting evidence rather than a production update-rule
replacement because the older source-shape center-radius branch rejected the
same global promotion in experiment 62.

## Next Decision

The compact cross-condition objective-confidence report is completed in
experiment 65/run 532. Use that report to separate the base production update
rule from the veryhigh reporting diagnostic before scheduling additional GPU
sweeps.
