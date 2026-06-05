# Experiment 51: Multi-Rebar Source-Shape Basis Fit

## Goal

Carry the single-rebar source-shape calibration result into the smallest useful
multi-rebar local geometry test.

The single-rebar branch showed:

```text
421: no modeled ringdown -> delayed source ringing can select r=7.8 mm
424: primary/ringdown coefficient fit -> all tested ringdown rows recover r=6.0 mm
```

This experiment asks whether the coefficient-fit source profile still behaves
sensibly when other rebars are present.

## Code Change

Extended `run_multi_rebar_local_geometry_profile.py` with:

```text
--fit-ringdown-coefficient
--source-ringdown-delay-ps
--source-ringdown-frequency-scale
```

The runner now simulates primary and delayed-ringdown source bases for each
modeled source frequency scale, then fits the source coefficients in trace
space using `inversion.source_profile.source_profiled_ls_over_basis_profiles`.

Also updated multi-rebar CSV summaries to include:

```text
source_ringdown_scale
source_primary_coefficient
source_ringdown_coefficient
```

`run_multi_rebar_common_radius_profile.build_observed_cases` now preserves the
ringdown fields parsed from the eight-value replication-case format.

Focused validation before GPU:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_multi_rebar_local_geometry_profile.py \
  tests/test_source_profile.py \
  tests/test_source_profiled_polish_runner.py \
  tests/test_source_profiled_replication_runner.py

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_multi_rebar_local_geometry_profile.py \
  run_multi_rebar_common_radius_profile.py \
  inversion/source_profile.py \
  run_single_rebar_source_profiled_polish.py \
  run_single_rebar_source_profiled_replication.py
```

Result:

```text
41 passed in 0.33 s
py_compile passed
```

## 425: Narrow Left-Rebar Multi-Rebar Source-Shape Gate

Output:

```text
outputs/experiments/425_multi_rebar_left_source_shape_basis_fit_narrow
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 0 \
  --target-x-values-mm 150.0 \
  --target-z-values-mm 90.0 \
  --target-radius-values-mm 5.8,6.0,6.2,7.4,7.8 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise05_seed21:1.0,0.0,1.0,0.05,21,0.25,180.0,0.8|source_mismatch_ringdown025:1.1,-50.0,1.1,0.0,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 1 \
  --run-name multi_rebar_left_source_shape_basis_fit_narrow
```

Runtime and count:

```text
5 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
161.32 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 150 / 90 / 6.0 | 6.2 | 3.734e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 150 / 90 / 6.0 | 6.2 | 2.936e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former single-rebar failure mode |
| ringdown025_noise05_seed21 | 150 / 90 / 6.0 | 6.2 | 3.178e-04 | fc=1.0, shift=0 ps, ringdown=0.251 | correct noisy ringdown |
| source_mismatch_ringdown025 | 150 / 90 / 6.0 | 6.2 | 3.121e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct combined source mismatch/ringdown |

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 34.9028

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 33.9995
```

Figure notes:

```text
outputs/experiments/425_multi_rebar_left_source_shape_basis_fit_narrow/figures/FIGURE_NOTES.md
```

## 426: Compact Left-Rebar X/Z/R Source-Shape Gate

Output:

```text
outputs/experiments/426_multi_rebar_left_source_shape_basis_fit_compact_xzr
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 0 \
  --target-x-values-mm 149:151:1 \
  --target-z-values-mm 89:91:1 \
  --target-radius-values-mm 5.8,6.0,6.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise05_seed21:1.0,0.0,1.0,0.05,21,0.25,180.0,0.8|source_mismatch_ringdown025:1.1,-50.0,1.1,0.0,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 3 \
  --run-name multi_rebar_left_source_shape_basis_fit_compact_xzr
```

Runtime and count:

```text
27 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
880.56 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 150 / 90 / 6.0 | 6.2 | 3.734e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 150 / 90 / 6.0 | 6.2 | 2.936e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former single-rebar failure mode |
| ringdown025_noise05_seed21 | 150 / 90 / 6.0 | 6.2 | 3.178e-04 | fc=1.0, shift=0 ps, ringdown=0.251 | correct noisy ringdown |
| source_mismatch_ringdown025 | 150 / 90 / 6.0 | 6.2 | 3.121e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct combined source mismatch/ringdown |

