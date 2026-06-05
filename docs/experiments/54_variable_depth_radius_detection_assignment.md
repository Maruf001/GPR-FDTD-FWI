# Experiment 54: Variable-Depth Variable-Radius Detection Assignment

## Goal

Start the next multi-rebar generalization branch without launching an
unbounded coordinate-FWI run.

Prior evidence covered:

```text
variable depth with equal radii: experiments 115, 210, 212, 214
same-depth variable radii: experiments 216-419
```

This experiment combines both:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
source mismatch + 10% noise, seed 13
```

The first decision gate is detector/assignment quality:

```text
Do the detector and assignment policy recover a physical three-seed set before
we spend GPU time on coordinate FWI?
```

## 451: Variable-Depth Variable-Radius Detector

Output:

```text
outputs/experiments/451_detection_multi_rebar_variable_depth_radius_source_mismatch_noise10
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_rebar_detection_pipeline.py \
  --backend gpu-cpml \
  --grid-step-mm 2.0 \
  --scan-step-mm 4.0 \
  --truth-x-values-mm 150,250,350 \
  --truth-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --frequency-scale 1.1 \
  --time-shift-ps -50 \
  --amplitude-scale 1.1 \
  --noise-fraction 0.10 \
  --noise-seed 13 \
  --detector-x-values-mm 80:420:4 \
  --detector-z-values-mm 60:145:5 \
  --detector-time-offset-ps-values 350,450,550,650,750 \
  --top-k 12 \
  --x-min-separation-mm 45 \
  --z-min-separation-mm 35 \
  --run-name detection_multi_rebar_variable_depth_radius_source_mismatch_noise10
```

Runtime:

```text
16.39 s
```

Top detector candidates:

| Rank | x [mm] | z [mm] | Normalized score | Note |
| ---: | ---: | ---: | ---: | --- |
| 1 | 248 | 100 | 0.925 | center truth within 2 mm x |
| 2 | 148 | 85 | 0.872 | left truth within 2 mm x, 5 mm z |
| 3 | 348 | 125 | 0.844 | right truth within 2 mm x, 5 mm z |
| 4 | 252 | 65 | 0.772 | false shallow center duplicate |
| 5 | 348 | 90 | 0.767 | false shallow right duplicate |

Truth-match result:

```text
All three truth points were within the configured detector tolerance.
```

Plot validation:

```text
detection_overlay.png:
1885x1209 px, dynamic range 255, grayscale std 45.4045
```

Figure notes:

```text
outputs/experiments/451_detection_multi_rebar_variable_depth_radius_source_mismatch_noise10/figures/FIGURE_NOTES.md
```

## 452: Assignment Report

Output:

```text
outputs/experiments/452_detection_assignment_variable_depth_radius_451
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_detection_assignment_report.py \
  outputs/experiments/451_detection_multi_rebar_variable_depth_radius_source_mismatch_noise10/data/detection_candidates.csv \
  --count 3 \
  --min-x-separation-mm 45 \
  --run-name detection_assignment_variable_depth_radius_451
```

Assigned seeds:

| Assigned order | Detector rank | x [mm] | z [mm] | Normalized score |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 2 | 148 | 85 | 0.872 |
| 1 | 1 | 248 | 100 | 0.925 |
| 2 | 3 | 348 | 125 | 0.844 |

Interpretation:

```text
The assignment policy selects the physical left/center/right seed set and
rejects the rank-4 shallow duplicate near the center x position.
```

Plot validation:

```text
detector_assignment.png:
1444x1005 px, dynamic range 255, grayscale std 37.5480
```

Figure notes:

```text
outputs/experiments/452_detection_assignment_variable_depth_radius_451/figures/FIGURE_NOTES.md
```

## 453: Assigned Coordinate Command Dry Run

Output:

```text
outputs/experiments/453_assigned_coordinate_command_variable_depth_radius_451
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_assigned_coordinate_command_report.py \
  outputs/experiments/451_detection_multi_rebar_variable_depth_radius_source_mismatch_noise10/data/detection_summary.json \
  --count 3 \
  --min-x-separation-mm 45 \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --noise-fraction 0.10 \
  --noise-seed 13 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 0,1,2 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=-5:1:1 \
  --radius-offsets-mm=-1:2:0.5 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --coordinate-run-name coordinate_optimizer_variable_depth_radius_from_assignment_seed13 \
  --run-name assigned_coordinate_command_variable_depth_radius_451
