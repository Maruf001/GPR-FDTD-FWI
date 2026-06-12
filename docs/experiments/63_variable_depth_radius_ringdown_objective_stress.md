# Experiment 63: Variable-Depth/Radius Ringdown Objective Stress

## Goal

Test whether the Tx/Rx=50 mm variable-depth/variable-radius objective package
survives coupled source-shape stress rows:

```text
target 0 endpoint at x=150 mm, z=80 mm, r=5 mm
target 1 center at x=250 mm, z=100 mm, r=6 mm
target 2 endpoint at x=350 mm, z=120 mm, r=8 mm
source_mismatch_ringdown025_noise10_seed55
fit source primary and ringdown coefficients
compare the same diagnostic objective variants used in experiments 60-62
```

This is not a global source-shape transfer test. Experiment 62 already showed
that the veryhigh objective does not improve the older same-depth
source-shape center-radius interval. This experiment tests the newer
variable-depth/radius branch under fitted-ringdown rows.

Objective variants:

```text
base, highband, late, late_high, veryhigh, early_high
```

## 508: Target-0 Ringdown Objective Sweep

Output:

```text
outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --update-case-label source_mismatch_ringdown025_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives \
  --outdir outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives
```

Runtime:

```text
389.5 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-0 point: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
radius margin: 6.012e-04
confidence label: moderate
ambiguity interval: x=150 mm, z=80 mm, r=5.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.1026
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2503
fitted combined source_ringdown_coefficient column: 0.2760
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 150 / 80 / 5.0 | 5.25 | 6.012e-04 | 1.000 | moderate | 5.0 |
| highband | 150 / 80 / 5.0 | 5.25 | 5.800e-04 | 0.965 | moderate | 5.0 |
| late | 150 / 80 / 5.0 | 5.25 | 3.342e-04 | 0.556 | weak | 5.0-5.25 |
| late_high | 150 / 80 / 5.0 | 5.25 | 3.850e-04 | 0.640 | weak | 5.0 |
| veryhigh | 150 / 80 / 5.0 | 5.25 | 7.714e-04 | 1.283 | moderate | 5.0 |
| early_high | 150 / 80 / 5.0 | 5.25 | 4.194e-04 | 0.698 | weak | 5.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 68.4246
```

## 509: Target-0 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/509_variable_depth_radius_target0_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_target0_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/509_variable_depth_radius_target0_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
veryhigh margin ratio: 1.283x
highband margin ratio: 0.965x
late/later window variants reduce the margin on this case
base/highband/veryhigh confidence labels: moderate
late/late_high/early_high confidence labels: weak
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2055x1005 px, dynamic range 255, grayscale std 71.4260
```

## 510: Target-2 Ringdown Objective Sweep

Output:

```text
outputs/experiments/510_coordinate_optimizer_variable_depth_radius_target2_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 508, but target index 2 only, z offsets -1:0:1 from z=120 mm,
radius offsets -1:0:0.25 from r=8 mm, and top-k 10.
```

Runtime:

```text
326.0 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-2 point: x=350 mm, z=120 mm, r=8.0 mm
next radius: 7.25 mm
radius margin: 9.585e-04
confidence label: moderate
ambiguity interval: x=350 mm, z=120 mm, r=8.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.1026
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2503
fitted combined source_ringdown_coefficient column: 0.2760
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 350 / 120 / 8.0 | 7.25 | 9.585e-04 | 1.000 | moderate | 8.0 |
| highband | 350 / 120 / 8.0 | 7.25 | 9.950e-04 | 1.038 | moderate | 8.0 |
| late | 350 / 120 / 8.0 | 7.25 | 1.446e-03 | 1.508 | strong | 8.0 |
| late_high | 350 / 120 / 8.0 | 7.25 | 1.494e-03 | 1.559 | strong | 8.0 |
| veryhigh | 350 / 120 / 8.0 | 7.25 | 1.245e-03 | 1.299 | strong | 8.0 |
| early_high | 350 / 120 / 8.0 | 7.25 | 5.804e-04 | 0.606 | moderate | 8.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 72.6267
```

## 511: Target-2 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/511_variable_depth_radius_target2_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/510_coordinate_optimizer_variable_depth_radius_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_target2_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/511_variable_depth_radius_target2_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
late_high margin ratio: 1.559x
late margin ratio: 1.508x
veryhigh margin ratio: 1.299x
late, late_high, and veryhigh confidence labels: strong
base, highband, and early_high confidence labels: moderate
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2059x1005 px, dynamic range 255, grayscale std 74.9661
```

## 512: Target-1 Ringdown Objective Sweep

Output:

```text
outputs/experiments/512_coordinate_optimizer_variable_depth_radius_target1_txrx50_ringdown025_objectives
```

Command pattern:

```text
same as run 508, but target index 1 only, z offsets -1:1:1 from z=100 mm,
radius offsets -1:1:0.25 from r=6 mm, and top-k 27.
```

Runtime:

```text
882.6 s
```

Base result:

```text
final x=[150,250,350] mm
final z=[80,100,120] mm
final r=[5,6,8] mm
best target-1 point: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
radius margin: 6.209e-04
confidence label: moderate
ambiguity interval: x=250 mm, z=100 mm, r=6.0 mm
```

Fitted source coefficients:

```text
injected source amplitude scale: 1.10
fitted primary coefficient: 1.1026
injected ringdown scale: 0.25
fitted direct ringdown scale: 0.2503
fitted combined source_ringdown_coefficient column: 0.2760
```