The top competing candidate in all four rows was the adjacent r=6.2 mm
candidate at the true x/z location. The first shifted-location candidates were
worse than that, so this compact window did not expose a source-shape-driven
x/z drift branch.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 34.0556

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 34.7239
```

Figure notes:

```text
outputs/experiments/426_multi_rebar_left_source_shape_basis_fit_compact_xzr/figures/FIGURE_NOTES.md
```

## 427: Compact Center-Rebar X/Z/R Source-Shape Gate

Output:

```text
outputs/experiments/427_multi_rebar_center_source_shape_basis_fit_compact_xzr
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 249:251:1 \
  --target-z-values-mm 89:91:1 \
  --target-radius-values-mm 5.8,6.0,6.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise05_seed21:1.0,0.0,1.0,0.05,21,0.25,180.0,0.8|source_mismatch_ringdown025:1.1,-50.0,1.1,0.0,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 3 \
  --run-name multi_rebar_center_source_shape_basis_fit_compact_xzr
```

Runtime and count:

```text
27 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
873.29 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 250 / 90 / 6.0 | 6.2 | 4.137e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 250 / 90 / 6.0 | 6.2 | 3.194e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former single-rebar failure mode |
| ringdown025_noise05_seed21 | 250 / 90 / 6.0 | 6.2 | 2.353e-04 | fc=1.0, shift=0 ps, ringdown=0.251 | correct noisy ringdown, weakest margin so far |
| source_mismatch_ringdown025 | 250 / 90 / 6.0 | 6.2 | 3.327e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct combined source mismatch/ringdown |

The top competing candidate in all four rows was the adjacent r=6.2 mm
candidate at the true x/z location. Shifted x=249/251 mm candidates remained
behind the adjacent-radius competitor, including under source mismatch.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 34.2931

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 34.8143
```

Figure notes:

```text
outputs/experiments/427_multi_rebar_center_source_shape_basis_fit_compact_xzr/figures/FIGURE_NOTES.md
```

## 428: Compact Right-Rebar X/Z/R Source-Shape Gate

Output:

```text
outputs/experiments/428_multi_rebar_right_source_shape_basis_fit_compact_xzr
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 2 \
  --target-x-values-mm 349:351:1 \
  --target-z-values-mm 89:91:1 \
  --target-radius-values-mm 5.8,6.0,6.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise05_seed21:1.0,0.0,1.0,0.05,21,0.25,180.0,0.8|source_mismatch_ringdown025:1.1,-50.0,1.1,0.0,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 3 \
  --run-name multi_rebar_right_source_shape_basis_fit_compact_xzr
```

Runtime and count:

```text
27 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
877.31 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 350 / 90 / 6.0 | 6.2 | 3.657e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 350 / 90 / 6.0 | 6.2 | 2.843e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former single-rebar failure mode |
| ringdown025_noise05_seed21 | 350 / 90 / 6.0 | 6.2 | 2.446e-04 | fc=1.0, shift=0 ps, ringdown=0.251 | correct noisy ringdown |
| source_mismatch_ringdown025 | 350 / 90 / 6.0 | 6.2 | 2.929e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct combined source mismatch/ringdown |

The top competing candidate in all four rows was the adjacent r=6.2 mm
candidate at the true x/z location. Shifted x=349/351 mm candidates stayed
behind that adjacent-radius competitor.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 34.2527

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 34.7782
```

Figure notes:

```text
outputs/experiments/428_multi_rebar_right_source_shape_basis_fit_compact_xzr/figures/FIGURE_NOTES.md
```

## 429: Compact Center-Rebar Hard-Noise Source-Shape Stress

Output:

```text
outputs/experiments/429_multi_rebar_center_source_shape_basis_fit_hard_noise_compact_xzr
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 249:251:1 \
  --target-z-values-mm 89:91:1 \
  --target-radius-values-mm 5.8,6.0,6.2 \
  --replication-cases 'ringdown025_noise10_seed13:1.0,0.0,1.0,0.10,13,0.25,180.0,0.8|ringdown025_noise10_seed21:1.0,0.0,1.0,0.10,21,0.25,180.0,0.8|source_mismatch_ringdown025_noise05_seed21:1.1,-50.0,1.1,0.05,21,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 3 \
  --run-name multi_rebar_center_source_shape_basis_fit_hard_noise_compact_xzr
