# Experiment 52: Coupled Multi-Rebar Source-Shape Coordinate Stress

## Goal

Move beyond fixed-neighbor local source-shape profiles.

Experiments 425-439 showed that one target at a time selects the true x/z/r
when the neighboring rebars stay fixed at truth. This tracker starts the next
question:

```text
If neighboring rebar radii are initially wrong and the coordinate optimizer
updates targets sequentially, does the source-shape coefficient-fit objective
still recover the true multi-rebar state?
```

## Implementation

Extended the reporting-first coordinate optimizer so it can reuse the
source-shape model that fixed the single-rebar and fixed-neighbor multi-rebar
ringdown cases:

```text
run_multi_rebar_coordinate_optimizer.py
inversion/candidate_confidence.py
tests/test_multi_rebar_coordinate_optimizer.py
tests/test_candidate_confidence.py
```

New coordinate-optimizer controls:

```text
--fit-ringdown-coefficient
--source-ringdown-delay-ps
--source-ringdown-frequency-scale
```

The coordinate confidence report now preserves fitted source-shape fields:

```text
source_ringdown_scale
source_ringdown_delay_ps
source_ringdown_frequency_scale
source_primary_coefficient
source_ringdown_coefficient
```

Validation after the implementation patch:

```text
44 passed in 0.37 s
```

## 440: Seed55 Coupled Compact Pass

Output:

```text
outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --initial-radius-values-mm 6.2,6.2,6.2 \
  --target-indices 1,0,2 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --update-case-label source_mismatch_ringdown025_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --top-k 12 \
  --progress-every 9 \
  --run-name multi_rebar_coupled_source_shape_seed55_compact_pass
```

Purpose:

```text
Start all three radii at 6.2 mm, then update center, left, right. The center
target is updated first so it is evaluated while both neighbors are wrong.
```

Runtime and count:

```text
2642.63 s
3 coordinate steps
27 candidates per step
1 observed source-mismatch/ringdown/noise case
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
```

State history:

| Step | Target | State radii before [mm] | Updated x/z/r [mm] | Margin | Label |
| ---: | ---: | --- | --- | ---: | --- |
| 1 | 1 | 6.2 / 6.2 / 6.2 | 250 / 90 / 6.0 | 1.228e-04 | weak |
| 2 | 0 | 6.2 / 6.0 / 6.2 | 150 / 90 / 6.0 | 2.948e-04 | weak |
| 3 | 2 | 6.0 / 6.0 / 6.2 | 350 / 90 / 6.0 | 2.185e-04 | weak |

Final state:

```text
x = [150.0, 250.0, 350.0] mm
z = [90.0, 90.0, 90.0] mm
r = [6.0, 6.0, 6.0] mm
```

Source-shape recovery:

| Target | Fitted fc scale | Fitted shift [ps] | Fitted ringdown scale | Ringdown coefficient |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1.1 | -50 | 0.2510 | 0.2748 |
| 0 | 1.1 | -50 | 0.2505 | 0.2753 |
| 2 | 1.1 | -50 | 0.2503 | 0.2756 |

Top-candidate pattern:

```text
All three coordinate steps ranked true r=6.0 first and r=6.2 second at true
x/z. The ambiguity interval is therefore a local 6.0-6.2 mm radius interval,
not a shifted-location or high-radius branch.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1545x903 px, dynamic range 255, grayscale std 51.2725
```

Figure notes:

```text
outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass/figures/FIGURE_NOTES.md
```

## 441: Seed55 Coupled X/Z/R-Perturbed Compact Pass

Output:

```text
outputs/experiments/441_multi_rebar_coupled_source_shape_seed55_xzr_perturbed_pass
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --initial-x-values-mm 149,251,349 \
  --initial-z-values-mm 91,89,91 \
  --initial-radius-values-mm 6.2,5.8,6.2 \
  --target-indices 1,0,2 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --update-case-label source_mismatch_ringdown025_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --top-k 12 \
  --progress-every 9 \
  --run-name multi_rebar_coupled_source_shape_seed55_xzr_perturbed_pass
```

Purpose:

```text
Start all three targets with x/z/r perturbations, then update center, left,
right. The center target is evaluated while both neighboring locations and
radii are still wrong.
```

Runtime and count:

```text
2546.98 s
3 coordinate steps
27 candidates per step
1 observed source-mismatch/ringdown/noise case
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
```

State history:

| Step | Target | State before | Updated x/z/r [mm] | Margin | Label |
| ---: | ---: | --- | --- | ---: | --- |
| 1 | 1 | x=149/251/349, z=91/89/91, r=6.2/5.8/6.2 | 250 / 90 / 6.0 | 1.346e-03 | strong |
| 2 | 0 | x=149/250/349, z=91/90/91, r=6.2/6.0/6.2 | 150 / 90 / 6.0 | 3.283e-04 | weak |
| 3 | 2 | x=150/250/349, z=90/90/91, r=6.0/6.0/6.2 | 350 / 90 / 6.0 | 2.185e-04 | weak |

Final state:

```text
x = [150.0, 250.0, 350.0] mm
z = [90.0, 90.0, 90.0] mm
r = [6.0, 6.0, 6.0] mm
```

Source-shape recovery:

| Target | Fitted fc scale | Fitted shift [ps] | Fitted ringdown scale | Ringdown coefficient |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1.1 | -50 | 0.2580 | 0.2834 |
| 0 | 1.1 | -50 | 0.2583 | 0.2826 |
| 2 | 1.1 | -50 | 0.2503 | 0.2756 |

Top-candidate pattern:

```text
All three coordinate steps ranked the true x/z/r first. The center target's
next distinct radius was r=5.6 at z=89 mm, outside the ambiguity interval.
The left and right targets still have local 6.0-6.2 mm radius ambiguity at
true x/z.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1545x903 px, dynamic range 255, grayscale std 64.3103
```

Figure notes:

```text
outputs/experiments/441_multi_rebar_coupled_source_shape_seed55_xzr_perturbed_pass/figures/FIGURE_NOTES.md
```

## 442: Coupled Seed55 Coordinate Aggregate

Output:

```text
outputs/experiments/442_multi_rebar_coupled_source_shape_seed55_coordinate_aggregate
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/441_multi_rebar_coupled_source_shape_seed55_xzr_perturbed_pass/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name multi_rebar_coupled_source_shape_seed55_coordinate_aggregate
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 6 |
| Truth geometry rows | 6 |
| Weak rows | 5 |
| Strong rows | 1 |
| Fallback warning rows | 5 |
| Minimum radius margin | 1.228e-04 |
| Mean radius margin | 4.215e-04 |
| Maximum radius margin | 1.346e-03 |
| Maximum x ambiguity width | 0.0 mm |
| Maximum z ambiguity width | 0.0 mm |
| Maximum radius ambiguity width | 0.2 mm |

Per-target summary:

| Target | Rows | Truth geometry rows | Confidence labels | Margin range |
| ---: | ---: | ---: | --- | --- |
| 0 | 2 | 2 | weak=2 | 2.948e-04 to 3.283e-04 |
| 1 | 2 | 2 | weak=1, strong=1 | 1.228e-04 to 1.346e-03 |
| 2 | 2 | 2 | weak=2 | 2.185e-04 to 2.185e-04 |

Plot validation:

```text
coordinate_confidence_aggregate.png:
1718x971 px, dynamic range 255, grayscale std 56.6893

coordinate_ambiguity_widths.png:
1718x971 px, dynamic range 255, grayscale std 45.5804
```

Figure notes:

```text
outputs/experiments/442_multi_rebar_coupled_source_shape_seed55_coordinate_aggregate/figures/FIGURE_NOTES.md
```

## 443: Independent Seed55 Coupled Order Replication

Output:

```text
outputs/experiments/443_multi_rebar_coupled_source_shape_seed55_xzr_order_replication
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --initial-x-values-mm 151,249,351 \
  --initial-z-values-mm 89,91,89 \
  --initial-radius-values-mm 5.8,6.2,5.8 \
  --target-indices 2,1,0 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --update-case-label source_mismatch_ringdown025_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --top-k 12 \
  --progress-every 9 \
  --run-name multi_rebar_coupled_source_shape_seed55_xzr_order_replication