```

Packaged coordinate-FWI command:

```text
outputs/experiments/453_assigned_coordinate_command_variable_depth_radius_451/data/assigned_coordinate_command.txt
```

Important command fields:

```text
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: [148,248,348] / [85,100,125] / [6,6,6] mm
main x window: -2:2:1 mm
main z window: -5:1:1 mm
main radius window: -1:2:0.5 mm
guards: weak high-radius revisit and broad radius-ambiguity revisit
diagnostics: base and highband
launcher mode: dry_run
```

## 454-455: Location-Only Coordinate Stage

Wrapper output:

```text
outputs/experiments/454_assigned_coordinate_command_variable_depth_radius_location_only_451
```

Coordinate-FWI output:

```text
outputs/experiments/455_coordinate_optimizer_variable_depth_radius_location_only_seed13
```

Wrapper command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_assigned_coordinate_command_report.py \
  outputs/experiments/451_detection_multi_rebar_variable_depth_radius_source_mismatch_noise10/data/detection_summary.json \
  --count 3 \
  --min-x-separation-mm 45 \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --noise-fraction 0.10 \
  --noise-seed 13 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 0,1,2 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=-5:1:1 \
  --radius-offsets-mm=0 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 10 \
  --coordinate-run-name coordinate_optimizer_variable_depth_radius_location_only_seed13 \
  --coordinate-outdir outputs/experiments/455_coordinate_optimizer_variable_depth_radius_location_only_seed13 \
  --run-coordinate-fwi \
  --coordinate-log-mode file \
  --run-name assigned_coordinate_command_variable_depth_radius_location_only_451
```

Runtime:

```text
1723.0 s for the coordinate optimizer
```

Final coordinate state:

| Target | Truth x/z/r [mm] | Initial x/z/r [mm] | Final x/z/r [mm] | x/z error |
| ---: | --- | --- | --- | ---: |
| 0 | 150 / 80 / 5 | 148 / 85 / 6 | 149 / 81 / 6 | 1.41 mm |
| 1 | 250 / 100 / 6 | 248 / 100 / 6 | 250 / 100 / 6 | 0.00 mm |
| 2 | 350 / 120 / 8 | 348 / 125 / 6 | 349 / 120 / 6 | 1.00 mm |

Update-case objective diagnostics:

| Target | Base best x/z/r [mm] | Highband best x/z/r [mm] | Base competing geometry gap |
| ---: | --- | --- | ---: |
| 0 | 149 / 81 / 6 | 149 / 81 / 6 | 9.944e-04 |
| 1 | 250 / 100 / 6 | 250 / 100 / 6 | 2.128e-03 |
| 2 | 349 / 120 / 6 | 349 / 120 / 6 | 1.911e-03 |

Interpretation:

```text
The staged location-only coordinate step passes. Base and highband objectives
agree on all three x/z basins under source mismatch and 10% noise, even though
the radius is intentionally fixed at [6,6,6] mm.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 29.7661
```

Figure notes:

```text
outputs/experiments/455_coordinate_optimizer_variable_depth_radius_location_only_seed13/figures/FIGURE_NOTES.md
```

## 456: Focused Radius-Only Pass

Output:

```text
outputs/experiments/456_coordinate_optimizer_variable_depth_radius_radius_only_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 149,250,349 \
  --initial-z-values-mm 81,100,120 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 0,1,2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.1,13|source_mismatch_noise10_seed13:1.1,-50,1.1,0.1,13' \
  --update-case-label source_mismatch_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=0 \
  --revisit-z-offsets-mm=0 \
  --revisit-radius-step-mm 0.25 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_radius_only_seed13 \
  --outdir outputs/experiments/456_coordinate_optimizer_variable_depth_radius_radius_only_seed13
```

Runtime:

```text
338.3 s
```

Final state:

```text
x=[149,250,349] mm
z=[81,100,120] mm
r=[6,6,8] mm
```

Update-case radius rows:

| Target | Truth radius [mm] | Best radius [mm] | Next radius [mm] | Margin | Label |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 5.0 | 6.0 | 5.5 | 1.471e-03 | strong |
| 1 | 6.0 | 6.0 | 6.5 | 2.815e-03 | strong |
| 2 | 8.0 | 8.0 | 7.5 | 2.314e-03 | strong |

Interpretation:

```text
The first radius-only pass recovers the right/deep 8 mm bar and keeps the
center 6 mm bar. The left bar remains at 6 mm, but this row was evaluated
before the right bar was corrected from 6 to 8 mm, so it needs a second pass
before it can be interpreted as final radius evidence.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 76.8750
```

## 457: Second Radius-Only Pass

Output:

```text
outputs/experiments/457_coordinate_optimizer_variable_depth_radius_radius_second_pass_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 149,250,349 \
  --initial-z-values-mm 81,100,120 \
  --initial-radius-values-mm 6,6,8 \
  --target-indices 0,1,2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.1,13|source_mismatch_noise10_seed13:1.1,-50,1.1,0.1,13' \
  --update-case-label source_mismatch_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=0 \
  --revisit-z-offsets-mm=0 \
  --revisit-radius-step-mm 0.25 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_radius_second_pass_seed13 \
  --outdir outputs/experiments/457_coordinate_optimizer_variable_depth_radius_radius_second_pass_seed13
```

Runtime:

```text
389.1 s
```

Final state:

```text
x=[149,250,349] mm
z=[81,100,120] mm
r=[6,6,8] mm
```

Update-case radius rows:

| Step | Target | Truth radius [mm] | Best radius [mm] | Next radius [mm] | Margin | Label |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| main | 0 | 5.0 | 6.0 | 5.5 | 9.886e-04 | moderate |
| main | 1 | 6.0 | 6.0 | 5.5 | 4.142e-03 | strong |
| main | 2 | 8.0 | 8.0 | 7.5 | 2.314e-03 | strong |
| revisit | 0 | 5.0 | 6.0 | 5.75 | 8.431e-05 | weak |

Highband diagnostic:

```text
target 0 revisit: best r=6.0 mm, next r=5.75 mm, margin=6.994e-05
target 1 main: best r=6.0 mm, next r=5.5 mm, margin=3.749e-03
target 2 main: best r=8.0 mm, next r=7.5 mm, margin=2.168e-03
```

Interpretation:

```text
The center and right radii are stable after the second pass. The left radius
does not recover the true 5 mm point; after the target-0 revisit, 6.0 mm and
5.75 mm are nearly tied, and 5.5 mm remains inside the broad ambiguity set.
Report the left radius as interval-supported around 5.5-6.0 mm, not as a
point-correct estimate.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 64.8098
```

Figure notes:

```text
outputs/experiments/457_coordinate_optimizer_variable_depth_radius_radius_second_pass_seed13/figures/FIGURE_NOTES.md
```

## 458: Target-0 Seven-Source Radius Diagnostic

Output:

```text
outputs/experiments/458_coordinate_optimizer_variable_depth_radius_target0_radius_7source_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 149,250,349 \
  --initial-z-values-mm 81,100,120 \
  --initial-radius-values-mm 6,6,8 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0 \
  --radius-offsets-mm=-1.5:0.25:0.25 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.1,13|source_mismatch_noise10_seed13:1.1,-50,1.1,0.1,13' \
  --update-case-label source_mismatch_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=0 \
  --revisit-z-offsets-mm=0 \
  --revisit-radius-step-mm 0.125 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_target0_radius_7source_seed13 \
  --outdir outputs/experiments/458_coordinate_optimizer_variable_depth_radius_target0_radius_7source_seed13
```

Runtime:

```text
333.4 s
```

Seven-source scan positions:

```text
x=[50,114,178,250,314,378,450] mm
```

Final state:

```text
x=[149,250,349] mm
z=[81,100,120] mm
r=[5.875,6,8] mm
```

Update-case radius rows:

| Step | Best radius [mm] | Next radius [mm] | Margin | Label | Ambiguity interval |
| --- | ---: | ---: | ---: | --- | --- |
| main | 6.0 | 5.75 | 3.888e-04 | weak | 5.5-6.25 mm |
| revisit | 5.875 | 6.0 | 3.550e-04 | weak | 5.75-6.0 mm |

Highband diagnostic:

```text
main: best r=6.0 mm, next r=5.75 mm, margin=3.220e-04
revisit: best r=5.875 mm, next r=6.0 mm, margin=3.677e-04
```

Top update-case base candidates:

```text
main: r=6.0, 5.75, 6.25, 5.5, 5.25, 5.0
revisit: r=5.875, 6.0, 5.75, 6.125/6.25, 5.5/5.625
```

Interpretation:

```text
Seven sources move the weak target-0 interval inward from the 5-source
6.0-versus-5.75 near-tie to a 5.875 mm best point, but all rows remain weak
and the true 5.0 mm radius is still only rank 6 in the main objective. Extra
source count alone is not enough to promote target-0 radius as a point
recovery.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 61.4701
```

Figure notes:

```text
outputs/experiments/458_coordinate_optimizer_variable_depth_radius_target0_radius_7source_seed13/figures/FIGURE_NOTES.md
```

## 459: Target-0 Local x/z-Radius Coupling Diagnostic

Output:

```text
outputs/experiments/459_coordinate_optimizer_variable_depth_radius_target0_xz_radius_coupled_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 149,250,349 \
  --initial-z-values-mm 81,100,120 \
  --initial-radius-values-mm 6,6,8 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0:1:1 \
  --z-offsets-mm=-1:0:1 \
  --radius-offsets-mm=-1:0.25:0.25 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.1,13|source_mismatch_noise10_seed13:1.1,-50,1.1,0.1,13' \
  --update-case-label source_mismatch_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=0:1:1 \
  --revisit-z-offsets-mm=-1:0:1 \
  --revisit-radius-step-mm 0.125 \
  --progress-every 6 \
  --run-name coordinate_optimizer_variable_depth_radius_target0_xz_radius_coupled_seed13 \
  --outdir outputs/experiments/459_coordinate_optimizer_variable_depth_radius_target0_xz_radius_coupled_seed13
```

Runtime:

```text
586.6 s
```

Final state:

```text
x=[150,250,349] mm
z=[80,100,120] mm
r=[5,6,8] mm
```

Update-case rows:

| Step | Best x/z/r [mm] | Next radius [mm] | Radius margin | Confidence | Ambiguity interval |
| --- | --- | ---: | ---: | --- | --- |
| main | 150 / 80 / 5.0 | 5.25 | 5.104e-04 | moderate | x=149-150, z=80, r=5.0-5.25 |
| revisit | 150 / 80 / 5.0 | 5.125 | 5.104e-04 | moderate | x=150, z=80, r=5.0-5.25 |

Highband diagnostic:

```text
main: best x=150 mm, z=80 mm, r=5.0 mm, next r=5.25 mm, margin=4.453e-04
revisit: best x=150 mm, z=80 mm, r=5.0 mm, next r=5.125 mm, margin=4.453e-04
```

Top update-case base candidates:

```text
main:
1. x=150, z=80, r=5.0, J=0.087222550
2. x=150, z=80, r=5.25, J=0.087732957
3. x=149, z=80, r=5.0, J=0.087988887

revisit:
1. x=150, z=80, r=5.0, J=0.087222550
2. x=150, z=80, r=5.125, J=0.087732957
3. x=150, z=80, r=5.25, J=0.087732957
```

Interpretation:

```text
The left-radius miss was caused by residual x/z-radius coupling. Once target 0
is allowed to move from x/z=149/81 mm to the true x/z=150/80 mm, both base and
highband objectives recover the true r=5.0 mm. The result is still interval
aware, with r=5.0-5.25 mm, but the point best is now truth.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 63.8798
```

Figure notes:

```text
outputs/experiments/459_coordinate_optimizer_variable_depth_radius_target0_xz_radius_coupled_seed13/figures/FIGURE_NOTES.md
```

## 460: Target-2 Final x Polish

Output:

```text
outputs/experiments/460_coordinate_optimizer_variable_depth_radius_target2_x_polish_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,349 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=0:1:1 \
  --z-offsets-mm=0 \
  --radius-offsets-mm=0 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.1,13|source_mismatch_noise10_seed13:1.1,-50,1.1,0.1,13' \
  --update-case-label source_mismatch_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --progress-every 1 \
  --run-name coordinate_optimizer_variable_depth_radius_target2_x_polish_seed13 \
  --outdir outputs/experiments/460_coordinate_optimizer_variable_depth_radius_target2_x_polish_seed13
```