```

Runtime and count:

```text
27 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
881.69 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| ringdown025_noise10_seed13 | 250 / 90 / 6.0 | 6.2 | 2.079e-04 | fc=1.0, shift=0 ps, ringdown=0.250 | correct 10% noisy ringdown |
| ringdown025_noise10_seed21 | 250 / 90 / 6.0 | 6.2 | 1.813e-04 | fc=1.0, shift=0 ps, ringdown=0.252 | correct weakest margin |
| source_mismatch_ringdown025_noise05_seed21 | 250 / 90 / 6.0 | 6.2 | 3.201e-04 | fc=1.1, shift=-50 ps, ringdown=0.251 | correct source mismatch plus noise |
| source_mismatch_ringdown025_noise10_seed13 | 250 / 90 / 6.0 | 6.2 | 2.695e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct source mismatch plus 10% noise |

The top competing radius was again r=6.2 mm at the true x/z location. This
means the harder noise tightened the radius margin but did not turn the compact
center window into an x/z drift failure.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 35.2059

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 36.6925
```

Figure notes:

```text
outputs/experiments/429_multi_rebar_center_source_shape_basis_fit_hard_noise_compact_xzr/figures/FIGURE_NOTES.md
```

## 430: Compact Center-Rebar High-Radius Source-Shape Stress

Output:

```text
outputs/experiments/430_multi_rebar_center_source_shape_basis_fit_high_radius_compact_xzr
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 249:251:1 \
  --target-z-values-mm 89:91:1 \
  --target-radius-values-mm 5.8,6.0,6.2,7.4,7.8 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise10_seed21:1.0,0.0,1.0,0.10,21,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 5 \
  --run-name multi_rebar_center_source_shape_basis_fit_high_radius_compact_xzr
```

Runtime and count:

```text
45 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
1471.51 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 250 / 90 / 6.0 | 6.2 | 4.137e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 250 / 90 / 6.0 | 6.2 | 3.194e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former discrete-grid failure row |
| ringdown025_noise10_seed21 | 250 / 90 / 6.0 | 6.2 | 1.813e-04 | fc=1.0, shift=0 ps, ringdown=0.252 | correct weakest high-radius row |
| source_mismatch_ringdown025_noise10_seed13 | 250 / 90 / 6.0 | 6.2 | 2.695e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct source mismatch plus 10% noise |

The high-radius candidates r=7.4 and r=7.8 mm did not enter the top eight
candidates in any row. The closest branch remained r=6.2 mm at the true x/z
location.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 34.4552

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 34.4660
```

Figure notes:

```text
outputs/experiments/430_multi_rebar_center_source_shape_basis_fit_high_radius_compact_xzr/figures/FIGURE_NOTES.md
```

## 431: Wider Center-Rebar High-Radius X/Z Source-Shape Stress

Output:

```text
outputs/experiments/431_multi_rebar_center_source_shape_basis_fit_high_radius_wide_xz
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 248:252:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.8,6.0,6.2,7.4,7.8 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise10_seed21:1.0,0.0,1.0,0.10,21,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 10 \
  --run-name multi_rebar_center_source_shape_basis_fit_high_radius_wide_xz
```

Runtime and count:

```text
125 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
4075.72 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 250 / 90 / 6.0 | 6.2 | 4.137e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 250 / 90 / 6.0 | 6.2 | 3.194e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former discrete-grid failure row |
| ringdown025_noise10_seed21 | 250 / 90 / 6.0 | 6.2 | 1.813e-04 | fc=1.0, shift=0 ps, ringdown=0.252 | correct weakest wide-window row |
| source_mismatch_ringdown025_noise10_seed13 | 250 / 90 / 6.0 | 6.2 | 2.695e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct source mismatch plus 10% noise |