```

Purpose:

```text
Replicate the coupled x/z/r-perturbed seed with the opposite perturbation
direction and reversed target order: right, center, left.
```

Runtime and count:

```text
2420.47 s
3 coordinate steps
27 candidates per step
1 observed source-mismatch/ringdown/noise case
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
```

State history:

| Step | Target | State before | Updated x/z/r [mm] | Margin | Label |
| ---: | ---: | --- | --- | ---: | --- |
| 1 | 2 | x=151/249/351, z=89/91/89, r=5.8/6.2/5.8 | 350 / 90 / 6.0 | 8.522e-04 | moderate |
| 2 | 1 | x=151/249/350, z=89/91/90, r=5.8/6.2/6.0 | 250 / 90 / 6.0 | 4.022e-04 | weak |
| 3 | 0 | x=151/250/350, z=89/90/90, r=5.8/6.0/6.0 | 150 / 90 / 6.0 | 1.399e-03 | strong |

Final state:

```text
x = [150.0, 250.0, 350.0] mm
z = [90.0, 90.0, 90.0] mm
r = [6.0, 6.0, 6.0] mm
```

Source-shape recovery:

| Target | Fitted fc scale | Fitted shift [ps] | Fitted ringdown scale | Ringdown coefficient |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 1.1 | -50 | 0.2604 | 0.2828 |
| 1 | 1.1 | -50 | 0.2538 | 0.2775 |
| 0 | 1.1 | -50 | 0.2503 | 0.2756 |

Top-candidate pattern:

```text
All three coordinate steps ranked true x/z/r first. The right target had a
5.6-6.0 mm ambiguity interval, the center had a 6.0-6.2 mm interval, and the
left target was strong with no radius interval expansion.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1545x903 px, dynamic range 255, grayscale std 68.5450
```

Figure notes:

```text
outputs/experiments/443_multi_rebar_coupled_source_shape_seed55_xzr_order_replication/figures/FIGURE_NOTES.md
```

## 444: Coupled Seed55 Coordinate Aggregate V2

Output:

```text
outputs/experiments/444_multi_rebar_coupled_source_shape_seed55_coordinate_aggregate_v2
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/441_multi_rebar_coupled_source_shape_seed55_xzr_perturbed_pass/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/443_multi_rebar_coupled_source_shape_seed55_xzr_order_replication/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name multi_rebar_coupled_source_shape_seed55_coordinate_aggregate_v2
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 9 |
| Truth geometry rows | 9 |
| Weak rows | 6 |
| Moderate rows | 1 |
| Strong rows | 2 |
| Fallback warning rows | 6 |
| Minimum radius margin | 1.228e-04 |
| Mean radius margin | 5.757e-04 |
| Maximum radius margin | 1.399e-03 |
| Maximum x ambiguity width | 0.0 mm |
| Maximum z ambiguity width | 1.0 mm |
| Maximum radius ambiguity width | 0.4 mm |

Per-target summary:

| Target | Rows | Truth geometry rows | Confidence labels | Margin range |
| ---: | ---: | ---: | --- | --- |
| 0 | 3 | 3 | weak=2, strong=1 | 2.948e-04 to 1.399e-03 |
| 1 | 3 | 3 | weak=2, strong=1 | 1.228e-04 to 1.346e-03 |
| 2 | 3 | 3 | weak=2, moderate=1 | 2.185e-04 to 8.522e-04 |

Plot validation:

```text
coordinate_confidence_aggregate.png:
1719x971 px, dynamic range 255, grayscale std 61.6773

coordinate_ambiguity_widths.png:
1719x971 px, dynamic range 255, grayscale std 41.1445
```

Figure notes:

```text
outputs/experiments/444_multi_rebar_coupled_source_shape_seed55_coordinate_aggregate_v2/figures/FIGURE_NOTES.md
```

## 445: Reversed-Order Two-Pass Compact Check

Output:

```text
outputs/experiments/445_multi_rebar_coupled_source_shape_seed55_xzr_order_two_pass
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --initial-x-values-mm 151,249,351 \
  --initial-z-values-mm 89,91,89 \
  --initial-radius-values-mm 5.8,6.2,5.8 \
  --target-indices 2,1,0 \
  --passes 2 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --update-case-label source_mismatch_ringdown025_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --top-k 12 \
  --progress-every 9 \
  --run-name multi_rebar_coupled_source_shape_seed55_xzr_order_two_pass
```

Runtime and count:

```text
4904.25 s
2 passes
6 coordinate steps
27 candidates per step
1 observed source-mismatch/ringdown/noise case
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
```

State and confidence result:

| Pass | Target | Updated x/z/r [mm] | Margin | Label | Note |
| ---: | ---: | --- | ---: | --- | --- |
| 0 | 2 | 350 / 90 / 6.0 | 8.522e-04 | moderate | reproduces 443 first step |
| 0 | 1 | 250 / 90 / 6.0 | 4.022e-04 | weak | reproduces 443 second step |
| 0 | 0 | 150 / 90 / 6.0 | 1.399e-03 | strong | reproduces 443 final step |
| 1 | 2 | 350 / 90 / 6.0 | 2.185e-04 | weak | stable, no drift |
| 1 | 1 | 250 / 90 / 6.0 | 1.006e-04 | weak | stable, weakest row |
| 1 | 0 | 150 / 90 / 6.0 | 3.456e-04 | weak | stable, no drift |

Final state:

```text
x = [150.0, 250.0, 350.0] mm
z = [90.0, 90.0, 90.0] mm
r = [6.0, 6.0, 6.0] mm
```

Interpretation:

```text
The second pass does not drift away from truth. It also does not remove the
weak radius intervals; once the whole state is true, the closest competitor is
again usually r=6.2 at true x/z.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 58.4517
```

Figure notes:

```text
outputs/experiments/445_multi_rebar_coupled_source_shape_seed55_xzr_order_two_pass/figures/FIGURE_NOTES.md
```

## 446: Coupled Seed55 Coordinate Aggregate V3

Output:

```text
outputs/experiments/446_multi_rebar_coupled_source_shape_seed55_coordinate_aggregate_v3
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/441_multi_rebar_coupled_source_shape_seed55_xzr_perturbed_pass/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/443_multi_rebar_coupled_source_shape_seed55_xzr_order_replication/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/445_multi_rebar_coupled_source_shape_seed55_xzr_order_two_pass/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name multi_rebar_coupled_source_shape_seed55_coordinate_aggregate_v3
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 15 |
| Truth geometry rows | 15 |
| Weak rows | 10 |
| Moderate rows | 2 |
| Strong rows | 3 |
| Fallback warning rows | 10 |
| Minimum radius margin | 1.006e-04 |
| Mean radius margin | 5.666e-04 |
| Maximum radius margin | 1.399e-03 |
| Maximum x ambiguity width | 0.0 mm |
| Maximum z ambiguity width | 1.0 mm |
| Maximum radius ambiguity width | 0.4 mm |

Per-target summary:

| Target | Rows | Truth geometry rows | Confidence labels | Margin range |
| ---: | ---: | ---: | --- | --- |
| 0 | 5 | 5 | weak=3, strong=2 | 2.948e-04 to 1.399e-03 |
| 1 | 5 | 5 | weak=4, strong=1 | 1.006e-04 to 1.346e-03 |
| 2 | 5 | 5 | weak=3, moderate=2 | 2.185e-04 to 8.522e-04 |

Plot validation:

```text
coordinate_confidence_aggregate.png:
1855x971 px, dynamic range 255, grayscale std 64.0147

coordinate_ambiguity_widths.png:
1855x971 px, dynamic range 255, grayscale std 46.1648
```

Figure notes:

```text
outputs/experiments/446_multi_rebar_coupled_source_shape_seed55_coordinate_aggregate_v3/figures/FIGURE_NOTES.md
```

## 447: True-State Center Radius Objective Diagnostic

Output:

```text
outputs/experiments/447_multi_rebar_coupled_source_shape_true_state_radius_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --initial-radius-values-mm 6.0,6.0,6.0 \
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0 \
  --radius-offsets-mm=-0.4:0.4:0.2 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --update-case-label source_mismatch_ringdown025_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --top-k 5 \
  --progress-every 1 \
  --run-name multi_rebar_coupled_source_shape_true_state_radius_objectives \
  --outdir outputs/experiments/447_multi_rebar_coupled_source_shape_true_state_radius_objectives