Objective-specific confidence rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 250 / 100 / 6.0 | 6.25 | 6.209e-04 | 1.000 | moderate | 6.0 |
| highband | 250 / 100 / 6.0 | 6.25 | 6.493e-04 | 1.046 | moderate | 6.0 |
| late | 250 / 100 / 6.0 | 6.25 | 7.117e-04 | 1.146 | moderate | 6.0 |
| late_high | 250 / 100 / 6.0 | 6.25 | 8.189e-04 | 1.319 | moderate | 6.0 |
| veryhigh | 250 / 100 / 6.0 | 6.25 | 6.572e-04 | 1.058 | moderate | 6.0 |
| early_high | 250 / 100 / 6.0 | 6.25 | 3.839e-04 | 0.618 | weak | 6.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 68.9804
```

## 513: Target-1 Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/513_variable_depth_radius_target1_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/512_coordinate_optimizer_variable_depth_radius_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_target1_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/513_variable_depth_radius_target1_txrx50_ringdown025_objective_confidence_report
```

Report result:

```text
diagnostic ratio rows: 5
all diagnostic variants preserve truth geometry
late_high margin ratio: 1.319x
late margin ratio: 1.146x
veryhigh margin ratio: 1.058x
early_high margin ratio: 0.618x
base/highband/late/late_high/veryhigh confidence labels: moderate
early_high confidence label: weak
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2055x1005 px, dynamic range 255, grayscale std 75.4044
```

## 514: All-Target Ringdown Objective Confidence Report

Output:

```text
outputs/experiments/514_variable_depth_radius_all_targets_txrx50_ringdown025_objective_confidence_report
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/512_coordinate_optimizer_variable_depth_radius_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/510_coordinate_optimizer_variable_depth_radius_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_all_targets_txrx50_ringdown025_objective_confidence_report \
  --outdir outputs/experiments/514_variable_depth_radius_all_targets_txrx50_ringdown025_objective_confidence_report
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Ratio min/mean/max |
| --- | ---: | ---: | ---: | --- |
| early_high | 3 | 3 | 0 | 0.606 / 0.640 / 0.698 |
| highband | 3 | 3 | 0 | 0.965 / 1.016 / 1.046 |
| late | 3 | 3 | 0 | 0.556 / 1.070 / 1.508 |
| late_high | 3 | 3 | 0 | 0.640 / 1.173 / 1.559 |
| veryhigh | 3 | 3 | 0 | 1.058 / 1.213 / 1.299 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 3 | 3 | moderate=3 | 0 / 0 / 0 |
| early_high | 3 | 3 | weak=2, moderate=1 | 0 / 0 / 0 |
| highband | 3 | 3 | moderate=3 | 0 / 0 / 0 |
| late | 3 | 3 | weak=1, moderate=1, strong=1 | 0 / 0 / 0.25 |
| late_high | 3 | 3 | weak=1, moderate=1, strong=1 | 0 / 0 / 0 |
| veryhigh | 3 | 3 | moderate=2, strong=1 | 0 / 0 / 0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2058x1005 px, dynamic range 255, grayscale std 72.2196
```

Figure notes:

```text
outputs/experiments/508_coordinate_optimizer_variable_depth_radius_target0_txrx50_ringdown025_objectives/figures/FIGURE_NOTES.md
outputs/experiments/509_variable_depth_radius_target0_txrx50_ringdown025_objective_confidence_report/figures/FIGURE_NOTES.md
outputs/experiments/510_coordinate_optimizer_variable_depth_radius_target2_txrx50_ringdown025_objectives/figures/FIGURE_NOTES.md
outputs/experiments/511_variable_depth_radius_target2_txrx50_ringdown025_objective_confidence_report/figures/FIGURE_NOTES.md
outputs/experiments/512_coordinate_optimizer_variable_depth_radius_target1_txrx50_ringdown025_objectives/figures/FIGURE_NOTES.md
outputs/experiments/513_variable_depth_radius_target1_txrx50_ringdown025_objective_confidence_report/figures/FIGURE_NOTES.md
outputs/experiments/514_variable_depth_radius_all_targets_txrx50_ringdown025_objective_confidence_report/figures/FIGURE_NOTES.md
```

## Interpretation

All three variable-depth/radius rows pass the fitted-ringdown stress:

```text
base recovers the exact x/z/r point and is already moderate on targets 0, 1,
and 2;
the fitted source coefficients recover the injected primary amplitude and
direct ringdown scale closely;
target 0: veryhigh is the best tested diagnostic objective at 1.283x;
target 1: late_high is best at 1.319x, and veryhigh is mildly helpful at 1.058x;
target 2: late_high is best at 1.559x, and veryhigh is still helpful at 1.299x;
all-target report: veryhigh is the only diagnostic with margin ratio >1 on
every target and zero x/z/r ambiguity width.
```

This differs from experiment 62. In the older same-depth source-shape center
case, veryhigh preserved truth but reduced the margin. Here, with
variable-depth/radius geometry and Tx/Rx=50 mm, veryhigh improves target-0
confidence under the ringdown stress. On targets 1 and 2, late_high is
stronger. The correct conclusion is branch-specific support, not global
promotion or a single universal objective window.

## Next Decision

Do not change the production update rule from this single-seed guardrail. The
next bounded GPU step is seed replication of the same fitted-ringdown stress,
starting with the more sensitive target 0 on another noise seed.