The nearest competitor remained r=6.2 mm at the true x/z location. High-radius
r=7.4 and r=7.8 candidates appeared around ranks 9-12, mostly at z=92 mm, but
they were not near-ties.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 34.2769

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 34.6816
```

Figure notes:

```text
outputs/experiments/431_multi_rebar_center_source_shape_basis_fit_high_radius_wide_xz/figures/FIGURE_NOTES.md
```

## 432: Dense Stage 4C Center-Rebar Source-Shape Radius Grid

Output:

```text
outputs/experiments/432_multi_rebar_center_source_shape_basis_fit_stage4c_dense_radius
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 248:252:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise10_seed21:1.0,0.0,1.0,0.10,21,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 25 \
  --run-name multi_rebar_center_source_shape_basis_fit_stage4c_dense_radius
```

Runtime and count:

```text
325 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
10526.32 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 250 / 90 / 6.0 | 6.2 | 4.137e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 250 / 90 / 6.0 | 6.2 | 3.194e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former discrete-grid failure row |
| ringdown025_noise10_seed21 | 250 / 90 / 6.0 | 6.2 | 1.813e-04 | fc=1.0, shift=0 ps, ringdown=0.252 | correct weakest dense-grid row |
| source_mismatch_ringdown025_noise10_seed13 | 250 / 90 / 6.0 | 6.2 | 2.695e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct source mismatch plus 10% noise |

The dense grid introduced a secondary shifted-depth branch around
z=91 mm, r=6.8-7.0 mm. It reached rank 3 in several rows, but stayed behind
the true geometry and the adjacent r=6.2 mm candidate at true x/z.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 33.8087

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 33.9736
```

Figure notes:

```text
outputs/experiments/432_multi_rebar_center_source_shape_basis_fit_stage4c_dense_radius/figures/FIGURE_NOTES.md
```

## 433: Dense Stage 4C Left-Rebar Source-Shape Radius Grid

Output:

```text
outputs/experiments/433_multi_rebar_left_source_shape_basis_fit_stage4c_dense_radius
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 0 \
  --target-x-values-mm 148:152:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise10_seed21:1.0,0.0,1.0,0.10,21,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 25 \
  --run-name multi_rebar_left_source_shape_basis_fit_stage4c_dense_radius
```

Runtime and count:

```text
325 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
10486.88 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 150 / 90 / 6.0 | 6.2 | 3.734e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 150 / 90 / 6.0 | 6.2 | 2.936e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former discrete-grid failure row |
| ringdown025_noise10_seed21 | 150 / 90 / 6.0 | 6.2 | 3.606e-04 | fc=1.0, shift=0 ps, ringdown=0.252 | correct 10% noisy ringdown |
| source_mismatch_ringdown025_noise10_seed13 | 150 / 90 / 6.0 | 6.2 | 2.675e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct source mismatch plus 10% noise |

As in the center dense run, a shifted-depth branch around z=91 mm and
r=6.8-7.0 mm appears in the top candidates, but it stays behind the true
geometry and the adjacent r=6.2 mm candidate at true x/z.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 33.8833

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 34.2919
```

Figure notes:

```text
outputs/experiments/433_multi_rebar_left_source_shape_basis_fit_stage4c_dense_radius/figures/FIGURE_NOTES.md
```

## 434: Dense Stage 4C Right-Rebar Source-Shape Radius Grid

Output:

```text
outputs/experiments/434_multi_rebar_right_source_shape_basis_fit_stage4c_dense_radius
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 2 \
  --target-x-values-mm 348:352:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown025_noise10_seed21:1.0,0.0,1.0,0.10,21,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 25 \
  --run-name multi_rebar_right_source_shape_basis_fit_stage4c_dense_radius
```

Runtime and count:

```text
325 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
10208.39 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| nominal | 350 / 90 / 6.0 | 6.2 | 3.657e-04 | fc=1.0, shift=0 ps, ringdown=0.000 | correct |
| ringdown020 | 350 / 90 / 6.0 | 6.2 | 2.843e-04 | fc=1.0, shift=0 ps, ringdown=0.200 | correct former discrete-grid failure row |
| ringdown025_noise10_seed21 | 350 / 90 / 6.0 | 6.2 | 2.288e-04 | fc=1.0, shift=0 ps, ringdown=0.252 | correct 10% noisy ringdown |
| source_mismatch_ringdown025_noise10_seed13 | 350 / 90 / 6.0 | 6.2 | 3.663e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct source mismatch plus 10% noise |