Runtime:

```text
32.3 s
```

Final state:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
```

Update-case geometry rows:

| Objective | Best x/z/r [mm] | Competing x/z/r [mm] | Misfit gap |
| --- | --- | --- | ---: |
| base | 350 / 120 / 8 | 349 / 120 / 8 | 2.672e-03 |
| highband | 350 / 120 / 8 | 349 / 120 / 8 | 2.421e-03 |

Interpretation:

```text
After target-0 local x/z-radius coupling corrected the left bar, a tiny
target-2 x polish closes the remaining right-target 1 mm offset. The staged
pipeline reaches the exact truth tuple x=[150,250,350], z=[80,100,120],
r=[5,6,8] under source mismatch and 10% noise.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 27.0401
```

Figure notes:

```text
outputs/experiments/460_coordinate_optimizer_variable_depth_radius_target2_x_polish_seed13/figures/FIGURE_NOTES.md
```

## 461: Staged Coordinate Confidence Summary

Output:

```text
outputs/experiments/461_variable_depth_radius_staged_coordinate_confidence_summary
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  outputs/experiments/455_coordinate_optimizer_variable_depth_radius_location_only_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/456_coordinate_optimizer_variable_depth_radius_radius_only_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/457_coordinate_optimizer_variable_depth_radius_radius_second_pass_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/458_coordinate_optimizer_variable_depth_radius_target0_radius_7source_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/459_coordinate_optimizer_variable_depth_radius_target0_xz_radius_coupled_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/460_coordinate_optimizer_variable_depth_radius_target2_x_polish_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name variable_depth_radius_staged_coordinate_confidence_summary \
  --outdir outputs/experiments/461_variable_depth_radius_staged_coordinate_confidence_summary
```

Aggregate metrics:

```text
rows: 30
truth-geometry rows: 11
confidence labels: missing=8, weak=8, moderate=3, strong=11
minimum radius margin: 8.431e-05
maximum x/z/r ambiguity widths: 2.0 / 1.0 / 0.75 mm
target-0 rows: 16, truth-geometry rows: 4, weakest radius margin: 8.431e-05
target-1 rows: 6, truth-geometry rows: 5, weakest radius margin: 1.835e-03
target-2 rows: 8, truth-geometry rows: 2, weakest radius margin: 1.347e-03
```

Interpretation:

```text
The aggregate intentionally includes intermediate staged rows, so the
truth-geometry count is not a final-success count. It is useful as a diagnostic
ledger: target 0 carries the weak/intermediate rows, while target 1 and target
2 are stable once their focused stages are reached.
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
3690x971 px, dynamic range 255, grayscale std 54.3035

coordinate_ambiguity_widths.png:
3690x971 px, dynamic range 255, grayscale std 43.1309
```

Figure notes:

```text
outputs/experiments/461_variable_depth_radius_staged_coordinate_confidence_summary/figures/FIGURE_NOTES.md
```

## Interpretation

The combined variable-depth/variable-radius staged gate now has a clearer
split result:

```text
detector and assignment recover the physical seed set;
location-only FWI recovers all three x/z basins within 1.5 mm;
focused radius passes recover center r=6 mm and right r=8 mm;
local target-0 x/z-radius coupling recovers the true left x/z/r point,
with a remaining radius interval of 5.0-5.25 mm;
target-2 x polish closes the final right-target 1 mm offset.
the coordinate confidence aggregate records the weak intermediate target-0
rows and the stable focused center/right rows.
```

This argues against launching the broad 453 all-parameter command as the next
step. The staged policy found the real limitation more cheaply and with better
diagnostic visibility. The final staged tuple is exact truth, but confidence
should still be reported with the observed local intervals.

## Next Decision

Do not run the full broad x/z/r command from 453 as the next step. The branch
now needs a CPU summary artifact and then one bounded seed replication, not a
larger search:

```text
summarize the staged path 451-460 with detector, assignment, location, radius,
and final-polish metrics;
replicate the staged policy on one new noise seed before promoting it as a
branch-level procedure;
keep broad all-parameter FWI deferred unless replication exposes a new failure
mode.
```