```

Purpose:

```text
Directly test the remaining weak center-target true-state radius interval.
The x/z state and neighboring radii are fixed at truth, and only the center
radius is swept from 5.6 to 6.4 mm. The objective diagnostics compare the base
window against the established highband reporting diagnostic.
```

Runtime and count:

```text
162.5 s
1 coordinate step
5 radius candidates
1 observed source-mismatch/ringdown/noise case
base and highband objective diagnostics
```

Result:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Relative margin | Geometry changed? |
| --- | --- | ---: | ---: | ---: | --- |
| base | 250 / 90 / 6.0 | 6.2 | 1.006e-04 | 1.586e-03 | no |
| highband | 250 / 90 / 6.0 | 6.2 | 1.146e-04 | 9.714e-02 | no |

Top-candidate pattern:

```text
Both objectives rank the same radius order: 6.0, 6.2, 6.4, 5.8, 5.6 mm.
Highband raises the absolute 6.0-vs-6.2 gap by only 1.139x relative to base.
The large highband relative margin mostly reflects the smaller highband
objective scale, not a collapsed physical interval.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 42.1151
```

Figure notes:

```text
outputs/experiments/447_multi_rebar_coupled_source_shape_true_state_radius_objectives/figures/FIGURE_NOTES.md
```

## 448: Objective Diagnostic Report for 447

Output:

```text
outputs/experiments/448_coordinate_objective_diagnostic_report_447
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/447_multi_rebar_coupled_source_shape_true_state_radius_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name coordinate_objective_diagnostic_report_447
```

Aggregate result:

| Objective | Rows | Truth rows | Geometry changes | Margin ratio vs base |
| --- | ---: | ---: | ---: | ---: |
| highband | 1 | 1 | 0 | 1.139 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2059x1005 px, dynamic range 255, grayscale std 81.3671
```

Figure notes:

```text
outputs/experiments/448_coordinate_objective_diagnostic_report_447/figures/FIGURE_NOTES.md
```

## Interpretation

Experiment 440 is the first coupled-neighbor source-shape pass. It starts with
all three radii wrong at 6.2 mm and recovers the exact true all-target state in
one sequential coordinate pass.

Experiment 441 is a harder coupled-neighbor pass because all three targets
start with x/z/r perturbations. It also recovers the exact true all-target
state in one sequential coordinate pass. The center correction is especially
important because it happens while both neighboring targets still have wrong
x/z/r states.

The important caveat is confidence, not point accuracy. All three rows are
weak in 440 because r=6.2 mm remains close to r=6.0 mm. In 441, the center
row becomes strong, while the left and right rows remain weak with 6.0-6.2 mm
radius intervals. This means the coupled source-shape branch is point-correct
for these compact passes, but edge-target radii still need interval reporting.

Experiment 442 packages that interpretation across both coupled runs: 6/6 rows
are true geometry, no row has x/z ambiguity, and the only aggregate ambiguity
is a 0.2 mm radius interval. The weakest row is still the center target in
run 440, where the point estimate is correct but r=6.2 is close.

Experiment 443 independently replicates the harder coupled pass with reversed
perturbation direction and target order. It also recovers exact true geometry
in every step. Confidence improves relative to 440-441: one row is weak, one
is moderate, and one is strong.

Experiment 444 updates the coupled aggregate with run 443. Across all nine
coupled rows, every row is true geometry and no row has lateral x ambiguity.
The largest remaining ambiguity is a 1 mm z interval and a 0.4 mm radius
interval from the reversed-order right-target row. That is still an interval
reporting issue rather than a point-estimate failure.

Experiment 445 proves the compact two-pass update is point-stable. The second
pass starts from the true state and stays at the true state for all targets.
It does not narrow the weakest interval; the center second-pass row reaches the
known weak margin of 1.006e-04 against r=6.2 at true x/z.

Experiment 446 packages all coupled rows to date. Across 15 rows, every row is
true geometry and no row has x ambiguity. The coupled source-shape branch is
therefore stable for compact coordinate updates, but radius sizing still needs
confidence labels and ambiguity intervals.

Experiments 447-448 directly test the known weakest true-state center radius
row. The highband diagnostic preserves the correct 6.0 mm branch and modestly
increases the absolute best-vs-6.2 mm gap, but only by 1.139x. That is
diagnostic support for the selected branch, not enough evidence to replace the
6.0-6.2 mm ambiguity interval with a high-precision point-radius claim.

## Next Decision

Run one of these, in order of value:

```text
1. Do not run a full dense coupled Stage 4C source-shape sweep yet; 447-448
   show the weakest ambiguity is a true-state 6.0-6.2 mm interval, not an
   undiscovered high-radius or shifted-location branch.
2. Do not repeat base/highband true-state center diagnostics unless a new
   objective or physics lever changes the evidence; the current highband gain
   is too small to change the reporting decision.
3. If continuing source-shape work, move to a different lever such as material
   perturbation tied to the known radius interval, or keep the source-shape
   branch as interval-supported and advance a non-source multi-rebar branch.
```

Follow-up:

```text
Experiment 53 ran that material-profile branch. It did not collapse the
6.0-6.2 mm interval, so the source-shape/material result remains
interval-supported.
```