As in the center and left dense runs, a shifted-depth branch around z=91 mm and
r=6.8-7.0 mm appears in the top candidates, but it stays behind the true
geometry and the adjacent r=6.2 mm candidate at true x/z.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 33.7672

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 33.9993
```

Figure notes:

```text
outputs/experiments/434_multi_rebar_right_source_shape_basis_fit_stage4c_dense_radius/figures/FIGURE_NOTES.md
```

## 435: Source-Shape Dense Synthesis

Output:

```text
outputs/experiments/435_multi_rebar_source_shape_dense_synthesis
```

Inputs:

```text
experiments 425-434
40 source-shape case rows
10 source-shape runs
```

Artifacts:

```text
data/source_shape_dense_synthesis_rows.csv
data/source_shape_dense_synthesis_summary.json
figures/source_shape_margin_timeline.png
figures/dense_stage4c_margin_heatmap.png
figures/FIGURE_NOTES.md
```

Synthesis result:

| Metric | Value |
| --- | --- |
| Truth geometry rows | 40 / 40 |
| Weakest all-row margin | 1.813e-04 |
| Weakest all-row case | experiment 429, center, ringdown025_noise10_seed21 |
| Weakest dense-grid margin | 1.813e-04 |
| Weakest dense-grid case | experiment 432, center, ringdown025_noise10_seed21 |
| Dense targets covered | left, center, right |

Interpretation:

```text
Runs 425-434 recover true geometry in every recorded source-shape row. The
weakest margin is the center target, ringdown025_noise10_seed21, with
radius_margin_abs=1.8134590293075736e-04. Dense Stage 4C runs show a secondary
z=91 mm / r=6.8-7.0 mm branch, but it remains below true r=6.0 and adjacent
r=6.2 at true x/z.
```

Plot validation:

```text
source_shape_margin_timeline.png:
2080x960 px, dynamic range 255, grayscale std 31.7068

dense_stage4c_margin_heatmap.png:
1920x768 px, dynamic range 255, grayscale std 48.8804
```

## 436: Compact Center-Rebar Hard-Noise Seed Replication

Output:

```text
outputs/experiments/436_multi_rebar_center_source_shape_seed_replication_compact_xzr
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 249:251:1 \
  --target-z-values-mm 89:91:1 \
  --target-radius-values-mm 5.8,6.0,6.2 \
  --replication-cases 'ringdown025_noise10_seed34:1.0,0.0,1.0,0.10,34,0.25,180.0,0.8|ringdown025_noise10_seed55:1.0,0.0,1.0,0.10,55,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed34:1.1,-50.0,1.1,0.10,34,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 3 \
  --run-name multi_rebar_center_source_shape_seed_replication_compact_xzr
```

Runtime and count:

```text
27 target candidates
4 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
849.33 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| ringdown025_noise10_seed34 | 250 / 90 / 6.0 | 6.2 | 2.719e-04 | fc=1.0, shift=0 ps, ringdown=0.252 | correct |
| ringdown025_noise10_seed55 | 250 / 90 / 6.0 | 6.2 | 2.741e-04 | fc=1.0, shift=0 ps, ringdown=0.251 | correct |
| source_mismatch_ringdown025_noise10_seed34 | 250 / 90 / 6.0 | 6.2 | 2.847e-04 | fc=1.1, shift=-50 ps, ringdown=0.251 | correct |
| source_mismatch_ringdown025_noise10_seed55 | 250 / 90 / 6.0 | 6.2 | 1.006e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct but new weakest margin |

The source-mismatch seed55 row is the new weakest source-shape result. Its top
two candidates are still r=6.0 and r=6.2 at true x/z, so this compact window
does not show location drift, but the margin is tight enough to justify a
wider/high-radius seed55 check.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 35.6081

multi_rebar_objective_variant_radius_profiles.png:
1855x2467 px, dynamic range 255, grayscale std 36.5885
```

Figure notes:

```text
outputs/experiments/436_multi_rebar_center_source_shape_seed_replication_compact_xzr/figures/FIGURE_NOTES.md
```

## 437: Center Seed55 High-Radius 5x5 X/Z Check

Output:

```text
outputs/experiments/437_multi_rebar_center_source_shape_seed55_high_radius_wide_xz
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 248:252:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.8,6.0,6.2,7.4,7.8 \
  --replication-cases 'ringdown025_noise10_seed55:1.0,0.0,1.0,0.10,55,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 10 \
  --run-name multi_rebar_center_source_shape_seed55_high_radius_wide_xz
```

Runtime and count:

```text
125 target candidates
2 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
4086.62 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| ringdown025_noise10_seed55 | 250 / 90 / 6.0 | 6.2 | 2.741e-04 | fc=1.0, shift=0 ps, ringdown=0.251 | correct |
| source_mismatch_ringdown025_noise10_seed55 | 250 / 90 / 6.0 | 6.2 | 1.006e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct but still weakest margin |

The sparse high-radius candidates r=7.4 and r=7.8 mm appear only around ranks
10-12, so they do not explain the weak seed55 margin. The dense r=6.8/7.0 mm
branch seen in experiments 432-434 remains the next seed55 check.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 31.9734

multi_rebar_objective_variant_radius_profiles.png:
1855x1243 px, dynamic range 255, grayscale std 36.8441
```

Figure notes:

```text
outputs/experiments/437_multi_rebar_center_source_shape_seed55_high_radius_wide_xz/figures/FIGURE_NOTES.md
```

## 438: Center Seed55 Dense Stage 4C Radius Check

Output:

```text
outputs/experiments/438_multi_rebar_center_source_shape_seed55_stage4c_dense_radius
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 248:252:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases 'ringdown025_noise10_seed55:1.0,0.0,1.0,0.10,55,0.25,180.0,0.8|source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --progress-every 25 \
  --run-name multi_rebar_center_source_shape_seed55_stage4c_dense_radius
```

Runtime and count:

```text
325 target candidates
2 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
10588.34 s
```

Result:

| Case | Best x/z/r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| ringdown025_noise10_seed55 | 250 / 90 / 6.0 | 6.2 | 2.741e-04 | fc=1.0, shift=0 ps, ringdown=0.251 | correct |
| source_mismatch_ringdown025_noise10_seed55 | 250 / 90 / 6.0 | 6.2 | 1.006e-04 | fc=1.1, shift=-50 ps, ringdown=0.250 | correct but weakest margin |

The dense z=91 mm, r=6.8-7.0 mm branch appears at ranks 3-4, but it remains
below the adjacent r=6.2 candidate at true x/z. The seed55 source-mismatch row
is therefore margin-weak but not a wrong-geometry or shifted-depth failure.

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png:
1617x920 px, dynamic range 255, grayscale std 31.3656

multi_rebar_objective_variant_radius_profiles.png:
1855x1243 px, dynamic range 255, grayscale std 36.1861
```

Figure notes:

```text
outputs/experiments/438_multi_rebar_center_source_shape_seed55_stage4c_dense_radius/figures/FIGURE_NOTES.md
```

## 439: Source-Shape Seed Synthesis

Output:

```text
outputs/experiments/439_multi_rebar_source_shape_seed_synthesis
```

Inputs:

```text
experiments 425-434, 436-438
48 source-shape case rows
13 source-shape runs
```

Artifacts:

```text
data/source_shape_seed_synthesis_rows.csv
data/source_shape_seed_synthesis_summary.json
figures/source_shape_seed_margin_timeline.png
figures/seed55_margin_heatmap.png
figures/FIGURE_NOTES.md
```

Synthesis result:

| Metric | Value |
| --- | --- |
| Truth geometry rows | 48 / 48 |
| Weakest all-row margin | 1.006e-04 |
| Weakest all-row case | experiment 436, center, source_mismatch_ringdown025_noise10_seed55 |
| Dense-grid rows | 14 |
| Seed55 rows | 6 |
| Dense seed55 conclusion | z=91 mm / r=6.8-7.0 mm branch stays secondary |

Interpretation:

```text
Runs 425-438 recover true geometry in every recorded source-shape row. The
weakest margin is the center source_mismatch_ringdown025_noise10_seed55 row,
with radius_margin_abs=1.0060989770306616e-04. Dense seed55 keeps the z=91 mm /
r=6.8-7.0 mm branch below true r=6.0 and adjacent r=6.2 at true x/z.
```

Plot validation:

```text
source_shape_seed_margin_timeline.png:
2240x1040 px, dynamic range 255, grayscale std 30.7522

seed55_margin_heatmap.png:
1760x768 px, dynamic range 255, grayscale std 50.1509
```

## Interpretation

This branch now has four passes.

It shows that source-basis coefficient fitting still recovers the true radius
when two neighboring rebars are present. The former single-rebar failure mode,
observed ringdown 0.20, is correctly handled in the multi-rebar left-target
center-target, and right-target scenes, and the fitted source coefficient
reports the expected ringdown scale.

Experiment 425 proved that at fixed x/z. Experiment 426 then allowed x, z, and
radius to move in a compact 27-candidate local window, and the true geometry
still ranked first in every tested source-shape case for the left target.
Experiment 427 repeated the compact window for the center target and again
ranked the true geometry first, with a weaker but still positive noisy-ringdown
margin of 2.353e-04. Experiment 428 repeated the compact window for the right
target and again ranked the true geometry first, with a weakest margin of
2.446e-04.

Experiment 429 then stressed the weakest center-target row with 10% noisy
ringdown and combined source-mismatch/noise cases. The true geometry still
ranked first in all four rows, but the weakest radius margin dropped to
1.813e-04.

Experiment 430 reintroduced the old high-radius failure candidates, r=7.4 and
r=7.8 mm, into the compact center window. They did not become top candidates;
the closest competitor stayed r=6.2 mm at the true x/z location.

Experiment 431 widened that high-radius center window from 3x3 to 5x5 in x/z.
The true geometry still ranked first in all rows. High-radius candidates
appeared only around ranks 9-12 and did not become near-ties.

Experiment 432 then ran the full dense Stage 4C radius grid for the center
target. The true geometry still ranked first in all rows. A shifted-depth
branch around z=91 mm and r=6.8-7.0 mm became visible in the top candidates,
but it stayed below the true r=6.0 and adjacent r=6.2 at true x/z.

Experiment 433 repeated the dense Stage 4C source-shape grid on the left
target. The true geometry again ranked first in all rows. The same shifted-depth
branch appeared, but it remained secondary.

Experiment 434 repeated the dense Stage 4C source-shape grid on the right
target. The true geometry again ranked first in all rows. The shifted-depth
z=91 mm, r=6.8-7.0 mm branch appeared again, but remained secondary.

Experiment 435 packaged the branch synthesis. Across 40 recorded rows from
experiments 425-434, every row selected the true target x/z/r. The weakest
margin is 1.813e-04 in the center target's ringdown025_noise10_seed21 row.

Experiment 436 replicated the hard center noise/source rows for seeds 34 and
55. All rows selected the true geometry. Seed55 under source mismatch produced
a new weakest margin, 1.006e-04, against r=6.2 at true x/z.

Experiment 437 widened the seed55 weak row to 5x5 x/z and sparse high-radius
candidates. The true geometry still ranked first; sparse high-radius candidates
did not become near-ties.

Experiment 438 ran the dense Stage 4C radius grid for seed55. The true geometry
again ranked first. The known z=91 mm, r=6.8-7.0 mm branch appeared at ranks
3-4, but stayed below r=6.2 at true x/z.

Experiment 439 updated the branch synthesis. Across 48 recorded rows from
experiments 425-434 and 436-438, every row selected the true target x/z/r. The
weakest result remains seed55 under source mismatch, with margin 1.006e-04
against r=6.2 at true x/z.

This is now a strong local multi-rebar source-shape validation for fixed
neighbor geometry. It is not yet a full coupled multi-rebar validation because
only one target was moved at a time while neighboring rebar geometries stayed
at truth.

## Next Decision

Scale one step, not many steps:

```text
move to coupled-neighbor geometry development or another explicitly new physics
stress. Do not spend more GPU time on fixed-neighbor source-shape replication
unless a new failure mode appears.
```

Follow-up:

```text
Experiment 52 / run 440 starts the coupled-neighbor source-shape coordinate
branch.
```
