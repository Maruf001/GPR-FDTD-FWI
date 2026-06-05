# Stage 9: Radius-Confidence Objective Matrix

## Motivation

The guarded coordinate optimizer now recovers the true final geometry for the
2 mm seed-offset stress runs, but confidence is still weak for edge rebar
radii. The clearest unresolved case is seed 34, target 2: the nominal update
case selects the true 6.0 mm radius, while the source-mismatch case is almost
flat and selects 6.2 mm by only `5.894e-06`.

The goal of this stage is not to force a more confident answer. The goal is to
test whether paper-backed objective variants improve radius discrimination
without hiding ambiguity.

## Objective Variants

Implementation:

```text
inversion/objective_variants.py
run_multi_rebar_local_geometry_profile.py
tests/test_objective_variants.py
tests/test_multi_rebar_local_geometry_profile.py
```

Supported variant format:

```text
label:t_start_ns,t_end_ns,taper_ns,low_ghz,high_ghz,band_taper_ghz
```

Use `none` for open bandpass bounds. The runner applies the bandpass to both
observed and synthetic B-scans, builds a matching time window, then reuses the
existing source-profiled LS objective.

Validation:

```text
tests/test_objective_variants.py: 4 passed
tests/test_multi_rebar_local_geometry_profile.py: 7 passed
coordinate optimizer focused tests: 18 passed
py_compile passed for objective variant and local profile modules
```

## 099: Objective-Variant CLI Smoke

Output:

```text
outputs/experiments/099_objective_variant_cli_cpu_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_multi_rebar_local_geometry_profile.py \
  --backend cpu \
  --grid-step-mm 20 \
  --sources 1 \
  --target-rebar-index 0 \
  --target-x-values-mm 150 \
  --target-z-values-mm 90 \
  --target-radius-values-mm 6.0,6.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13' \
  --source-frequency-scales 1.0 \
  --source-time-shift-ps-values 0 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0|late:1.5,5.5,0.2,none,none,0.0' \
  --progress-every 1 \
  --run-name objective_variant_cli_cpu_smoke
```

Plot validation:

| Figure | Size | Dynamic range | Standard deviation |
| --- | --- | ---: | ---: |
| `multi_rebar_local_geometry_radius_profiles.png` | `1617x920` | 255 | 29.99 |
| `multi_rebar_objective_variant_radius_profiles.png` | `1855x699` | 255 | 34.28 |

Interpretation:

The new CLI path writes both legacy and objective-variant outputs and produces
valid figures. The smoke case is intentionally too coarse to evaluate
scientific performance.

## Next Run

Run the first GPU objective matrix on the current hardest case:

```text
target rebar: 2
truth/final neighboring state: x=[150,250,350], z=[90,90,90], r=[6,6,6]
local search: x=349-351 mm, z=89-91 mm, r=5.8-6.8 mm
cases: noise10_seed34 and source_mismatch_noise10_seed34
objective variants: base, late, early reflection, high-band, late high-band
```

Decision gate:

```text
Promote an objective variant only if it keeps the nominal true-radius result,
improves the source-mismatch true-radius margin, and shrinks the ambiguity
interval without simply creating a new wrong-radius minimum.
```

## 100: Target-2 Final-State Objective Matrix, Seed 34

Output:

```text
outputs/experiments/100_multi_rebar_target2_radius_objective_matrix_seed34
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --rebar-x-values-mm 150,250,350 \
  --rebar-z-values-mm 90,90,90 \
  --truth-radius-mm 6.0 \
  --target-rebar-index 2 \
  --target-x-values-mm 349:351:1 \
  --target-z-values-mm 89:91:1 \
  --target-radius-values-mm 5.8:6.8:0.2 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.10,34|source_mismatch_noise10_seed34:1.1,-50.0,1.1,0.10,34' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0|late:1.5,5.5,0.2,none,none,0.0|early_reflection:1.0,3.5,0.2,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late_highband:1.5,5.5,0.2,1.1,3.4,0.15' \
  --progress-every 9 \
  --run-name multi_rebar_target2_radius_objective_matrix_seed34
```

Result:

| Case | Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Relative margin |
| --- | --- | --- | ---: | ---: | ---: |
| noise10_seed34 | base | 350 / 90 / 6.0 | 6.2 | 2.930e-04 | 3.678e-03 |
| noise10_seed34 | late | 350 / 90 / 6.0 | 6.2 | 2.370e-04 | 2.712e-03 |
| noise10_seed34 | early_reflection | 350 / 90 / 6.0 | 6.2 | 3.203e-04 | 9.140e-03 |
| noise10_seed34 | highband | 350 / 90 / 6.0 | 6.2 | 4.166e-04 | 4.241e-01 |
| noise10_seed34 | late_highband | 350 / 90 / 6.0 | 6.2 | 3.636e-04 | 2.841e-01 |
| source_mismatch_noise10_seed34 | base | 350 / 90 / 6.0 | 6.2 | 1.947e-04 | 2.191e-03 |
| source_mismatch_noise10_seed34 | late | 350 / 90 / 6.0 | 6.2 | 1.738e-04 | 1.426e-03 |
| source_mismatch_noise10_seed34 | early_reflection | 350 / 90 / 6.0 | 6.2 | 2.924e-04 | 7.628e-03 |
| source_mismatch_noise10_seed34 | highband | 350 / 90 / 6.0 | 6.2 | 3.248e-04 | 2.584e-01 |
| source_mismatch_noise10_seed34 | late_highband | 350 / 90 / 6.0 | 6.2 | 2.284e-04 | 1.454e-01 |

Runtime:

```text
866.4 s for 54 candidates, 2 cases, 5 objective variants
```

Plot validation:

| Figure | Size | Dynamic range | Standard deviation |
| --- | --- | ---: | ---: |
| `multi_rebar_local_geometry_radius_profiles.png` | `1617x920` | 255 | 31.64 |
| `multi_rebar_objective_variant_radius_profiles.png` | `1855x1243` | 255 | 39.44 |

Interpretation:

- With neighboring rebars fixed at the final true state, target 2 selects the
  true 6.0 mm radius even under the source-mismatch case.
- This means the earlier source-mismatch target-2 `6.2 mm` row in experiment
  097 was partly coupled to the left-edge high-radius branch that existed
  before guarded revisit, not only to target-2 local radius ambiguity.
- High-band weighting improved the source-mismatch absolute radius margin from
  `1.947e-04` to `3.248e-04` and the relative margin from `2.191e-03` to
  `2.584e-01`.
- The late-only time window did not help. The early-reflection and high-band
  variants are the useful candidates to replicate.

Implementation note:

`run_multi_rebar_local_geometry_profile.py` now accepts
`--rebar-radius-values-mm` so local objective matrices can reproduce
coordinate-step states where non-target rebar radii are still imperfect.

Next decision:

Run a small branch-focused target-0 matrix using the original wider-offset
coordinate-step state before guarded revisit:

```text
base state: x=[148,252,348], z=[92,88,92], r=[6.4,5.6,6.4]
target: 0
candidate branch: x=150 mm, z=90-91 mm, r=6.0-6.8 mm
```

This directly tests whether high-band or early-reflection weighting would have
preferred the true lower-radius branch over the `150/91/6.8` branch that the
base objective selected in the main pass.

## 101: Target-0 Branch-Focused Objective Matrix, Seed 34

Output:

```text
outputs/experiments/101_multi_rebar_target0_branch_objective_matrix_seed34
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --truth-x-values-mm 150,250,350 \
  --truth-z-values-mm 90,90,90 \
  --rebar-x-values-mm 148,252,348 \
  --rebar-z-values-mm 92,88,92 \
  --rebar-radius-values-mm 6.4,5.6,6.4 \
  --truth-radius-mm 6.0 \
  --target-rebar-index 0 \
  --target-x-values-mm 150 \
  --target-z-values-mm 90:91:1 \
  --target-radius-values-mm 6.0:6.8:0.2 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.10,34|source_mismatch_noise10_seed34:1.1,-50.0,1.1,0.10,34' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --objective-variants 'base:1.0,7.0,0.3,none,none,0.0|late:1.5,5.5,0.2,none,none,0.0|early_reflection:1.0,3.5,0.2,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late_highband:1.5,5.5,0.2,1.1,3.4,0.15' \
  --progress-every 2 \
  --run-name multi_rebar_target0_branch_objective_matrix_seed34
```

Result:

| Case | Objective | Best x/z/r [mm] | True-rank gap | Best-vs-next radius margin | Interpretation |
| --- | --- | --- | ---: | ---: | --- |
| noise10_seed34 | base | 150 / 91 / 6.8 | 5.618e-04 | 5.618e-04 | reproduces wrong high-radius branch |
| noise10_seed34 | early_reflection | 150 / 91 / 6.8 | 8.124e-04 | 7.996e-04 | wrong branch stronger |
| noise10_seed34 | highband | 150 / 91 / 6.8 | 1.226e-03 | 9.359e-04 | wrong branch stronger |
| noise10_seed34 | late_highband | 150 / 91 / 6.8 | 1.593e-03 | 2.101e-04 | wrong branch still selected |
| source_mismatch_noise10_seed34 | base | 150 / 91 / 6.8 | 5.719e-04 | 5.719e-04 | reproduces wrong high-radius branch |
| source_mismatch_noise10_seed34 | early_reflection | 150 / 91 / 6.8 | 8.971e-04 | 8.971e-04 | wrong branch stronger |
| source_mismatch_noise10_seed34 | highband | 150 / 91 / 6.8 | 1.535e-03 | 1.295e-03 | wrong branch stronger |
| source_mismatch_noise10_seed34 | late_highband | 150 / 91 / 6.6 | 1.800e-03 | 6.518e-05 | wrong radius/depth branch |

Runtime:

```text
160.2 s for 10 branch-focused candidates
```

Plot validation:

| Figure | Size | Dynamic range | Standard deviation |
| --- | --- | ---: | ---: |
| `multi_rebar_local_geometry_radius_profiles.png` | `1617x920` | 255 | 32.64 |
| `multi_rebar_objective_variant_radius_profiles.png` | `1855x1243` | 255 | 40.63 |

Interpretation:

High-band and early-reflection weighting do not fix the original target-0
high-radius branch when neighboring target estimates are still wrong. They
actually increase the objective gap favoring the wrong `z=91 mm, r=6.8 mm`
branch. Therefore, objective weighting cannot replace the guarded revisit
mechanism for the wider-offset coordinate stage.

Decision:

Keep guarded revisit as the coordinate-stage remedy. Continue evaluating
high-band and early-reflection weighting only as a post-correction radius
confidence tool. The next run should mirror experiment 100 for target 0 after
the final corrected state, so both edge targets are evaluated under the same
post-revisit condition.

## 102: Target-0 Final-State Objective Matrix, Seed 34

Output:

```text
outputs/experiments/102_multi_rebar_target0_radius_objective_matrix_seed34
```

Result:

| Case | Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Relative margin |
| --- | --- | --- | ---: | ---: | ---: |
| noise10_seed34 | base | 150 / 90 / 6.0 | 6.2 | 3.417e-04 | 4.289e-03 |
| noise10_seed34 | late | 150 / 90 / 6.0 | 6.2 | 2.097e-04 | 2.399e-03 |
| noise10_seed34 | early_reflection | 150 / 90 / 6.0 | 6.2 | 3.784e-04 | 1.080e-02 |
| noise10_seed34 | highband | 150 / 90 / 6.0 | 6.2 | 4.353e-04 | 4.431e-01 |
| noise10_seed34 | late_highband | 150 / 90 / 6.0 | 6.2 | 2.560e-04 | 1.999e-01 |
| source_mismatch_noise10_seed34 | base | 150 / 90 / 6.0 | 6.2 | 4.672e-04 | 5.257e-03 |
| source_mismatch_noise10_seed34 | late | 150 / 90 / 6.0 | 6.2 | 4.742e-04 | 3.890e-03 |
| source_mismatch_noise10_seed34 | early_reflection | 150 / 90 / 6.0 | 6.2 | 5.741e-04 | 1.498e-02 |
| source_mismatch_noise10_seed34 | highband | 150 / 90 / 6.0 | 6.2 | 6.095e-04 | 4.849e-01 |
| source_mismatch_noise10_seed34 | late_highband | 150 / 90 / 6.0 | 6.2 | 5.101e-04 | 3.249e-01 |

Runtime:

```text
867.6 s for 54 candidates, 2 cases, 5 objective variants
```

Plot validation:

| Figure | Size | Dynamic range | Standard deviation |
| --- | --- | ---: | ---: |
| `multi_rebar_local_geometry_radius_profiles.png` | `1617x920` | 255 | 31.63 |
| `multi_rebar_objective_variant_radius_profiles.png` | `1855x1243` | 255 | 39.50 |

Interpretation:

After the guarded revisit has corrected the coordinate state, target 0 behaves
like target 2. The base objective already selects the true radius, and
high-band weighting increases the radius margin in both nominal and
source-mismatch cases. This does not contradict experiment 101: high-band is
helpful after correction but harmful as a replacement for the correction.

Decision:

Replicate the post-correction objective comparison on another seed. Drop the
`late` and `late_highband` variants for the next replication because they did
not improve the decision gate in experiments 100 or 102. Keep:

```text
base
early_reflection
highband
```

## 103: Target-2 Final-State Objective Matrix, Seed 13

Output:

```text
outputs/experiments/103_multi_rebar_target2_radius_objective_matrix_seed13
```

Result:

| Case | Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Relative margin |
| --- | --- | --- | ---: | ---: | ---: |
| noise10_seed13 | base | 350 / 90 / 6.0 | 6.2 | 4.766e-04 | 5.928e-03 |
| noise10_seed13 | early_reflection | 350 / 90 / 6.0 | 6.2 | 5.288e-04 | 1.513e-02 |
| noise10_seed13 | highband | 350 / 90 / 6.0 | 6.2 | 5.250e-04 | 4.424e-01 |
| source_mismatch_noise10_seed13 | base | 350 / 90 / 6.0 | 6.2 | 5.033e-04 | 5.625e-03 |
| source_mismatch_noise10_seed13 | early_reflection | 350 / 90 / 6.0 | 6.2 | 6.625e-04 | 1.738e-02 |
| source_mismatch_noise10_seed13 | highband | 350 / 90 / 6.0 | 6.2 | 6.542e-04 | 4.350e-01 |

Runtime:

```text
864.2 s for 54 candidates, 2 cases, 3 objective variants
```

Plot validation:

| Figure | Size | Dynamic range | Standard deviation |
| --- | --- | ---: | ---: |
| `multi_rebar_local_geometry_radius_profiles.png` | `1617x920` | 255 | 31.84 |
| `multi_rebar_objective_variant_radius_profiles.png` | `1855x1243` | 255 | 37.97 |

Interpretation:

Seed 13 supports the seed 34 post-correction conclusion for target 2. The true
radius remains selected for all tested objectives. Early-reflection and
high-band weighting improve absolute margins, with high-band giving the
largest relative separation because the filtered objective has a much smaller
best misfit scale.

Decision:

Add wavefield animations for recent representative experiments before the next
GPU science run, then replicate the reduced objective set on target 0 seed 13.

## Wavefield Animation Support

Implementation:

```text
gpu/fdtd_gpu_v2.py
visualization/plot_wavefield.py
run_wavefield_animation.py
run_wavefield_comparison_animation.py
run_residual_backprop_animation.py
tests/test_wavefield_animation.py
```

Details:

- `gpu-cpml` single-source runs now support sparse `save_fields_every`
  snapshots without storing every time step.
- `run_wavefield_animation.py` generates representative GIFs in an existing
  experiment folder and writes validation metadata under `data/`. It also has
  guarded single-rebar material overrides for material-tradeoff animations.
- `run_wavefield_comparison_animation.py` generates true/candidate/difference
  GIFs and can use separate true and candidate source wavelets for authentic
  source-mismatch visualizations.
- `run_residual_backprop_animation.py` injects a time-reversed residual at the
  receiver and labels the result as residual back-propagation, not as a
  physical received wave.
- The reusable marathon skill now includes a rule to add representative
  wavefield animations for recent and future FDTD/FWI experiments when useful.

Validation:

```text
tests/test_wavefield_animation.py: 9 passed
full test suite: 127 passed in 23.57 s
git diff --check: passed
```

Generated animations:

| Experiment | Animation | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| 100 | `figures/target2_final_seed34_wavefield.gif` | 48 | `1000x600` | 255 | 34.09 |
| 101 | `figures/target0_high_radius_branch_seed34_wavefield.gif` | 48 | `1000x600` | 255 | 34.30 |
| 101 | `figures/target0_truth_vs_high_radius_branch_seed34_comparison.gif` | 48 | `1550x560` | 255 | 39.11 |
| 102 | `figures/target0_final_seed34_wavefield.gif` | 48 | `1000x600` | 255 | 34.08 |
| 103 | `figures/target2_final_seed13_wavefield.gif` | 48 | `1000x600` | 255 | 34.08 |
| 104 | `figures/target0_final_seed13_wavefield.gif` | 48 | `1000x600` | 255 | 34.08 |

Note:

The 100-104 forward GIFs were regenerated after adding Tx/Rx overlays. The
experiment 101 comparison is a geometry-specific diagnostic for the wrong
target-0 high-radius branch.

Policy update:

Future/current experiment animations follow the same scientific-use policy as
the previous-experiment animation tracker:

- label true-model forward, candidate-model forward, side-by-side comparison,
  and residual/adjoint back-propagation as distinct products.
- do not use decorative wave movies as substitutes for experiment-specific
  source/geometry/candidate visualizations.
- show transmitter/receiver markers in new generated animations.
- use separate observed/modelled source parameters when the experiment is about
  source mismatch.

## 104: Target-0 Final-State Objective Matrix, Seed 13

Output:

```text
outputs/experiments/104_multi_rebar_target0_radius_objective_matrix_seed13
```

Result:

| Case | Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Relative margin |
| --- | --- | --- | ---: | ---: | ---: |
| noise10_seed13 | base | 150 / 90 / 6.0 | 6.2 | 2.263e-04 | 2.814e-03 |
| noise10_seed13 | early_reflection | 150 / 90 / 6.0 | 6.2 | 2.342e-04 | 6.700e-03 |
| noise10_seed13 | highband | 150 / 90 / 6.0 | 6.2 | 2.684e-04 | 2.262e-01 |
| source_mismatch_noise10_seed13 | base | 150 / 90 / 6.0 | 6.2 | 3.117e-04 | 3.484e-03 |
| source_mismatch_noise10_seed13 | early_reflection | 150 / 90 / 6.0 | 6.2 | 3.580e-04 | 9.393e-03 |
| source_mismatch_noise10_seed13 | highband | 150 / 90 / 6.0 | 6.2 | 3.987e-04 | 2.651e-01 |

Runtime:

```text
862.2 s for 54 candidates, 2 cases, 3 objective variants
```

Plot validation:

| Figure | Size | Dynamic range | Standard deviation |
| --- | --- | ---: | ---: |
| `multi_rebar_local_geometry_radius_profiles.png` | `1617x920` | 255 | 31.85 |
| `multi_rebar_objective_variant_radius_profiles.png` | `1855x1243` | 255 | 37.98 |

Animation validation:

| Animation | Frames | Size | Dynamic range | Mean frame std |
| --- | ---: | --- | ---: | ---: |
| `figures/target0_final_seed13_wavefield.gif` | 48 | `1000x600` | 255 | 34.08 |

## Post-Correction Objective Aggregate

Scope:

```text
experiments 100, 102, 103, 104
targets 0 and 2
seeds 13 and 34
cases: nominal 10% noise and source mismatch + 10% noise
objectives: base, early_reflection, highband
```

Aggregate:

| Objective | Min margin | Mean margin | Max margin |
| --- | ---: | ---: | ---: |
| base | 1.947e-04 | 3.518e-04 | 5.033e-04 |
| early_reflection | 2.342e-04 | 4.186e-04 | 6.625e-04 |
| highband | 2.684e-04 | 4.541e-04 | 6.542e-04 |

Result:

- All 24 objective/case rows selected the true corrected geometry and
  6.0 mm radius.
- High-band improved the absolute radius margin over base in every row.
- Early-reflection also improved every row, but usually by less than high-band.
- The strongest high-band improvement was seed34 target2 under source mismatch:
  `1.668x` the base margin.
- The weakest high-band improvement was seed13 target2 nominal:
  `1.101x` the base margin.

Decision:

For post-correction edge-radius confidence, high-band is worth promoting as a
secondary confidence diagnostic. It should not replace the base objective for
coordinate updates, because experiment 101 showed high-band strengthens the
wrong high-radius branch before neighboring coordinates are corrected.

Next action:

Add high-band confidence reporting to the coordinate/revisit workflow as an
optional post-correction diagnostic, not as the update objective. Keep the base
objective as the optimizer decision rule until a broader update-objective test
proves otherwise.

## 105: Coordinate Diagnostic Objective CPU Smoke

Output:

```text
outputs/experiments/105_coordinate_optimizer_diagnostic_objective_cpu_smoke
```

Implementation:

```text
run_multi_rebar_coordinate_optimizer.py
tests/test_multi_rebar_coordinate_optimizer.py
```

New CLI option:

```text
--diagnostic-objective-variants
```

Behavior:

- The first diagnostic variant must be labelled `base`.
- Coordinate updates still use the base objective through the existing
  `case_results` path.
- Additional variants such as `highband` are written to
  `data/coordinate_objective_diagnostics.csv`.
- Diagnostic variants reuse the same FDTD candidate simulations; they add
  filtering/source-profiled scoring and reporting, not extra candidate
  simulations.

Validation:

```text
22 focused tests passed
py_compile passed for run_multi_rebar_coordinate_optimizer.py
CPU CLI smoke wrote coordinate_objective_diagnostics.csv
plot validation: coordinate_confidence_margins.png size 1549x903, dynamic range 255, std 26.36
```

Interpretation:

The coordinate runner can now emit high-band diagnostic margins without
changing the optimizer decision rule. The next production use should be a
GPU guarded coordinate run with:

```text
base
early_reflection
highband
```

as diagnostic variants.

## 106: Guarded Coordinate Run With Objective Diagnostics, Seed 55

Output:

```text
outputs/experiments/106_coordinate_optimizer_seed_offset2mm_guarded_diag_seed55
```

Result:

| Step kind | Target | Case | Best x/z/r [mm] | Base margin | Label |
| --- | ---: | --- | --- | ---: | --- |
| main | 0 | noise10_seed55 | 150 / 91 / 6.8 | 3.277e-04 | weak |
| main | 0 | source_mismatch_noise10_seed55 | 150 / 91 / 6.8 | 6.016e-04 | weak |
| main | 1 | noise10_seed55 | 250 / 90 / 6.0 | 1.713e-03 | strong |
| main | 1 | source_mismatch_noise10_seed55 | 250 / 90 / 6.0 | 1.930e-03 | strong |
| main | 2 | noise10_seed55 | 350 / 90 / 6.0 | 6.130e-05 | weak |
| main | 2 | source_mismatch_noise10_seed55 | 350 / 90 / 6.0 | 8.430e-05 | weak |
| revisit | 0 | noise10_seed55 | 150 / 90 / 6.0 | 2.550e-04 | weak |
| revisit | 0 | source_mismatch_noise10_seed55 | 150 / 90 / 6.0 | 4.052e-04 | weak |

Summary:

- Final state after guarded revisit:
  `x=[150,250,350]`, `z=[90,90,90]`, `r=[6,6,6]`.
- Runtime was `6667.3 s`.
- Confidence rows: 8 total; `weak=6`, `strong=2`.
- Objective diagnostic rows: 24 total; `base=8`, `early_reflection=8`,
  `highband=8`.
- Plot validation:
  `coordinate_confidence_margins.png`, size `1549x903`, dynamic range `255`,
  standard deviation `67.32`.

Diagnostic objective interpretation:

| Row | Early/base | High/base | Interpretation |
| --- | ---: | ---: | --- |
| target0 main nominal | 2.041 | 3.129 | high-band strengthens the wrong high-radius branch |
| target0 main mismatch | 1.726 | 2.323 | high-band strengthens the wrong high-radius branch |
| target0 revisit nominal | 0.945 | 1.266 | high-band improves post-correction margin |
| target0 revisit mismatch | 0.976 | 1.237 | high-band improves post-correction margin |
| target2 main nominal | 0.057 | 1.570 | early-reflection fails; high-band helps weak true branch |
| target2 main mismatch | 0.154 | 1.384 | early-reflection fails; high-band helps weak true branch |

Decision:

Seed55 strengthens the earlier conclusion:

```text
base objective + guarded revisit remains the update rule.
high-band is useful as a post-correction or reporting diagnostic.
early-reflection is not robust enough to promote.
```

The next objective-diagnostic development should remove `early_reflection` from
the recommended production diagnostic set unless a separate use case appears.

## 202: Coordinate Objective Diagnostic Report for Seed 55

Purpose:

```text
make the base-vs-diagnostic objective comparison explicit for coordinate
optimizer runs that already wrote objective_diagnostic_rows.
```

Implementation:

```text
added run_coordinate_objective_diagnostic_report.py
added tests/test_coordinate_objective_diagnostic_report.py
```

Focused validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_coordinate_objective_diagnostic_report.py \
  tests/test_multi_rebar_coordinate_optimizer.py
10 passed

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_coordinate_objective_diagnostic_report.py
passed
```

Output:

```text
outputs/experiments/202_coordinate_objective_diagnostic_report_106
```

Input:

```text
outputs/experiments/106_coordinate_optimizer_seed_offset2mm_guarded_diag_seed55/data/multi_rebar_coordinate_optimizer_summary.json
```

Aggregate:

| Objective | Rows | Truth rows | Geometry changes | Mean margin ratio vs base | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| early_reflection | 8 | 6 | 0 | 1.005 | 0.0567 | 2.041 |
| highband | 8 | 6 | 0 | 1.693 | 1.237 | 3.129 |

High-band detail:

| Step | Target | Case | Base truth? | High-band truth? | Ratio | Radius [mm] |
| --- | ---: | --- | --- | --- | ---: | ---: |
| main | 0 | noise10_seed55 | no | no | 3.129 | 6.8 |
| main | 0 | source_mismatch_noise10_seed55 | no | no | 2.323 | 6.8 |
| main | 1 | noise10_seed55 | yes | yes | 1.304 | 6.0 |
| main | 1 | source_mismatch_noise10_seed55 | yes | yes | 1.334 | 6.0 |
| main | 2 | noise10_seed55 | yes | yes | 1.570 | 6.0 |
| main | 2 | source_mismatch_noise10_seed55 | yes | yes | 1.384 | 6.0 |
| revisit | 0 | noise10_seed55 | yes | yes | 1.266 | 6.0 |
| revisit | 0 | source_mismatch_noise10_seed55 | yes | yes | 1.237 | 6.0 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png: 2059x1005 px, dynamic range 255,
std 74.14
```

Interpretation:

High-band is a good confidence diagnostic after the coordinate branch is
correct: it improves every margin ratio in experiment 106. But it also
strengthens the wrong target-0 high-radius branch during the main pass. That
confirms the prior decision: do not use high-band as the coordinate update
objective yet. Use it as a reporting diagnostic after base-objective coordinate
updates and guarded revisits.

Pause-and-ponder decision:

```text
for the next multi-rebar GPU work, keep base as the update objective and
include highband as the only recommended diagnostic objective. Drop
early_reflection from the default diagnostic set unless a future scenario
specifically needs early arrivals.
```

## 203: Seed34 Guarded Coordinate Optimizer with High-Band Diagnostic

Purpose:

```text
replicate the seed55 objective-diagnostic conclusion on seed34, but with only
the recommended diagnostic set: base objective for updates, guarded revisit
for weak high-radius branches, and highband as the reporting diagnostic.
```

Output:

```text
outputs/experiments/203_coordinate_optimizer_seed_offset2mm_guarded_highband_diag_seed34
```

Result:

```text
initial state:
  x=[148,252,348], z=[92,88,92], r=[6.4,5.6,6.4]

main pass:
  target 0 -> x=150, z=91, r=6.8, margin=5.61755e-04, weak
  target 1 -> x=250, z=90, r=6.0, margin=1.65270e-03, strong
  target 2 -> x=350, z=90, r=6.0, margin=9.03891e-05, weak

guarded revisit:
  target 0 -> x=150, z=90, r=6.0, margin=3.41730e-04, weak

final state:
  x=[150,250,350], z=[90,90,90], r=[6,6,6]
```

The target-0 main pass repeated the known high-radius ambiguity, but the
guarded revisit corrected it after targets 1 and 2 were updated. Target 2 was
geometrically correct but weak, so this run is a point-estimate success with
important radius-confidence caveats.

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 60.36
```

Implementation note:

```text
run_multi_rebar_coordinate_optimizer.py now writes FIGURE_NOTES.md for future
coordinate-optimizer figures. Experiment 203 started before that patch was
loaded, so its figure notes were written immediately after completion using
the same helper.
```

Focused validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_multi_rebar_coordinate_optimizer.py \
  tests/test_coordinate_objective_diagnostic_report.py
11 passed

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_multi_rebar_coordinate_optimizer.py
passed
```

## 204-205: Seed34 and Combined Objective Diagnostic Reports

Purpose:

```text
turn the seed34 objective-diagnostic rows into plain report products, then
combine seed55 and seed34 to judge highband from replicated evidence.
```

Outputs:

```text
204: outputs/experiments/204_coordinate_objective_diagnostic_report_203
205: outputs/experiments/205_coordinate_objective_diagnostic_report_106_203
```

Seed34 high-band diagnostic rows:

| Step | Target | Case | Base truth? | High-band truth? | Changed geometry? | Ratio | Radius [mm] |
| --- | ---: | --- | --- | --- | --- | ---: | ---: |
| main | 0 | noise10_seed34 | no | no | no | 1.666 | 6.8 |
| main | 0 | source_mismatch_noise10_seed34 | no | no | no | 2.265 | 6.8 |
| main | 1 | noise10_seed34 | yes | yes | no | 1.338 | 6.0 |
| main | 1 | source_mismatch_noise10_seed34 | yes | yes | no | 1.424 | 6.0 |
| main | 2 | noise10_seed34 | yes | yes | no | 1.844 | 6.0 |
| main | 2 | source_mismatch_noise10_seed34 | no | yes | yes | 0.683 | 6.0 |
| revisit | 0 | noise10_seed34 | yes | yes | no | 1.274 | 6.0 |
| revisit | 0 | source_mismatch_noise10_seed34 | yes | yes | no | 1.305 | 6.0 |

Combined 106+203 aggregate:

| Objective | Rows | Truth rows | Base truth rows | Geometry changes | Mean margin ratio vs base | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| early_reflection | 8 | 6 | 6 | 0 | 1.005 | 0.0567 | 2.041 |
| highband | 16 | 12 | 11 | 1 | 1.584 | 0.683 | 3.129 |

Plot validation:

```text
204 coordinate_objective_diagnostic_ratios.png: 2059x1005 px, dynamic range
255, std 75.08

205 coordinate_objective_diagnostic_ratios.png: 2549x1005 px, dynamic range
255, std 68.83
```

Interpretation:

Highband is still not safe as the coordinate update objective because it
strengthens the wrong target-0 high-radius branch in both seed55 and seed34.
But seed34 also shows a useful upside: for the source-mismatch target-2 row,
highband changes the diagnostic best geometry from a wrong 6.2 mm branch to
the true 6.0 mm branch. The replicated policy is therefore:

```text
use base objective for coordinate updates,
keep guarded revisits for weak high-radius branches,
use highband as a diagnostic/confidence objective,
do not promote highband to the default update objective yet.
```

Pause-and-ponder decision:

```text
the same-depth three-rebar policy is replicated across seed55 and seed34.
The next research stage should test generalization under stronger physical
coupling: close-spacing three-rebar detector-seeded coordinate FWI, using the
same reporting discipline and highband diagnostic.
```

## 206-207: Close-Spacing Detector-Seeded Coordinate FWI

Purpose:

```text
test whether the same-depth coordinate policy generalizes to a physically
harder three-rebar case with 60 mm spacing. Initial x/z seeds came from the
detector output of experiment 114, sorted into true-index order:
  x=[188,248,312], z=[90,90,90], r=[6.4,5.6,6.4].
The update case was the source-mismatch/noise case, matching the detector
stress condition.
```

Outputs:

```text
206: outputs/experiments/206_coordinate_optimizer_close_spacing_detector_seeded_highband_diag_seed13
207: outputs/experiments/207_coordinate_objective_diagnostic_report_206
```

Result:

```text
target order: 1,2,0

target 1 -> x=250, z=89, r=5.8, margin=9.21781e-04, moderate
target 2 -> x=310, z=91, r=6.6, margin=6.63947e-04, moderate
target 0 -> x=190, z=90, r=6.0, margin=1.79495e-04, weak

final state:
  x=[190,250,310], z=[90,89,91], r=[6.0,5.8,6.6]
```

The x locations recovered exactly, but close spacing exposed a new radius/depth
failure mode. The true target-1 and target-2 candidates were near the top of
their candidate tables, but the source-mismatch update case preferred adjacent
weak/moderate branches:

```text
target 1 source-mismatch top candidates:
  best: x=250, z=89, r=5.8, misfit=0.123418
  true: x=250, z=90, r=6.0, misfit=0.124869

target 2 source-mismatch top candidates:
  best: x=310, z=91, r=6.6, misfit=0.105030
  true: x=310, z=90, r=6.0, misfit=0.105813
```

The old guard did not trigger because it only revisited weak rows sitting on
the high-radius endpoint of the ambiguity interval. In 206, target 1 was a
moderate low-radius branch and target 2 was a moderate interior/high branch,
so the high-endpoint-only rule was too narrow.

Diagnostic objective report:

```text
highband rows=6
truth rows=1
base truth rows=2
geometry changes=1
mean margin ratio to base=0.760
```

Unlike same-depth runs, highband was not a reliable confidence enhancer for
this close-spacing case. It reduced most margins and changed the source-
mismatch target-0 diagnostic row from the true r=6.0 geometry to r=6.6. That
means close spacing should still use highband only as a diagnostic, and even
that diagnostic must be interpreted cautiously.

Plot validation:

```text
206 coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 62.86
207 coordinate_objective_diagnostic_ratios.png: 2059x1005 px, dynamic range
255, std 67.58
```

Implementation response:

```text
run_multi_rebar_coordinate_optimizer.py now has an opt-in
--revisit-broad-radius-ambiguity-targets flag. It revisits latest update-case
rows whose radius ambiguity interval is broad even if the row is labelled
moderate, not only weak high-radius endpoint rows.

FIGURE_NOTES.md generation now also names broad radius-ambiguity rows so the
reader knows which result rows need attention first.
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
187 passed

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_multi_rebar_coordinate_optimizer.py
passed

git diff --check
passed
```

Pause-and-ponder decision:

```text
run a corrected close-spacing GPU experiment with both revisit triggers:
  --revisit-weak-high-radius-targets
  --revisit-broad-radius-ambiguity-targets

If broad ambiguity revisits fix the z/r biases, keep this as the production
close-spacing guard. If not, the next stage should test target-order
sensitivity rather than widening the whole search indiscriminately.
```

## 208-209: Corrected Close-Spacing Broad-Ambiguity Revisit

Purpose:

```text
rerun the close-spacing detector-seeded case from 206 with the same main pass,
but add --revisit-broad-radius-ambiguity-targets so moderate/weak broad
radius intervals are revisited after the neighboring bars have been updated.
```

Outputs:

```text
208: outputs/experiments/208_coordinate_optimizer_close_spacing_broad_ambiguity_revisit_seed13
209: outputs/experiments/209_coordinate_objective_diagnostic_report_208
```

Result:

```text
main pass reproduced 206:
  target 1 -> x=250, z=89, r=5.8, margin=9.21781e-04
  target 2 -> x=310, z=91, r=6.6, margin=6.63947e-04
  target 0 -> x=190, z=90, r=6.0, margin=1.79495e-04

broad ambiguity revisits:
  target 0 -> x=190, z=90, r=6.0, margin=1.79495e-04
  target 1 -> x=250, z=90, r=6.0, margin=2.55099e-03
  target 2 -> x=310, z=90, r=6.0, margin=8.04718e-04

final state:
  x=[190,250,310], z=[90,90,90], r=[6,6,6]
```

Interpretation:

The broad ambiguity revisit fixed the close-spacing failure from 206. Target 1
became strong after revisit. Target 2 corrected to the true point but remains
moderate with a broad 6.0-6.8 mm ambiguity interval, so the point estimate is
right but radius confidence is still not as clean as same-depth wider-spacing
cases.

High-band diagnostic report:

```text
highband rows=12
truth rows=6
base truth rows=8
geometry changes=2
mean margin ratio to base=0.750
```

Highband remains a diagnostic only. In close spacing it reduced average margin
and sometimes moved a diagnostic row away from the base truth geometry, even
though the base-plus-broad-revisit update path recovered the exact final
geometry.

Plot validation:

```text
208 coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 57.56
209 coordinate_objective_diagnostic_ratios.png: 2059x1005 px, dynamic range
255, std 67.30
```

Pause-and-ponder decision:

```text
for close-spacing three-rebar cases, the production coordinate policy should
be:
  update objective: base objective,
  revisit guard: broad radius ambiguity, not only weak high-radius endpoints,
  diagnostic objective: highband for reporting only, interpreted cautiously.

Next research stage: variable-depth multi-rebar detector-seeded FWI. Use the
broad ambiguity guard from the start, because the variable-depth detector seeds
also contain z offsets that can create shallow competing branches.
```

## 210-211: Variable-Depth Detector-Seeded Broad-Ambiguity Revisit

Purpose:

```text
test the next generalization after close spacing: three rebars at different
depths, seeded from truth-matched detector candidates in experiment 115.
The initial detector seeds were:
  x=[148,252,352], z=[85,105,120], r=[6.4,5.6,6.4]
for truth:
  x=[150,250,350], z=[80,100,120], r=[6,6,6].
The main z window was expanded to -5:+1 mm to include the shallower true
depths for targets 0 and 1.
```

Outputs:

```text
210: outputs/experiments/210_coordinate_optimizer_variable_depth_broad_ambiguity_revisit_seed13
211: outputs/experiments/211_coordinate_objective_diagnostic_report_210
```

Result:

```text
main pass:
  target 0 -> x=150, z=81, r=6.8, margin=1.45109e-03
  target 1 -> x=250, z=100, r=6.0, margin=3.13770e-03
  target 2 -> x=350, z=120, r=6.0, margin=2.45047e-04

broad ambiguity revisits:
  target 0 -> x=150, z=80, r=6.0, margin=3.84331e-04
  target 2 -> x=350, z=120, r=6.0, margin=1.86642e-04

final state:
  x=[150,250,350], z=[80,100,120], r=[6,6,6]
```

Interpretation:

Variable depth was harder than close spacing in a different way. The shallow
target 0 initially chose a high-radius branch one millimeter too deep under
the source-mismatch update case. The broad revisit corrected it after targets
1 and 2 were placed. Target 1 recovered strongly in the main pass. Target 2
was geometrically correct but weak and stayed correct after revisit.

High-band diagnostic report:

```text
highband rows=10
truth rows=8
base truth rows=8
geometry changes=1
mean margin ratio to base=8.721
```

The very large mean highband ratio is not a general endorsement of highband as
an update rule: it comes from a tiny base margin in the nominal target-0 main
row, and highband still did not repair the wrong main-pass source-mismatch
target-0 branch. Continue treating highband as a diagnostic, not an update
objective.

Plot validation:

```text
210 coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 56.75
211 coordinate_objective_diagnostic_ratios.png: 2059x1005 px, dynamic range
255, std 44.42
```

Pause-and-ponder decision:

```text
base objective + broad radius-ambiguity revisit now generalizes across:
  same-depth 100 mm spacing,
  same-depth 60 mm spacing,
  variable-depth detector-seeded three-rebar cases.

The next research stage should stop assuming truth-matched detector picks.
Use experiment 115's full detector candidate list, including the false shallow
duplicate near x=252,z=65, and develop/test a detector-to-FWI assignment
policy that selects the physical three-rebar set before coordinate FWI.
```

## 212: Variable-Depth Detector Candidate Assignment

Purpose:

```text
remove the oracle step from experiment 210 by selecting the three FWI seed
candidates directly from experiment 115's full detector candidate list.
```

Implementation:

```text
added assign_rebar_candidates in inversion/rebar_detection.py
added run_detection_assignment_report.py
added tests/test_detection_assignment_report.py
```

Assignment rule:

```text
choose the highest-scoring set of N detector candidates that satisfies a
minimum x-separation, then sort the assigned seeds left-to-right for
coordinate FWI.
```

Output:

```text
outputs/experiments/212_detection_assignment_variable_depth_115
```

Input:

```text
outputs/experiments/115_detection_multi_rebar_variable_depth_source_mismatch_noise10/data/detection_candidates.csv
```

Selected seeds:

| Assigned order | Detector rank | x [mm] | z [mm] | Normalized score |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 148.0 | 85.0 | 0.9519 |
| 1 | 2 | 252.0 | 105.0 | 0.9456 |
| 2 | 4 | 352.0 | 120.0 | 0.7846 |

The assignment rejects rank 3 at `x=252 mm, z=65 mm` because it violates the
45 mm x-separation constraint with the stronger rank-2 candidate. The selected
seeds are exactly the seeds used in experiment 210, so 210 now serves as the
coordinate-FWI validation of the non-oracle assignment.

Plot validation:

```text
detector_assignment.png: 1445x1005 px, dynamic range 255, std 37.43
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
190 passed
```

Pause-and-ponder decision:

```text
the detector-to-FWI path now has:
  detector candidates,
  assignment by score subject to physical x separation,
  coordinate FWI with broad ambiguity revisits.

Next stage: run the same assignment report on the close-spacing detector case
114 and confirm it selects ranks 3,1,2 left-to-right. Then avoid duplicate GPU
FWI if the assigned seeds match the already validated close-spacing run 208.
```

## 213: Close-Spacing Detector Candidate Assignment

Purpose:

```text
apply the same detector-to-FWI assignment policy to close-spacing detector
experiment 114.
```

Output:

```text
outputs/experiments/213_detection_assignment_close_spacing_114
```

Selected seeds:

| Assigned order | Detector rank | x [mm] | z [mm] | Normalized score |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 3 | 188.0 | 90.0 | 0.8132 |
| 1 | 1 | 248.0 | 90.0 | 0.8806 |
| 2 | 2 | 312.0 | 90.0 | 0.8146 |

These are exactly the seeds used in close-spacing coordinate-FWI experiments
206 and 208 after sorting left-to-right. Experiment 208 therefore validates
the non-oracle close-spacing detector-to-FWI chain.

Plot validation:

```text
detector_assignment.png: 1444x1005 px, dynamic range 255, std 38.07
```

Pause-and-ponder decision:

```text
assignment policy now connects detector output to the validated FWI runs for:
  close spacing: 114 -> 213 -> 208,
  variable depth: 115 -> 212 -> 210.

Next stage should either:
  1. package detection assignment + coordinate FWI into one CLI, or
  2. test assignment robustness on a harder synthetic case with a deliberately
     stronger false positive.

Packaging is the better engineering step before more scenario expansion,
because it removes manual transfer of assigned seed x/z values.
```

## 214: Assigned Coordinate Command, Variable-Depth Case 115

Purpose:

```text
package the detector-assignment result from experiment 212 into a runnable
GPU coordinate-FWI command for the variable-depth detector case 115.
```

Implementation:

```text
added run_assigned_coordinate_command_report.py
```

Output:

```text
outputs/experiments/214_assigned_coordinate_command_variable_depth_115
```

The report reads experiment 115's detection summary, applies the same
assignment policy as experiment 212, writes the assigned candidates, and emits
a shell-safe coordinate optimizer command. Negative-valued range arguments are
saved in equals form, for example `--z-offsets-mm=-5:1:1`, so the command can
be pasted into a shell without argparse treating `-5:1:1` as another option.

Assigned seeds:

| Assigned order | Detector rank | x [mm] | z [mm] | Initial radius [mm] |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 148.0 | 85.0 | 6.4 |
| 1 | 2 | 252.0 | 105.0 | 5.6 |
| 2 | 4 | 352.0 | 120.0 | 6.4 |

Command policy:

```text
backend: gpu-cpml
grid step: 1 mm
sources: 5
update case: source_mismatch_noise10_seed13
main offsets: x=-2:2:1 mm, z=-5:1:1 mm, radius=-0.4:0.4:0.2 mm
guards: weak high-radius revisit + broad radius-ambiguity revisit
revisit offsets: x=-1:1:1 mm, z=-2:2:1 mm
diagnostics: base and highband objective variants
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_assigned_coordinate_command_report.py \
  tests/test_detection_assignment_report.py \
  tests/test_rebar_detection.py \
  tests/test_multi_rebar_coordinate_optimizer.py

21 passed
```

Pause-and-ponder decision:

```text
this report recreates the seeds that led to the exact variable-depth result in
experiment 210, but now the handoff is explicit and reproducible. The next
packaging check is to emit the equivalent command for the close-spacing
detector case 114.
```

## 215: Assigned Coordinate Command, Close-Spacing Case 114

Purpose:

```text
package the close-spacing detector-assignment result from experiment 213 into
a runnable GPU coordinate-FWI command.
```

Output:

```text
outputs/experiments/215_assigned_coordinate_command_close_spacing_114
```

Assigned seeds:

| Assigned order | Detector rank | x [mm] | z [mm] | Initial radius [mm] |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 3 | 188.0 | 90.0 | 6.4 |
| 1 | 1 | 248.0 | 90.0 | 5.6 |
| 2 | 2 | 312.0 | 90.0 | 6.4 |

Command policy:

```text
backend: gpu-cpml
grid step: 1 mm
sources: 5
update case: source_mismatch_noise10_seed13
main offsets: x=-2:2:1 mm, z=-2:2:1 mm, radius=-0.4:0.4:0.2 mm
guards: weak high-radius revisit + broad radius-ambiguity revisit
revisit offsets: x=-1:1:1 mm, z=-1:1:1 mm
diagnostics: base and highband objective variants
```

Interpretation:

```text
this command report formalizes the already validated chain:
  114 detector -> 213 assignment -> 208 broad-ambiguity coordinate FWI.

No duplicate GPU rerun is needed unless the command wrapper itself starts
launching the optimizer directly. The saved command is the reproducible bridge
from detector output to the known exact close-spacing FWI recovery.
```

Pause-and-ponder decision:

```text
the detector-to-FWI handoff is now reproducible for both validated hard
three-rebar scenarios. Next stage: convert the command emitter into an
optional launcher/dry-run workflow, then use that wrapper for the next new
scenario instead of manually assembling coordinate-FWI commands.
```

## 216: Variable-Radius Close-Spacing Detector

Purpose:

```text
start the next generalization branch: three close-spaced rebars at the same
depth but with unequal radii. This tests whether the detector still gives
usable coordinate seeds before FWI estimates size.
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_rebar_detection_pipeline.py \
  --backend gpu-cpml --grid-step-mm 2.0 --scan-step-mm 4.0 \
  --truth-x-values-mm 190,250,310 --truth-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --frequency-scale 1.1 --time-shift-ps=-50 --amplitude-scale 1.1 \
  --noise-fraction 0.10 --noise-seed 13 \
  --detector-x-values-mm 120:380:4 --detector-z-values-mm 65:125:5 \
  --detector-time-offset-ps-values 350,450,550,650,750 \
  --top-k 12 --x-min-separation-mm 35 --z-min-separation-mm 35
```

Output:

```text
outputs/experiments/216_detection_multi_rebar_variable_radius_close_spacing_source_mismatch_noise10
```

Truth:

| Target | x [mm] | z [mm] | Radius [mm] |
| ---: | ---: | ---: | ---: |
| 0 | 190 | 90 | 5 |
| 1 | 250 | 90 | 6 |
| 2 | 310 | 90 | 8 |

Top detector candidates:

| Rank | x [mm] | z [mm] | Normalized score |
| ---: | ---: | ---: | ---: |
| 1 | 312 | 95 | 0.8979 |
| 2 | 248 | 90 | 0.8801 |
| 3 | 188 | 100 | 0.7570 |
| 4 | 184 | 65 | 0.7203 |

All truth points were within the configured detector tolerance. The important
imperfection is the smallest 5 mm bar: the detector seed is `x=188 mm,
z=100 mm`, which is 2 mm left and 10 mm too deep. That is acceptable as a seed
test, but it means the coordinate-FWI z window must include a -10 mm
correction.

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.16
FIGURE_NOTES.md was generated by the detector pipeline.
```

Pause-and-ponder decision:

```text
continue to assignment and coordinate FWI, but do not use the narrow z window
from the already-good close-spacing case. The first coordinate pass must cover
z offsets -10,-5,0,5 mm from the assigned detector seeds.
```

## 217: Variable-Radius Candidate Assignment

Purpose:

```text
select the physical three-rebar seed set from experiment 216's detector
candidates.
```

Output:

```text
outputs/experiments/217_detection_assignment_variable_radius_close_spacing_216
```

Selected seeds:

| Assigned order | Detector rank | x [mm] | z [mm] | Normalized score |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 3 | 188.0 | 100.0 | 0.7570 |
| 1 | 2 | 248.0 | 90.0 | 0.8801 |
| 2 | 1 | 312.0 | 95.0 | 0.8979 |

The assignment rule rejected same-x duplicate branches and kept one seed per
physical bar. Because assignment order is sorted left-to-right, the weakest
and smallest bar becomes target 0 in the coordinate optimizer.

## 218: Variable-Radius Assigned Coordinate Command and Launcher

Purpose:

```text
use the new wrapper/launcher path to build the GPU coordinate-FWI command for
experiment 216's assigned seeds.
```

Output:

```text
outputs/experiments/218_assigned_coordinate_command_variable_radius_216
```

Command policy:

```text
truth radii: 5,6,8 mm
initial radii: 6,6,6 mm
update case: source_mismatch_noise10_seed13
main x offsets: -2:2:1 mm
main z offsets: -10,-5,0,5 mm
main radius offsets: -1:2:0.5 mm
revisit z offsets: -2:2:1 mm
guards: weak high-radius revisit + broad radius-ambiguity revisit
launcher mode: run, with optimizer stdout/stderr captured under data/
```

The wrapper now supports dry-run by default and explicit launch with
`--run-coordinate-fwi`. It also supports unequal truth radii through
`--truth-radius-values-mm`.

Implementation note after launching 219:

```text
the initial launch used captured stdout/stderr, which made long optimizer
progress hard to inspect. The wrapper now also supports
--coordinate-log-mode file for future long runs, so optimizer logs are written
directly to data/coordinate_launcher_stdout.txt and
data/coordinate_launcher_stderr.txt while the process runs. After starting
220/221, the launcher was also updated to force PYTHONUNBUFFERED=1 for future
file-log launches; 221 had already started before that buffering fix.
```

## 219: Variable-Radius Coordinate FWI, Left-to-Right Order

Status:

```text
completed GPU run launched through experiment 218's wrapper.
```

Output:

```text
outputs/experiments/219_coordinate_optimizer_variable_radius_close_spacing_from_assignment_seed13
```

Partial result after target 0:

| Case | Best x [mm] | Best z [mm] | Best radius [mm] | Note |
| --- | ---: | ---: | ---: | --- |
| source_mismatch_noise10_seed13 | 189 | 95 | 8.0 | update case selected wrong high-radius branch |
| noise10_seed13 | 188 | 95 | 5.0 | nominal noisy case selected correct radius but still too deep |

Interpretation so far:

```text
variable-radius coordinate FWI is more target-order sensitive than common-
radius FWI. Updating the smallest/weakest bar first appears to let target 0
absorb missing amplitude from the still-unupdated large target 2. The current
run should continue to see whether the broad revisit repairs this after target
2 is updated.
```

Partial result after target 1:

| Case | Best x [mm] | Best z [mm] | Best radius [mm] | Note |
| --- | ---: | ---: | ---: | --- |
| source_mismatch_noise10_seed13 | 250 | 90 | 7.0 | update case over-estimated the center radius |
| noise10_seed13 | 250 | 95 | 6.5 | nominal case stayed closer in radius but too deep |

This reinforces the target-order concern. With target 0 already inflated to
8 mm, the center target also drifts high under the source-mismatch update
case. The run should still continue to target 2 and any revisits, because the
large right bar being updated may change the later ambiguity/revisit behavior.

Partial result after target 2:

| Case | Best x [mm] | Best z [mm] | Best radius [mm] | Note |
| --- | ---: | ---: | ---: | --- |
| source_mismatch_noise10_seed13 | 310 | 90 | 8.0 | exact right/large bar recovery |
| noise10_seed13 | 310 | 90 | 8.0 | exact right/large bar recovery |

This shows the model can identify the 8 mm bar cleanly once that target is
updated. The main failure mechanism is therefore the coupled update order, not
the basic radius representation for a large bar.

Revisit target 0:

| Case | Best x [mm] | Best z [mm] | Best radius [mm] | Note |
| --- | ---: | ---: | ---: | --- |
| source_mismatch_noise10_seed13 | 189 | 94 | 7.5 | revisit stayed on wrong high-radius branch |
| noise10_seed13 | 189 | 94 | 7.5 | nominal also stayed on wrong high-radius branch after target 2 update |

The broad ambiguity revisit did not recover the true 5 mm radius. Its revisit
window was built from the already-wrong high-radius ambiguity interval, so the
true small-radius branch was not reconsidered. This is a stronger failure mode
than the common-radius cases: a locally confident compensation branch can
exclude the correct radius from the confirmatory revisit.

Final state:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
final: x=[189,250,310], z=[94,91,90], r=[7.5,7.0,8.0]
elapsed: 7927.0 s
```

Step sequence:

| Step | Kind | Target | Best x [mm] | Best z [mm] | Best radius [mm] | Radius error [mm] |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | main | 0 | 189 | 95 | 8.0 | +3.0 |
| 2 | main | 1 | 250 | 90 | 7.0 | +1.0 |
| 3 | main | 2 | 310 | 90 | 8.0 | 0.0 |
| 4 | revisit | 0 | 189 | 94 | 7.5 | +2.5 |
| 5 | revisit | 1 | 250 | 91 | 7.0 | +1.0 |

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 65.58
FIGURE_NOTES.md exists and flags target 0 broad ambiguity and target 1 weak
update rows.
```

Verdict:

```text
experiment 219 is a useful controlled failure. The pipeline can recover the
large 8 mm bar exactly, but left-to-right coordinate updates over-estimate the
small and medium bars under source mismatch. The current broad revisit is not
enough because it revisits only the local wrong ambiguity interval.
```

Next decision, pending final result:

```text
run an order-sensitivity comparison with target order 2,1,0 so the strongest
detector candidate and largest true bar is updated first. Use the new
--coordinate-log-mode file launcher option so progress logs are written during
the run.
```

## 220: Variable-Radius Assigned Command, Target Order 2-1-0

Purpose:

```text
launch the order-sensitivity comparison recommended by experiment 219 using
the same detector/assignment inputs but target order 2,1,0.
```

Output:

```text
outputs/experiments/220_assigned_coordinate_command_variable_radius_order210_216
```

Policy change relative to 218/219:

```text
target order: 2,1,0
launcher log mode: file
all geometry/source/search settings otherwise match experiment 219
```

The intent is to update the strongest detector candidate and largest true bar
first, then the center bar, then the small left bar. This tests whether the
left-to-right failure was mostly caused by early small-bar compensation.

## 221: Variable-Radius Coordinate FWI, Target Order 2-1-0

Status:

```text
completed GPU run launched through experiment 220.
```

Output:

```text
outputs/experiments/221_coordinate_optimizer_variable_radius_target_order_210_seed13
```

Progress:

```text
running with file-backed optimizer logs under experiment 220/data.
```

Partial result after first step, target 2:

| Case | Best x [mm] | Best z [mm] | Best radius [mm] | Note |
| --- | ---: | ---: | ---: | --- |
| source_mismatch_noise10_seed13 | 312 | 90 | 7.0 | large bar under-estimated when updated first |
| noise10_seed13 | 310 | 90 | 5.0 | nominal case selected a small-radius branch |

This weakens the simple "largest first fixes it" hypothesis. In experiment
219, the large bar recovered exactly only after targets 0 and 1 had already
been inflated. The unequal-radius scene appears to need either a joint/block
radius update or a stronger radius prior, not only a different greedy order.

Partial result after second step, target 1:

| Case | Best x [mm] | Best z [mm] | Best radius [mm] | Note |
| --- | ---: | ---: | ---: | --- |
| source_mismatch_noise10_seed13 | 247 | 90 | 7.5 | center bar over-estimated and shifted left |
| noise10_seed13 | 247 | 90 | 5.0 | nominal case under-estimated radius |

The second step confirms that target order alone is not enough. The same
fixed source-profiled objective can prefer opposite wrong radius branches in
the nominal and source-mismatch cases.

Partial result after third step, target 0:

| Case | Best x [mm] | Best z [mm] | Best radius [mm] | Note |
| --- | ---: | ---: | ---: | --- |
| source_mismatch_noise10_seed13 | 187 | 95 | 7.5 | small bar over-estimated |
| noise10_seed13 | 188 | 95 | 7.5 | nominal also over-estimated after prior updates |

At this point, order 2,1,0 is also a failed greedy variant. It did not recover
the large bar first, then over-estimated the center and small bars. Continue
to final/revisit only to document confidence labels and final state.

Final state:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
final: x=[187,248,311], z=[95,91,90], r=[7.5,7.0,7.5]
elapsed: 8370.7 s
```

Step sequence:

| Step | Kind | Target | Best x [mm] | Best z [mm] | Best radius [mm] | Radius error [mm] |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | main | 2 | 312 | 90 | 7.0 | -1.0 |
| 2 | main | 1 | 247 | 90 | 7.5 | +1.5 |
| 3 | main | 0 | 187 | 95 | 7.5 | +2.5 |
| 4 | revisit | 1 | 248 | 91 | 7.0 | +1.0 |
| 5 | revisit | 2 | 311 | 90 | 7.5 | -0.5 |

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 62.32
FIGURE_NOTES.md exists and flags weak/broad target 2 and target 1 rows.
```

Verdict:

```text
target order 2,1,0 does not rescue the unequal-radius case. It is worse than
219 for the right/large bar and still over-estimates the small and center
bars. The failure is therefore not only left-to-right order. The next test
should be a joint radius-tuple diagnostic at fixed x/z to separate objective
ambiguity from greedy coordinate coupling.
```

## 222: Joint Radius Tuple Diagnostic, True x/z

Purpose:

```text
test whether the source-profiled objective can identify the correct unequal
radius tuple [5,6,8] when x/z coordinate error and greedy target-order
coupling are removed.
```

Output:

```text
outputs/experiments/222_joint_radius_variable_radius_true_xz_seed13
```

Setup:

```text
truth x/z/r: x=[190,250,310], z=[90,90,90], r=[5,6,8]
candidate x/z: fixed to true x/z
radius tuple grid: each radius in 5:8:0.5 mm
tuple count: 7^3 = 343
backend: gpu-cpml
```

Status:

```text
completed GPU run.
```

Interpretation rule:

```text
if [5,6,8] ranks first or near-first, the objective can estimate the sizes
when updated jointly, and the next method should be a block radius update.
if [5,6,8] does not rank well even at true x/z, the objective/source treatment
or a radius prior must change before more coordinate FWI runs.
```

Result:

```text
elapsed: 5484.9 s
tuple count: 343
truth tuple [5,6,8] rank in noise10_seed13: 1
truth tuple [5,6,8] rank in source_mismatch_noise10_seed13: 1
```

Top source-mismatch tuples:

| Rank | Radius tuple [mm] | Misfit |
| ---: | --- | ---: |
| 1 | [5.0, 6.0, 8.0] | 0.09794 |
| 2 | [5.5, 6.0, 8.0] | 0.10226 |
| 3 | [5.0, 6.0, 7.5] | 0.10407 |
| 4 | [5.0, 5.5, 8.0] | 0.10520 |
| 5 | [5.0, 6.5, 8.0] | 0.10529 |

Plot validation:

```text
joint_radius_top_candidates.png: 1804x1039 px, dynamic range 255, std 79.67
FIGURE_NOTES.md exists.
```

Verdict:

```text
the source-profiled objective can identify the true unequal radii when x/z is
fixed correctly and the radii are updated as a block. The failure in 219 and
221 is therefore the greedy coordinate/radius update path, not the basic
ability of the forward model and objective to distinguish [5,6,8].
```

Pause-and-ponder decision:

```text
next run the same joint radius tuple profile at the detector-assigned x/z
seeds from 216: x=[188,248,312], z=[100,90,95]. If [5,6,8] fails there, the
pipeline needs coordinate correction before block radii. If it still ranks
well, implement a block radius update after detector assignment.
```

## 223: Joint Radius Tuple Diagnostic, Detector-Assigned x/z

Purpose:

```text
test whether the successful joint radius tuple objective from 222 still works
when x/z is fixed to the detector-assigned seeds rather than the true
coordinates.
```

Output:

```text
outputs/experiments/223_joint_radius_variable_radius_assigned_xz_seed13
```

Setup:

```text
truth x/z/r: x=[190,250,310], z=[90,90,90], r=[5,6,8]
candidate x/z: x=[188,248,312], z=[100,90,95]
radius tuple grid: each radius in 5:8:0.5 mm
tuple count: 343
backend: gpu-cpml
```

Status:

```text
completed GPU run.
```

Result:

```text
elapsed: 5495.3 s
tuple count: 343
truth tuple [5,6,8] rank in noise10_seed13 top 20: not present
truth tuple [5,6,8] rank in source_mismatch_noise10_seed13 top 20: not present
```

Top source-mismatch tuples:

| Rank | Radius tuple [mm] | Misfit |
| ---: | --- | ---: |
| 1 | [8.0, 7.0, 8.0] | 0.48616 |
| 2 | [8.0, 7.5, 8.0] | 0.48716 |
| 3 | [8.0, 6.5, 8.0] | 0.49055 |
| 4 | [8.0, 8.0, 8.0] | 0.49493 |
| 5 | [8.0, 6.0, 8.0] | 0.50242 |

Plot validation:

```text
joint_radius_top_candidates.png: 1804x1039 px, dynamic range 255, std 79.68
FIGURE_NOTES.md exists.
```

Verdict:

```text
block radius estimation works at true x/z (222) but fails at detector-assigned
x/z (223). The detector seed depth error, especially target 0 at z=100 mm
instead of z=90 mm and target 2 at z=95 mm instead of z=90 mm, causes the
radius tuple objective to prefer inflated radii.
```

Pause-and-ponder decision:

```text
next run a location-only coordinate pass with radii held fixed at 6 mm. This
prevents radius from absorbing depth/source errors during the coordinate
correction stage. After that, run joint radius estimation at the corrected
x/z.
```

## 224: Assigned Command, Variable-Radius Location-Only Stage

Purpose:

```text
package and launch a coordinate pass that corrects x/z while holding all
radii fixed at 6 mm.
```

Output:

```text
outputs/experiments/224_assigned_coordinate_command_variable_radius_location_only_216
```

Policy:

```text
target order: 0,1,2
initial radii: [6,6,6] mm
radius offsets: 0
main z offsets: -10,-5,0,5 mm
launcher log mode: file
```

## 225: Variable-Radius Location-Only Coordinate FWI

Status:

```text
completed GPU run launched through experiment 224.
```

Output:

```text
outputs/experiments/225_coordinate_optimizer_variable_radius_location_only_seed13
```

Result:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
initial: x=[188,248,312], z=[100,90,95], r=[6,6,6]
final: x=[190,250,310], z=[90,90,85], r=[6,6,6]
elapsed: 961.0 s
```

Interpretation:

```text
holding radius fixed at 6 mm corrected target 0 and target 1 exactly. Target
2, whose true radius is 8 mm, moved shallower to z=85 mm. This is a sensible
compensation: with the radius artificially held too small, the optimizer uses
shallower depth to match the large bar's response.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 29.77
FIGURE_NOTES.md exists.
```

Pause-and-ponder decision:

```text
run joint radius estimation at the 225 final x/z state:
  x=[190,250,310], z=[90,90,85].
If the radius block recovers a large target-2 radius, the next step is a
coordinate polish after block radii. If it fails, the location and radius need
to be updated together for target 2.
```

## 226: Joint Radius Tuple Diagnostic, Location-Only x/z

Purpose:

```text
run the joint radius tuple diagnostic at the geometry produced by the
location-only pass in experiment 225.
```

Output:

```text
outputs/experiments/226_joint_radius_variable_radius_location_only_xz_seed13
```

Setup:

```text
truth x/z/r: x=[190,250,310], z=[90,90,90], r=[5,6,8]
candidate x/z: x=[190,250,310], z=[90,90,85]
radius tuple grid: each radius in 5:8:0.5 mm
tuple count: 343
backend: gpu-cpml
```

Status:

```text
completed GPU run.
```

Result:

```text
elapsed: 5485.4 s
tuple count: 343
truth tuple [5,6,8] rank in noise10_seed13 top 20: not present
truth tuple [5,6,8] rank in source_mismatch_noise10_seed13 top 20: not present
```

Top source-mismatch tuples:

| Rank | Radius tuple [mm] | Misfit |
| ---: | --- | ---: |
| 1 | [5.0, 6.5, 5.0] | 0.12270 |
| 2 | [5.0, 6.0, 5.0] | 0.12750 |
| 3 | [5.0, 7.0, 5.0] | 0.12755 |
| 4 | [5.5, 6.5, 5.0] | 0.12867 |
| 5 | [5.5, 6.0, 5.0] | 0.12936 |

Plot validation:

```text
joint_radius_top_candidates.png: 1804x1039 px, dynamic range 255, std 79.66
FIGURE_NOTES.md exists.
```

Verdict:

```text
location-only geometry is not sufficient when target 2 is left at z=85 mm.
The joint radius objective then explains the right bar as a small/shallow
target, not as the true large/deeper target. Target 2 needs a coupled local
x/z/r polish after targets 0 and 1 are corrected.
```

Pause-and-ponder decision:

```text
run a focused target-2 local x/z/r coordinate polish from state
x=[190,250,310], z=[90,90,85], r=[6,6,6], with target 2 allowed to search
z offsets 0,5,10 mm and radius offsets -1:2:0.5 mm.
```

## 227: Focused Target-2 Coupled x/z/r Polish After Location-Only Stage

Purpose:

```text
test whether the right/largest bar can recover its true coupled depth and
radius after targets 0 and 1 have already been corrected by the location-only
stage.
```

Output:

```text
outputs/experiments/227_coordinate_optimizer_variable_radius_target2_after_location_polish_seed13
```

Setup:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
initial state: x=[190,250,310], z=[90,90,85], r=[6,6,6]
updated target: target 2 only
main candidate grid: x offsets -2:2:1 mm, z offsets 0,5,10 mm,
  radius offsets -1:2:0.5 mm
source profiling: frequency scales [0.9,1.0,1.1], time shifts [-50,0,50] ps
backend: gpu-cpml, 1 mm forward grid, 5 sources
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 1669.2 s
final state: x=[190,250,310], z=[90,90,90], r=[6,6,8]
noise10_seed13 best: x=310, z=90, r=8, margin=6.71762e-03, strong
source_mismatch_noise10_seed13 best: x=310, z=90, r=8, margin=8.77646e-03,
  strong
radius-ambiguity revisit: not triggered
```

Objective diagnostic detail:

```text
base objective selected exact target-2 truth in both cases.
highband diagnostic also selected r=8,z=90; in the source-mismatch case it
preferred x=309 instead of x=310, with a slightly larger radius margin.
```

Landscape validation:

```text
source-mismatch z/radius landscape: truth z=90,r=8 ranked 1,
  misfit=0.120325
nominal/noisy z/radius landscape: truth z=90,r=8 ranked 1,
  misfit=0.105338
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.49
coordinate_step_01_target_2_source_mismatch_z_radius_landscape.png:
  1515x1073 px, dynamic range 255, std 82.62
coordinate_step_01_target_2_noise10_z_radius_landscape.png:
  1515x1073 px, dynamic range 255, std 84.19
FIGURE_NOTES.md includes the confidence plot and both z/radius landscapes.
```

Verdict:

```text
the staged approach works for the right/largest bar once the small and medium
bars have corrected locations. Fixed-radius location-only correction moved
the large bar too shallow, but a focused coupled x/z/r polish from that state
recovered the exact large-bar depth and radius with strong margins.
```

Pause-and-ponder decision:

```text
test whether this is a reusable staged pipeline, not a one-off fix:
  1. after location-only correction, run focused coupled polish for target 2;
  2. then run joint radius estimation at the corrected x/z state to recover
     all radii together.

The immediate next experiment should use the 227 x/z state
x=[190,250,310], z=[90,90,90] and run the joint radius tuple diagnostic. This
should reproduce the oracle result from 222, but now the x/z state came from
the staged pipeline rather than being manually supplied as truth.
```

## 229: Variable-Radius Coordinate Objective Diagnostic, 219/221/225

Purpose:

```text
aggregate existing objective-variant diagnostics from the variable-radius
coordinate runs before deciding whether a high-band objective should be used
for updates instead of only reporting.
```

Output:

```text
outputs/experiments/229_coordinate_objective_diagnostic_variable_radius_219_221_225
```

Implementation fixes made before the report:

```text
run_coordinate_objective_diagnostic_report.py now reads
truth_radius_values_mm when present, rather than assuming one common truth
radius. It also treats missing/None margin values as unavailable ratios
instead of crashing.
```

Result:

```text
rows: 26
highband truth rows: 3
base truth rows: 3
geometry changes caused by highband: 8
highband/base margin ratio mean: 1.28969
margin ratio range: 0.16507 to 9.79136
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png: 2760x1005 px, dynamic range 255,
std 46.10
FIGURE_NOTES.md exists.
```

Interpretation:

```text
the high-band diagnostic often changes geometry and only matches truth in 3
of 26 rows, the same count as the base objective. It can increase the margin,
but not reliably on the correct branch. This is useful evidence against simply
switching the coordinate-update rule to high-band globally.
```

## 230-231: Seed-21 Variable-Radius Detection and Assignment Replication

Purpose:

```text
start a second noise-seed/source-mismatch replication of the staged
variable-radius pipeline. Seed 21 tests whether the detector-to-location-only
stage gives a comparable correction problem to seed 13 before using the
target-2 focused polish recipe.
```

Outputs:

```text
230: outputs/experiments/230_detection_multi_rebar_variable_radius_close_spacing_source_mismatch_noise10_seed21
231: outputs/experiments/231_detection_assignment_variable_radius_close_spacing_seed21_230
```

Detection result:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
source mismatch: frequency scale=1.1, time shift=-50 ps, amplitude scale=1.1
noise: 10%, seed=21
top candidates:
  rank 1: x=312, z=95
  rank 2: x=248, z=100
  rank 3: x=248, z=65
  rank 4: x=188, z=85
all truths within detector tolerance: true
```

Assignment result:

```text
selected left-to-right seeds:
  target 0 seed: rank 4 at x=188, z=85
  target 1 seed: rank 2 at x=248, z=100
  target 2 seed: rank 1 at x=312, z=95
```

Plot validation:

```text
230 detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.18
231 detector_assignment.png: 1444x1005 px, dynamic range 255, std 36.77
FIGURE_NOTES.md exists for both experiments.
```

Pause-and-ponder decision:

```text
seed 21 gives a different detector error pattern from seed 13: target 0 is
shallow by 5 mm, target 1 is deep by 10 mm, and target 2 is deep by 5 mm. The
next run should repeat the location-only coordinate correction with radii
fixed at 6 mm and then decide which targets need coupled x/z/r polishing.
```

## 232-233: Seed-21 Location-Only Coordinate Stage

Purpose:

```text
repeat the staged pipeline's first FWI stage on seed 21: correct x/z while all
radii are fixed at 6 mm.
```

Outputs:

```text
232: outputs/experiments/232_assigned_coordinate_command_variable_radius_location_only_seed21_230
233: outputs/experiments/233_coordinate_optimizer_variable_radius_location_only_seed21
```

Setup:

```text
initial seeds from 231: x=[188,248,312], z=[85,100,95], r=[6,6,6]
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
target order: 0,1,2
x offsets: -2:2:1 mm
z offsets: -10,-5,0,5 mm
radius offsets: 0
backend: gpu-cpml, 1 mm forward grid, 5 sources
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 962.4 s
initial: x=[188,248,312], z=[85,100,95], r=[6,6,6]
final update-case state: x=[190,250,310], z=[90,90,85], r=[6,6,6]
target 0 update case: x=190, z=90, r=6
target 1 update case: x=250, z=90, r=6
target 2 update case: x=310, z=85, r=6
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 29.77
FIGURE_NOTES.md exists and notes that radius margins are missing because
radius was fixed.
```

Verdict:

```text
seed 21 reproduces the seed-13 staged behavior. Location-only correction fixes
the small and medium bars, but the large 8 mm bar is represented as a
small/shallow 6 mm bar at z=85 mm. This supports the staged policy:
location-only first, then focused coupled x/z/r polish for target 2.
```

Pause-and-ponder decision:

```text
run the same focused target-2 coupled x/z/r polish used in experiment 227,
but with seed 21 replication cases and initial state
x=[190,250,310], z=[90,90,85], r=[6,6,6].
```

## 234: Seed-21 Focused Target-2 Coupled x/z/r Polish

Purpose:

```text
test whether the focused large-bar recovery from experiment 227 generalizes to
seed 21 after the location-only stage produced the same small/shallow
target-2 compensation.
```

Output:

```text
outputs/experiments/234_coordinate_optimizer_variable_radius_target2_after_location_polish_seed21
```

Setup:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
initial state: x=[190,250,310], z=[90,90,85], r=[6,6,6]
updated target: target 2 only
main candidate grid: x offsets -2:2:1 mm, z offsets 0,5,10 mm,
  radius offsets -1:2:0.5 mm
source profiling: frequency scales [0.9,1.0,1.1], time shifts [-50,0,50] ps
backend: gpu-cpml, 1 mm forward grid, 5 sources
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 1673.6 s
final state: x=[190,250,310], z=[90,90,90], r=[6,6,8]
noise10_seed21 best: x=310, z=90, r=8, margin=6.42653e-03, strong
source_mismatch_noise10_seed21 best: x=310, z=90, r=8, margin=9.56024e-03,
  strong
radius-ambiguity revisit: not triggered
```

Objective diagnostic detail:

```text
base objective selected exact target-2 truth in both cases.
highband diagnostic selected r=8,z=90 but preferred x=309 in both cases.
As in experiment 227, highband remains useful diagnostic evidence but should
not replace the base update rule globally.
```

Landscape validation:

```text
source-mismatch z/radius landscape: truth z=90,r=8 ranked 1,
  misfit=0.120343
nominal/noisy z/radius landscape: truth z=90,r=8 ranked 1,
  misfit=0.104454
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 81.54
coordinate_step_01_target_2_source_mismatch_z_radius_landscape.png:
  1515x1073 px, dynamic range 255, std 82.47
coordinate_step_01_target_2_noise10_z_radius_landscape.png:
  1515x1073 px, dynamic range 255, std 84.42
FIGURE_NOTES.md includes the confidence plot and both z/radius landscapes.
```

Verdict:

```text
seed 21 independently confirms the staged policy:
  detector assignment -> location-only x/z correction -> focused target-2
  coupled x/z/r polish
recovers the large right bar's true depth and radius after fixed-radius
location-only correction pushes it to a small/shallow surrogate.
```

Pause-and-ponder decision:

```text
the remaining radius gap is target 0: the staged coordinate state after 234 is
x/z correct, target 2 radius correct, but target 0 radius is still held at
6 mm rather than the true 5 mm. The next stage should estimate all radii
jointly at the staged x/z state. Because 222 already proved this works for
seed 13 at true x/z, run a seed-21 joint-radius tuple diagnostic at
x=[190,250,310], z=[90,90,90] to test cross-seed robustness.
```

## 235: Seed-21 Joint Radius Tuple Diagnostic at Staged x/z

Purpose:

```text
test whether joint/block radius estimation recovers the full unequal-radius
tuple [5,6,8] under seed 21 once the staged coordinate pipeline has corrected
x/z.
```

Output:

```text
outputs/experiments/235_joint_radius_variable_radius_staged_xz_seed21
```

Setup:

```text
truth x/z/r: x=[190,250,310], z=[90,90,90], r=[5,6,8]
candidate x/z: x=[190,250,310], z=[90,90,90]
radius tuple grid: each radius in 5:8:0.5 mm
tuple count: 343
cases: noise10_seed21 and source_mismatch_noise10_seed21
backend: gpu-cpml, 1 mm forward grid, 5 sources
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 5467.5 s
tuple count: 343
truth tuple: [5,6,8]
noise10_seed21 truth rank: 1
source_mismatch_noise10_seed21 truth rank: 1
```

Top source-mismatch tuples:

| Rank | Radius tuple [mm] | Misfit |
| ---: | --- | ---: |
| 1 | [5.0, 6.0, 8.0] | 0.09636 |
| 2 | [5.5, 6.0, 8.0] | 0.10140 |
| 3 | [5.0, 6.0, 7.5] | 0.10284 |
| 4 | [5.0, 5.5, 8.0] | 0.10353 |
| 5 | [5.0, 6.5, 8.0] | 0.10375 |

Plot validation:

```text
joint_radius_top_candidates.png: 1804x1039 px, dynamic range 255, std 79.66
FIGURE_NOTES.md exists.
```

Verdict:

```text
seed 21 confirms the final block-radius stage. Once staged x/z is correct,
joint radius estimation recovers the full unequal-radius tuple [5,6,8] under
both nominal/noisy and source-mismatch/noisy cases.
```

Pause-and-ponder decision:

```text
the variable-radius close-spacing pipeline is now empirically supported across
two noise seeds:
  detector assignment -> location-only x/z correction -> focused target-2
  x/z/r polish -> joint radius tuple estimation.

The next development step should package this staged policy into a
reproducible summary/runner rather than continuing manual command assembly.
```

## 236: Target-2 Focused Polish Aggregate, Seeds 13 and 21

Purpose:

```text
summarize the focused target-2 coupled-polish evidence across the two
replicated noise seeds.
```

Output:

```text
outputs/experiments/236_coordinate_confidence_aggregate_variable_radius_target2_seed13_21
```

Input runs:

```text
227: seed 13 focused target-2 polish
234: seed 21 focused target-2 polish
```

Result:

```text
rows: 4
truth-geometry rows: 4
confidence labels: strong=4
radius margin min/mean/max:
  6.42653e-03 / 7.87021e-03 / 9.56024e-03
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1718x971 px, dynamic range 255, std 71.32
FIGURE_NOTES.md exists.
```

Interpretation:

```text
the focused target-2 stage is replicated across seed 13 and seed 21: both
nominal/noisy and source-mismatch/noisy cases recover the exact large-bar
geometry with strong margins.
```

## 237: Target-2 Focused Polish Objective Diagnostic, Seeds 13 and 21

Purpose:

```text
test whether the high-band diagnostic objective should become the update rule
for the focused target-2 stage, or remain diagnostic-only.
```

Output:

```text
outputs/experiments/237_coordinate_objective_diagnostic_target2_focus_seed13_21
```

Result:

```text
rows: 4
highband truth rows: 1
base truth rows: 4
highband geometry-change rows: 3
highband/base margin ratio mean: 0.92662
margin ratio range: 0.80064 to 1.03889
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png: 2059x1005 px, dynamic range 255,
std 81.91
FIGURE_NOTES.md exists.
```

Interpretation:

```text
for the successful target-2 focused polish, the base objective is better as
the update rule. High-band often shifts x from 310 to 309 and only matches the
full truth geometry in 1 of 4 rows. Keep high-band as a diagnostic/reporting
view, not as the coordinate update criterion.
```

## 238: Staged Variable-Radius Pipeline Summary, Seeds 13 and 21

Purpose:

```text
package the manually executed staged variable-radius pipeline into one
comparison artifact across seed 13 and seed 21.
```

Output:

```text
outputs/experiments/238_variable_radius_staged_pipeline_seed13_21_summary
```

Input chains:

```text
seed 13:
  detection 216 -> location-only 225 -> target-2 polish 227 -> joint radii 222
seed 21:
  detection 230 -> location-only 233 -> target-2 polish 234 -> joint radii 235
```

Result:

```text
location-only stage, both seeds:
  max x error=0 mm, max z error=5 mm, max radius error=2 mm
focused target-2 stage, both seeds:
  max x error=0 mm, max z error=0 mm, max radius error=1 mm
joint radius stage, both seeds:
  max x error=0 mm, max z error=0 mm, max radius error=0 mm
joint best radii, both seeds: [5,6,8]
truth tuple rank, both seeds: 1
```

Plot validation:

```text
staged_variable_radius_pipeline_errors.png: 1719x971 px, dynamic range 255,
std 39.05
FIGURE_NOTES.md exists.
```

Interpretation:

```text
the staged pipeline summary makes the correction path explicit. Location-only
removes detector x/z errors except for the large-bar depth/radius tradeoff.
Focused target-2 polishing fixes that depth/radius tradeoff. Joint radius
estimation then recovers the small-left-bar radius, producing exact x/z/r
under both tested seeds.
```

## 239: Seed-34 Variable-Radius Detection Replication

Purpose:

```text
start a third noise-seed replication of the staged variable-radius pipeline.
```

Output:

```text
outputs/experiments/239_detection_multi_rebar_variable_radius_close_spacing_source_mismatch_noise10_seed34
```

Detection result:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
source mismatch: frequency scale=1.1, time shift=-50 ps, amplitude scale=1.1
noise: 10%, seed=34
top candidates:
  rank 1: x=312, z=95
  rank 2: x=248, z=90
  rank 3: x=188, z=85
all truths within detector tolerance: true
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.15
FIGURE_NOTES.md exists.
```

Pause-and-ponder decision:

```text
seed 34 starts from a slightly cleaner assignment pattern than seed 21:
target 0 is shallow by 5 mm, target 1 is exact in z, and target 2 is deep by
5 mm. Continue with assignment and the location-only stage.
```

## 240: Seed-34 Detection Assignment

Purpose:

```text
select one physical left-to-right seed per bar from the seed-34 detector
candidates.
```

Output:

```text
outputs/experiments/240_detection_assignment_variable_radius_close_spacing_seed34_239
```

Assignment result:

```text
selected left-to-right seeds:
  target 0 seed: rank 3 at x=188, z=85
  target 1 seed: rank 2 at x=248, z=90
  target 2 seed: rank 1 at x=312, z=95
```

Plot validation:

```text
detector_assignment.png: 1444x1005 px, dynamic range 255, std 37.19
FIGURE_NOTES.md exists.
```

Pause-and-ponder decision:

```text
run the location-only coordinate stage with radii fixed at 6 mm. If the
pattern from seeds 13 and 21 holds, target 0 and target 1 should correct to
z=90, while target 2 may again move to the small/shallow surrogate at z=85.
```

## 241-242: Seed-34 Location-Only Coordinate Stage

Purpose:

```text
repeat the staged pipeline's location-only coordinate correction on seed 34.
```

Outputs:

```text
241: outputs/experiments/241_assigned_coordinate_command_variable_radius_location_only_seed34_239
242: outputs/experiments/242_coordinate_optimizer_variable_radius_location_only_seed34
```

Setup:

```text
initial seeds from 240: x=[188,248,312], z=[85,90,95], r=[6,6,6]
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
target order: 0,1,2
x offsets: -2:2:1 mm
z offsets: -10,-5,0,5 mm
radius offsets: 0
backend: gpu-cpml, 1 mm forward grid, 5 sources
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 962.5 s
initial: x=[188,248,312], z=[85,90,95], r=[6,6,6]
final update-case state: x=[190,250,310], z=[90,90,85], r=[6,6,6]
target 0 update case: x=190, z=90, r=6
target 1 update case: x=250, z=90, r=6
target 2 update case: x=310, z=85, r=6
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 29.81
FIGURE_NOTES.md exists and notes that radius margins are missing because
radius was fixed.
```

Verdict:

```text
seed 34 repeats the seed 13/21 location-only pattern. Location-only correction
fixes target 0 and target 1, but the large 8 mm target 2 is again represented
as a small/shallow 6 mm bar at z=85 mm.
```

Pause-and-ponder decision:

```text
run the focused target-2 coupled x/z/r polish from
x=[190,250,310], z=[90,90,85], r=[6,6,6].
```

## 243: Seed-34 Focused Target-2 Coupled x/z/r Polish

Purpose:

```text
test whether focused target-2 recovery holds for a third noise seed after the
same location-only small/shallow surrogate appears.
```

Output:

```text
outputs/experiments/243_coordinate_optimizer_variable_radius_target2_after_location_polish_seed34
```

Setup:

```text
truth: x=[190,250,310], z=[90,90,90], r=[5,6,8]
initial state: x=[190,250,310], z=[90,90,85], r=[6,6,6]
updated target: target 2 only
main candidate grid: x offsets -2:2:1 mm, z offsets 0,5,10 mm,
  radius offsets -1:2:0.5 mm
cases: noise10_seed34 and source_mismatch_noise10_seed34
backend: gpu-cpml, 1 mm forward grid, 5 sources
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 1696.5 s
final state: x=[190,250,309], z=[90,90,90], r=[6,6,8]
noise10_seed34 best: x=310, z=90, r=8, margin=7.24390e-03, strong
source_mismatch_noise10_seed34 best: x=309, z=90, r=8, margin=8.71475e-03,
  strong
radius-ambiguity revisit: not triggered
```

Candidate detail:

```text
for the source-mismatch update case, x=309,z=90,r=8 misfit=0.11889191 and
x=310,z=90,r=8 misfit=0.11899114. The selected x=309 branch is only
9.92e-05 lower in objective than the true x=310 branch.
```

Landscape validation:

```text
source-mismatch z/radius landscape: truth z=90,r=8 ranked 1,
  best x at that pair=309, misfit=0.118892
nominal/noisy z/radius landscape: truth z=90,r=8 ranked 1,
  best x at that pair=310, misfit=0.106037
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 83.09
coordinate_step_01_target_2_source_mismatch_z_radius_landscape.png:
  1515x1073 px, dynamic range 255, std 82.55
coordinate_step_01_target_2_noise10_z_radius_landscape.png:
  1515x1073 px, dynamic range 255, std 84.50
FIGURE_NOTES.md includes the confidence plot and both z/radius landscapes.
```

Verdict:

```text
seed 34 confirms the depth/radius part of the focused target-2 stage, but
reveals a small 1 mm lateral ambiguity under the source-mismatch update case.
The radius/depth evidence is strong; x=309 and x=310 are nearly tied.
```

Pause-and-ponder decision:

```text
continue the realistic staged pipeline by running joint radius estimation at
the recovered x/z state x=[190,250,309], z=[90,90,90]. This asks whether the
final radius tuple is robust to the 1 mm lateral ambiguity.
```

## 244: Seed-34 Joint Radius Tuple Diagnostic at Recovered x=309 State

Purpose:

```text
test whether joint/block radius estimation still recovers [5,6,8] when the
seed-34 staged coordinate state has a 1 mm lateral target-2 ambiguity.
```

Output:

```text
outputs/experiments/244_joint_radius_variable_radius_staged_xz_seed34_x309
```

Setup:

```text
truth x/z/r: x=[190,250,310], z=[90,90,90], r=[5,6,8]
candidate x/z: x=[190,250,309], z=[90,90,90]
radius tuple grid: each radius in 5:8:0.5 mm
tuple count: 343
cases: noise10_seed34 and source_mismatch_noise10_seed34
backend: gpu-cpml, 1 mm forward grid, 5 sources
```

Status:

```text
interrupted before completion during the VS Code/OOM crash recovery window.
The saved Codex transcript shows progress at 1/343 and 25/343 tuples, with
25/343 reached after 399.2 s. A recovery audit found no matching process
running and the output directory has empty data/ and figures/ folders only,
so this run needs to be restarted before it can support a conclusion.
```

Restart:

```text
2026-06-01 local: restarted as detached PID 3346220 with --outdir pointing to
the same 244 output directory, --progress-every 10, and --checkpoint-every 10.
The launcher log is run.log and partial candidate checkpoints are written under
data/ as joint_radius_candidates_checkpoint.csv and joint_radius_checkpoint.json.
BLAS thread counts were capped at 1 to reduce RAM pressure during the marathon.
```

Recovery hardening:

```text
run_multi_rebar_joint_radius_profile.py now writes atomic partial-candidate
checkpoints during the tuple grid and supports --resume-from-checkpoint for
future restarts. Focused checkpoint/resume helper tests passed.
```

Result:

```text
completed restarted GPU run.
elapsed: 5535.5 s
tuple count: 343
candidate x/z: x=[190,250,309], z=[90,90,90]

noise10_seed34:
  best tuple: [5.0,6.0,8.0], misfit=0.0965887398
  truth tuple rank: 1
  top-2 margin: 1.14127e-05

source_mismatch_noise10_seed34:
  best tuple: [5.5,6.0,8.0], misfit=0.1058759480
  truth tuple [5.0,6.0,8.0] rank: 2, misfit=0.1058932097
  top-2 margin: 1.72616e-05
```

Plot validation:

```text
joint_radius_top_candidates.png: 1804x1039 px, dynamic range 255, std 79.71
FIGURE_NOTES.md exists.
```

Verdict:

```text
the final radius tuple stage is robust for the nominal/noisy seed-34 case, but
the source-mismatch case exposes a very weak left-radius ambiguity: [5.5,6,8]
beats the true [5,6,8] by only 1.73e-05 misfit. This is far below a strong
margin and should be reported as a [5.0,5.5] left-radius uncertainty rather
than as a confident radius error.
```

Pause-and-ponder decision:

```text
run the same seed-34 joint-radius diagnostic at x=[190,250,310],
z=[90,90,90]. This separates two explanations:
  1. the 1 mm target-2 lateral ambiguity at x=309 perturbs the block-radius
     objective enough to tie left radius 5.0 and 5.5 mm;
  2. seed-34/source-mismatch noise itself makes the left radius ambiguous even
     when x/z are exact.
```

## 245: Target-2 Focused Polish Aggregate, Seeds 13, 21, and 34

Purpose:

```text
update the focused target-2 aggregate after the third seed-34 focused-polish
run.
```

Output:

```text
outputs/experiments/245_coordinate_confidence_aggregate_variable_radius_target2_seed13_21_34
```

Result:

```text
rows: 6
truth-geometry rows: 5
confidence labels: strong=6
radius margin min/mean/max:
  6.42653e-03 / 7.90658e-03 / 9.56024e-03
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 71.10
FIGURE_NOTES.md exists.
```

Interpretation:

```text
target-2 depth and radius recovery is strong across all three seeds. The only
non-truth-geometry row is seed 34 source-mismatch, where x=309 mm is selected
instead of x=310 mm with a very small objective difference. This should be
reported as lateral uncertainty, not radius/depth failure.
```

## 246: Target-2 Focused Polish Objective Diagnostic, Seeds 13, 21, and 34

Purpose:

```text
update the high-band diagnostic check after seed 34.
```

Output:

```text
outputs/experiments/246_coordinate_objective_diagnostic_target2_focus_seed13_21_34
```

Result:

```text
rows: 6
highband truth rows: 1
base truth rows: 5
highband geometry-change rows: 4
highband/base margin ratio mean: 0.93720
margin ratio range: 0.80064 to 1.07144
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png: 2059x1005 px, dynamic range 255,
std 81.73
FIGURE_NOTES.md exists.
```

Interpretation:

```text
the high-band objective still should not become the update rule. It changes
geometry in 4 of 6 rows and matches full truth geometry in only 1 of 6 rows.
Keep high-band as diagnostic evidence only.
```

## 247: Seed-34 Joint Radius Tuple Diagnostic at x=310 State

Purpose:

```text
separate whether experiment 244's tiny source-mismatch radius-tuple tie was
caused by the recovered target-2 x=309 lateral ambiguity, or by seed-34/source
mismatch noise even when x/z are exact.
```

Output:

```text
outputs/experiments/247_joint_radius_variable_radius_staged_xz_seed34_x310
```

Setup:

```text
truth x/z/r: x=[190,250,310], z=[90,90,90], r=[5,6,8]
candidate x/z: x=[190,250,310], z=[90,90,90]
radius tuple grid: each radius in 5:8:0.5 mm
tuple count: 343
cases: noise10_seed34 and source_mismatch_noise10_seed34
backend: gpu-cpml, 1 mm forward grid, 5 sources
checkpointing: every 10 tuples, resumable with --resume-from-checkpoint
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 5504.6 s
tuple count: 343
candidate x/z: x=[190,250,310], z=[90,90,90]

noise10_seed34:
  best tuple: [5.0,6.0,8.0], misfit=0.0891242008
  truth tuple rank: 1
  top-2 margin: 3.29682e-03

source_mismatch_noise10_seed34:
  best tuple: [5.0,6.0,8.0], misfit=0.0973287944
  truth tuple rank: 1
  top-2 margin: 4.01541e-03
```

Plot validation:

```text
joint_radius_top_candidates.png: 1804x1039 px, dynamic range 255, std 79.67
FIGURE_NOTES.md exists.
```

Interpretation:

```text
when target 2 is fixed at x=310 mm, the seed-34 joint-radius stage recovers
the true [5,6,8] tuple with strong top-2 separation. Therefore experiment
244's source-mismatch [5.5,6,8] winner was caused by the prior 1 mm lateral
x ambiguity at target 2, not by an inherent seed-34 radius/objective failure.
Report seed34 as: exact depth and large-bar radius, target-2 x interval
309-310 mm, and left-radius tuple uncertainty 5.0-5.5 mm only if the x=309
branch is used.
```

## 248: Staged Variable-Radius Pipeline Summary, Seeds 13, 21, and 34

Purpose:

```text
summarize the realistic staged variable-radius pipeline across three noise
seeds, using seed34's recovered x=309 final state from experiment 244.
```

Output:

```text
outputs/experiments/248_variable_radius_staged_pipeline_seed13_21_34_summary
```

Input chains:

```text
seed 13:
  detection 216 -> location-only 225 -> target-2 polish 227 -> joint radii 222
seed 21:
  detection 230 -> location-only 233 -> target-2 polish 234 -> joint radii 235
seed 34 realistic x309:
  detection 239 -> location-only 242 -> target-2 polish 243 -> joint radii 244
```

Result:

```text
seed13 joint best: [5,6,8], truth rank=1, top-2 margin=4.31460e-03
seed21 joint best: [5,6,8], truth rank=1, top-2 margin=5.04798e-03
seed34_x309 joint best: [5.5,6,8], truth rank=2, top-2 margin=1.72616e-05

seed34_x309 max final errors:
  x=1.0 mm
  z=0.0 mm
  radius=0.5 mm
```

Plot validation:

```text
staged_variable_radius_pipeline_errors.png: 1719x971 px, dynamic range 255,
std 41.43
FIGURE_NOTES.md exists and reports joint best radii, truth ranks, and top-2
margins for all three seeds.
```

Interpretation:

```text
the staged policy is strongly replicated for seeds 13 and 21. Seed 34 remains
scientifically usable but must be reported with uncertainty: the point chain
has a 1 mm target-2 lateral ambiguity and a weak left-radius 5.0/5.5 mm tie.
Experiment 247 shows that exact x=310 removes the radius tie and recovers the
true [5,6,8] tuple with strong separation.
```

## 249: Target-2 Focused Polish Aggregate With x-Ambiguity Widths

Purpose:

```text
make the target-2 lateral ambiguity explicit in the aggregate report, instead
of only plotting radius confidence margins.
```

Output:

```text
outputs/experiments/249_coordinate_confidence_aggregate_variable_radius_target2_seed13_21_34_xambiguity
```

Implementation:

```text
run_coordinate_confidence_aggregate.py now adds ambiguity_x_width_mm,
ambiguity_z_width_mm, and ambiguity_radius_width_mm to enriched rows; the JSON
aggregate reports max ambiguity widths and row counts; figures include a new
coordinate_ambiguity_widths.png plot.
```

Result:

```text
rows: 6
truth-geometry rows: 5
confidence labels: strong=6
x-ambiguity rows: 6
max x/z/r ambiguity width: 1.0 / 0.0 / 0.0 mm
radius margin min/mean/max:
  6.42653e-03 / 7.90658e-03 / 9.56024e-03
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 71.10
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 47.27
FIGURE_NOTES.md describes both plots.
```

Interpretation:

```text
the target-2 focused-polish stage is radius/depth strong across all three
seeds, but every row retains a 1 mm x ambiguity interval. The publication or
handoff result should therefore report target-2 x as 309-310 mm unless an
additional lateral disambiguation stage is added.
```

## 250: Seed-34 Target-2 Focused Polish With 9 Scan Positions

Purpose:

```text
test whether denser acquisition breaks the target-2 lateral x=309/310 mm tie
seen in the standard 5-source focused polish.
```

Output:

```text
outputs/experiments/250_coordinate_optimizer_variable_radius_target2_seed34_sources9
```

Setup:

```text
same seed-34 focused target-2 x/z/r polish as experiment 243, except sources=9
instead of sources=5. Truth remains x=[190,250,310], z=[90,90,90],
r=[5,6,8]. Initial state remains x=[190,250,310], z=[90,90,85], r=[6,6,6].
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 3108.1 s
final state: x=[190,250,310], z=[90,90,90], r=[6,6,8]

noise10_seed34:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.08704764
  best misfit=0.08526931
  radius margin=5.54072e-03, strong
  ambiguity x interval: 310-310 mm

source_mismatch_noise10_seed34:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.09507250
  best misfit=0.09258073
  radius margin=7.35509e-03, strong
  ambiguity x interval: 310-310 mm
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.37
FIGURE_NOTES.md exists.
```

Interpretation:

```text
denser acquisition removes the target-2 lateral x ambiguity for seed34 in this
controlled synthetic setting. With 9 scan positions, both nominal/noisy and
source-mismatch/noisy cases choose x=310 with no near-best x=309 candidate
inside the ambiguity interval. Acquisition density is therefore a viable
method lever for resolving the 309-310 mm tie seen with 5 sources.
```

## 251: Seed-34 Target-2 Sources 5 vs 9 Aggregate

Purpose:

```text
compare the standard 5-source focused-polish rows against the 9-source rerun
to separate radius confidence from lateral x ambiguity.
```

Output:

```text
outputs/experiments/251_coordinate_confidence_aggregate_seed34_target2_sources5_vs_sources9
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  --run-name coordinate_confidence_aggregate_seed34_target2_sources5_vs_sources9 \
  outputs/experiments/243_coordinate_optimizer_variable_radius_target2_after_location_polish_seed34/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/250_coordinate_optimizer_variable_radius_target2_seed34_sources9/data/multi_rebar_coordinate_optimizer_summary.json
```

Result:

```text
rows: 4
truth-geometry rows: 3
confidence labels: strong=4
radius margin min/mean/max:
  5.54072e-03 / 7.21361e-03 / 8.71475e-03

5-source rows:
  x ambiguity width: 1.0 mm in both cases
  source-mismatch best x: 309 mm

9-source rows:
  x ambiguity width: 0.0 mm in both cases
  nominal and source-mismatch best x: 310 mm
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1718x971 px, dynamic range 255, std 77.81
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 38.48
FIGURE_NOTES.md describes both plots.
```

Interpretation:

```text
the 9-source rerun does not merely keep the radius margin strong; it collapses
the target-2 lateral ambiguity interval from 309-310 mm to 310-310 mm under
both nominal/noisy and source-mismatch/noisy cases. This makes acquisition
density a credible disambiguation lever. The next dose-response check is a
7-source focused polish to see whether the cheaper intermediate acquisition
already resolves the tie.
```

## 252: Seed-34 Target-2 Focused Polish With 7 Scan Positions

Purpose:

```text
run the acquisition-density dose-response between the standard 5-source
focused polish and the successful 9-source focused polish. The decision gate
is whether 7 sources already collapses the target-2 x interval to 310-310 mm.
```

Output:

```text
outputs/experiments/252_coordinate_optimizer_variable_radius_target2_seed34_sources7
```

Source positions:

```text
sources=5: 50, 146, 250, 346, 450 mm
sources=7: 50, 114, 178, 250, 314, 378, 450 mm
sources=9: 50, 98, 146, 194, 250, 298, 346, 394, 450 mm
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 7 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,310 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,310 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.1,34|source_mismatch_noise10_seed34:1.1,-50,1.1,0.1,34' \
  --update-case-label source_mismatch_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_variable_radius_target2_seed34_sources7 \
  --outdir outputs/experiments/252_coordinate_optimizer_variable_radius_target2_seed34_sources7
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 2305.6 s
final state: x=[190,250,310], z=[90,90,90], r=[6,6,8]

noise10_seed34:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.08209375
  best misfit=0.08040277
  x309-minus-x310 gap at z=90,r=8: 1.69098e-03
  radius margin=5.39179e-03, strong
  ambiguity x interval: 310-310 mm

source_mismatch_noise10_seed34:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.08952637
  best misfit=0.08778171
  x309-minus-x310 gap at z=90,r=8: 1.74466e-03
  radius margin=6.53863e-03, strong
  ambiguity x interval: 310-310 mm
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 91.14
FIGURE_NOTES.md exists.
```

Interpretation:

```text
7 scan positions are enough to remove the target-2 x=309/310 mm ambiguity in
this seed34 focused-polish case. The source-mismatch row flips from x=309 at
5 sources to x=310 at 7 sources, with a 1.74e-03 objective separation against
the x=309 competitor. Since 7 sources also avoids the ambiguity interval seen
with 5 sources, prefer 7 sources as the cheaper acquisition-density
refinement; keep 9 sources as a stronger but costlier confirmation setting.
```

## 253: Seed-34 Target-2 Sources 5/7/9 Aggregate

Purpose:

```text
combine the standard 5-source run, the 7-source threshold run, and the
9-source confirmation run with source-count-aware aggregate reporting.
```

Output:

```text
outputs/experiments/253_coordinate_confidence_aggregate_seed34_target2_sources5_7_9
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  --run-name coordinate_confidence_aggregate_seed34_target2_sources5_7_9 \
  outputs/experiments/243_coordinate_optimizer_variable_radius_target2_after_location_polish_seed34/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/252_coordinate_optimizer_variable_radius_target2_seed34_sources7/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/250_coordinate_optimizer_variable_radius_target2_seed34_sources9/data/multi_rebar_coordinate_optimizer_summary.json
```

Implementation:

```text
run_coordinate_confidence_aggregate.py now propagates sources and
frequency_ghz into enriched rows, adds per-source-count summaries, and labels
aggregate plot rows with source counts.
```

Result:

```text
rows: 6
truth-geometry rows: 5
confidence labels: strong=6
radius margin min/mean/max:
  5.39179e-03 / 6.79748e-03 / 8.71475e-03
max x/z/r ambiguity width: 1.0 / 0.0 / 0.0 mm

source summary:
  5 sources: rows=2, truth-geometry rows=1, x-ambiguity rows=2
  7 sources: rows=2, truth-geometry rows=2, x-ambiguity rows=0
  9 sources: rows=2, truth-geometry rows=2, x-ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 75.81
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 37.62
FIGURE_NOTES.md includes per-source-count summary.
```

Interpretation:

```text
the acquisition-density threshold for this controlled seed34 target-2 case is
at or below 7 scan positions. Five sources keep strong radius confidence but
retain a lateral x interval and one wrong point x under source mismatch; 7 and
9 sources both recover the true point geometry with zero x-ambiguity rows.
```

## 254: Seed-13 Target-2 Focused Polish With 7 Scan Positions

Purpose:

```text
test whether the 7-source ambiguity reduction seen on seed34 generalizes to a
seed where the standard 5-source run already selected the true point geometry
but still retained a 309-310 mm x ambiguity interval.
```

Output:

```text
outputs/experiments/254_coordinate_optimizer_variable_radius_target2_seed13_sources7
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 7 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,310 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,310 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.1,13|source_mismatch_noise10_seed13:1.1,-50,1.1,0.1,13' \
  --update-case-label source_mismatch_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_variable_radius_target2_seed13_sources7 \
  --outdir outputs/experiments/254_coordinate_optimizer_variable_radius_target2_seed13_sources7
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 2306.0 s
final state: x=[190,250,310], z=[90,90,90], r=[6,6,8]

noise10_seed13:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.08416236
  best misfit=0.08201994
  x309-minus-x310 gap at z=90,r=8: 2.14242e-03
  radius margin=6.36662e-03, strong
  ambiguity x interval: 310-310 mm

source_mismatch_noise10_seed13:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.08928957
  best misfit=0.08709067
  x309-minus-x310 gap at z=90,r=8: 2.19891e-03
  radius margin=6.76235e-03, strong
  ambiguity x interval: 310-310 mm
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 92.18
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed13 matches the seed34 7-source behavior. The standard 5-source run had
the correct point x=310 in both cases but retained a 309-310 mm ambiguity
interval; 7 sources remove that interval and increase the x=309/x=310
separation to roughly 2.1-2.2e-03.
```

## 255: Seed-21 Target-2 Focused Polish With 7 Scan Positions

Purpose:

```text
complete the cross-seed 7-source robustness check for the target-2 focused
polish stage. Seed21 was already point-correct with 5 sources but retained the
same 309-310 mm x ambiguity interval in aggregate reporting.
```

Output:

```text
outputs/experiments/255_coordinate_optimizer_variable_radius_target2_seed21_sources7
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 7 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,310 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,310 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed21:1.0,0.0,1.0,0.1,21|source_mismatch_noise10_seed21:1.1,-50,1.1,0.1,21' \
  --update-case-label source_mismatch_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_variable_radius_target2_seed21_sources7 \
  --outdir outputs/experiments/255_coordinate_optimizer_variable_radius_target2_seed21_sources7
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 2372.2 s
final state: x=[190,250,310], z=[90,90,90], r=[6,6,8]

noise10_seed21:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.08279599
  best misfit=0.08101617
  x309-minus-x310 gap at z=90,r=8: 1.77982e-03
  radius margin=6.15010e-03, strong
  ambiguity x interval: 310-310 mm

source_mismatch_noise10_seed21:
  best: x=310, z=90, r=8
  competing x=309,z=90,r=8 misfit=0.08802209
  best misfit=0.08644082
  x309-minus-x310 gap at z=90,r=8: 1.58127e-03
  radius margin=5.92622e-03, strong
  ambiguity x interval: 310-310 mm
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 92.35
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed21 also matches the seed13/seed34 7-source result: both target-2 focused
polish rows recover the true point geometry with no x ambiguity interval.
Across all three seeds, the 7-source acquisition removes the 1 mm x interval
that remained in the standard 5-source focused-polish rows.
```

## 256: Target-2 Sources 5 vs 7 Cross-Seed Aggregate

Purpose:

```text
aggregate seeds 13, 21, and 34 to decide whether 7-source focused polishing
should be the recommended lateral-disambiguation refinement for the
variable-radius close-spacing target-2 stage.
```

Output:

```text
outputs/experiments/256_coordinate_confidence_aggregate_variable_radius_target2_seeds13_21_34_sources5_vs7
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  --run-name coordinate_confidence_aggregate_variable_radius_target2_seeds13_21_34_sources5_vs7 \
  outputs/experiments/227_coordinate_optimizer_variable_radius_target2_after_location_polish_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/234_coordinate_optimizer_variable_radius_target2_after_location_polish_seed21/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/243_coordinate_optimizer_variable_radius_target2_after_location_polish_seed34/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/254_coordinate_optimizer_variable_radius_target2_seed13_sources7/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/255_coordinate_optimizer_variable_radius_target2_seed21_sources7/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/252_coordinate_optimizer_variable_radius_target2_seed34_sources7/data/multi_rebar_coordinate_optimizer_summary.json
```

Result:

```text
rows: 12
truth-geometry rows: 11
confidence labels: strong=12
radius margin min/mean/max:
  5.39179e-03 / 7.04793e-03 / 9.56024e-03
max x/z/r ambiguity width: 1.0 / 0.0 / 0.0 mm

source summary:
  5 sources: rows=6, truth-geometry rows=5, x-ambiguity rows=6
  7 sources: rows=6, truth-geometry rows=6, x-ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255, std 75.61
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255, std 44.95
FIGURE_NOTES.md includes per-source-count summary.
```

Interpretation:

```text
the 7-source focused-polish setting generalizes across seeds 13, 21, and 34
for this target-2 variable-radius close-spacing case. It converts all six
focused-polish rows from interval-valued x estimates to point x=310 estimates,
while keeping every radius margin strong. The recommended policy is now:
standard 5-source runs report x intervals; 7-source focused polishing is the
default optional refinement when a single lateral coordinate is required.
```

## 257: Staged Pipeline Summary With 7-Source Focused Refinement

Purpose:

```text
package the 7-source focused-polish option into the staged variable-radius
summary/report path instead of leaving it as separate manual reruns.
```

Output:

```text
outputs/experiments/257_variable_radius_staged_pipeline_seed13_21_34_sources7_refinement_summary
```

Implementation:

```text
run_variable_radius_staged_pipeline_summary.py now accepts an optional sixth
case field, focused_refinement_json. When present, the summary records
standard focused x-ambiguity rows, refined focused x-ambiguity rows, refined
stage errors, and a focused_policy field such as use_refined_focus_for_point_x.
```

Result:

```text
seed13:
  focused 5-source x-ambiguity rows: 2
  refined 7-source x-ambiguity rows: 0
  focused policy: use_refined_focus_for_point_x
  joint best: [5,6,8], truth rank=1, top-2 margin=4.31460e-03

seed21:
  focused 5-source x-ambiguity rows: 2
  refined 7-source x-ambiguity rows: 0
  focused policy: use_refined_focus_for_point_x
  joint best: [5,6,8], truth rank=1, top-2 margin=5.04798e-03

seed34_sources7:
  focused 5-source x-ambiguity rows: 2
  refined 7-source x-ambiguity rows: 0
  focused policy: use_refined_focus_for_point_x
  joint best: [5,6,8], truth rank=1, top-2 margin=4.01541e-03
```

Plot validation:

```text
staged_variable_radius_pipeline_errors.png: 1753x971 px, dynamic range 255,
std 45.85
FIGURE_NOTES.md lists focused policy per seed.
```

Interpretation:

```text
the staged variable-radius report can now express the recommended policy:
run economical 5-source focused polishing first, report x intervals when they
remain, and attach a 7-source focused refinement when a point x coordinate is
needed. With that refinement, all three seed13/21/34 staged paths reach exact
x/z/r after the joint radius stage.
```

## 258: Harder Close-Spacing Target-2 Focused Polish, x=300, Sources=5

Purpose:

```text
start a nearby-geometry robustness check by moving the large right bar from
x=310 mm to x=300 mm, reducing center-right spacing from 60 mm to 50 mm. This
5-source run is the baseline before testing whether the 7-source refinement
still removes lateral ambiguity in the harder spacing.
```

Output:

```text
outputs/experiments/258_coordinate_optimizer_variable_radius_target2_close50_seed34_sources5
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,300 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,300 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.1,34|source_mismatch_noise10_seed34:1.1,-50,1.1,0.1,34' \
  --update-case-label source_mismatch_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_variable_radius_target2_close50_seed34_sources5 \
  --outdir outputs/experiments/258_coordinate_optimizer_variable_radius_target2_close50_seed34_sources5
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 1689.0 s
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]

noise10_seed34:
  best: x=299, z=90, r=8
  true x=300,z=90,r=8 misfit=0.09569018
  best misfit=0.09535616
  x299-minus-x300 gap at z=90,r=8: -3.34026e-04
  radius margin=5.92450e-03, strong
  ambiguity x interval: 299-300 mm

source_mismatch_noise10_seed34:
  best: x=300, z=90, r=8
  competing x=299,z=90,r=8 misfit=0.10416962
  best misfit=0.10220577
  x299-minus-x300 gap at z=90,r=8: 1.96385e-03
  radius margin=8.03466e-03, strong
  ambiguity x interval: 300-300 mm
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 90.28
FIGURE_NOTES.md exists.
```

Interpretation:

```text
the harder 50 mm center-right spacing reproduces the core lateral ambiguity:
5 sources keep radius/depth strong but the nominal/noisy row selects x=299 mm
with the true x=300 mm inside the ambiguity interval. This justifies the
paired 7-source run before deciding whether the acquisition-density policy
generalizes beyond the original 60 mm spacing.
```

## 259: Harder Close-Spacing Target-2 Focused Polish, x=300, Sources=7

Purpose:

```text
test whether the 7-source focused-polish refinement removes the x=299/300 mm
ambiguity found in experiment 258 for the harder 50 mm center-right spacing.
```

Output:

```text
outputs/experiments/259_coordinate_optimizer_variable_radius_target2_close50_seed34_sources7
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 7 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,300 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,300 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.1,34|source_mismatch_noise10_seed34:1.1,-50,1.1,0.1,34' \
  --update-case-label source_mismatch_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_variable_radius_target2_close50_seed34_sources7 \
  --outdir outputs/experiments/259_coordinate_optimizer_variable_radius_target2_close50_seed34_sources7
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 2329.8 s
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]

noise10_seed34:
  best: x=300, z=90, r=8
  competing x=299,z=90,r=8 misfit=0.08374229
  best misfit=0.08268180
  x299-minus-x300 gap at z=90,r=8: 1.06048e-03
  radius margin=5.70626e-03, strong
  ambiguity x interval: 299-300 mm

source_mismatch_noise10_seed34:
  best: x=300, z=90, r=8
  competing x=299,z=90,r=8 misfit=0.08767527
  best misfit=0.08576258
  x299-minus-x300 gap at z=90,r=8: 1.91269e-03
  radius margin=6.32126e-03, strong
  ambiguity x interval: 300-300 mm
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 91.85
FIGURE_NOTES.md exists.
```

Interpretation:

```text
7 sources fix the point estimate for the close-50 nominal row, changing the
best x from 299 to the true 300 mm. However, x=299 remains inside the
near-best ambiguity interval for the nominal/noisy row. This is a partial
generalization: 7-source refinement corrects the selected point but does not
fully collapse the interval in the harder 50 mm spacing.
```

## 260: Harder Close-Spacing Sources 5 vs 7 Aggregate

Purpose:

```text
compare the close-50 seed34 5-source and 7-source focused-polish rows and
separate point-coordinate correction from full ambiguity-interval collapse.
```

Output:

```text
outputs/experiments/260_coordinate_confidence_aggregate_close50_seed34_sources5_vs7
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  --run-name coordinate_confidence_aggregate_close50_seed34_sources5_vs7 \
  outputs/experiments/258_coordinate_optimizer_variable_radius_target2_close50_seed34_sources5/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/259_coordinate_optimizer_variable_radius_target2_close50_seed34_sources7/data/multi_rebar_coordinate_optimizer_summary.json
```

Result:

```text
rows: 4
truth-geometry rows: 3
confidence labels: strong=4
radius margin min/mean/max:
  5.70626e-03 / 6.49667e-03 / 8.03466e-03

source summary:
  5 sources: rows=2, truth-geometry rows=1, x-ambiguity rows=1
  7 sources: rows=2, truth-geometry rows=2, x-ambiguity rows=1
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1718x971 px, dynamic range 255, std 78.47
coordinate_ambiguity_widths.png: 1718x971 px, dynamic range 255, std 39.06
FIGURE_NOTES.md includes per-source-count summary.
```

Interpretation:

```text
for 50 mm center-right spacing, 7 sources improve point accuracy but are not
sufficient to remove every x-ambiguity row. The next acquisition-density check
should test 9 sources on this same close-50 geometry before claiming that the
7-source rule generalizes to tighter spacing.
```

## 261: Harder Close-Spacing Target-2 Focused Polish, x=300, Sources=9

Purpose:

```text
test whether 9 scan positions collapse the remaining nominal/noisy x=299-300
ambiguity interval in the 50 mm close-spacing geometry where 7 sources fixed
the point estimate but not the interval.
```

Output:

```text
outputs/experiments/261_coordinate_optimizer_variable_radius_target2_close50_seed34_sources9
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 9 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,300 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,300 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.1,34|source_mismatch_noise10_seed34:1.1,-50,1.1,0.1,34' \
  --update-case-label source_mismatch_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_variable_radius_target2_close50_seed34_sources9 \
  --outdir outputs/experiments/261_coordinate_optimizer_variable_radius_target2_close50_seed34_sources9
```

Status:

```text
completed GPU experiment.
```

Result:

```text
elapsed: 3068.4 s
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]

noise10_seed34:
  best: x=300, z=90, r=8
  competing x=299,z=90,r=8 misfit=0.08953523
  best misfit=0.08854008
  x299-minus-x300 gap at z=90,r=8: 9.95150e-04
  radius margin=5.69705e-03, strong
  ambiguity x interval: 299-300 mm

source_mismatch_noise10_seed34:
  best: x=300, z=90, r=8
  competing x=299,z=90,r=8 misfit=0.09582823
  best misfit=0.09379103
  x299-minus-x300 gap at z=90,r=8: 2.03721e-03
  radius margin=6.60955e-03, strong
  ambiguity x interval: 300-300 mm
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 91.50
FIGURE_NOTES.md exists.
```

Interpretation:

```text
9 sources do not collapse the close-50 nominal/noisy x interval either. The
point estimate is correct, but x=299 mm remains within the ambiguity threshold
alongside the true x=300 mm. Acquisition density up to 9 scan positions is
therefore insufficient for deterministic lateral x at this tighter spacing.
```

## 262: Harder Close-Spacing Sources 5/7/9 Aggregate

Purpose:

```text
summarize the close-50 acquisition-density dose response across 5, 7, and
9 scan positions.
```

Output:

```text
outputs/experiments/262_coordinate_confidence_aggregate_close50_seed34_sources5_7_9
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  --run-name coordinate_confidence_aggregate_close50_seed34_sources5_7_9 \
  outputs/experiments/258_coordinate_optimizer_variable_radius_target2_close50_seed34_sources5/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/259_coordinate_optimizer_variable_radius_target2_close50_seed34_sources7/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/261_coordinate_optimizer_variable_radius_target2_close50_seed34_sources9/data/multi_rebar_coordinate_optimizer_summary.json
```

Result:

```text
rows: 6
truth-geometry rows: 5
confidence labels: strong=6
radius margin min/mean/max:
  5.69705e-03 / 6.38221e-03 / 8.03466e-03

source summary:
  5 sources: rows=2, truth-geometry rows=1, x-ambiguity rows=1
  7 sources: rows=2, truth-geometry rows=2, x-ambiguity rows=1
  9 sources: rows=2, truth-geometry rows=2, x-ambiguity rows=1
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 77.41
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 40.57
FIGURE_NOTES.md includes per-source-count summary.
```

Interpretation:

```text
for 50 mm center-right spacing, denser acquisition improves the point estimate
but not the nominal/noisy ambiguity interval. The robust report should state:
60 mm spacing supports 7-source point refinement with zero x-ambiguity rows;
50 mm spacing remains interval-valued even at 9 sources under this objective
and ambiguity threshold.
```

## 263: Lateral Gap Threshold Summary, Close50 vs Close60

Purpose:

```text
quantify why 7 sources collapse the original 60 mm spacing interval but 9
sources still fail to collapse the tighter 50 mm spacing interval under the
default 1.5% ambiguity threshold.
```

Output:

```text
outputs/experiments/263_lateral_gap_threshold_close50_vs_close60_summary
```

Result:

```text
default ambiguity threshold: 1.5% above best/true misfit

close60 nominal/noisy left-neighbor relative gaps:
  sources=5: 0.443%
  sources=7: 2.103%
  sources=9: 2.086%

close50 nominal/noisy left-neighbor relative gaps:
  sources=5: -0.349% (left neighbor is the point best)
  sources=7: 1.283%
  sources=9: 1.124%
```

Plot validation:

```text
lateral_neighbor_gap_thresholds.png: 1680x928 px, dynamic range 255,
std 28.99
FIGURE_NOTES.md explains the 1.5% threshold line.
```

Interpretation:

```text
the threshold analysis explains the spacing-dependent behavior. At 60 mm
spacing, 7 and 9 sources push the nearest-left x competitor above the 1.5%
ambiguity threshold. At 50 mm spacing, even 9 sources leave the nominal/noisy
left competitor below the threshold. A stricter threshold could force a point
answer, but the current evidence says the honest result is an interval unless
a new objective or acquisition geometry increases the lateral gap.
```

## 264: Coordinate Objective Top-Candidate Reporting Smoke

Purpose:

```text
add and validate a coordinate-optimizer CSV that flattens ranked top candidates
for each diagnostic objective variant. The close-50 high-band summaries looked
promising, but the prior coordinate optimizer output only exposed the best
candidate per objective in CSV form; this smoke run verifies that future runs
will preserve ranked competitors for ambiguity inspection.
```

Output:

```text
outputs/experiments/264_coordinate_objective_top_candidate_reporting_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend cpu \
  --grid-step-mm 20 \
  --sources 1 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,300 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,300 \
  --initial-z-values-mm 90,90,90 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm 0 \
  --z-offsets-mm 0 \
  --radius-offsets-mm 0 \
  --replication-cases 'smoke:1.0,0.0,1.0,0.0,0' \
  --update-case-label smoke \
  --source-frequency-scales 1.0 \
  --source-time-shift-ps-values=0 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --top-k 3 \
  --progress-every 1 \
  --run-name coordinate_objective_top_candidate_reporting_smoke \
  --outdir outputs/experiments/264_coordinate_objective_top_candidate_reporting_smoke
```

Result:

```text
new artifact:
  data/coordinate_objective_top_candidates.csv

CSV columns include:
  run_name, case_label, objective_label, rank, pass_index,
  step_target_index, step_kind, x_mm, z_mm, radius_mm,
  x_values_mm, z_values_mm, radii_mm, misfit, and source-profile fields.

smoke rows:
  base rank 1: x=300, z=90, r=8, misfit=0
  highband rank 1: x=300, z=90, r=8, misfit=0

run_manifest.json and the optimizer summary both include
objective_top_candidate_csv.
```

Validation:

```text
unit tests: tests/test_multi_rebar_coordinate_optimizer.py, 15 passed
py_compile: run_multi_rebar_coordinate_optimizer.py and matching test passed
git diff --check for edited optimizer/test files passed
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 26.35
FIGURE_NOTES.md exists.
```

Interpretation:

```text
future coordinate optimizer runs with --diagnostic-objective-variants now write
a ranked top-candidate objective CSV. The next close-50 objective experiment
can inspect high-band competitors such as x=299 versus x=300 directly, rather
than relying only on best-objective summaries.
```

## 265: Close-50 Sources=5 Objective Top-Candidate Diagnostic

Purpose:

```text
rerun the close-50 target-2 sources=5 focused polish with the new ranked
objective top-candidate CSV, so the base and high-band x=299/x=300 competitors
can be compared directly.
```

Output:

```text
outputs/experiments/265_coordinate_optimizer_close50_seed34_sources5_topcandidate_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,300 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,300 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.1,34|source_mismatch_noise10_seed34:1.1,-50,1.1,0.1,34' \
  --update-case-label source_mismatch_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --top-k 20 \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_close50_seed34_sources5_topcandidate_objectives \
  --outdir outputs/experiments/265_coordinate_optimizer_close50_seed34_sources5_topcandidate_objectives
```

Result:

```text
elapsed: 1699.4 s
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

base objective, noise10_seed34:
  rank 1: x=299,z=90,r=8, misfit=0.09535616
  rank 2: x=300,z=90,r=8, misfit=0.09569018
  x299-minus-x300 gap: -3.34026e-04 (-0.3491% relative to x300)

high-band objective, noise10_seed34:
  rank 1: x=300,z=90,r=8, misfit=0.01460155
  rank 2: x=299,z=90,r=8, misfit=0.01481562
  x299-minus-x300 gap: +2.14063e-04 (1.4660% relative to x300)

base objective, source_mismatch_noise10_seed34:
  rank 1: x=300,z=90,r=8, misfit=0.10220577
  rank 2: x=299,z=90,r=8, misfit=0.10416962
  x299-minus-x300 gap: +1.96385e-03 (1.9215% relative to x300)

high-band objective, source_mismatch_noise10_seed34:
  rank 1: x=300,z=90,r=8, misfit=0.02112941
  rank 2: x=299,z=90,r=8, misfit=0.02378779
  x299-minus-x300 gap: +2.65838e-03 (12.5814% relative to x300)
```

Plot/artifact validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 92.80
FIGURE_NOTES.md exists.
coordinate_objective_top_candidates.csv contains base/highband top-20 rows
for both observed cases.
```

Interpretation:

```text
high-band weighting is a useful disambiguation lever but is not yet enough to
claim deterministic close-50 x under the existing 1.5% ambiguity threshold.
For the nominal/noisy row, high-band flips the point estimate from x=299 to
the true x=300, but the x=299 competitor remains only 1.466% above the x=300
misfit. That is just below the current threshold. Source-mismatch/noisy is
well separated under both base and high-band objectives.
```

## 266: Coordinate Optimizer Tx/Rx Offset Smoke

Purpose:

```text
add and smoke-test a coordinate optimizer --tx-rx-offset-mm option so close-50
experiments can test measurement geometry as a real disambiguation lever,
instead of only changing source count, objective weighting, or reporting
thresholds.
```

Output:

```text
outputs/experiments/266_coordinate_optimizer_txrx_offset_reporting_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend cpu \
  --grid-step-mm 20 \
  --sources 1 \
  --tx-rx-offset-mm 40 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,300 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,300 \
  --initial-z-values-mm 90,90,90 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm 0 \
  --z-offsets-mm 0 \
  --radius-offsets-mm 0 \
  --replication-cases 'smoke:1.0,0.0,1.0,0.0,0' \
  --update-case-label smoke \
  --source-frequency-scales 1.0 \
  --source-time-shift-ps-values=0 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --top-k 3 \
  --progress-every 1 \
  --run-name coordinate_optimizer_txrx_offset_reporting_smoke \
  --outdir outputs/experiments/266_coordinate_optimizer_txrx_offset_reporting_smoke
```

Result:

```text
summary records tx_rx_offset_mm: 40.0
summary records scan_x_values_mm: [50.0]
objective top-candidate rows: 2
final state: x=[190,250,300], z=[90,90,90], r=[5,6,8]
```

Validation:

```text
tests: test_multi_rebar_local_geometry_profile.py and
test_multi_rebar_coordinate_optimizer.py, 27 passed
py_compile: common radius profile, coordinate optimizer, and matching tests passed
git diff --check for edited offset files passed
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 26.35
run_manifest.json includes --tx-rx-offset-mm 40.
```

Interpretation:

```text
the coordinate optimizer can now run controlled close50 Tx/Rx geometry
experiments. The first production test should keep the close50 sources=5
target-2 setup fixed and change only the Tx/Rx offset from 20 mm to 40 mm.
```

## 267: Close-50 Sources=5, Tx/Rx Offset 40 mm Objective Diagnostic

Purpose:

```text
test whether changing measurement geometry separates the close-50 target-2
x=299/x=300 ambiguity that remained under the default 20 mm Tx/Rx offset.
This run keeps the experiment-265 setup fixed except for --tx-rx-offset-mm 40.
```

Output:

```text
outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1 \
  --sources 5 \
  --tx-rx-offset-mm 40 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 190,250,300 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 190,250,300 \
  --initial-z-values-mm 90,90,85 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=0,5,10 \
  --radius-offsets-mm=-1:2:0.5 \
  --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.1,34|source_mismatch_noise10_seed34:1.1,-50,1.1,0.1,34' \
  --update-case-label source_mismatch_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' \
  --top-k 20 \
  --revisit-weak-high-radius-targets \
  --revisit-broad-radius-ambiguity-targets \
  --revisit-ambiguity-min-width-mm 0.2 \
  --revisit-x-offsets-mm=-1:1:1 \
  --revisit-z-offsets-mm=-2:2:1 \
  --revisit-radius-step-mm 0.5 \
  --progress-every 25 \
  --run-name coordinate_optimizer_close50_seed34_sources5_txrx40_objectives \
  --outdir outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives
```

Result:

```text
elapsed: 1684.6 s
tx_rx_offset_mm: 40.0
scan x positions: [50,146,250,346,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed34: best x=300,z=90,r=8, strong, x interval 300-300

base objective, noise10_seed34:
  rank 1: x=300,z=90,r=8, misfit=0.03292190
  rank 2: x=299,z=90,r=8, misfit=0.03425852
  x299-minus-x300 gap: +1.33662e-03 (4.0600% relative to x300)

high-band objective, noise10_seed34:
  rank 1: x=300,z=90,r=8, misfit=0.00925383
  rank 2: x=299,z=90,r=8, misfit=0.01087978
  x299-minus-x300 gap: +1.62595e-03 (17.5706% relative to x300)

base objective, source_mismatch_noise10_seed34:
  x299-minus-x300 gap: +1.77230e-03 (4.8615% relative to x300)

high-band objective, source_mismatch_noise10_seed34:
  x299-minus-x300 gap: +1.89442e-03 (16.2537% relative to x300)
```

Plot/artifact validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 92.81
FIGURE_NOTES.md exists.
coordinate_objective_top_candidates.csv contains base/highband top-20 rows
for both observed cases.
```

Interpretation:

```text
for the close-50 sources=5 target-2 case, widening Tx/Rx separation from
20 mm to 40 mm is a stronger lever than source count or high-band weighting
alone. The base objective now selects the true x=300 and moves the x=299
competitor to 4.06% above the true-x misfit in the nominal/noisy row, well
above the default 1.5% ambiguity threshold. High-band separation also improves
from 1.466% at 20 mm to 17.57% at 40 mm.
```

## 268: Close-50 Tx/Rx Offset Objective Gap Summary

Purpose:

```text
summarize experiments 265 and 267 in one comparison artifact: default 20 mm
Tx/Rx offset versus 40 mm Tx/Rx offset, base versus high-band objective, and
nominal/noisy versus source-mismatch/noisy cases.
```

Output:

```text
outputs/experiments/268_close50_txrx_offset_objective_gap_summary
```

Inputs:

```text
outputs/experiments/265_coordinate_optimizer_close50_seed34_sources5_topcandidate_objectives
outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives
```

Result:

```text
nominal/noisy base objective:
  20 mm Tx/Rx: x299-minus-x300 = -0.3491%, point x=299, interval 299-300
  40 mm Tx/Rx: x299-minus-x300 = +4.0600%, point x=300, interval 300-300

nominal/noisy high-band objective:
  20 mm Tx/Rx: x299-minus-x300 = +1.4660%
  40 mm Tx/Rx: x299-minus-x300 = +17.5706%

source-mismatch/noisy base objective:
  20 mm Tx/Rx: x299-minus-x300 = +1.9215%
  40 mm Tx/Rx: x299-minus-x300 = +4.8615%

source-mismatch/noisy high-band objective:
  20 mm Tx/Rx: x299-minus-x300 = +12.5814%
  40 mm Tx/Rx: x299-minus-x300 = +16.2537%
```

Plot validation:

```text
txrx_offset_objective_gap_comparison.png: 2263x903 px, dynamic range 255,
std 67.27
FIGURE_NOTES.md explains the 1.5% ambiguity-threshold line.
```

Interpretation:

```text
the 40 mm Tx/Rx offset gives the first close-50 sources=5 configuration in
this branch that collapses the nominal/noisy base-objective x interval while
keeping strong radius confidence. This should be replicated across seeds
before changing the staged policy, but it is now the strongest measured
disambiguation lever for the 50 mm spacing case.
```

## 269: Close-50 Sources=5, Tx/Rx Offset 40 mm, Seed13 Replication

Purpose:

```text
replicate the 40 mm Tx/Rx close-50 target-2 result from seed34 on seed13,
holding the source count, candidate grid, objective variants, and source
profile grid fixed.
```

Output:

```text
outputs/experiments/269_coordinate_optimizer_close50_seed13_sources5_txrx40_objectives
```

Result:

```text
elapsed: 1686.9 s
tx_rx_offset_mm: 40.0
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed13: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed13:
  x299-minus-x300 gap: +1.75870e-03 (5.2602% relative to x300)

high-band objective, noise10_seed13:
  x299-minus-x300 gap: +2.09376e-03 (22.8065% relative to x300)

base objective, source_mismatch_noise10_seed13:
  x299-minus-x300 gap: +1.64444e-03 (4.5031% relative to x300)

high-band objective, source_mismatch_noise10_seed13:
  x299-minus-x300 gap: +1.71643e-03 (15.1750% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 92.89
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed13 confirms the 40 mm Tx/Rx offset effect. The nominal/noisy base-objective
x=299 competitor is 5.26% above the true x=300 misfit, comfortably beyond the
1.5% ambiguity threshold, and both reported x intervals collapse to 300-300 mm.
```

## 270: Close-50 Sources=5, Tx/Rx Offset 40 mm, Seed21 Replication

Purpose:

```text
complete the three-seed close-50 40 mm Tx/Rx replication set by running seed21
with the same setup as experiments 267 and 269.
```

Output:

```text
outputs/experiments/270_coordinate_optimizer_close50_seed21_sources5_txrx40_objectives
```

Result:

```text
elapsed: 1633.2 s
tx_rx_offset_mm: 40.0
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed21: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed21:
  x299-minus-x300 gap: +1.68356e-03 (5.1651% relative to x300)

high-band objective, noise10_seed21:
  x299-minus-x300 gap: +2.05162e-03 (22.7687% relative to x300)

base objective, source_mismatch_noise10_seed21:
  x299-minus-x300 gap: +1.27291e-03 (3.4376% relative to x300)

high-band objective, source_mismatch_noise10_seed21:
  x299-minus-x300 gap: +1.40343e-03 (11.2142% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 92.94
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed21 also confirms the 40 mm Tx/Rx offset effect. The weakest row in this
run is still 3.44% above the x=300 misfit, more than twice the default 1.5%
ambiguity threshold, and both reported x intervals collapse to 300-300 mm.
```

## 271: Close-50 40 mm Tx/Rx Three-Seed Summary

Purpose:

```text
aggregate the seed34, seed13, and seed21 40 mm Tx/Rx close-50 target-2 runs
into one objective-gap and confidence summary.
```

Output:

```text
outputs/experiments/271_close50_txrx40_seed_replication_summary
```

Inputs:

```text
outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives
outputs/experiments/269_coordinate_optimizer_close50_seed13_sources5_txrx40_objectives
outputs/experiments/270_coordinate_optimizer_close50_seed21_sources5_txrx40_objectives
```

Result:

```text
confidence rows: 6
all confidence rows: best x=300,z=90,r=8, x interval 300-300, strong

x299-minus-x300 relative gap summaries:
  nominal/noisy base: min/mean/max = 4.06% / 4.83% / 5.26%
  nominal/noisy high-band: min/mean/max = 17.57% / 21.05% / 22.81%
  source-mismatch/noisy base: min/mean/max = 3.44% / 4.27% / 4.86%
  source-mismatch/noisy high-band: min/mean/max = 11.21% / 14.21% / 16.25%
```

Plot validation:

```text
txrx40_seed_gap_replication.png: 2263x903 px, dynamic range 255, std 70.35
FIGURE_NOTES.md explains the 1.5% ambiguity-threshold line.
```

Interpretation:

```text
the 40 mm Tx/Rx offset has now replicated across seeds 13, 21, and 34 for the
close-50 sources=5 target-2 setup. Every objective/case/seed x=299 competitor
is above the 1.5% threshold relative to x=300, and every confidence row reports
the true point geometry with x interval 300-300 mm.
```

## 272: Staged Pipeline Acquisition Metadata Smoke

Purpose:

```text
verify that staged variable-radius summaries now carry acquisition metadata
columns, including sources, Tx/Rx offset when recorded, and frequency, so
future 20 mm and 40 mm Tx/Rx reports are not mixed silently.
```

Output:

```text
outputs/experiments/272_variable_radius_staged_pipeline_acquisition_metadata_smoke
```

Result:

```text
new staged case CSV columns:
  location_sources
  location_tx_rx_offset_mm
  location_frequency_ghz
  focused_sources
  focused_tx_rx_offset_mm
  focused_frequency_ghz
  refined_focused_sources
  refined_focused_tx_rx_offset_mm
  refined_focused_frequency_ghz
  joint_sources
  joint_tx_rx_offset_mm
  joint_frequency_ghz

old input runs predate tx_rx_offset_mm, so their Tx/Rx offset fields are blank.
source count and frequency are recorded and figure notes now show focused and
refined-focused acquisition settings per case.
```

Validation:

```text
tests/test_variable_radius_staged_pipeline_summary.py: 7 passed
py_compile for staged summary and matching tests passed
git diff --check for staged metadata files passed
staged_variable_radius_pipeline_errors.png: 1753x971 px, dynamic range 255,
std 46.62
FIGURE_NOTES.md includes focused/refined acquisition text.
```

Interpretation:

```text
staged reporting is now acquisition-aware. New coordinate optimizer summaries
that include tx_rx_offset_mm will flow through staged reports, while older runs
remain visibly blank rather than being implicitly treated as the default.
```

## 273: Acquisition-Aware Coordinate Confidence Aggregate, Close50 Sources=5

Purpose:

```text
verify that coordinate confidence aggregate reports now group rows by
acquisition metadata, specifically source count plus Tx/Rx offset, so default
and widened-offset close50 runs are not summarized only as "5 sources".
```

Output:

```text
outputs/experiments/273_coordinate_confidence_aggregate_close50_txrx20_vs_txrx40_sources5
```

Inputs:

```text
outputs/experiments/265_coordinate_optimizer_close50_seed34_sources5_topcandidate_objectives
outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives
outputs/experiments/269_coordinate_optimizer_close50_seed13_sources5_txrx40_objectives
outputs/experiments/270_coordinate_optimizer_close50_seed21_sources5_txrx40_objectives
```

Result:

```text
rows: 8
truth-geometry rows: 7
confidence labels: strong=8
x-ambiguity rows: 1

source-only summary:
  5 sources: rows=8, truth-geometry rows=7, x-ambiguity rows=1

acquisition summary:
  5 sources, Tx/Rx offset 40 mm:
    rows=6, truth-geometry rows=6, x-ambiguity rows=0
  5 sources, Tx/Rx offset not recorded:
    rows=2, truth-geometry rows=1, x-ambiguity rows=1
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 67.33
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 36.83
FIGURE_NOTES.md includes per-acquisition summary text.
```

Interpretation:

```text
source count alone hides the close50 acquisition effect. The acquisition-aware
summary cleanly separates the 40 mm Tx/Rx group, which is fully truth-correct
and interval-collapsed, from the older default/not-recorded group, which keeps
one x-ambiguity row and one wrong nominal/noisy point x.
```

## 274: Close-50 Sources=3, Tx/Rx Offset 40 mm, Seed34 Diagnostic

Purpose:

```text
test whether the successful close50 40 mm Tx/Rx geometry can be made cheaper
by reducing scan positions from 5 to 3 while keeping the same candidate grid,
source-profile grid, and objective variants.
```

Output:

```text
outputs/experiments/274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives
```

Result:

```text
elapsed: 1279.3 s
sources: 3
tx_rx_offset_mm: 40.0
final state: x=[190,250,299], z=[90,90,90], r=[6,6,7.5]
objective top-candidate rows: 160

main rows:
  noise10_seed34: best x=299,z=90,r=7.5, weak,
    x interval 298-299, radius interval 7.0-7.5
  source_mismatch_noise10_seed34: best x=299,z=90,r=7.5, weak,
    x interval 298-299, radius interval 7.0-7.5

revisit rows:
  both cases remained x=299,z=90,r=7.5 with weak radius confidence.

top candidates, main base objective:
  noise10_seed34:
    rank 1 x=299,z=90,r=7.5, misfit=0.02665525
    rank 3 x=300,z=90,r=8.0, misfit=0.02797868
  source_mismatch_noise10_seed34:
    rank 1 x=299,z=90,r=7.5, misfit=0.02852933
    rank 4 x=300,z=90,r=8.0, misfit=0.03031080
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 54.53
FIGURE_NOTES.md reports 4 weak rows and broad radius ambiguity.
```

Interpretation:

```text
3 sources is too sparse for close50 target-2 even with the 40 mm Tx/Rx offset.
It is faster than the 5-source run but moves the optimizer to the wrong
lateral coordinate and an undersized radius, and the scripted revisit does not
recover the truth. The efficient acquisition floor is therefore not yet below
5 sources for this setup.
```

## 275: Close-50 Tx/Rx 40 mm Sources=3 vs Sources=5 Aggregate

Purpose:

```text
compare the negative sources=3 result against the successful sources=5 40 mm
Tx/Rx seed34 run using the acquisition-aware coordinate aggregate.
```

Output:

```text
outputs/experiments/275_coordinate_confidence_aggregate_close50_txrx40_sources3_vs5_seed34
```

Inputs:

```text
outputs/experiments/274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives
outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives
```

Result:

```text
rows: 6
truth-geometry rows: 2
confidence labels: weak=4, strong=2
x-ambiguity rows: 4

acquisition summary:
  3 sources, Tx/Rx offset 40 mm:
    rows=4, truth-geometry rows=0, x-ambiguity rows=4,
    radius margin min/mean/max=1.75584e-04/1.75783e-04/1.75981e-04
  5 sources, Tx/Rx offset 40 mm:
    rows=2, truth-geometry rows=2, x-ambiguity rows=0,
    radius margin min/mean/max=2.35607e-03/2.73323e-03/3.11039e-03
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 61.23
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 49.35
FIGURE_NOTES.md includes per-acquisition summary text.
```

Interpretation:

```text
for close50 seed34 at 40 mm Tx/Rx, 5 sources are necessary in the tested
acquisition family. Reducing to 3 sources saves runtime but loses both point
accuracy and confidence; all 3-source rows remain ambiguous and none match the
truth geometry.
```

## 276: Close-50 Sources=4, Tx/Rx Offset 40 mm, Seed34 Diagnostic

Purpose:

```text
bracket the close50 40 mm Tx/Rx source-count threshold after 3 sources failed
and 5 sources succeeded.
```

Output:

```text
outputs/experiments/276_coordinate_optimizer_close50_seed34_sources4_txrx40_objectives
```

Result:

```text
elapsed: 1309.4 s
sources: 4
tx_rx_offset_mm: 40.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed34: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed34:
  x299-minus-x300 gap: +2.24245e-03 (4.2463% relative to x300)

high-band objective, noise10_seed34:
  x299-minus-x300 gap: +2.35697e-03 (20.2756% relative to x300)

base objective, source_mismatch_noise10_seed34:
  x299-minus-x300 gap: +3.45786e-03 (5.4488% relative to x300)

high-band objective, source_mismatch_noise10_seed34:
  x299-minus-x300 gap: +3.55207e-03 (25.3343% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 91.32
FIGURE_NOTES.md exists.
```

Interpretation:

```text
4 sources are sufficient for close50 seed34 with the 40 mm Tx/Rx offset, and
are about 23% faster than the 5-source run. This makes 4 sources the current
minimum positive source-count result for this acquisition geometry, but it
still needs seed replication before replacing the 5-source recommendation.
```

## 277: Close-50 Tx/Rx 40 mm Sources=3/4/5 Aggregate, Seed34

Purpose:

```text
summarize the close50 seed34 source-count threshold at 40 mm Tx/Rx offset.
```

Output:

```text
outputs/experiments/277_coordinate_confidence_aggregate_close50_txrx40_sources3_4_5_seed34
```

Inputs:

```text
outputs/experiments/274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives
outputs/experiments/276_coordinate_optimizer_close50_seed34_sources4_txrx40_objectives
outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives
```

Result:

```text
rows: 8
truth-geometry rows: 4
confidence labels: weak=4, strong=4
x-ambiguity rows: 4

acquisition summary:
  3 sources, Tx/Rx offset 40 mm:
    rows=4, truth-geometry rows=0, x-ambiguity rows=4,
    radius margin mean=1.75783e-04
  4 sources, Tx/Rx offset 40 mm:
    rows=2, truth-geometry rows=2, x-ambiguity rows=0,
    radius margin mean=6.25877e-03
  5 sources, Tx/Rx offset 40 mm:
    rows=2, truth-geometry rows=2, x-ambiguity rows=0,
    radius margin mean=2.73323e-03
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 60.24
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 47.22
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
the seed34 source-count threshold under 40 mm Tx/Rx lies between 3 and 4
sources. Three sources fail with weak radius confidence and x ambiguity;
four sources succeed with strong confidence and interval collapse. Keep 5
sources as the robust cross-seed setting until the 4-source result is
replicated across seeds.
```

## 278: Close-50 Sources=4, Tx/Rx Offset 40 mm, Seed13 Replication

Purpose:

```text
replicate the positive seed34 4-source 40 mm Tx/Rx result on seed13.
```

Output:

```text
outputs/experiments/278_coordinate_optimizer_close50_seed13_sources4_txrx40_objectives
```

Result:

```text
elapsed: 1274.9 s
sources: 4
tx_rx_offset_mm: 40.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed13: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed13:
  x299-minus-x300 gap: +2.30155e-03 (4.2979% relative to x300)

high-band objective, noise10_seed13:
  x299-minus-x300 gap: +2.54749e-03 (21.1614% relative to x300)

base objective, source_mismatch_noise10_seed13:
  x299-minus-x300 gap: +3.20677e-03 (5.0257% relative to x300)

high-band objective, source_mismatch_noise10_seed13:
  x299-minus-x300 gap: +3.33368e-03 (22.4067% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 91.29
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed13 confirms that 4 sources with 40 mm Tx/Rx can collapse the close50
target-2 interval. The weakest x299-minus-x300 gap is still 4.30%, well above
the 1.5% ambiguity threshold.
```

## 279: Close-50 Sources=4, Tx/Rx Offset 40 mm, Seed21 Replication

Purpose:

```text
complete the seed13/21/34 replication set for the 4-source 40 mm Tx/Rx
close50 target-2 diagnostic.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 40 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/279_coordinate_optimizer_close50_seed21_sources4_txrx40_objectives
```

Result:

```text
elapsed: 1265.9 s
sources: 4
tx_rx_offset_mm: 40.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed21: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed21:
  x299-minus-x300 gap: +2.08910e-03 (3.9894% relative to x300)

high-band objective, noise10_seed21:
  x299-minus-x300 gap: +2.37172e-03 (21.4182% relative to x300)

base objective, source_mismatch_noise10_seed21:
  x299-minus-x300 gap: +3.13209e-03 (4.8487% relative to x300)

high-band objective, source_mismatch_noise10_seed21:
  x299-minus-x300 gap: +3.33318e-03 (21.9256% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 81.15
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed21 confirms the same 4-source 40 mm Tx/Rx behavior seen on seeds 34 and
13. The weakest x299-minus-x300 gap is 3.99%, above the 1.5% ambiguity
threshold, and the ambiguity interval collapses to x=300 mm for both observed
cases.
```

## 280: Close-50 Sources=4, Tx/Rx Offset 40 mm, Seed Aggregate

Purpose:

```text
summarize the replicated 4-source 40 mm Tx/Rx close50 diagnostics across
seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close50_sources4_txrx40_seed_replicates
  --outdir outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates
  outputs/experiments/276_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/278_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/279_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  4.81717e-03 / 6.37699e-03 / 8.14137e-03
acquisition group:
  4 sources, Tx/Rx offset 40 mm: rows=6, truth rows=6, x ambiguity=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 73.02
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.58
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
4 sources with 40 mm Tx/Rx is now replicated across seeds 13, 21, and 34 for
the close50 target-2 geometry under both nominal noise and source-mismatch
observations. This setting is the current minimum validated close50 40 mm
Tx/Rx acquisition. Three sources remain a documented failure boundary; five
sources remain the conservative backup when extra acquisition cost is
acceptable.
```

## 281: Close-50 Sources=4, Tx/Rx Offset 30 mm, Seed34 Threshold Probe

Purpose:

```text
test whether the replicated 4-source close50 acquisition can reduce Tx/Rx
offset from 40 mm to 30 mm without reopening the target-2 lateral ambiguity.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 30 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/281_coordinate_optimizer_close50_seed34_sources4_txrx30_objectives
```

Result:

```text
elapsed: 1334.9 s
sources: 4
tx_rx_offset_mm: 30.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed34: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed34:
  x301-minus-x300 gap: +1.36121e-03 (1.9557% relative to x300)
  x299-minus-x300 gap: +3.85461e-03 (5.5381% relative to x300)

high-band objective, noise10_seed34:
  x301-minus-x300 gap: +1.50778e-03 (15.2796% relative to x300)

base objective, source_mismatch_noise10_seed34:
  x301-minus-x300 gap: +1.33916e-03 (2.0451% relative to x300)
  x299-minus-x300 gap: +4.62013e-03 (7.0557% relative to x300)

high-band objective, source_mismatch_noise10_seed34:
  x301-minus-x300 gap: +1.27840e-03 (13.1394% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 84.02
FIGURE_NOTES.md exists.
```

Interpretation:

```text
30 mm Tx/Rx passes the first seed34 threshold probe: the truth geometry wins,
both rows are strong, and the ambiguity interval still collapses to x=300 mm.
The margin is notably tighter than 40 mm, though. The closest base competitor
is x=301 mm at only 1.96-2.05% above the truth, so 30 mm should be treated as
promising but unvalidated until replicated on seeds 13 and 21.
```

## 282: Close-50 Sources=4, Tx/Rx Offset 30 mm, Seed13 Replication

Purpose:

```text
replicate the positive seed34 30 mm Tx/Rx threshold probe on seed13 before
promoting the reduced offset.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 30 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/282_coordinate_optimizer_close50_seed13_sources4_txrx30_objectives
```

Result:

```text
elapsed: 1284.4 s
sources: 4
tx_rx_offset_mm: 30.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed13: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed13:
  x301-minus-x300 gap: +1.11754e-03 (1.5888% relative to x300)
  x299-minus-x300 gap: +4.09691e-03 (5.8244% relative to x300)

high-band objective, noise10_seed13:
  x301-minus-x300 gap: +1.17069e-03 (11.5485% relative to x300)

base objective, source_mismatch_noise10_seed13:
  x301-minus-x300 gap: +1.57298e-03 (2.3862% relative to x300)
  x299-minus-x300 gap: +4.33349e-03 (6.5738% relative to x300)

high-band objective, source_mismatch_noise10_seed13:
  x301-minus-x300 gap: +1.43522e-03 (13.6635% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 84.19
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed13 is a borderline positive 30 mm Tx/Rx replication. The truth geometry
wins, both rows are strong, and the ambiguity interval still collapses to
x=300 mm, but the nominal base x301-minus-x300 gap is only 1.5888%, barely
above the 1.5% ambiguity threshold. Seed21 is required before any reduced
offset recommendation.
```

## 283: Close-50 Sources=4, Tx/Rx Offset 30 mm, Seed21 Replication

Purpose:

```text
complete the seed34/13/21 replication set for the 4-source 30 mm Tx/Rx
close50 target-2 threshold probe.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 30 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/283_coordinate_optimizer_close50_seed21_sources4_txrx30_objectives
```

Result:

```text
elapsed: 1314.6 s
sources: 4
tx_rx_offset_mm: 30.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed21: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed21:
  x301-minus-x300 gap: +1.29042e-03 (1.8585% relative to x300)
  x299-minus-x300 gap: +3.88125e-03 (5.5900% relative to x300)

high-band objective, noise10_seed21:
  x301-minus-x300 gap: +1.19166e-03 (12.2502% relative to x300)

base objective, source_mismatch_noise10_seed21:
  x301-minus-x300 gap: +1.33013e-03 (1.9898% relative to x300)
  x299-minus-x300 gap: +4.59319e-03 (6.8713% relative to x300)

high-band objective, source_mismatch_noise10_seed21:
  x301-minus-x300 gap: +1.25759e-03 (11.4560% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.67
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed21 completes the 30 mm Tx/Rx replication set as another truth-geometry
pass with collapsed x interval. The weakest seed21 base gap is 1.8585%, above
the 1.5% ambiguity threshold but still far below the 40 mm replicated margin.
```

## 284: Close-50 Sources=4, Tx/Rx Offset 30 mm, Seed Aggregate

Purpose:

```text
summarize the replicated 4-source 30 mm Tx/Rx close50 diagnostics across
seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close50_sources4_txrx30_seed_replicates
  --outdir outputs/experiments/284_coordinate_confidence_close50_sources4_txrx30_seed_replicates
  outputs/experiments/281_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/282_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/283_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/284_coordinate_confidence_close50_sources4_txrx30_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  1.70176e-03 / 2.11014e-03 / 2.30368e-03
acquisition group:
  4 sources, Tx/Rx offset 30 mm: rows=6, truth rows=6, x ambiguity=0

weakest x301-minus-x300 relative gaps:
  base: 1.5888% (seed13 nominal)
  highband: 11.4560% (seed21 source-mismatch)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 76.36
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.55
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
30 mm Tx/Rx is replicated across seeds 13, 21, and 34 as a truth-geometry
pass with zero x ambiguity, but it is a borderline acquisition compared with
40 mm. The weakest base lateral gap is 1.5888%, just above the 1.5% threshold,
and the aggregate radius margins are roughly one-third of the 40 mm mean
margin. Treat 30 mm as the minimum replicated offset only with margin-aware
reporting; keep 40 mm as the robust default.
```

## 285: Close-50 Sources=4, Tx/Rx Offset 25 mm, Seed34 Lower-Bound Probe

Purpose:

```text
test whether the 30 mm replicated lower offset can be reduced further to
25 mm on seed34, using the same 4-source close50 target-2 diagnostic.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 25 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/285_coordinate_optimizer_close50_seed34_sources4_txrx25_objectives
```

Result:

```text
elapsed: 1691.5 s
sources: 4
tx_rx_offset_mm: 25.0
scan x positions: [50,178,314,450] mm
main final update: x=301,z=90,r=8
revisit final update: x=301,z=90,r=8
final state: x=[190,250,301], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 160

confidence rows:
  noise10_seed34 main: best x=300,z=90,r=8, weak,
    x interval 300-301, radius interval 7.5-8.0
  source_mismatch_noise10_seed34 main: best x=301,z=90,r=8, weak,
    x interval 300-301, radius interval 7.5-8.0
  revisit rows repeat the same weak intervals and best candidates.

base objective, noise10_seed34:
  x301-minus-x300 gap: +1.16364e-04 (0.1527% relative to x300)

base objective, source_mismatch_noise10_seed34:
  x300-minus-x301 gap: +6.54031e-05 (0.0941% relative to x301)

high-band objective, noise10_seed34:
  best branch is x=301,z=90,r=7.5; truth x=300,z=90,r=8 is
  +2.11627e-04 (2.2947%) above that branch.

high-band objective, source_mismatch_noise10_seed34:
  best branch is x=301,z=90,r=7.5; truth x=300,z=90,r=8 is
  +3.58012e-04 (3.8567%) above that branch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 63.94
FIGURE_NOTES.md reports 4 weak rows and broad radius-ambiguity rows.
```

Interpretation:

```text
25 mm Tx/Rx fails as the lower-bound offset. It reopens x=300-301 ambiguity,
keeps weak radius margins after revisit, and the source-mismatch row selects
the wrong lateral point x=301 mm. The practical close50 offset bracket is now
25 mm fail, 30 mm replicated but borderline, and 40 mm robust.
```

## 286: Close-50 Sources=4, Tx/Rx Offset 35 mm, Seed34 Robustness Probe

Purpose:

```text
test whether 35 mm Tx/Rx gives 40 mm-like robustness while reducing the
offset below the current robust default.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/286_coordinate_optimizer_close50_seed34_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1310.2 s
sources: 4
tx_rx_offset_mm: 35.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed34: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed34:
  x299-minus-x300 gap: +2.95010e-03 (4.7127% relative to x300)
  x301-minus-x300 gap: +3.16728e-03 (5.0597% relative to x300)

high-band objective, noise10_seed34:
  x299-minus-x300 gap: +2.79594e-03 (25.8368% relative to x300)
  x301-minus-x300 gap: +3.51051e-03 (32.4400% relative to x300)

base objective, source_mismatch_noise10_seed34:
  x299-minus-x300 gap: +4.03588e-03 (6.2386% relative to x300)
  x301-minus-x300 gap: +3.81040e-03 (5.8900% relative to x300)

high-band objective, source_mismatch_noise10_seed34:
  x299-minus-x300 gap: +4.14400e-03 (36.9574% relative to x300)
  x301-minus-x300 gap: +4.07639e-03 (36.3545% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.40
FIGURE_NOTES.md exists.
```

Interpretation:

```text
35 mm Tx/Rx passes the seed34 robustness probe. The weakest base lateral gap
is 4.71%, comparable to the 40 mm seed34 run and much stronger than the 30 mm
borderline seed34 run. Replicate 35 mm on seeds 13 and 21 before promoting it
as the robust default.
```

## 287: Close-50 Sources=4, Tx/Rx Offset 35 mm, Seed13 Replication

Purpose:

```text
replicate the positive seed34 35 mm Tx/Rx robustness probe on seed13.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/287_coordinate_optimizer_close50_seed13_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1275.5 s
sources: 4
tx_rx_offset_mm: 35.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed13: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed13:
  x301-minus-x300 gap: +2.94248e-03 (4.6435% relative to x300)
  x299-minus-x300 gap: +3.14914e-03 (4.9696% relative to x300)

high-band objective, noise10_seed13:
  x301-minus-x300 gap: +3.16570e-03 (28.4665% relative to x300)
  x299-minus-x300 gap: +3.13235e-03 (28.1666% relative to x300)

base objective, source_mismatch_noise10_seed13:
  x301-minus-x300 gap: +4.08443e-03 (6.2679% relative to x300)
  x299-minus-x300 gap: +3.72104e-03 (5.7102% relative to x300)

high-band objective, source_mismatch_noise10_seed13:
  x301-minus-x300 gap: +4.29028e-03 (35.4578% relative to x300)
  x299-minus-x300 gap: +3.89328e-03 (32.1767% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.76
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed13 confirms the 35 mm Tx/Rx robustness probe. The weakest base lateral
gap is 4.64%, much stronger than the 30 mm replicated minimum and comparable
to 40 mm. Run seed21 to complete the 35 mm robustness set.
```

## 288: Close-50 Sources=4, Tx/Rx Offset 35 mm, Seed21 Replication

Purpose:

```text
complete the seed34/13/21 replication set for the 4-source 35 mm Tx/Rx
close50 target-2 robustness probe.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/288_coordinate_optimizer_close50_seed21_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1266.8 s
sources: 4
tx_rx_offset_mm: 35.0
scan x positions: [50,178,314,450] mm
final state: x=[190,250,300], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=300,z=90,r=8, strong, x interval 300-300
  source_mismatch_noise10_seed21: best x=300,z=90,r=8, strong,
    x interval 300-300

base objective, noise10_seed21:
  x299-minus-x300 gap: +2.88779e-03 (4.6368% relative to x300)
  x301-minus-x300 gap: +3.18264e-03 (5.1103% relative to x300)

high-band objective, noise10_seed21:
  x299-minus-x300 gap: +2.97962e-03 (28.5291% relative to x300)
  x301-minus-x300 gap: +3.27934e-03 (31.3989% relative to x300)

base objective, source_mismatch_noise10_seed21:
  x299-minus-x300 gap: +3.85294e-03 (5.8377% relative to x300)
  x301-minus-x300 gap: +3.97268e-03 (6.0192% relative to x300)

high-band objective, source_mismatch_noise10_seed21:
  x299-minus-x300 gap: +4.01066e-03 (32.1162% relative to x300)
  x301-minus-x300 gap: +4.21111e-03 (33.7213% relative to x300)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.21
FIGURE_NOTES.md exists.
```

Interpretation:

```text
seed21 completes the 35 mm Tx/Rx robustness set as another truth-geometry
pass with collapsed x interval. The weakest seed21 base lateral gap is 4.64%,
which is stronger than every 30 mm base gap and above the weakest 40 mm base
gap.
```

## 289: Close-50 Sources=4, Tx/Rx Offset 35 mm, Seed Aggregate

Purpose:

```text
summarize the replicated 4-source 35 mm Tx/Rx close50 diagnostics across
seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close50_sources4_txrx35_seed_replicates
  --outdir outputs/experiments/289_coordinate_confidence_close50_sources4_txrx35_seed_replicates
  outputs/experiments/286_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/287_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/288_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/289_coordinate_confidence_close50_sources4_txrx35_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  4.27278e-03 / 5.18816e-03 / 6.02166e-03
acquisition group:
  4 sources, Tx/Rx offset 35 mm: rows=6, truth rows=6, x ambiguity=0

weakest lateral relative gaps:
  base: 4.6368% (seed21 nominal)
  highband: 25.8368% (seed34 nominal)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 75.02
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.53
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
35 mm Tx/Rx is replicated across seeds 13, 21, and 34 as a robust
truth-geometry setting. It keeps the zero-ambiguity behavior of 40 mm while
using 5 mm less offset. Its aggregate radius margin mean is lower than 40 mm
but far above 30 mm, and its weakest base lateral percentage gap exceeds the
40 mm replicated set. Promote 35 mm as the robust close50 default; keep 30 mm
as the minimum replicated margin-aware setting and 25 mm as the failed lower
bound.
```

## 290: Close-45 Sources=4, Tx/Rx Offset 35 mm, Seed34 Geometry Stress

Purpose:

```text
test whether the new robust 35 mm Tx/Rx default still resolves target 2 when
the center/right separation tightens from 50 mm to 45 mm.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,295 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,295
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/290_coordinate_optimizer_close45_seed34_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1272.8 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,295] mm
scan x positions: [50,178,314,450] mm
final state: x=[190,250,295], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=295,z=90,r=8, strong, x interval 295-295
  source_mismatch_noise10_seed34: best x=295,z=90,r=8, strong,
    x interval 295-295

base objective, noise10_seed34:
  x294-minus-x295 gap: +3.22385e-03 (4.6352% relative to x295)
  x296-minus-x295 gap: +5.14044e-03 (7.3909% relative to x295)

high-band objective, noise10_seed34:
  x294-minus-x295 gap: +2.91270e-03 (24.2249% relative to x295)
  x296-minus-x295 gap: +5.76624e-03 (47.9577% relative to x295)

base objective, source_mismatch_noise10_seed34:
  x294-minus-x295 gap: +4.03884e-03 (5.5379% relative to x295)
  x296-minus-x295 gap: +6.52531e-03 (8.9473% relative to x295)

high-band objective, source_mismatch_noise10_seed34:
  x294-minus-x295 gap: +3.77718e-03 (29.8296% relative to x295)
  x296-minus-x295 gap: +7.20266e-03 (56.8816% relative to x295)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 81.93
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close45 seed34 passes strongly under the 35 mm robust default. The weakest
base lateral gap is 4.64%, effectively matching the close50 35 mm replicated
floor. Replicate close45 on seeds 13 and 21 before declaring the geometry
limit shifted from 50 mm to 45 mm.
```

## 291: Close-45 Sources=4, Tx/Rx Offset 35 mm, Seed13 Replication

Purpose:

```text
replicate the positive close45 seed34 geometry-stress result on seed13.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,295 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,295
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/291_coordinate_optimizer_close45_seed13_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1272.5 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,295] mm
final state: x=[190,250,295], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=295,z=90,r=8, strong, x interval 295-295
  source_mismatch_noise10_seed13: best x=295,z=90,r=8, strong,
    x interval 295-295

base objective, noise10_seed13:
  x294-minus-x295 gap: +3.12724e-03 (4.4358% relative to x295)
  x296-minus-x295 gap: +5.19040e-03 (7.3622% relative to x295)

high-band objective, noise10_seed13:
  x294-minus-x295 gap: +2.96008e-03 (23.7980% relative to x295)
  x296-minus-x295 gap: +5.69713e-03 (45.8030% relative to x295)

base objective, source_mismatch_noise10_seed13:
  x294-minus-x295 gap: +4.02206e-03 (5.4922% relative to x295)
  x296-minus-x295 gap: +6.63186e-03 (9.0560% relative to x295)

high-band objective, source_mismatch_noise10_seed13:
  x294-minus-x295 gap: +3.80706e-03 (28.2116% relative to x295)
  x296-minus-x295 gap: +7.27469e-03 (53.9078% relative to x295)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.06
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close45 seed13 confirms the seed34 result under the 35 mm robust default. The
weakest base lateral gap is 4.44%, still well above the 1.5% ambiguity
threshold. Run seed21 to complete close45 replication.
```

## 292: Close-45 Sources=4, Tx/Rx Offset 35 mm, Seed21 Replication

Purpose:

```text
complete the seed34/13/21 replication set for close45 target-2 geometry under
the 35 mm robust acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,295 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,295
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/292_coordinate_optimizer_close45_seed21_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1287.4 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,295] mm
final state: x=[190,250,295], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=295,z=90,r=8, strong, x interval 295-295
  source_mismatch_noise10_seed21: best x=295,z=90,r=8, strong,
    x interval 295-295

base objective, noise10_seed21:
  x294-minus-x295 gap: +2.87542e-03 (4.1528% relative to x295)
  x296-minus-x295 gap: +5.43804e-03 (7.8538% relative to x295)

high-band objective, noise10_seed21:
  x294-minus-x295 gap: +2.72571e-03 (23.2602% relative to x295)
  x296-minus-x295 gap: +5.90064e-03 (50.3540% relative to x295)

base objective, source_mismatch_noise10_seed21:
  x294-minus-x295 gap: +3.85376e-03 (5.1813% relative to x295)
  x296-minus-x295 gap: +6.74725e-03 (9.0714% relative to x295)

high-band objective, source_mismatch_noise10_seed21:
  x294-minus-x295 gap: +3.80887e-03 (27.1254% relative to x295)
  x296-minus-x295 gap: +7.25460e-03 (51.6646% relative to x295)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.23
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close45 seed21 completes the replication set as another strong truth-geometry
pass. The weakest base lateral gap is 4.15%, still comfortably above the
1.5% ambiguity threshold.
```

## 293: Close-45 Sources=4, Tx/Rx Offset 35 mm, Seed Aggregate

Purpose:

```text
summarize the replicated close45 4-source 35 mm Tx/Rx diagnostics across
seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close45_sources4_txrx35_seed_replicates
  --outdir outputs/experiments/293_coordinate_confidence_close45_sources4_txrx35_seed_replicates
  outputs/experiments/290_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/291_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/292_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/293_coordinate_confidence_close45_sources4_txrx35_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  5.34539e-03 / 6.56100e-03 / 7.94417e-03
acquisition group:
  4 sources, Tx/Rx offset 35 mm: rows=6, truth rows=6, x ambiguity=0

weakest lateral relative gaps:
  base: 4.1528% (seed21 nominal)
  highband: 23.2602% (seed21 nominal)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 74.09
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.53
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
close45 is replicated across seeds 13, 21, and 34 under the 4-source 35 mm
Tx/Rx robust acquisition. The replicated close45 set has zero x ambiguity and
stronger aggregate radius margins than the close50 35 mm set, while the
weakest base lateral gap remains well above the ambiguity threshold. Move the
geometry-stress branch to close40 before claiming a tighter geometry limit.
```

## 294: Close-40 Sources=4, Tx/Rx Offset 35 mm, Seed34 Geometry Stress

Purpose:

```text
test whether the 4-source 35 mm robust acquisition still resolves target 2
when the center/right separation tightens from 45 mm to 40 mm.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,290 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,290
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/294_coordinate_optimizer_close40_seed34_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1409.0 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,290] mm
final state: x=[190,250,290], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=290,z=90,r=8, strong, x interval 290-290
  source_mismatch_noise10_seed34: best x=290,z=90,r=8, strong,
    x interval 290-290

base objective, noise10_seed34:
  x289-minus-x290 gap: +4.96251e-03 (6.6059% relative to x290)
  x291-minus-x290 gap: +6.76536e-03 (9.0058% relative to x290)

high-band objective, noise10_seed34:
  x289-minus-x290 gap: +4.74275e-03 (36.5545% relative to x290)
  x291-minus-x290 gap: +7.40839e-03 (57.0998% relative to x290)

base objective, source_mismatch_noise10_seed34:
  x289-minus-x290 gap: +6.57982e-03 (8.0021% relative to x290)
  x291-minus-x290 gap: +9.12203e-03 (11.0938% relative to x290)

high-band objective, source_mismatch_noise10_seed34:
  x289-minus-x290 gap: +6.30773e-03 (43.0940% relative to x290)
  x291-minus-x290 gap: +9.90929e-03 (67.6997% relative to x290)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 81.35
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close40 seed34 passes strongly under the 4-source 35 mm acquisition. The
weakest base lateral gap is 6.61%, stronger than close45 and close50, and the
ambiguity interval collapses to x=290 mm. Replicate seeds 13 and 21 before
moving the geometry-stress branch tighter.
```

## 295: Close-40 Sources=4, Tx/Rx Offset 35 mm, Seed13 Replication

Purpose:

```text
replicate the positive close40 seed34 geometry-stress result on seed13.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,290 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,290
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/295_coordinate_optimizer_close40_seed13_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1396.4 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,290] mm
final state: x=[190,250,290], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=290,z=90,r=8, strong, x interval 290-290
  source_mismatch_noise10_seed13: best x=290,z=90,r=8, strong,
    x interval 290-290

base objective, noise10_seed13:
  x289-minus-x290 gap: +4.79918e-03 (6.3074% relative to x290)
  x291-minus-x290 gap: +6.95227e-03 (9.1371% relative to x290)

high-band objective, noise10_seed13:
  x289-minus-x290 gap: +4.71134e-03 (35.0766% relative to x290)
  x291-minus-x290 gap: +7.49038e-03 (55.7669% relative to x290)

base objective, source_mismatch_noise10_seed13:
  x289-minus-x290 gap: +7.23560e-03 (8.7646% relative to x290)
  x291-minus-x290 gap: +8.52185e-03 (10.3227% relative to x290)

high-band objective, source_mismatch_noise10_seed13:
  x289-minus-x290 gap: +6.97342e-03 (45.3200% relative to x290)
  x291-minus-x290 gap: +9.31995e-03 (60.5699% relative to x290)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 81.32
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close40 seed13 confirms the seed34 result. The weakest base lateral gap is
6.31%, with strong confidence and x interval 290-290 mm. Run seed21 to
complete close40 replication.
```

## 296: Close-40 Sources=4, Tx/Rx Offset 35 mm, Seed21 Replication

Purpose:

```text
complete the close40 seed replication under the 4-source 35 mm robust
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,290 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,290
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/296_coordinate_optimizer_close40_seed21_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1411.5 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,290] mm
final state: x=[190,250,290], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=290,z=90,r=8, strong, x interval 290-290
  source_mismatch_noise10_seed21: best x=290,z=90,r=8, strong,
    x interval 290-290

base objective, noise10_seed21:
  x289-minus-x290 gap: +4.71837e-03 (6.3125% relative to x290)
  x291-minus-x290 gap: +7.07980e-03 (9.4718% relative to x290)

high-band objective, noise10_seed21:
  x289-minus-x290 gap: +4.58447e-03 (36.0600% relative to x290)
  x291-minus-x290 gap: +7.64893e-03 (60.1640% relative to x290)

base objective, source_mismatch_noise10_seed21:
  x289-minus-x290 gap: +6.72788e-03 (8.0265% relative to x290)
  x291-minus-x290 gap: +9.04535e-03 (10.7913% relative to x290)

high-band objective, source_mismatch_noise10_seed21:
  x289-minus-x290 gap: +6.72221e-03 (41.8766% relative to x290)
  x291-minus-x290 gap: +9.58594e-03 (59.7164% relative to x290)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 82.04
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close40 seed21 completes the close40 replication as another strong
truth-geometry pass. The weakest base lateral gap is 6.31% nominal and 8.03%
under source mismatch, with zero x ambiguity. Aggregate the close40 seed set
before moving tighter.
```

## 297: Close-40 Sources=4, Tx/Rx Offset 35 mm, Seed Aggregate

Purpose:

```text
summarize the replicated close40 4-source 35 mm Tx/Rx diagnostics across
seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close40_sources4_txrx35_seed_replicates
  --outdir outputs/experiments/297_coordinate_confidence_close40_sources4_txrx35_seed_replicates
  outputs/experiments/294_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/295_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/296_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/297_coordinate_confidence_close40_sources4_txrx35_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  5.87764e-03 / 7.41450e-03 / 9.22123e-03
acquisition group:
  4 sources, Tx/Rx offset 35 mm: rows=6, truth rows=6, x ambiguity=0

weakest lateral relative gaps:
  base nominal: 6.3074% (seed13)
  base source mismatch: 8.0021% (seed34)
  highband nominal: 35.0766% (seed13)
  highband source mismatch: 41.8766% (seed21)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 73.52
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.54
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
close40 is replicated across seeds 13, 21, and 34 under the 4-source 35 mm
Tx/Rx robust acquisition. All six rows recover truth geometry with strong
confidence, zero x ambiguity, and larger aggregate radius margins than the
close45 and close50 35 mm sets. Move the geometry-stress branch to close35
with the same acquisition before claiming the tight-separation limit.
```

## 298: Close-35 Sources=4, Tx/Rx Offset 35 mm, Seed34 Geometry Stress

Purpose:

```text
test whether the replicated 4-source 35 mm robust acquisition still resolves
target 2 when the center/right separation tightens from 40 mm to 35 mm.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,285 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,285
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/298_coordinate_optimizer_close35_seed34_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1404.9 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,285] mm
final state: x=[190,250,285], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=285,z=90,r=8, strong, x interval 285-285
  source_mismatch_noise10_seed34: best x=285,z=90,r=8, strong,
    x interval 285-285

base objective, noise10_seed34:
  x284-minus-x285 gap: +7.11576e-03 (9.4885% relative to x285)
  x286-minus-x285 gap: +5.45803e-03 (7.2780% relative to x285)

high-band objective, noise10_seed34:
  x284-minus-x285 gap: +7.15466e-03 (55.7079% relative to x285)
  x286-minus-x285 gap: +5.68654e-03 (44.2767% relative to x285)

base objective, source_mismatch_noise10_seed34:
  x284-minus-x285 gap: +1.16354e-02 (13.2461% relative to x285)
  x286-minus-x285 gap: +7.69844e-03 (8.7641% relative to x285)

high-band objective, source_mismatch_noise10_seed34:
  x284-minus-x285 gap: +1.14626e-02 (71.3695% relative to x285)
  x286-minus-x285 gap: +8.22707e-03 (51.2242% relative to x285)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 81.08
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close35 seed34 passes strongly under the same 4-source 35 mm acquisition. The
nearest lateral branch is the right-shifted x=286 mm candidate, but it remains
7.28% worse than truth under the base objective and 44.28% worse under
highband. Replicate close35 on seeds 13 and 21 before setting a tighter
geometry limit.
```

## 299: Close-35 Sources=4, Tx/Rx Offset 35 mm, Seed13 Replication

Purpose:

```text
replicate the positive close35 seed34 geometry-stress result on seed13.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,285 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,285
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/299_coordinate_optimizer_close35_seed13_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1406.3 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,285] mm
final state: x=[190,250,285], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=285,z=90,r=8, strong, x interval 285-285
  source_mismatch_noise10_seed13: best x=285,z=90,r=8, strong,
    x interval 285-285

base objective, noise10_seed13:
  x284-minus-x285 gap: +6.79769e-03 (8.9622% relative to x285)
  x286-minus-x285 gap: +5.72695e-03 (7.5505% relative to x285)

high-band objective, noise10_seed13:
  x284-minus-x285 gap: +6.86944e-03 (51.9828% relative to x285)
  x286-minus-x285 gap: +5.94125e-03 (44.9589% relative to x285)

base objective, source_mismatch_noise10_seed13:
  x284-minus-x285 gap: +1.22496e-02 (13.8733% relative to x285)
  x286-minus-x285 gap: +7.00493e-03 (7.9334% relative to x285)

high-band objective, source_mismatch_noise10_seed13:
  x284-minus-x285 gap: +1.21057e-02 (72.5841% relative to x285)
  x286-minus-x285 gap: +7.55372e-03 (45.2911% relative to x285)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 80.57
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close35 seed13 confirms the seed34 result as another strong truth-geometry
pass with x interval 285-285 mm and no revisit. The weakest base lateral gap
is 7.55% nominal and 7.93% under source mismatch. Run seed21 to complete the
close35 seed set.
```

## 300: Close-35 Sources=4, Tx/Rx Offset 35 mm, Seed21 Replication

Purpose:

```text
complete the close35 seed replication under the 4-source 35 mm robust
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,285 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,285
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/300_coordinate_optimizer_close35_seed21_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1411.7 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,285] mm
final state: x=[190,250,285], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=285,z=90,r=8, strong, x interval 285-285
  source_mismatch_noise10_seed21: best x=285,z=90,r=8, strong,
    x interval 285-285

base objective, noise10_seed21:
  x284-minus-x285 gap: +7.20729e-03 (9.6689% relative to x285)
  x286-minus-x285 gap: +5.36333e-03 (7.1952% relative to x285)

high-band objective, noise10_seed21:
  x284-minus-x285 gap: +7.22998e-03 (57.9170% relative to x285)
  x286-minus-x285 gap: +5.61841e-03 (45.0073% relative to x285)

base objective, source_mismatch_noise10_seed21:
  x284-minus-x285 gap: +1.16166e-02 (12.9949% relative to x285)
  x286-minus-x285 gap: +7.67460e-03 (8.5851% relative to x285)

high-band objective, source_mismatch_noise10_seed21:
  x284-minus-x285 gap: +1.15882e-02 (66.8119% relative to x285)
  x286-minus-x285 gap: +8.07187e-03 (46.5386% relative to x285)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 81.52
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close35 seed21 completes the replicated close35 seed set as another strong
truth-geometry pass with x interval 285-285 mm. The weakest base lateral gap
is 7.20% nominal and 8.59% under source mismatch. Aggregate close35 before
moving tighter.
```

## 301: Close-35 Sources=4, Tx/Rx Offset 35 mm, Seed Aggregate

Purpose:

```text
summarize the replicated close35 4-source 35 mm Tx/Rx diagnostics across
seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close35_sources4_txrx35_seed_replicates
  --outdir outputs/experiments/301_coordinate_confidence_close35_sources4_txrx35_seed_replicates
  outputs/experiments/298_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/299_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/300_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/301_coordinate_confidence_close35_sources4_txrx35_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  4.32560e-03 / 5.74808e-03 / 7.34131e-03
acquisition group:
  4 sources, Tx/Rx offset 35 mm: rows=6, truth rows=6, x ambiguity=0

weakest lateral relative gaps:
  base nominal: 7.1952% (seed21)
  base source mismatch: 7.9334% (seed13)
  highband nominal: 44.2767% (seed34)
  highband source mismatch: 45.2911% (seed13)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 72.94
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.51
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
close35 is replicated across seeds 13, 21, and 34 under the 4-source 35 mm
Tx/Rx robust acquisition. All six rows recover truth geometry with strong
confidence and zero x ambiguity. The right-shifted x=286 mm branch is the
nearest repeated competitor but remains at least 7.20% worse under the base
objective. Move the geometry-stress branch to close30 with the same
acquisition before claiming the tight-separation limit.
```

## 302: Close-30 Sources=4, Tx/Rx Offset 35 mm, Seed34 Geometry Stress

Purpose:

```text
test whether the replicated 4-source 35 mm robust acquisition still resolves
target 2 when the center/right separation tightens from 35 mm to 30 mm.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,280 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,280
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/302_coordinate_optimizer_close30_seed34_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1399.5 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,280] mm
final state: x=[190,250,280], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=280,z=90,r=8, strong, x interval 280-280
  source_mismatch_noise10_seed34: best x=280,z=90,r=8, strong,
    x interval 280-280

base objective, noise10_seed34:
  x281/r7.5-minus-x280/r8 gap: +1.68189e-03 (2.4364% relative)
  x281/r8-minus-x280/r8 gap: +2.59941e-03 (3.7656% relative)
  x279/r8-minus-x280/r8 gap: +5.92264e-03 (8.5797% relative)

high-band objective, noise10_seed34:
  x281/r7.5-minus-x280/r8 gap: +1.26722e-03 (11.0084% relative)
  x281/r8-minus-x280/r8 gap: +2.52234e-03 (21.9117% relative)
  x279/r8-minus-x280/r8 gap: +5.93636e-03 (51.5697% relative)

base objective, source_mismatch_noise10_seed34:
  x281/r7.5-minus-x280/r8 gap: +3.42169e-03 (4.0612% relative)
  x281/r8-minus-x280/r8 gap: +4.31369e-03 (5.1200% relative)
  x279/r8-minus-x280/r8 gap: +9.85685e-03 (11.6992% relative)

high-band objective, source_mismatch_noise10_seed34:
  x281/r7.5-minus-x280/r8 gap: +3.21554e-03 (21.3384% relative)
  x281/r8-minus-x280/r8 gap: +4.45915e-03 (29.5910% relative)
  x279/r8-minus-x280/r8 gap: +9.60794e-03 (63.7585% relative)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 79.26
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close30 seed34 is a truth-geometry pass with strong labels and zero x
ambiguity, but it is the first geometry-stress result where the nearest
competitor is a coupled lateral/radius branch: x=281 mm, r=7.5 mm. The
nominal base gap is 2.44%, above the ambiguity threshold but much smaller than
close35. Treat close30 as a margin-aware pass and replicate seeds 13 and 21
before calling it validated.
```

## 303: Close-30 Sources=4, Tx/Rx Offset 35 mm, Seed13 Replication

Purpose:

```text
replicate the close30 seed34 margin-aware pass on seed13.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,280 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,280
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/303_coordinate_optimizer_close30_seed13_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1399.1 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,280] mm
final state: x=[190,250,280], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=280,z=90,r=8, strong, x interval 280-280
  source_mismatch_noise10_seed13: best x=280,z=90,r=8, strong,
    x interval 280-280

base objective, noise10_seed13:
  x281/r7.5-minus-x280/r8 gap: +1.85341e-03 (2.6598% relative)
  x281/r8-minus-x280/r8 gap: +3.04018e-03 (4.3629% relative)
  x279/r8-minus-x280/r8 gap: +5.50173e-03 (7.8955% relative)

high-band objective, noise10_seed13:
  x281/r7.5-minus-x280/r8 gap: +1.54403e-03 (13.1390% relative)
  x281/r8-minus-x280/r8 gap: +3.03493e-03 (25.8258% relative)
  x279/r8-minus-x280/r8 gap: +5.45893e-03 (46.4530% relative)

base objective, source_mismatch_noise10_seed13:
  x281/r7.5-minus-x280/r8 gap: +3.00141e-03 (3.5384% relative)
  x281/r8-minus-x280/r8 gap: +3.99171e-03 (4.7059% relative)
  x279/r8-minus-x280/r8 gap: +1.00804e-02 (11.8839% relative)

high-band objective, source_mismatch_noise10_seed13:
  x281/r7.5-minus-x280/r8 gap: +2.89518e-03 (18.5339% relative)
  x281/r8-minus-x280/r8 gap: +4.07965e-03 (26.1165% relative)
  x279/r8-minus-x280/r8 gap: +9.93335e-03 (63.5898% relative)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 80.82
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close30 seed13 confirms the seed34 result as another truth-geometry,
strong-label pass with zero x ambiguity. The same coupled x=281 mm, r=7.5 mm
branch is nearest, with a nominal base gap of 2.66% and source-mismatch base
gap of 3.54%. Run seed21 to complete the close30 seed set.
```

## 304: Close-30 Sources=4, Tx/Rx Offset 35 mm, Seed21 Replication

Purpose:

```text
complete the close30 seed replication under the 4-source 35 mm robust
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,280 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,280
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/304_coordinate_optimizer_close30_seed21_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1412.0 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,280] mm
final state: x=[190,250,280], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=280,z=90,r=8, strong, x interval 280-280
  source_mismatch_noise10_seed21: best x=280,z=90,r=8, strong,
    x interval 280-280

base objective, noise10_seed21:
  x281/r7.5-minus-x280/r8 gap: +1.49602e-03 (2.1815% relative)
  x281/r8-minus-x280/r8 gap: +2.57016e-03 (3.7479% relative)
  x279/r8-minus-x280/r8 gap: +5.93203e-03 (8.6502% relative)

high-band objective, noise10_seed21:
  x281/r7.5-minus-x280/r8 gap: +1.15278e-03 (10.4013% relative)
  x281/r8-minus-x280/r8 gap: +2.58570e-03 (23.3303% relative)
  x279/r8-minus-x280/r8 gap: +5.87037e-03 (52.9672% relative)

base objective, source_mismatch_noise10_seed21:
  x281/r7.5-minus-x280/r8 gap: +3.14644e-03 (3.6730% relative)
  x281/r8-minus-x280/r8 gap: +4.34803e-03 (5.0757% relative)
  x279/r8-minus-x280/r8 gap: +9.86470e-03 (11.5155% relative)

high-band objective, source_mismatch_noise10_seed21:
  x281/r7.5-minus-x280/r8 gap: +3.06856e-03 (18.9014% relative)
  x281/r8-minus-x280/r8 gap: +4.52857e-03 (27.8946% relative)
  x279/r8-minus-x280/r8 gap: +9.59165e-03 (59.0816% relative)
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 79.00
FIGURE_NOTES.md exists.
```

Interpretation:

```text
close30 seed21 completes the close30 seed set as a truth-geometry, strong-label
pass with zero x ambiguity. The coupled x=281 mm, r=7.5 mm branch remains the
nearest competitor and is only 2.18% worse under nominal base. Aggregate the
close30 set before deciding whether to probe closer spacing.
```

## 305: Close-30 Sources=4, Tx/Rx Offset 35 mm, Seed Aggregate

Purpose:

```text
summarize the replicated close30 4-source 35 mm Tx/Rx diagnostics across
seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close30_sources4_txrx35_seed_replicates
  --outdir outputs/experiments/305_coordinate_confidence_close30_sources4_txrx35_seed_replicates
  outputs/experiments/302_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/303_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/304_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/305_coordinate_confidence_close30_sources4_txrx35_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  1.49602e-03 / 2.43348e-03 / 3.42169e-03
acquisition group:
  4 sources, Tx/Rx offset 35 mm: rows=6, truth rows=6, x ambiguity=0

weakest coupled-branch relative gaps:
  base nominal: 2.1815% (seed21, x281/r7.5)
  base source mismatch: 3.5384% (seed13, x281/r7.5)
  highband nominal: 10.4013% (seed21, x281/r7.5)
  highband source mismatch: 18.5339% (seed13, x281/r7.5)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 71.20
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.52
FIGURE_NOTES.md includes source-count and acquisition summaries.
```

Interpretation:

```text
close30 is replicated across seeds 13, 21, and 34 under the 4-source 35 mm
Tx/Rx robust acquisition. All six rows recover truth geometry with strong
confidence and zero x ambiguity, but the aggregate radius margin mean is much
lower than close35 and the nearest repeated competitor is a coupled x=281 mm,
r=7.5 mm branch only 2.18% worse under nominal base. Treat close30 as the
current tightest replicated 35 mm-offset result, with margin-aware reporting.
Use a close25 seed34 lower-bound probe before claiming close30 as the final
geometry-separation limit.
```

## 306: Close-25 Sources=4, Tx/Rx Offset 35 mm, Seed34 Lower-Bound Probe

Purpose:

```text
probe whether the 4-source 35 mm robust acquisition can resolve target 2 when
the center/right separation tightens from 30 mm to 25 mm.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,275 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,275
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/306_coordinate_optimizer_close25_seed34_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1810.5 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,275] mm
final state: x=[190,250,275], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 160
revisit triggered for target 2; revisit did not resolve the ambiguity.

confidence rows:
  noise10_seed34 main: best x=276,z=90,r=7.5, weak,
    x interval 275-276, radius interval 7.5-8.0
  source_mismatch_noise10_seed34 main: best x=275,z=90,r=8, weak,
    x interval 275-276, radius interval 7.5-8.0
  noise10_seed34 revisit: best x=276,z=90,r=7.5, weak,
    x interval 275-276, radius interval 7.5-8.0
  source_mismatch_noise10_seed34 revisit: best x=275,z=90,r=8, weak,
    x interval 275-276, radius interval 7.5-8.0

base objective, noise10_seed34:
  x276/r7.5 is best.
  truth x275/r8 is +3.83534e-04 worse (0.6126% relative).

high-band objective, noise10_seed34:
  x276/r7.5 is best.
  truth x275/r8 is +7.38335e-04 worse (7.8952% relative).

base objective, source_mismatch_noise10_seed34:
  truth x275/r8 is best.
  x276/r7.5 is +3.24950e-04 worse (0.4272% relative).

high-band objective, source_mismatch_noise10_seed34:
  x276/r7.5 is best.
  truth x275/r8 is +1.73149e-04 worse (1.3864% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 63.12
FIGURE_NOTES.md exists and reports weak=4 with broad radius ambiguity.
```

Interpretation:

```text
close25 fails as a lower-bound probe for the 4-source 35 mm acquisition. The
main and revisit rows remain weak, keep x=275-276 mm and radius 7.5-8.0 mm
ambiguity intervals, and the nominal observation selects the shifted
x=276 mm, r=7.5 mm branch rather than truth. Treat close30 as the tightest
replicated result for the 35 mm Tx/Rx acquisition unless the extra-conservative
40 mm Tx/Rx offset rescues close25.
```

## 307: Close-25 Sources=4, Tx/Rx Offset 40 mm, Seed34 Rescue Probe

Purpose:

```text
test whether the extra-conservative 40 mm Tx/Rx offset rescues the failed
close25 seed34 geometry under the same 4-source scan count.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 40 --frequency-ghz 1.5
  --true-x-values-mm 190,250,275 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,275
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/307_coordinate_optimizer_close25_seed34_sources4_txrx40_objectives
```

Result:

```text
elapsed: 1408.4 s
sources: 4
tx_rx_offset_mm: 40.0
truth x positions: [190,250,275] mm
final state: x=[190,250,275], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=275,z=90,r=8, moderate,
    x interval 275-276, radius interval 7.5-8.0
  source_mismatch_noise10_seed34: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8

base objective, noise10_seed34:
  truth x275/r8 is best.
  x276/r7.5 is +6.32088e-04 worse (1.2365% relative).

high-band objective, noise10_seed34:
  truth x275/r8 is best.
  x276/r7.5 is +5.93536e-04 worse (5.8391% relative).

base objective, source_mismatch_noise10_seed34:
  truth x275/r8 is best.
  x276/r7.5 is +1.88927e-03 worse (2.6009% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x275/r8 is best.
  x276/r7.5 is +1.38954e-03 worse (9.6490% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 74.50
FIGURE_NOTES.md exists and reports moderate=1, strong=1.
```

Interpretation:

```text
the extra-conservative 40 mm Tx/Rx offset partially rescues close25 seed34:
both observed cases now select truth and no revisit is triggered. However, the
nominal row is only moderate and retains a near-best x=275-276 mm,
r=7.5-8.0 mm interval, with the x276/r7.5 branch only 1.24% above truth under
the base objective. Replicate seeds 13 and 21 before treating close25 as
validated under 40 mm Tx/Rx.
```

## 308: Close-25 Sources=4, Tx/Rx Offset 40 mm, Seed13 Rescue Replicate

Purpose:

```text
replicate the close25 40 mm Tx/Rx rescue probe on seed13 after seed34 showed
truth selection but only moderate nominal confidence.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 40 --frequency-ghz 1.5
  --true-x-values-mm 190,250,275 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,275
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/308_coordinate_optimizer_close25_seed13_sources4_txrx40_objectives
```

Result:

```text
elapsed: 1418.7 s
sources: 4
tx_rx_offset_mm: 40.0
truth x positions: [190,250,275] mm
final state: x=[190,250,275], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=275,z=90,r=8, moderate,
    x interval 275-276, radius interval 7.5-8.0
  source_mismatch_noise10_seed13: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8

base objective, noise10_seed13:
  truth x275/r8 is best.
  x276/r7.5 is +6.94296e-04 worse (1.3465% relative).

high-band objective, noise10_seed13:
  truth x275/r8 is best.
  x276/r7.5 is +7.31617e-04 worse (7.0607% relative).

base objective, source_mismatch_noise10_seed13:
  truth x275/r8 is best.
  x276/r7.5 is +1.66729e-03 worse (2.2767% relative).

high-band objective, source_mismatch_noise10_seed13:
  truth x275/r8 is best.
  x276/r7.5 is +1.27501e-03 worse (8.4155% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 75.34
FIGURE_NOTES.md exists and reports moderate=1, strong=1.
```

Interpretation:

```text
close25 seed13 repeats the 40 mm Tx/Rx rescue pattern from seed34: truth is
selected in both observed cases, no revisit is triggered, and the
source-mismatch row is strong. The nominal row is still only moderate and
retains the same near-best x=275-276 mm, r=7.5-8.0 mm interval, with the
x276/r7.5 branch only 1.35% above truth under the base objective. Run seed21
before validating close25 under 40 mm Tx/Rx; if seed21 also passes, aggregate
307-309 and report the result as margin-aware rather than high-margin.
```

## 309: Close-25 Sources=4, Tx/Rx Offset 40 mm, Seed21 Rescue Replicate

Purpose:

```text
complete the seed replication set for the close25 40 mm Tx/Rx rescue branch.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 40 --frequency-ghz 1.5
  --true-x-values-mm 190,250,275 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,275
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/309_coordinate_optimizer_close25_seed21_sources4_txrx40_objectives
```

Result:

```text
elapsed: 1402.4 s
sources: 4
tx_rx_offset_mm: 40.0
truth x positions: [190,250,275] mm
final state: x=[190,250,275], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=275,z=90,r=8, weak,
    x interval 275-276, radius interval 7.5-8.0
  source_mismatch_noise10_seed21: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8

base objective, noise10_seed21:
  truth x275/r8 is best.
  x276/r7.5 is +4.88175e-04 worse (0.9647% relative).

high-band objective, noise10_seed21:
  truth x275/r8 is best.
  x276/r7.5 is +4.70687e-04 worse (4.9112% relative).

base objective, source_mismatch_noise10_seed21:
  truth x275/r8 is best.
  x276/r7.5 is +1.42873e-03 worse (1.9323% relative).

high-band objective, source_mismatch_noise10_seed21:
  truth x275/r8 is best.
  x276/r7.5 is +9.76376e-04 worse (6.3329% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 75.88
FIGURE_NOTES.md exists and reports weak=1, strong=1.
```

Interpretation:

```text
close25 seed21 remains a truth-selected 40 mm Tx/Rx run, but it is the weakest
replicate: the nominal row is weak and keeps the near-best x=275-276 mm,
r=7.5-8.0 mm ambiguity interval, with the x276/r7.5 branch less than 1% above
truth under the base objective. Aggregate 307-309 before making any policy
statement; this should not be promoted as a zero-ambiguity geometry limit.
```

## 310: Close-25 Sources=4, Tx/Rx Offset 40 mm, Seed Aggregate

Purpose:

```text
summarize the close25 40 mm Tx/Rx rescue branch across seeds 34, 13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close25_sources4_txrx40_seed_replicates
  --outdir outputs/experiments/310_coordinate_confidence_close25_sources4_txrx40_seed_replicates
  outputs/experiments/307_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/308_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/309_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/310_coordinate_confidence_close25_sources4_txrx40_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=3, moderate=2, weak=1
fallback warning rows: 1
x-ambiguity rows: 3
max x/z/r ambiguity widths: 1.0 / 0.0 / 0.5 mm
radius margin abs min/mean/max:
  4.88175e-04 / 1.13331e-03 / 1.88927e-03
acquisition group:
  4 sources, Tx/Rx offset 40 mm: rows=6, truth rows=6, x ambiguity=3

weakest coupled-branch relative gaps:
  base nominal: 0.9647% (seed21, x276/r7.5)
  base source mismatch: 1.9323% (seed21, x276/r7.5)
  highband nominal: 4.9112% (seed21, x276/r7.5)
  highband source mismatch: 6.3329% (seed21, x276/r7.5)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 65.96
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 44.79
FIGURE_NOTES.md reports rows=6, truth rows=6, and x-ambiguity rows=3.
```

Interpretation:

```text
the 40 mm Tx/Rx offset rescues close25 as a truth-selected point estimate
across all three seeds, but not as a clean zero-ambiguity geometry limit. Half
of the rows retain a 1 mm lateral ambiguity interval, one nominal row is weak,
and the weakest base gap is only 0.9647%. Keep close30 under 35 mm Tx/Rx as
the tightest replicated zero-ambiguity geometry result. Record close25 under
40 mm Tx/Rx as a lower-margin recovery mode that requires interval reporting.
The next useful bracket is close28 under the original 35 mm robust acquisition
to locate the transition between close30 pass and close25 fail.
```

## 311: Close-28 Sources=4, Tx/Rx Offset 35 mm, Seed34 Bracket Probe

Purpose:

```text
bracket the transition between close30 truth-geometry pass and close25 35 mm
failure using the original 4-source, 35 mm Tx/Rx robust acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,278 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,278
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/311_coordinate_optimizer_close28_seed34_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1405.7 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,278] mm
final state: x=[190,250,278], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=278,z=90,r=8, weak,
    x interval 278-279, radius interval 7.5-8.0
  source_mismatch_noise10_seed34: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8

base objective, noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +4.53024e-04 worse (0.6831% relative).

high-band objective, noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +3.04065e-05 worse (0.2796% relative).

base objective, source_mismatch_noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +1.73564e-03 worse (2.1432% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +1.40613e-03 worse (9.9504% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 74.67
FIGURE_NOTES.md exists and reports weak=1, strong=1.
```

Interpretation:

```text
close28 seed34 is a truth-selected point-estimate pass under the original
35 mm robust acquisition, but it is already below the clean-confidence line:
the nominal row is weak, retains a 1 mm x ambiguity interval, and the
high-band x279/r7.5 branch is only 0.2796% above truth. Replicate seed13 only
if the goal is to map the transition band; do not treat close28 as validated
until seed replication and aggregate ambiguity reporting are complete.
```

## 312: Close-28 Sources=4, Tx/Rx Offset 35 mm, Seed13 Bracket Replicate

Purpose:

```text
replicate the close28 35 mm Tx/Rx transition-band probe on seed13 after seed34
selected truth but showed weak nominal confidence and lateral ambiguity.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,278 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,278
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/312_coordinate_optimizer_close28_seed13_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1407.8 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,278] mm
final state: x=[190,250,278], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=278,z=90,r=8, moderate,
    x interval 278-279, radius interval 7.5-8.0
  source_mismatch_noise10_seed13: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8

base objective, noise10_seed13:
  truth x278/r8 is best.
  x279/r7.5 is +5.83239e-04 worse (0.8714% relative).

high-band objective, noise10_seed13:
  truth x278/r8 is best.
  x279/r7.5 is +2.73266e-04 worse (2.4603% relative).

base objective, source_mismatch_noise10_seed13:
  truth x278/r8 is best.
  x279/r7.5 is +1.39728e-03 worse (1.7138% relative).

high-band objective, source_mismatch_noise10_seed13:
  truth x278/r8 is best.
  x279/r7.5 is +1.14618e-03 worse (7.8336% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 75.47
FIGURE_NOTES.md exists and reports moderate=1, strong=1.
```

Interpretation:

```text
close28 seed13 repeats the seed34 truth-selected transition-band pattern but
with slightly stronger nominal confidence. The nominal row is still not a
clean strong result and keeps the same x=278-279 mm, r=7.5-8.0 mm near-best
interval. Run seed21 and aggregate 311-313 before making a close28 policy
statement. Current evidence says close28 may be point-recoverable under
35 mm Tx/Rx, but still requires interval reporting like close25/40 mm.
```

## 313: Close-28 Sources=4, Tx/Rx Offset 35 mm, Seed21 Bracket Replicate

Purpose:

```text
complete the close28 35 mm Tx/Rx seed set before deciding whether close28 is
a clean geometry limit or only a transition-band point-recovery case.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 35 --frequency-ghz 1.5
  --true-x-values-mm 190,250,278 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,278
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/313_coordinate_optimizer_close28_seed21_sources4_txrx35_objectives
```

Result:

```text
elapsed: 1373.1 s
sources: 4
tx_rx_offset_mm: 35.0
truth x positions: [190,250,278] mm
final state: x=[190,250,278], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=278,z=90,r=8, weak,
    x interval 278-279, radius interval 7.5-8.0
  source_mismatch_noise10_seed21: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8

base objective, noise10_seed21:
  truth x278/r8 is best.
  x279/r7.5 is +2.82689e-04 worse (0.4291% relative).

high-band objective, noise10_seed21:
  x279/r7.5 is best.
  truth x278/r8 is +5.53495e-05 worse (0.5322% relative).

base objective, source_mismatch_noise10_seed21:
  truth x278/r8 is best.
  x279/r7.5 is +1.50218e-03 worse (1.8248% relative).

high-band objective, source_mismatch_noise10_seed21:
  truth x278/r8 is best.
  x279/r7.5 is +1.27499e-03 worse (8.3906% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 73.53
FIGURE_NOTES.md exists and reports weak=1, strong=1.
```

Interpretation:

```text
close28 seed21 completes the seed set as a truth-selected point update, but it
is the weakest close28 replicate. The nominal row is weak, retains the same
x=278-279 mm, r=7.5-8.0 mm ambiguity interval, and the high-band diagnostic
actually ranks the x279/r7.5 competitor above truth by 0.5322%. Aggregate
311-313 before setting policy; close28 should not be promoted as a clean
zero-ambiguity limit from this single run.
```

## 314: Close-28 Sources=4, Tx/Rx Offset 35 mm, Seed Aggregate

Purpose:

```text
summarize the close28 35 mm Tx/Rx transition-band bracket across seeds 34,
13, and 21.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close28_sources4_txrx35_seed_replicates
  --outdir outputs/experiments/314_coordinate_confidence_close28_sources4_txrx35_seed_replicates
  outputs/experiments/311_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/312_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/313_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/314_coordinate_confidence_close28_sources4_txrx35_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=3, moderate=1, weak=2
fallback warning rows: 2
x-ambiguity rows: 3
max x/z/r ambiguity widths: 1.0 / 0.0 / 0.5 mm
radius margin abs min/mean/max:
  2.82689e-04 / 9.92343e-04 / 1.73564e-03
acquisition group:
  4 sources, Tx/Rx offset 35 mm: rows=6, truth rows=6, x ambiguity=3

weakest coupled-branch relative gaps:
  base nominal: 0.4291% (seed21, x279/r7.5)
  base source mismatch: 1.7138% (seed13, x279/r7.5)
  highband nominal: x279/r7.5 beats truth by 0.5322% (seed21)
  highband source mismatch: 7.8336% (seed13, x279/r7.5)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 65.86
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 44.77
FIGURE_NOTES.md reports rows=6, truth rows=6, and x-ambiguity rows=3.
```

Interpretation:

```text
close28 is replicated as a truth-selected point estimate under the 4-source,
35 mm Tx/Rx acquisition, but it is not a clean zero-ambiguity geometry limit.
Half of the rows retain a 1 mm lateral ambiguity interval, two rows are weak,
and seed21 high-band nominal prefers the shifted x279/r7.5 branch. Keep
close30 as the tightest replicated clean 35 mm-offset separation result.
Classify close28 as a transition-band recovery mode requiring interval
reporting. The next useful question is whether an intermediate 37.5 mm or
40 mm Tx/Rx acquisition can make close28 clean without paying the ambiguity
cost seen at close25/40 mm.
```

## 315: Close-28 Sources=4, Tx/Rx Offset 40 mm, Seed34 Rescue Probe

Purpose:

```text
test whether the extra-conservative 40 mm Tx/Rx acquisition cleans up the
close28 ambiguity observed under the original 35 mm robust acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 40 --frequency-ghz 1.5
  --true-x-values-mm 190,250,278 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,278
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/315_coordinate_optimizer_close28_seed34_sources4_txrx40_objectives
```

Result:

```text
elapsed: 1394.8 s
sources: 4
tx_rx_offset_mm: 40.0
truth x positions: [190,250,278] mm
final state: x=[190,250,278], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=278,z=90,r=8, moderate,
    x interval 278-279, radius interval 7.5-8.0
  source_mismatch_noise10_seed34: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8

base objective, noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +6.40575e-04 worse (1.2088% relative).

high-band objective, noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +5.28545e-04 worse (4.8776% relative).

base objective, source_mismatch_noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +2.31717e-03 worse (3.0391% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x278/r8 is best.
  x279/r7.5 is +1.94764e-03 worse (12.2749% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 73.93
FIGURE_NOTES.md exists and reports moderate=1, strong=1.
```

Interpretation:

```text
the 40 mm Tx/Rx offset improves close28 seed34 relative to the 35 mm bracket:
truth now wins both base and high-band diagnostics, and the nominal high-band
gap increases from 0.2796% to 4.8776%. However, the nominal base gap is still
only 1.2088%, leaving the same x=278-279 mm, r=7.5-8.0 mm ambiguity interval.
Do not replicate 40 mm yet as a clean setting; first test whether an even more
conservative 45 mm Tx/Rx seed34 probe crosses the zero-ambiguity threshold.
```

## 316: Close-28 Sources=4, Tx/Rx Offset 45 mm, Seed34 Rescue Probe

Purpose:

```text
test whether an extra-conservative 45 mm Tx/Rx acquisition removes the close28
seed34 lateral/radius ambiguity that persisted at 40 mm.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,278 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,278
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/316_coordinate_optimizer_close28_seed34_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1422.0 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,278] mm
final state: x=[190,250,278], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8
  source_mismatch_noise10_seed34: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8

base objective, noise10_seed34:
  truth x278/r8 is best.
  x278/r7.5 is +2.25056e-03 worse (5.4584% relative).

high-band objective, noise10_seed34:
  truth x278/r8 is best.
  x278/r7.5 is +2.68644e-03 worse (25.8367% relative).

base objective, source_mismatch_noise10_seed34:
  truth x278/r8 is best.
  x278/r7.5 is +4.46740e-03 worse (6.5331% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x278/r8 is best.
  x278/r7.5 is +4.42880e-03 worse (25.3243% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 79.51
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
45 mm Tx/Rx cleans close28 seed34: both observed cases are strong, no x/radius
ambiguity interval remains, and the nearest competitor is now the same-x
smaller-radius x278/r7.5 branch rather than the shifted x279/r7.5 branch.
Replicate seeds 13 and 21 before promoting 45 mm as a clean close28 acquisition
rescue. This is a conservative acquisition, so compare its cost/geometry
against the existing close30 35 mm clean limit when writing final guidance.
```

## 317: Close-28 Sources=4, Tx/Rx Offset 45 mm, Seed13 Rescue Replicate

Purpose:

```text
replicate the clean close28 45 mm Tx/Rx seed34 rescue result on seed13.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,278 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,278
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/317_coordinate_optimizer_close28_seed13_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1407.8 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,278] mm
final state: x=[190,250,278], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8
  source_mismatch_noise10_seed13: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8

base objective, noise10_seed13:
  truth x278/r8 is best.
  x278/r7.5 is +2.26401e-03 worse (5.4497% relative).

high-band objective, noise10_seed13:
  truth x278/r8 is best.
  x278/r7.5 is +2.72573e-03 worse (25.9517% relative).

base objective, source_mismatch_noise10_seed13:
  truth x278/r8 is best.
  x278/r7.5 is +3.92538e-03 worse (5.6737% relative).

high-band objective, source_mismatch_noise10_seed13:
  truth x278/r8 is best.
  x278/r7.5 is +3.92275e-03 worse (21.1786% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 80.41
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close28 45 mm Tx/Rx seed13 replicates the clean seed34 result: both rows are
strong, no ambiguity interval remains, and the nearest competitor is again
the same-x smaller-radius x278/r7.5 branch with at least a 5.45% base gap.
Run seed21 and aggregate 316-318 before promoting 45 mm as a replicated clean
close28 acquisition rescue.
```

## 318: Close-28 Sources=4, Tx/Rx Offset 45 mm, Seed21 Rescue Replicate

Purpose:

```text
complete the close28 45 mm Tx/Rx seed replicate set with seed21 before
aggregating the extra-conservative acquisition rescue.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,278 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,278
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/318_coordinate_optimizer_close28_seed21_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1400.3 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,278] mm
final state: x=[190,250,278], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8
  source_mismatch_noise10_seed21: best x=278,z=90,r=8, strong,
    x interval 278-278, radius interval 8-8

base objective, noise10_seed21:
  truth x278/r8 is best.
  x278/r7.5 is +2.18203e-03 worse (5.3608% relative).

high-band objective, noise10_seed21:
  truth x278/r8 is best.
  x278/r7.5 is +2.57994e-03 worse (26.5229% relative).

base objective, source_mismatch_noise10_seed21:
  truth x278/r8 is best.
  x278/r7.5 is +4.15616e-03 worse (5.9815% relative).

high-band objective, source_mismatch_noise10_seed21:
  truth x278/r8 is best.
  x278/r7.5 is +4.02109e-03 worse (21.8081% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.79,
  nonwhite fraction 0.315978
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close28 45 mm Tx/Rx seed21 replicates the clean seed34 and seed13 pattern:
both rows are strong, no ambiguity interval remains, and all base/high-band
diagnostic objectives rank the true x278/z90/r8 geometry first. The nearest
competitor is the same-x smaller-radius x278/r7.5 branch, with the weakest
base gap still 5.36%. Aggregate 316-318 next; if all six rows stay strong with
zero x/radius ambiguity, classify 45 mm Tx/Rx as a replicated clean close28
acquisition rescue while keeping close30 as the cleaner 35 mm-offset limit.
```

## 319: Close-28 Sources=4, Tx/Rx Offset 45 mm, Seed Aggregate

Purpose:

```text
aggregate the close28 45 mm Tx/Rx seed34/seed13/seed21 rescue replicates and
decide whether the extra-conservative acquisition is a clean replicated result.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close28_sources4_txrx45_seed_replicates
  --outdir outputs/experiments/319_coordinate_confidence_close28_sources4_txrx45_seed_replicates
  outputs/experiments/316_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/317_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/318_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/319_coordinate_confidence_close28_sources4_txrx45_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
fallback warning rows: 0
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  2.18203e-03 / 3.20759e-03 / 4.46740e-03
acquisition group:
  4 sources, Tx/Rx offset 45 mm: rows=6, truth rows=6, x ambiguity=0

weakest base gaps:
  nominal: 5.3608% (seed21, x278/r7.5)
  source mismatch: 5.6737% (seed13, x278/r7.5)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 78.73,
  nonwhite fraction 0.221877
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.65,
  nonwhite fraction 0.039757
FIGURE_NOTES.md reports rows=6, truth rows=6, strong=6, and x-ambiguity rows=0.
```

Interpretation:

```text
45 mm Tx/Rx is a replicated clean close28 acquisition rescue: every row across
seed34, seed13, and seed21 selected truth geometry, every row was strong, and
no x/z/r ambiguity interval remained. This does not make close28 clean under
the standard 35 mm-offset acquisition; it means a larger Tx/Rx offset can buy
enough angular/offset diversity to separate the coupled x/radius branch.
Current policy should distinguish the two limits: close30 is the tightest
replicated clean result at 35 mm Tx/Rx, while close28 is clean only with the
extra-conservative 45 mm Tx/Rx acquisition.
Next run a close25 seed34 45 mm Tx/Rx lower-bound rescue probe. If it fails,
45 mm likely brackets between close25 and close28; if it passes cleanly, then
replicate seed13 and seed21 before lowering the clean-separation guidance.
```

## 320: Close-25 Sources=4, Tx/Rx Offset 45 mm, Seed34 Lower-Bound Rescue Probe

Purpose:

```text
test whether the extra-conservative 45 mm Tx/Rx acquisition that cleaned
close28 can also rescue the harder close25 geometry on seed34.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,275 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,275
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/320_coordinate_optimizer_close25_seed34_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1390.1 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,275] mm
final state: x=[190,250,275], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8
  source_mismatch_noise10_seed34: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8

base objective, noise10_seed34:
  truth x275/r8 is best.
  x274/r8 is +1.65541e-03 worse (4.1200% relative).

high-band objective, noise10_seed34:
  truth x275/r8 is best.
  x274/r8 is +1.76313e-03 worse (17.8553% relative).

base objective, source_mismatch_noise10_seed34:
  truth x275/r8 is best.
  x274/r8 is +4.08932e-03 worse (6.2006% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x275/r8 is best.
  x274/r8 is +4.28142e-03 worse (26.1069% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.59,
  nonwhite fraction 0.315134
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close25 seed34 is clean under the 45 mm Tx/Rx acquisition. Both observed cases
are strong, no ambiguity interval remains, and all base/high-band diagnostics
rank truth first. The nearest competitor has shifted from the earlier
close25/40 mm coupled x276/r7.5 branch to a same-radius lateral x274/r8 branch,
and the weakest base lateral gap is still 4.12%. This is enough to replicate
seed13 and seed21 before deciding whether 45 mm Tx/Rx can lower the clean
multi-rebar separation guidance from close28 to close25.
```

## 321: Close-25 Sources=4, Tx/Rx Offset 45 mm, Seed13 Rescue Replicate

Purpose:

```text
replicate the clean close25 45 mm Tx/Rx seed34 lower-bound rescue result on
seed13 before deciding whether to aggregate the seed set.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,275 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,275
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/321_coordinate_optimizer_close25_seed13_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1403.4 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,275] mm
final state: x=[190,250,275], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8
  source_mismatch_noise10_seed13: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8

base objective, noise10_seed13:
  truth x275/r8 is best.
  x274/r8 is +1.72347e-03 worse (4.2551% relative).

high-band objective, noise10_seed13:
  truth x275/r8 is best.
  x274/r8 is +1.84965e-03 worse (18.4776% relative).

base objective, source_mismatch_noise10_seed13:
  truth x275/r8 is best.
  x274/r8 is +3.68215e-03 worse (5.5210% relative).

high-band objective, source_mismatch_noise10_seed13:
  truth x275/r8 is best.
  x274/r8 is +3.73000e-03 worse (21.4676% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 90.89,
  nonwhite fraction 0.329789
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close25 45 mm Tx/Rx seed13 replicates the clean seed34 rescue: both rows are
strong, no ambiguity interval remains, and all base/high-band diagnostics rank
truth first. The nearest competitor is again the same-radius lateral x274/r8
branch, with the weakest base gap still 4.26%. Run seed21 and then aggregate
320-322 before lowering the clean separation guidance.
```

## 322: Close-25 Sources=4, Tx/Rx Offset 45 mm, Seed21 Rescue Replicate

Purpose:

```text
complete the close25 45 mm Tx/Rx seed replicate set before aggregating the
extra-conservative lower-bound rescue evidence.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,275 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,275
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/322_coordinate_optimizer_close25_seed21_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1393.8 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,275] mm
final state: x=[190,250,275], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8
  source_mismatch_noise10_seed21: best x=275,z=90,r=8, strong,
    x interval 275-275, radius interval 8-8

base objective, noise10_seed21:
  truth x275/r8 is best.
  x274/r8 is +1.72412e-03 worse (4.3456% relative).

high-band objective, noise10_seed21:
  truth x275/r8 is best.
  x274/r8 is +1.79334e-03 worse (19.4257% relative).

base objective, source_mismatch_noise10_seed21:
  truth x275/r8 is best.
  x274/r8 is +4.23134e-03 worse (6.3081% relative).

high-band objective, source_mismatch_noise10_seed21:
  truth x275/r8 is best.
  x274/r8 is +4.36969e-03 worse (25.2227% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.99,
  nonwhite fraction 0.318414
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close25 45 mm Tx/Rx seed21 completes the clean replicate set: both rows are
strong, no ambiguity interval remains, and all base/high-band diagnostics rank
truth first. The nearest competitor remains the same-radius lateral x274/r8
branch, with the weakest base gap 4.35%. Aggregate 320-322 next; if all six
rows stay strong with zero ambiguity, promote close25 as clean under 45 mm
Tx/Rx while clearly distinguishing that from the standard 35 mm acquisition.
```

## 323: Close-25 Sources=4, Tx/Rx Offset 45 mm, Seed Aggregate

Purpose:

```text
aggregate the close25 45 mm Tx/Rx seed34/seed13/seed21 rescue replicates and
decide whether the extra-conservative acquisition cleanly validates close25.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close25_sources4_txrx45_seed_replicates
  --outdir outputs/experiments/323_coordinate_confidence_close25_sources4_txrx45_seed_replicates
  outputs/experiments/320_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/321_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/322_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/323_coordinate_confidence_close25_sources4_txrx45_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
fallback warning rows: 0
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  2.50749e-03 / 3.64800e-03 / 5.02189e-03
acquisition group:
  4 sources, Tx/Rx offset 45 mm: rows=6, truth rows=6, x ambiguity=0

weakest base lateral gaps:
  nominal: 4.1200% (seed34, x274/r8)
  source mismatch: 5.5210% (seed13, x274/r8)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 79.04,
  nonwhite fraction 0.225545
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.63,
  nonwhite fraction 0.039700
FIGURE_NOTES.md reports rows=6, truth rows=6, strong=6, and x-ambiguity rows=0.
```

Interpretation:

```text
45 mm Tx/Rx cleanly validates close25 across seeds 34, 13, and 21: every row
selects truth, every row is strong, and no ambiguity interval remains. The
standard 35 mm acquisition still has close30 as the tightest clean replicated
limit, and close28/close25 require larger acquisition offsets. Under the
extra-conservative 45 mm Tx/Rx geometry, the clean limit now extends to
close25. The nearest systematic competitor is a same-radius lateral x274/r8
branch, not the earlier x276/r7.5 coupled branch from close25/40 mm.
Next run a close20 seed34 45 mm Tx/Rx lower-bound probe. If it fails, treat
close25 as the current practical 45 mm clean limit; if it passes cleanly,
replicate seeds 13 and 21 before lowering the guidance again.
```

## 324: Close-20 Sources=4, Tx/Rx Offset 45 mm, Seed34 Lower-Bound Probe

Purpose:

```text
test whether the 45 mm Tx/Rx acquisition that cleaned close25 can also recover
the tighter close20 geometry on seed34.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,270 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,270
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/324_coordinate_optimizer_close20_seed34_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1404.0 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,270] mm
final state: x=[190,250,270], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=270,z=90,r=8, strong,
    x interval 270-270, radius interval 8-8
  source_mismatch_noise10_seed34: best x=270,z=90,r=8, strong,
    x interval 270-270, radius interval 8-8

base objective, noise10_seed34:
  truth x270/r8 is best.
  x269/r8 is +1.08399e-03 worse (2.7705% relative).

high-band objective, noise10_seed34:
  truth x270/r8 is best.
  x269/r8 is +9.53060e-04 worse (10.1322% relative).

base objective, source_mismatch_noise10_seed34:
  truth x270/r8 is best.
  x269/r8 is +2.58113e-03 worse (4.0933% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x270/r8 is best.
  x269/r8 is +2.34524e-03 worse (14.9554% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.79,
  nonwhite fraction 0.317571
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close20 45 mm Tx/Rx seed34 is a clean point pass: both observed cases are
strong, no ambiguity interval remains, and all base/high-band diagnostics rank
truth first. The margin is narrower than close25, and the systematic
competitor is now same-radius lateral x269/r8 with the weakest base gap
2.77%. Replicate seed13 and seed21 before promoting close20 under 45 mm Tx/Rx.
```

## 325: Close-20 Sources=4, Tx/Rx Offset 45 mm, Seed13 Rescue Replicate

Purpose:

```text
replicate the close20 45 mm Tx/Rx seed34 lower-bound pass on seed13 before
aggregating the seed set.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,270 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,270
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/325_coordinate_optimizer_close20_seed13_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1398.6 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,270] mm
final state: x=[190,250,270], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=270,z=90,r=8, strong,
    x interval 270-270, radius interval 8-8
  source_mismatch_noise10_seed13: best x=270,z=90,r=8, strong,
    x interval 270-270, radius interval 8-8

base objective, noise10_seed13:
  truth x270/r8 is best.
  x269/r8 is +1.28725e-03 worse (3.2599% relative).

high-band objective, noise10_seed13:
  truth x270/r8 is best.
  x269/r8 is +1.22924e-03 worse (12.8285% relative).

base objective, source_mismatch_noise10_seed13:
  truth x270/r8 is best.
  x269/r8 is +2.23408e-03 worse (3.5078% relative).

high-band objective, source_mismatch_noise10_seed13:
  truth x270/r8 is best.
  x269/r8 is +1.84809e-03 worse (11.1629% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 90.25,
  nonwhite fraction 0.323236
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close20 45 mm Tx/Rx seed13 replicates the clean seed34 result. Both rows are
strong, no ambiguity interval remains, and all base/high-band diagnostics rank
truth first. The nearest competitor remains the same-radius lateral x269/r8
branch, with weakest base gap 3.26%. Run seed21 and aggregate 324-326 before
promoting close20 under 45 mm Tx/Rx.
```

## 326: Close-20 Sources=4, Tx/Rx Offset 45 mm, Seed21 Rescue Replicate

Purpose:

```text
complete the close20 45 mm Tx/Rx seed replicate set before aggregating.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,270 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,270
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/326_coordinate_optimizer_close20_seed21_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1419.6 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,270] mm
final state: x=[190,250,270], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=270,z=90,r=8, strong,
    x interval 270-270, radius interval 8-8
  source_mismatch_noise10_seed21: best x=270,z=90,r=8, strong,
    x interval 270-270, radius interval 8-8

base objective, noise10_seed21:
  truth x270/r8 is best.
  x269/r8 is +1.18854e-03 worse (3.0737% relative).

high-band objective, noise10_seed21:
  truth x270/r8 is best.
  x269/r8 is +9.82884e-04 worse (11.1747% relative).

base objective, source_mismatch_noise10_seed21:
  truth x270/r8 is best.
  x269/r8 is +2.47846e-03 worse (3.8636% relative).

high-band objective, source_mismatch_noise10_seed21:
  truth x270/r8 is best.
  x269/r8 is +2.20704e-03 worse (13.3149% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.89,
  nonwhite fraction 0.318765
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close20 45 mm Tx/Rx seed21 completes the clean replicate set: both rows are
strong, no ambiguity interval remains, and all base/high-band diagnostics rank
truth first. The nearest competitor remains x269/r8, with weakest base gap
3.07%. Aggregate 324-326 next; if the aggregate remains all-strong with zero
ambiguity, promote close20 under 45 mm Tx/Rx.
```

## 327: Close-20 Sources=4, Tx/Rx Offset 45 mm, Seed Aggregate

Purpose:

```text
aggregate the close20 45 mm Tx/Rx seed34/seed13/seed21 replicates and decide
whether the extra-conservative acquisition validates close20.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close20_sources4_txrx45_seed_replicates
  --outdir outputs/experiments/327_coordinate_confidence_close20_sources4_txrx45_seed_replicates
  outputs/experiments/324_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/325_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/326_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/327_coordinate_confidence_close20_sources4_txrx45_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
fallback warning rows: 0
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  2.69458e-03 / 3.97425e-03 / 5.39289e-03
acquisition group:
  4 sources, Tx/Rx offset 45 mm: rows=6, truth rows=6, x ambiguity=0

weakest base lateral gaps:
  nominal: 2.7705% (seed34, x269/r8)
  source mismatch: 3.5078% (seed13, x269/r8)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 79.39,
  nonwhite fraction 0.227778
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.64,
  nonwhite fraction 0.039725
FIGURE_NOTES.md reports rows=6, truth rows=6, strong=6, and x-ambiguity rows=0.
```

Interpretation:

```text
45 mm Tx/Rx cleanly validates close20 across seeds 34, 13, and 21: every row
selects truth, every row is strong, and no ambiguity interval remains. The
margin is narrower than close25 but still replicated, with the weakest base
lateral gap 2.77%. The standard 35 mm acquisition remains clean only through
close30; the extra-conservative 45 mm acquisition now extends the clean
replicated geometry separation to close20.
Next run a close15 seed34 45 mm Tx/Rx lower-bound probe. This is a near-touching
case with only about 1 mm gap between the 6 mm and 8 mm bars, so failure would
bracket the 45 mm clean limit near close20; a clean pass would require seed
replication before promotion.
```

## 328: Close-15 Sources=4, Tx/Rx Offset 45 mm, Seed34 Objective Diagnostics

Purpose:

```text
test whether the 45 mm Tx/Rx acquisition that cleaned close20 can also recover
the near-touching close15 geometry on seed34. The center-to-target spacing is
15 mm while the two radii sum to 14 mm, leaving about 1 mm physical gap between
the 6 mm and 8 mm bars.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,265 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,265
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/328_coordinate_optimizer_close15_seed34_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1404.8 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,265] mm
truth radii: [5,6,8] mm
final state: x=[190,250,265], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=265,z=90,r=8, strong,
    x interval 265-265, radius interval 8-8
  source_mismatch_noise10_seed34: best x=265,z=90,r=8, strong,
    x interval 265-265, radius interval 8-8

base objective, noise10_seed34:
  truth x265/r8 is best.
  x264/r8 is +1.16167e-03 worse (2.9713% relative).
  first non-r8 branch x266/r7.5 is +2.73249e-03 worse (6.9892% relative).

high-band objective, noise10_seed34:
  truth x265/r8 is best.
  x264/r8 is +9.92373e-04 worse (10.6209% relative).
  first non-r8 branch x265/r7.5 is +3.59931e-03 worse (38.5219% relative).

base objective, source_mismatch_noise10_seed34:
  truth x265/r8 is best.
  x264/r8 is +2.42657e-03 worse (3.8532% relative).
  first non-r8 branch x266/r7.5 is +5.30392e-03 worse (8.4223% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x265/r8 is best.
  x264/r8 is +2.02880e-03 worse (12.7554% relative).
  first non-r8 branch x265/r7.5 is +6.01561e-03 worse (37.8211% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.62,
  nonwhite fraction 0.316626
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close15 45 mm Tx/Rx seed34 is a clean point pass despite being near-touching:
both observed rows are strong, no x/z/r ambiguity interval remains, and every
base/high-band diagnostic ranks truth first. The nearest competitor is now the
same-radius lateral x264/r8 branch, not a smaller-radius substitute. The weakest
base lateral gap is 2.97%, so this is promising but still needs seed13 and
seed21 replication before the clean 45 mm separation guidance can be lowered
from close20 to close15.
```

## 329: Close-15 Sources=4, Tx/Rx Offset 45 mm, Seed13 Objective Diagnostics

Purpose:

```text
replicate the clean close15 45 mm Tx/Rx seed34 near-touching result on seed13
before deciding whether close15 can be promoted under the extra-conservative
45 mm acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,265 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,265
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/329_coordinate_optimizer_close15_seed13_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1409.3 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,265] mm
truth radii: [5,6,8] mm
final state: x=[190,250,265], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=265,z=90,r=8, strong,
    x interval 265-265, radius interval 8-8
  source_mismatch_noise10_seed13: best x=265,z=90,r=8, strong,
    x interval 265-265, radius interval 8-8

base objective, noise10_seed13:
  truth x265/r8 is best.
  x264/r8 is +1.39319e-03 worse (3.5259% relative).
  first non-r8 branch x266/r7.5 is +2.68085e-03 worse (6.7847% relative).

high-band objective, noise10_seed13:
  truth x265/r8 is best.
  x264/r8 is +1.28556e-03 worse (13.4400% relative).
  first non-r8 branch x266/r7.5 is +3.77783e-03 worse (39.4957% relative).

base objective, source_mismatch_noise10_seed13:
  truth x265/r8 is best.
  x264/r8 is +2.31043e-03 worse (3.6390% relative).
  first non-r8 branch x266/r7.5 is +5.41505e-03 worse (8.5289% relative).

high-band objective, source_mismatch_noise10_seed13:
  truth x265/r8 is best.
  x264/r8 is +1.92273e-03 worse (11.5121% relative).
  first non-r8 branch x265/r7.5 is +6.14810e-03 worse (36.8109% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.31,
  nonwhite fraction 0.312955
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close15 45 mm Tx/Rx seed13 replicates the clean seed34 near-touching result:
both rows are strong, no ambiguity interval remains, and all base/high-band
diagnostics rank truth first. The nearest competitor remains the same-radius
lateral x264/r8 branch, with weakest base gap 3.53%. Run seed21 and aggregate
328-330 before promoting close15 under 45 mm Tx/Rx.
```

## 330: Close-15 Sources=4, Tx/Rx Offset 45 mm, Seed21 Objective Diagnostics

Purpose:

```text
complete the close15 45 mm Tx/Rx seed replicate set before aggregating the
near-touching clean-pass evidence.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,265 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,265
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/330_coordinate_optimizer_close15_seed21_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1409.0 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,265] mm
truth radii: [5,6,8] mm
final state: x=[190,250,265], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=265,z=90,r=8, strong,
    x interval 265-265, radius interval 8-8
  source_mismatch_noise10_seed21: best x=265,z=90,r=8, strong,
    x interval 265-265, radius interval 8-8

base objective, noise10_seed21:
  truth x265/r8 is best.
  x264/r8 is +1.30635e-03 worse (3.3777% relative).
  first non-r8 branch x266/r7.5 is +2.60681e-03 worse (6.7402% relative).

high-band objective, noise10_seed21:
  truth x265/r8 is best.
  x264/r8 is +1.04585e-03 worse (11.9636% relative).
  first non-r8 branch x265/r7.5 is +3.54135e-03 worse (40.5102% relative).

base objective, source_mismatch_noise10_seed21:
  truth x265/r8 is best.
  x264/r8 is +2.19690e-03 worse (3.4340% relative).
  first non-r8 branch x265/r7.5 is +5.26377e-03 worse (8.2280% relative).

high-band objective, source_mismatch_noise10_seed21:
  truth x265/r8 is best.
  x264/r8 is +1.72443e-03 worse (10.2826% relative).
  first non-r8 branch x265/r7.5 is +5.80819e-03 worse (34.6337% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.31,
  nonwhite fraction 0.312952
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close15 45 mm Tx/Rx seed21 completes the clean seed set: both rows are strong,
no ambiguity interval remains, and all base/high-band diagnostics rank truth
first. The nearest competitor remains the same-radius lateral x264/r8 branch,
with weakest base gap 3.38%. Aggregate 328-330 next; if all six rows remain
truth-selected, strong, and zero-ambiguity, promote close15 as a clean
near-touching result under 45 mm Tx/Rx.
```

## 331: Close-15 Sources=4, Tx/Rx Offset 45 mm, Seed Aggregate

Purpose:

```text
aggregate the close15 45 mm Tx/Rx seed34/seed13/seed21 replicates and decide
whether the near-touching geometry is cleanly validated.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close15_sources4_txrx45_seed_replicates
  --outdir outputs/experiments/331_coordinate_confidence_close15_sources4_txrx45_seed_replicates
  outputs/experiments/328_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/329_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/330_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/331_coordinate_confidence_close15_sources4_txrx45_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
fallback warning rows: 0
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  2.60681e-03 / 4.00048e-03 / 5.41505e-03
acquisition group:
  4 sources, Tx/Rx offset 45 mm: rows=6, truth rows=6, x ambiguity=0

weakest base lateral gaps:
  nominal: 2.9713% (seed34, x264/r8)
  source mismatch: 3.4340% (seed21, x264/r8)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 79.44,
  nonwhite fraction 0.233998
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.62,
  nonwhite fraction 0.045367
FIGURE_NOTES.md reports rows=6, truth rows=6, strong=6, and x-ambiguity rows=0.
```

Interpretation:

```text
45 mm Tx/Rx cleanly validates close15 across seeds 34, 13, and 21: every row
selects truth, every row is strong, and no ambiguity interval remains. This is
a near-touching geometry with about 1 mm physical gap between the 6 mm center
bar and 8 mm target bar, so it materially extends the extra-conservative
45 mm acquisition guidance beyond close20. Keep close30 as the tightest clean
replicated result under the standard 35 mm acquisition, and report close15 as
requiring the larger 45 mm Tx/Rx acquisition.
Next run a close14 seed34 45 mm Tx/Rx tangent lower-bound probe. At close14,
the 6 mm and 8 mm bars are tangent in the truth geometry. A failure would
bracket the practical 45 mm clean limit at close15; a clean pass would require
seed replication before promotion.
```

## 332: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Objective Diagnostics

Purpose:

```text
test the tangent close14 lower-bound geometry after close15 was replicated as
clean under the 45 mm Tx/Rx acquisition. At close14, the 6 mm center bar and
8 mm target bar touch in the truth geometry.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/332_coordinate_optimizer_close14_seed34_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1401.1 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise10_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise10_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.21482e-03 worse (3.0986% relative).
  first non-r8 branch x265/r7.5 is +2.69546e-03 worse (6.8753% relative).

high-band objective, noise10_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.05041e-03 worse (11.2065% relative).
  first non-r8 branch x264/r7.5 is +3.61575e-03 worse (38.5753% relative).

base objective, source_mismatch_noise10_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.46573e-03 worse (3.8958% relative).
  first non-r8 branch x265/r7.5 is +5.27299e-03 worse (8.3312% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05725e-03 worse (12.8285% relative).
  first non-r8 branch x264/r7.5 is +6.05291e-03 worse (37.7445% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.55,
  nonwhite fraction 0.315814
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close14 45 mm Tx/Rx seed34 passes the tangent lower-bound probe cleanly:
both rows are strong, no ambiguity interval remains, and all base/high-band
diagnostics rank truth first. The nearest competitor is the same-radius lateral
x263/r8 branch, with weakest base gap 3.10%. Replicate seeds 13 and 21 before
promoting close14 under 45 mm Tx/Rx.
```

## 333: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed13 Objective Diagnostics

Purpose:

```text
replicate the clean close14 45 mm Tx/Rx tangent seed34 result on seed13 before
deciding whether close14 can be promoted under the extra-conservative 45 mm
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed13|source_mismatch_noise10_seed13
  --update-case-label source_mismatch_noise10_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/333_coordinate_optimizer_close14_seed13_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1392.6 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise10_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise10_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.43649e-03 worse (3.6243% relative).
  first non-r8 branch x265/r7.5 is +2.64555e-03 worse (6.6749% relative).

high-band objective, noise10_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.32367e-03 worse (13.7819% relative).
  first non-r8 branch x265/r7.5 is +3.75610e-03 worse (39.1080% relative).

base objective, source_mismatch_noise10_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.41026e-03 worse (3.7782% relative).
  first non-r8 branch x265/r7.5 is +5.39906e-03 worse (8.4634% relative).

high-band objective, source_mismatch_noise10_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.04885e-03 worse (12.1770% relative).
  first non-r8 branch x264/r7.5 is +6.27730e-03 worse (37.3079% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.21,
  nonwhite fraction 0.311737
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close14 45 mm Tx/Rx seed13 replicates the clean seed34 tangent result:
both rows are strong, no ambiguity interval remains, and all base/high-band
diagnostics rank truth first. The nearest competitor remains the same-radius
lateral x263/r8 branch, with weakest base gap 3.62%. Run seed21 and aggregate
332-334 before promoting close14 under 45 mm Tx/Rx.
```

## 334: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed21 Objective Diagnostics

Purpose:

```text
complete the close14 45 mm Tx/Rx tangent seed replicate set before aggregating
the clean-pass evidence.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed21|source_mismatch_noise10_seed21
  --update-case-label source_mismatch_noise10_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/334_coordinate_optimizer_close14_seed21_sources4_txrx45_objectives
```

Result:

```text
elapsed: 1409.8 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise10_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise10_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.36926e-03 worse (3.5299% relative).
  first non-r8 branch x265/r7.5 is +2.57355e-03 worse (6.6345% relative).

high-band objective, noise10_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.11620e-03 worse (12.7265% relative).
  first non-r8 branch x264/r7.5 is +3.57587e-03 worse (40.7707% relative).

base objective, source_mismatch_noise10_seed21:
  truth x264/r8 is best.
  x263/r8 is +2.23329e-03 worse (3.4747% relative).
  first non-r8 branch x265/r7.5 is +5.28358e-03 worse (8.2206% relative).

high-band objective, source_mismatch_noise10_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.73474e-03 worse (10.2672% relative).
  first non-r8 branch x264/r7.5 is +5.86985e-03 worse (34.7414% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.17,
  nonwhite fraction 0.311328
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
close14 45 mm Tx/Rx seed21 completes the clean seed set: both rows are strong,
no ambiguity interval remains, and all base/high-band diagnostics rank truth
first. The nearest competitor remains the same-radius lateral x263/r8 branch,
with weakest base gap 3.53%. Aggregate 332-334 next; if all six rows remain
truth-selected, strong, and zero-ambiguity, promote close14 as clean under
45 mm Tx/Rx.
```

## 335: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed Aggregate

Purpose:

```text
aggregate the close14 45 mm Tx/Rx seed34/seed13/seed21 tangent replicates and
decide whether the tangent geometry is cleanly validated.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close14_sources4_txrx45_seed_replicates
  --outdir outputs/experiments/335_coordinate_confidence_close14_sources4_txrx45_seed_replicates
  outputs/experiments/332_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/333_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/334_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/335_coordinate_confidence_close14_sources4_txrx45_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
fallback warning rows: 0
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  2.57355e-03 / 3.97836e-03 / 5.39906e-03
acquisition group:
  4 sources, Tx/Rx offset 45 mm: rows=6, truth rows=6, x ambiguity=0

weakest base lateral gaps:
  nominal: 3.0986% (seed34, x263/r8)
  source mismatch: 3.4747% (seed21, x263/r8)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 79.38,
  nonwhite fraction 0.233560
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 32.63,
  nonwhite fraction 0.045375
FIGURE_NOTES.md reports rows=6, truth rows=6, strong=6, and x-ambiguity rows=0.
```

Interpretation:

```text
45 mm Tx/Rx cleanly validates close14 across seeds 34, 13, and 21: every row
selects truth, every row is strong, and no ambiguity interval remains. This is
the tangent physical limit for the 6 mm center bar and 8 mm target bar; closer
truth spacing would overlap the two circular bars rather than describe two
separate non-overlapping rebars. Promote close14 as the clean physical spacing
floor under the 4-source, 45 mm Tx/Rx acquisition. Keep close30 as the tightest
clean replicated result under the standard 35 mm acquisition.
Next move from spacing lower-bound probes to acquisition-cost probes. Run a
close14 seed34 sources=3, Tx/Rx=45 mm diagnostic: if it fails, 4 sources remain
the minimum clean tangent acquisition; if it passes, replicate before lowering
the source-count guidance.
```

## 336: Close-14 Sources=3, Tx/Rx Offset 45 mm, Seed34 Cost Probe

Purpose:

```text
test whether the replicated clean close14 tangent result under 4 sources and
45 mm Tx/Rx can be made cheaper by reducing the scan to 3 sources.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 3 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise10_seed34|source_mismatch_noise10_seed34
  --update-case-label source_mismatch_noise10_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/336_coordinate_optimizer_close14_seed34_sources3_txrx45_objectives
```

Result:

```text
elapsed: 1087.5 s
sources: 3
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,265], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise10_seed34: best x=264,z=90,r=8, strong,
    x interval 264-265, radius interval 8-8
  source_mismatch_noise10_seed34: best x=265,z=90,r=8, strong,
    x interval 264-265, radius interval 8-8

base objective, noise10_seed34:
  truth x264/r8 is best.
  x265/r8 is +3.00863e-04 worse (0.9100% relative).
  first non-r8 branch x265/r7.5 is +3.18855e-03 worse (9.6442% relative).

high-band objective, noise10_seed34:
  truth x264/r8 is best.
  x263/r8 is +4.15238e-04 worse (4.7243% relative).
  x265/r8 is +5.07431e-04 worse (5.7732% relative).

base objective, source_mismatch_noise10_seed34:
  x265/r8 is best.
  truth x264/r8 is rank2, +7.48547e-05 worse (0.1702% relative).
  first non-r8 branch x266/r7.5 is +3.54963e-03 worse (8.0711% relative).

high-band objective, source_mismatch_noise10_seed34:
  truth x264/r8 is best.
  x265/r8 is +1.95933e-04 worse (1.5857% relative).
  first non-r8 branch x265/r7.5 is +4.09832e-03 worse (33.1684% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 94.35,
  nonwhite fraction 0.387244
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
sources=3 is not a clean tangent acquisition even though the radius margins are
strong. The reduced scan is faster, but the x landscape becomes too flat:
nominal keeps a 264-265 mm ambiguity interval, and the source-mismatch update
selects x265/r8 while truth x264/r8 is only 0.1702% worse. Keep sources=4 as
the minimum clean close14 tangent acquisition under 45 mm Tx/Rx.
```

## 337: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise20 Robustness Probe

Purpose:

```text
test whether the replicated clean close14 4-source 45 mm Tx/Rx tangent result
remains clean when observation noise is doubled from 10% RMS to 20% RMS.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise20_seed34|source_mismatch_noise20_seed34
  --update-case-label source_mismatch_noise20_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/337_coordinate_optimizer_close14_seed34_sources4_txrx45_noise20_objectives
```

Result:

```text
elapsed: 1394.8 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise20_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise20_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8

base objective, noise20_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.10005e-03 worse (0.9217% relative).
  first non-r8 branch x265/r7.5 is +2.45546e-03 worse (2.0574% relative).

high-band objective, noise20_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04461e-03 worse (9.8315% relative).
  first non-r8 branch x264/r7.5 is +3.58662e-03 worse (33.7558% relative).

base objective, source_mismatch_noise20_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.19756e-03 worse (1.2320% relative).
  first non-r8 branch x265/r7.5 is +4.59742e-03 worse (2.5775% relative).

high-band objective, source_mismatch_noise20_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05708e-03 worse (12.3924% relative).
  first non-r8 branch x264/r7.5 is +5.97437e-03 worse (35.9912% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.92,
  nonwhite fraction 0.318705
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
20% noise preserves truth-selected point recovery but not clean zero-ambiguity
recovery. Both rows are radius-strong and rank truth first, but both retain a
263-264 mm x-ambiguity interval. Treat 20% noise as an interval-reporting
robustness mode, not as a clean close14 operating point. Run a 15% noise seed34
probe to bracket where the clean zero-ambiguity threshold sits between the
replicated 10% clean result and this 20% interval result.
```

## 338: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15 Robustness Probe

Purpose:

```text
test whether the close14 4-source 45 mm Tx/Rx tangent result remains clean at
15% RMS noise, midway between the replicated 10% clean operating point and the
20% point-correct but x-ambiguous robustness result.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15_seed34|source_mismatch_noise15_seed34
  --update-case-label source_mismatch_noise15_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/338_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15_objectives
```

Result:

```text
elapsed: 1397.6 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.16333e-03 worse (1.5649% relative).
  first non-r8 branch x265/r7.5 is +2.58892e-03 worse (3.4826% relative).

high-band objective, noise15_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04759e-03 worse (10.5574% relative).
  first non-r8 branch x264/r7.5 is +3.60145e-03 worse (36.2946% relative).

base objective, source_mismatch_noise15_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.34860e-03 worse (2.0440% relative).
  first non-r8 branch x265/r7.5 is +4.96752e-03 worse (4.3233% relative).

high-band objective, source_mismatch_noise15_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05739e-03 worse (12.6907% relative).
  first non-r8 branch x264/r7.5 is +6.01427e-03 worse (37.0982% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.74,
  nonwhite fraction 0.318645
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15% RMS noise is clean for close14 seed34 under the 4-source, 45 mm Tx/Rx
tangent acquisition. Both rows select truth, both are strong, and the
ambiguity set collapses to the single truth point x264/z90/r8. This separates
15% from the 20% case: 20% still selected truth, but required interval
reporting because x263/r8 stayed inside the near-best ambiguity threshold.
Replicate 15% noise on seeds 13 and 21 before promoting it as a noise-robust
operating point; until then, the fully replicated clean noise level remains
10% RMS and 15% is a promising seed34 bracket result.
```

## 339: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed13 Noise15 Robustness Replicate

Purpose:

```text
replicate the clean close14 15% RMS noise seed34 result on seed13 before
promoting 15% noise as a robust tangent acquisition setting.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15_seed13|source_mismatch_noise15_seed13
  --update-case-label source_mismatch_noise15_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/339_coordinate_optimizer_close14_seed13_sources4_txrx45_noise15_objectives
```

Result:

```text
elapsed: 1412.1 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.48329e-03 worse (1.9745% relative).
  first non-r8 branch x265/r7.5 is +2.51638e-03 worse (3.3498% relative).

high-band objective, noise15_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.45725e-03 worse (14.0820% relative).
  first non-r8 branch x265/r7.5 is +3.72693e-03 worse (36.0150% relative).

base objective, source_mismatch_noise15_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.27042e-03 worse (1.9666% relative).
  first non-r8 branch x265/r7.5 is +5.14695e-03 worse (4.4583% relative).

high-band objective, source_mismatch_noise15_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.04459e-03 worse (11.6870% relative).
  first non-r8 branch x264/r7.5 is +6.34984e-03 worse (36.2961% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.21,
  nonwhite fraction 0.311725
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15% RMS noise remains clean for close14 seed13 under the 4-source, 45 mm Tx/Rx
tangent acquisition. Seed34 and seed13 now give 4/4 truth-selected, strong,
zero-ambiguity rows at 15% noise. The nearest lateral competitor is still the
same-radius x263/r8 branch, but it stays outside the ambiguity interval in
both observed cases and both objective diagnostics. Run seed21 next; if the
last two rows stay clean, aggregate 338-340 and promote 15% RMS as a
replicated clean noise level. If seed21 fails, classify 15% as seed-sensitive
and keep the replicated clean threshold at 10% RMS.
```

## 340: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed21 Noise15 Robustness Replicate

Purpose:

```text
complete the seed34/13/21 replication set for close14 tangent recovery at
15% RMS noise under the 4-source, 45 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15_seed21|source_mismatch_noise15_seed21
  --update-case-label source_mismatch_noise15_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/340_coordinate_optimizer_close14_seed21_sources4_txrx45_noise15_objectives
```

Result:

```text
elapsed: 1386.5 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.38646e-03 worse (1.8794% relative).
  first non-r8 branch x265/r7.5 is +2.41265e-03 worse (3.2704% relative).

high-band objective, noise15_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.14612e-03 worse (12.5707% relative).
  first non-r8 branch x264/r7.5 is +3.54130e-03 worse (38.8412% relative).

base objective, source_mismatch_noise15_seed21:
  truth x264/r8 is best.
  x263/r8 is +2.01895e-03 worse (1.7349% relative).
  first non-r8 branch x264/r7.5 is +4.92789e-03 worse (4.2346% relative).

high-band objective, source_mismatch_noise15_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.57336e-03 worse (8.9222% relative).
  first non-r8 branch x264/r7.5 is +5.73882e-03 worse (32.5435% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.23,
  nonwhite fraction 0.312535
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15% RMS noise remains clean for close14 seed21 under the 4-source, 45 mm Tx/Rx
tangent acquisition. Seeds 34, 13, and 21 now produce 6/6 truth-selected,
strong, zero-ambiguity rows at 15% RMS noise. The nearest same-radius lateral
competitor x263/r8 stays outside the ambiguity threshold in every observed
case, while first non-r8 branches remain farther away. Aggregate 338-340 next;
if the aggregate confirms the six-row summary, promote 15% RMS as the
replicated clean close14 tangent noise level and keep 20% RMS as
point-correct but interval-reporting.
```

## 341: Close-14 Sources=4, Tx/Rx Offset 45 mm, Noise15 Seed Aggregate

Purpose:

```text
aggregate the close14 15% RMS noise seed34/seed13/seed21 tangent replicates
and decide whether 15% RMS can be promoted as a replicated clean noise level.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close14_sources4_txrx45_noise15_seed_replicates
  --outdir outputs/experiments/341_coordinate_confidence_close14_sources4_txrx45_noise15_seed_replicates
  outputs/experiments/338_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/339_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/340_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/341_coordinate_confidence_close14_sources4_txrx45_noise15_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
fallback warning rows: 0
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  2.41265e-03 / 3.76005e-03 / 5.14695e-03
acquisition group:
  4 sources, Tx/Rx offset 45 mm: rows=6, truth rows=6, x ambiguity=0

weakest base lateral gaps:
  nominal: 1.5649% (seed34, x263/r8)
  source mismatch: 1.7349% (seed21, x263/r8)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255, std 75.79,
  nonwhite fraction 0.209716
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255, std 33.00,
  nonwhite fraction 0.046983
FIGURE_NOTES.md reports rows=6, truth rows=6, strong=6, and x-ambiguity rows=0.
```

Interpretation:

```text
15% RMS noise is now a replicated clean close14 tangent operating point under
the 4-source, 45 mm Tx/Rx acquisition. Across seeds 34, 13, and 21, all six
rows select truth, all six are strong, and no near-best x/z/r ambiguity
interval remains. This is a stronger claim than the 20% RMS result, where truth
was still ranked first but x263/r8 stayed within the ambiguity threshold.
Promote 15% RMS as clean and keep 20% RMS as point-correct but
interval-reporting. Run a 17.5% noise seed34 bracket next if the goal is to
locate the clean-to-interval transition more tightly.
```

## 342: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise17.5 Bracket Probe

Purpose:

```text
test a 17.5% RMS noise midpoint between the replicated clean 15% result and
the point-correct but x-ambiguous 20% result.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise17p5_seed34|source_mismatch_noise17p5_seed34
  --update-case-label source_mismatch_noise17p5_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/342_coordinate_optimizer_close14_seed34_sources4_txrx45_noise17p5_objectives
```

Result:

```text
elapsed: 1409.5 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise17p5_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise17p5_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise17p5_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.13291e-03 worse (1.1825% relative).
  first non-r8 branch x265/r7.5 is +2.52500e-03 worse (2.6356% relative).

high-band objective, noise17p5_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04612e-03 worse (10.2011% relative).
  first non-r8 branch x264/r7.5 is +3.59410e-03 worse (35.0473% relative).

base objective, source_mismatch_noise17p5_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.27634e-03 worse (1.5641% relative).
  first non-r8 branch x265/r7.5 is +4.78835e-03 worse (3.2902% relative).

high-band objective, source_mismatch_noise17p5_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05729e-03 worse (12.5604% relative).
  first non-r8 branch x264/r7.5 is +5.99447e-03 worse (36.5983% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 89.22,
  nonwhite fraction 0.310432
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
17.5% RMS noise is point-correct but not clean for close14 seed34 under the
4-source, 45 mm Tx/Rx tangent acquisition. Both rows select truth and keep
strong radius margins, but the nominal row has two near-best x candidates:
truth x264/r8 and same-radius x263/r8. That 263-264 mm x interval puts 17.5%
in the same interval-reporting family as 20%, though milder because the
source-mismatch row is still zero-ambiguity. The clean noise threshold is now
bracketed between the replicated 15% clean result and this 17.5% nominal
ambiguity. Run a 16.25% seed34 bracket if a tighter threshold is needed.
```

## 343: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise16.25 Bracket Probe

Purpose:

```text
test a 16.25% RMS noise midpoint between the replicated clean 15% result and
the seed34-ambiguous 17.5% bracket result.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise16p25_seed34|source_mismatch_noise16p25_seed34
  --update-case-label source_mismatch_noise16p25_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/343_coordinate_optimizer_close14_seed34_sources4_txrx45_noise16p25_objectives
```

Result:

```text
elapsed: 1403.0 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise16p25_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise16p25_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise16p25_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.14846e-03 worse (1.3545% relative).
  first non-r8 branch x265/r7.5 is +2.55773e-03 worse (3.0167% relative).

high-band objective, noise16p25_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04686e-03 worse (10.3812% relative).
  first non-r8 branch x264/r7.5 is +3.59779e-03 worse (35.6777% relative).

base objective, source_mismatch_noise16p25_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.31341e-03 worse (1.7810% relative).
  first non-r8 branch x265/r7.5 is +4.87968e-03 worse (3.7566% relative).

high-band objective, source_mismatch_noise16p25_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05735e-03 worse (12.6305% relative).
  first non-r8 branch x264/r7.5 is +6.00441e-03 worse (36.8622% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 88.90,
  nonwhite fraction 0.308970
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
16.25% RMS noise is also point-correct but not clean for close14 seed34 under
the 4-source, 45 mm Tx/Rx tangent acquisition. The nominal row selects truth
and has a strong radius margin, but x263/r8 stays inside the ambiguity
threshold, leaving the same 263-264 mm interval seen at 17.5%. The
source-mismatch row remains zero-ambiguity. The clean threshold is now
bracketed between replicated-clean 15% RMS and seed34-ambiguous 16.25% RMS.
Run a 15.625% seed34 midpoint if the threshold needs further tightening.
```

## 344: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15.625 Bracket Probe

Purpose:

```text
test a 15.625% RMS noise midpoint between the replicated clean 15% result and
the seed34-ambiguous 16.25% bracket result.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p625_seed34|source_mismatch_noise15p625_seed34
  --update-case-label source_mismatch_noise15p625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/344_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p625_objectives
```

Result:

```text
elapsed: 1408.9 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p625_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise15p625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p625_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15599e-03 worse (1.4543% relative).
  first non-r8 branch x265/r7.5 is +2.57353e-03 worse (3.2376% relative).

high-band objective, noise15p625_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04723e-03 worse (10.4699% relative).
  first non-r8 branch x264/r7.5 is +3.59962e-03 worse (35.9880% relative).

base objective, source_mismatch_noise15p625_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.33125e-03 worse (1.9060% relative).
  first non-r8 branch x265/r7.5 is +4.92407e-03 worse (4.0258% relative).

high-band objective, source_mismatch_noise15p625_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05737e-03 worse (12.6618% relative).
  first non-r8 branch x264/r7.5 is +6.00935e-03 worse (36.9838% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 88.58,
  nonwhite fraction 0.305460
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.625% RMS noise is still point-correct but not clean for close14 seed34 under
the 4-source, 45 mm Tx/Rx tangent acquisition. The nominal row selects truth
with a strong radius margin, but x263/r8 remains inside the ambiguity threshold
and keeps a 263-264 mm x interval. The source-mismatch row remains
zero-ambiguity. The clean threshold is now bracketed tightly between
replicated-clean 15% RMS and seed34-ambiguous 15.625% RMS. A 15.3125% seed34
midpoint is the next finer bracket if this threshold needs more precision.
```

## 345: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15.3125 Bracket Probe

Purpose:

```text
test a 15.3125% RMS noise midpoint between the replicated clean 15% result and
the seed34-ambiguous 15.625% bracket result.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p3125_seed34|source_mismatch_noise15p3125_seed34
  --update-case-label source_mismatch_noise15p3125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/345_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p3125_objectives
```

Result:

```text
elapsed: 1395.2 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p3125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p3125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p3125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15968e-03 worse (1.5082% relative).
  first non-r8 branch x265/r7.5 is +2.58128e-03 worse (3.3569% relative).

high-band objective, noise15p3125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04741e-03 worse (10.5137% relative).
  first non-r8 branch x264/r7.5 is +3.60054e-03 worse (36.1417% relative).

base objective, source_mismatch_noise15p3125_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.33999e-03 worse (1.9733% relative).
  first non-r8 branch x265/r7.5 is +4.94591e-03 worse (4.1708% relative).

high-band objective, source_mismatch_noise15p3125_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05738e-03 worse (12.6766% relative).
  first non-r8 branch x264/r7.5 is +6.01181e-03 worse (37.0419% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 88.32,
  nonwhite fraction 0.302732
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.3125% RMS noise is formally clean for close14 seed34 under the 4-source,
45 mm Tx/Rx tangent acquisition: both rows select truth, both are strong, and
both ambiguity intervals collapse to the single x264/z90/r8 point. This is an
edge-clean result, not a wide-margin result. In the nominal row, x263/r8 is
just outside the ambiguity threshold by about 6.27e-06 absolute misfit. The
clean-to-interval transition is now bracketed between seed34-clean 15.3125% RMS
and seed34-ambiguous 15.625% RMS, while the replicated clean level remains
15% RMS until a higher level is replicated. A 15.46875% seed34 midpoint is the
next finer bracket if needed.
```

## 346: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15.46875 Bracket Probe

Purpose:

```text
test a 15.46875% RMS noise midpoint between the edge-clean 15.3125% seed34
result and the seed34-ambiguous 15.625% bracket result.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p46875_seed34|source_mismatch_noise15p46875_seed34
  --update-case-label source_mismatch_noise15p46875_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/346_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p46875_objectives
```

Result:

```text
elapsed: 1385.4 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p46875_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise15p46875_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15784e-03 worse (1.4809% relative).
  first non-r8 branch x265/r7.5 is +2.57742e-03 worse (3.2965% relative).

high-band objective, noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04732e-03 worse (10.4918% relative).
  first non-r8 branch x264/r7.5 is +3.60008e-03 worse (36.0650% relative).

base objective, source_mismatch_noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.33564e-03 worse (1.9392% relative).
  first non-r8 branch x265/r7.5 is +4.93502e-03 worse (4.0974% relative).

high-band objective, source_mismatch_noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05738e-03 worse (12.6693% relative).
  first non-r8 branch x264/r7.5 is +6.01058e-03 worse (37.0131% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 88.04,
  nonwhite fraction 0.299639
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.46875% RMS noise is point-correct but not clean for close14 seed34 under
the 4-source, 45 mm Tx/Rx tangent acquisition. The nominal row again contains
two near-best same-radius x candidates, x263/r8 and truth x264/r8, so it needs
interval reporting. The source-mismatch row remains zero-ambiguity. The seed34
transition is now bracketed between 15.3125% edge-clean and 15.46875%
ambiguous. Since 15.3125% is already edge-clean, the next useful step is
replicating 15.3125% on seed13 before treating it as anything more than a
single-seed bracket point.
```

## 347: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed13 Noise15.3125 Replicate

Purpose:

```text
replicate the edge-clean 15.3125% RMS seed34 bracket point on seed13 before
treating 15.3125% as more than a single-seed clean result.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p3125_seed13|source_mismatch_noise15p3125_seed13
  --update-case-label source_mismatch_noise15p3125_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/347_coordinate_optimizer_close14_seed13_sources4_txrx45_noise15p3125_objectives
```

Result:

```text
elapsed: 1396.8 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p3125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p3125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p3125_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.48538e-03 worse (1.9117% relative).
  first non-r8 branch x265/r7.5 is +2.50741e-03 worse (3.2270% relative).

high-band objective, noise15p3125_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.46558e-03 worse (14.0899% relative).
  first non-r8 branch x265/r7.5 is +3.72508e-03 worse (35.8126% relative).

base objective, source_mismatch_noise15p3125_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.26056e-03 worse (1.8976% relative).
  first non-r8 branch x265/r7.5 is +5.12840e-03 worse (4.3051% relative).

high-band objective, source_mismatch_noise15p3125_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.04431e-03 worse (11.6514% relative).
  first non-r8 branch x264/r7.5 is +6.35430e-03 worse (36.2160% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 87.77,
  nonwhite fraction 0.295211
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.3125% RMS noise replicates cleanly on close14 seed13 under the 4-source,
45 mm Tx/Rx tangent acquisition. Both rows select truth, both are strong, and
both ambiguity intervals collapse to the single x264/z90/r8 point. This is
less edge-like than the seed34 clean result: the nearest same-radius x263/r8
competitor is 3.20e-04 absolute misfit above the nominal ambiguity cutoff and
4.74e-04 above the source-mismatch cutoff. With seed34 and seed13 now clean,
the next useful step is a 15.3125% seed21 replicate before aggregating or
promoting 15.3125% above the current replicated-clean 15% RMS level.
```

## 348: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed21 Noise15.3125 Replicate

Purpose:

```text
complete the 15.3125% RMS close14 tangent replicate set by running seed21
after seed34 and seed13 both recovered clean single-point confidence intervals.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p3125_seed21|source_mismatch_noise15p3125_seed21
  --update-case-label source_mismatch_noise15p3125_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/348_coordinate_optimizer_close14_seed21_sources4_txrx45_noise15p3125_objectives
```

Result:

```text
elapsed: 1413.9 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p3125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p3125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p3125_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.38683e-03 worse (1.8171% relative).
  first non-r8 branch x265/r7.5 is +2.40183e-03 worse (3.1470% relative).

high-band objective, noise15p3125_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.14798e-03 worse (12.5512% relative).
  first non-r8 branch x264/r7.5 is +3.53912e-03 worse (38.6945% relative).

base objective, source_mismatch_noise15p3125_seed21:
  truth x264/r8 is best.
  x263/r8 is +2.00486e-03 worse (1.6695% relative).
  first non-r8 branch x264/r7.5 is +4.90149e-03 worse (4.0817% relative).

high-band objective, source_mismatch_noise15p3125_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.56326e-03 worse (8.8367% relative).
  first non-r8 branch x264/r7.5 is +5.73058e-03 worse (32.3935% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 87.80,
  nonwhite fraction 0.296015
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.3125% RMS noise also replicates cleanly on close14 seed21 under the
4-source, 45 mm Tx/Rx tangent acquisition. Both rows select truth, both are
strong, and both ambiguity intervals collapse to the single x264/z90/r8 point.
The nearest same-radius x263/r8 competitor remains outside the ambiguity
cutoff by 2.42e-04 absolute misfit in the nominal row and 2.04e-04 in the
source-mismatch row. Seed34, seed13, and seed21 now all have clean 15.3125%
point-and-interval results. Aggregate 345/347/348 next before promoting
15.3125% above the current replicated-clean 15% RMS guidance.
```

## 349: Close-14 Sources=4, Tx/Rx Offset 45 mm, Noise15.3125 Seed Aggregate

Purpose:

```text
aggregate the close14 15.3125% RMS seed34/seed13/seed21 tangent replicates
and decide whether 15.3125% RMS can replace 15% RMS as the replicated clean
noise level.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  --run-name coordinate_confidence_close14_sources4_txrx45_noise15p3125_seed_replicates
  --outdir outputs/experiments/349_coordinate_confidence_close14_sources4_txrx45_noise15p3125_seed_replicates
  outputs/experiments/345_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/347_.../data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/348_.../data/multi_rebar_coordinate_optimizer_summary.json
```

Output:

```text
outputs/experiments/349_coordinate_confidence_close14_sources4_txrx45_noise15p3125_seed_replicates
```

Aggregate result:

```text
rows: 6
truth-geometry rows: 6
confidence labels: strong=6
fallback warning rows: 0
x-ambiguity rows: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius margin abs min/mean/max:
  2.40183e-03 / 3.74438e-03 / 5.12840e-03
acquisition group:
  4 sources, Tx/Rx offset 45 mm: rows=6, truth rows=6, x ambiguity=0

weakest base lateral gaps:
  nominal: 1.5082% (seed34, x263/r8)
  source mismatch: 1.6695% (seed21, x263/r8)
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255, std 73.30,
  nonwhite fraction 0.189795
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255, std 33.79,
  nonwhite fraction 0.044199
FIGURE_NOTES.md reports rows=6, truth rows=6, strong=6, and x-ambiguity rows=0.
```

Interpretation:

```text
15.3125% RMS noise is now a replicated clean close14 tangent operating point
under the 4-source, 45 mm Tx/Rx acquisition. Across seeds 34, 13, and 21, all
six rows select truth, all six are strong, and no near-best x/z/r ambiguity
interval remains. Promote 15.3125% RMS as the clean noise guidance for this
acquisition, replacing the previous 15% RMS guidance. Keep 15.46875% RMS as a
seed34 point-correct but interval-reporting bracket until additional evidence
shows otherwise. If the goal is to tighten the clean-to-interval transition,
run a 15.390625% seed34 midpoint between replicated-clean 15.3125% and
seed34-ambiguous 15.46875%.
```

## 350: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15.390625 Bracket Probe

Purpose:

```text
test a 15.390625% RMS noise midpoint between replicated-clean 15.3125% and
seed34-ambiguous 15.46875% to tighten the clean-to-interval transition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p390625_seed34|source_mismatch_noise15p390625_seed34
  --update-case-label source_mismatch_noise15p390625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/350_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p390625_objectives
```

Result:

```text
elapsed: 1359.3 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p390625_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise15p390625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p390625_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15876e-03 worse (1.4944% relative).
  first non-r8 branch x265/r7.5 is +2.57935e-03 worse (3.3265% relative).

high-band objective, noise15p390625_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04736e-03 worse (10.5028% relative).
  first non-r8 branch x264/r7.5 is +3.60031e-03 worse (36.1034% relative).

base objective, source_mismatch_noise15p390625_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.33782e-03 worse (1.9561% relative).
  first non-r8 branch x265/r7.5 is +4.94047e-03 worse (4.1339% relative).

high-band objective, source_mismatch_noise15p390625_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05738e-03 worse (12.6730% relative).
  first non-r8 branch x264/r7.5 is +6.01119e-03 worse (37.0275% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 87.70,
  nonwhite fraction 0.295126
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.390625% RMS noise is point-correct but not clean for close14 seed34 under
the 4-source, 45 mm Tx/Rx tangent acquisition. Both rows select truth and both
have strong radius margins, but the nominal row has two near-best same-radius
x candidates: truth x264/r8 and x263/r8. The ambiguity is extremely close:
x263/r8 is only 4.33e-06 absolute misfit below the ambiguity cutoff. The
seed34 transition is now bracketed between replicated-clean 15.3125% and
seed34-ambiguous 15.390625%. The next midpoint is 15.3515625% RMS if the goal
is to tighten the transition further.
```

## 351: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15.3515625 Bracket Probe

Purpose:

```text
test a 15.3515625% RMS noise midpoint between replicated-clean 15.3125% and
seed34-ambiguous 15.390625% to tighten the clean-to-interval transition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p3515625_seed34|source_mismatch_noise15p3515625_seed34
  --update-case-label source_mismatch_noise15p3515625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/351_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p3515625_objectives
```

Result:

```text
elapsed: 1404.7 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p3515625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p3515625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p3515625_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15922e-03 worse (1.5013% relative).
  first non-r8 branch x265/r7.5 is +2.58031e-03 worse (3.3417% relative).

high-band objective, noise15p3515625_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04738e-03 worse (10.5083% relative).
  first non-r8 branch x264/r7.5 is +3.60042e-03 worse (36.1226% relative).

base objective, source_mismatch_noise15p3515625_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.33890e-03 worse (1.9647% relative).
  first non-r8 branch x265/r7.5 is +4.94319e-03 worse (4.1523% relative).

high-band objective, source_mismatch_noise15p3515625_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05738e-03 worse (12.6748% relative).
  first non-r8 branch x264/r7.5 is +6.01150e-03 worse (37.0347% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 87.36,
  nonwhite fraction 0.291538
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.3515625% RMS noise is formally clean for close14 seed34 under the
4-source, 45 mm Tx/Rx tangent acquisition. Both rows select truth, both are
strong, and both ambiguity intervals collapse to the single x264/z90/r8 point.
This is an edge-clean result, not a wide-margin result: the nominal x263/r8
competitor is only 9.75e-07 absolute misfit above the ambiguity cutoff. The
seed34 transition is now bracketed between edge-clean 15.3515625% and
ambiguous 15.390625%. The next midpoint is 15.37109375% RMS if the goal is to
locate the single-seed transition more tightly. Do not promote beyond the
replicated-clean 15.3125% RMS guidance from this single edge-clean result.
```

## 352: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15.37109375 Bracket Probe

Purpose:

```text
test a 15.37109375% RMS noise midpoint between edge-clean 15.3515625% and
seed34-ambiguous 15.390625% to further localize the single-seed transition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p37109375_seed34|source_mismatch_noise15p37109375_seed34
  --update-case-label source_mismatch_noise15p37109375_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/352_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p37109375_objectives
```

Result:

```text
elapsed: 1404.3 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p37109375_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise15p37109375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p37109375_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15899e-03 worse (1.4978% relative).
  first non-r8 branch x265/r7.5 is +2.57983e-03 worse (3.3341% relative).

high-band objective, noise15p37109375_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04737e-03 worse (10.5055% relative).
  first non-r8 branch x264/r7.5 is +3.60037e-03 worse (36.1130% relative).

base objective, source_mismatch_noise15p37109375_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.33836e-03 worse (1.9604% relative).
  first non-r8 branch x265/r7.5 is +4.94183e-03 worse (4.1431% relative).

high-band objective, source_mismatch_noise15p37109375_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05738e-03 worse (12.6739% relative).
  first non-r8 branch x264/r7.5 is +6.01135e-03 worse (37.0311% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 87.00,
  nonwhite fraction 0.287933
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.37109375% RMS noise is point-correct but not clean for close14 seed34 under
the 4-source, 45 mm Tx/Rx tangent acquisition. Both rows select truth and both
have strong radius margins, but the nominal row keeps the x263/r8 to x264/r8
ambiguity interval. The ambiguity is again tiny: x263/r8 is 1.67e-06 absolute
misfit below the ambiguity cutoff. The single-seed seed34 transition is now
bracketed between 15.3515625% edge-clean and 15.37109375% ambiguous. The next
midpoint is 15.361328125% RMS if tighter single-seed localization remains
worth the runtime. The replicated clean guidance remains 15.3125% RMS.
```

## 353: Close-14 Sources=4, Tx/Rx Offset 45 mm, Seed34 Noise15.361328125 Bracket Probe

Purpose:

```text
test a 15.361328125% RMS noise midpoint between edge-clean 15.3515625% and
seed34-ambiguous 15.37109375% to decide whether more bisection is useful.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p361328125_seed34|source_mismatch_noise15p361328125_seed34
  --update-case-label source_mismatch_noise15p361328125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/353_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p361328125_objectives
```

Result:

```text
elapsed: 1397.5 s
sources: 4
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15911e-03 worse (1.4995% relative).
  first non-r8 branch x265/r7.5 is +2.58007e-03 worse (3.3379% relative).

high-band objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.04738e-03 worse (10.5069% relative).
  first non-r8 branch x264/r7.5 is +3.60039e-03 worse (36.1178% relative).

base objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.33863e-03 worse (1.9625% relative).
  first non-r8 branch x265/r7.5 is +4.94251e-03 worse (4.1477% relative).

high-band objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.05738e-03 worse (12.6743% relative).
  first non-r8 branch x264/r7.5 is +6.01142e-03 worse (37.0329% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 86.65,
  nonwhite fraction 0.284438
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
15.361328125% RMS noise is point-correct but not clean for close14 seed34
under the 4-source, 45 mm Tx/Rx tangent acquisition. Both rows select truth
and both are strong, but the nominal row again includes the same-radius x263/r8
competitor inside the ambiguity threshold. The margin is tiny: x263/r8 is only
3.49e-07 absolute misfit below the ambiguity cutoff. The single-seed seed34
transition is bracketed between 15.3515625% edge-clean and 15.361328125%
ambiguous, a 0.009765625 percentage-point RMS-noise interval. Stop bisection
for now: the practical replicated clean guidance remains 15.3125% RMS, and the
15.35%-level single-seed boundary is too threshold-sensitive to promote.
```

## 354: Close-14 Sources=5, Tx/Rx Offset 45 mm, Seed34 Noise15.361328125 Acquisition-Density Rescue

Purpose:

```text
test whether adding one scan/source position collapses the 4-source
15.361328125% RMS x-ambiguity interval without changing Tx/Rx offset,
frequency, or objective variants.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 5 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p361328125_seed34|source_mismatch_noise15p361328125_seed34
  --update-case-label source_mismatch_noise15p361328125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/354_coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives
```

Result:

```text
elapsed: 1685.7 s
sources: 5
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-265, radius interval 8-8
  source_mismatch_noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-265, radius interval 8-8

base objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.29275e-03 worse (1.8645% relative).
  first non-r8 branch x265/r7.5 is +1.49998e-03 worse (2.1634% relative).

high-band objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.29091e-03 worse (10.6225% relative).
  first non-r8 branch x265/r7.5 is +1.61186e-03 worse (13.2634% relative).

base objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.79138e-03 worse (2.0411% relative).
  first non-r8 branch x265/r7.5 is +2.44987e-03 worse (2.7914% relative).

high-band objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.70806e-03 worse (10.1454% relative).
  first non-r8 branch x265/r7.5 is +2.48499e-03 worse (14.7602% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255, std 87.91,
  nonwhite fraction 0.296626
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Adding a fifth source does not rescue the 15.361328125% close14 tangent
ambiguity. The optimizer still selects truth and both rows keep strong radius
labels, but the ambiguity interval shifts to the high-x side: x264/r8 and
x265/r8 are both near-best in both nominal and source-mismatch rows. The
extra source also narrows the best-vs-next-radius margins relative to the
4-source case. Treat sources=5 as point-correct but not clean at this noise
level. The next acquisition-density dose-response check, if pursued, should be
sources=7 rather than more single-source bisection.
```

## 355: Close-14 Sources=7, Tx/Rx Offset 45 mm, Seed34 Noise15.361328125 Acquisition-Density Rescue

Purpose:

```text
test whether a larger acquisition-density increase collapses the sources=4 and
sources=5 15.361328125% RMS x-ambiguity interval without changing Tx/Rx
offset, frequency, or objective variants.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 7 --tx-rx-offset-mm 45 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p361328125_seed34|source_mismatch_noise15p361328125_seed34
  --update-case-label source_mismatch_noise15p361328125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/355_coordinate_optimizer_close14_seed34_sources7_txrx45_noise15p361328125_objectives
```

Result:

```text
elapsed: 2327.1 s
sources: 7
tx_rx_offset_mm: 45.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +8.15291e-04 worse (1.1765% relative) and remains inside the
    ambiguity cutoff by 2.24197e-04.
  x265/r8 is +1.59867e-03 worse (2.3069% relative).
  first non-r8 branch x265/r7.5 is +2.55729e-03 worse (3.6902% relative).

high-band objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +6.95865e-04 worse (6.2267% relative).
  x265/r8 is +2.08627e-03 worse (18.6683% relative).
  first non-r8 branch x265/r7.5 is +3.15095e-03 worse (28.1953% relative).

base objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.40736e-03 worse (1.5030% relative) and sits only
    2.79198e-06 outside the ambiguity cutoff.
  x265/r8 is +2.56741e-03 worse (2.7418% relative).
  first non-r8 branch x265/r7.5 is +4.39931e-03 worse (4.6982% relative).

high-band objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.15118e-03 worse (7.1127% relative).
  x265/r8 is +3.06463e-03 worse (18.9350% relative).
  first non-r8 branch x265/r7.5 is +4.83048e-03 worse (29.8454% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.206,63.895,90.434), nonwhite fraction 0.293338
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Adding seven sources improves the 15.361328125% close14 tangent case but does
not make it replicated-clean. The point estimate is correct and radius
identifiability is strong in both rows. Compared with sources=5, the ambiguity
shifts back from the high-x side to the low-x side and the source-mismatch row
formally collapses to x=264 only. However, the nominal row still keeps x263/r8
inside the ambiguity cutoff, and the source-mismatch x263/r8 competitor clears
the cutoff by only 2.79e-06. Treat sources=7 as a partial rescue but still an
edge interval result at this noise level. Do not promote 15.361328125% RMS as
clean; keep the practical replicated-clean close14 guidance at 15.3125% RMS
under the 4-source, 45 mm Tx/Rx acquisition.
```

## 356: Close-14 Seed34 Noise15.361328125 Sources 4/5/7 Aggregate

Purpose:

```text
aggregate the same seed34 close14 15.361328125% RMS boundary case across
sources=4, sources=5, and sources=7 so the acquisition-density branch has one
decision table for point correctness, x-ambiguity rows, and radius margins.
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  outputs/experiments/353_coordinate_optimizer_close14_seed34_sources4_txrx45_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/354_coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/355_coordinate_optimizer_close14_seed34_sources7_txrx45_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name coordinate_confidence_close14_seed34_noise15p361328125_sources4_5_7_aggregate \
  --outdir outputs/experiments/356_coordinate_confidence_close14_seed34_noise15p361328125_sources4_5_7_aggregate
```

Output:

```text
outputs/experiments/356_coordinate_confidence_close14_seed34_noise15p361328125_sources4_5_7_aggregate
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 6 |
| Rows with true x/z/r | 6 |
| Strong labels | 6 |
| Fallback warning rows | 0 |
| Rows with nonzero x ambiguity | 4 |
| Max x/z/r ambiguity width | 1.0 / 0.0 / 0.0 mm |
| Radius margin min | 1.49998e-03 |
| Radius margin mean | 3.07151e-03 |
| Radius margin max | 4.94251e-03 |

Source-count summary:

| Sources | Rows true x/z/r | Rows with x ambiguity | Radius margin min | Radius margin mean | Radius margin max |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 2/2 | 1 | 2.58007e-03 | 3.76129e-03 | 4.94251e-03 |
| 5 | 2/2 | 2 | 1.49998e-03 | 1.97493e-03 | 2.44987e-03 |
| 7 | 2/2 | 1 | 2.55729e-03 | 3.47830e-03 | 4.39931e-03 |

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px,
  std=(76.541,53.664,69.246), nonwhite fraction 0.164430
coordinate_ambiguity_widths.png: 1720x971 px,
  std=(46.881,41.744,37.631), nonwhite fraction 0.090259
FIGURE_NOTES.md exists and reports source-count and ambiguity summaries.
```

Interpretation:

```text
The source-count dose response confirms the acquisition-density branch should
stop here. All three source counts remain point-correct with strong radius
labels, but none gives a replicated-clean zero-ambiguity result at
15.361328125% RMS. Five sources is worse than four and seven in this specific
boundary case: both rows keep x ambiguity and the radius margins are smallest.
Seven sources partially recovers margin and collapses the source-mismatch row,
but the nominal row still has a 1 mm x interval. Keep 15.3125% RMS as the
replicated-clean close14 tangent guidance under the 4-source, 45 mm Tx/Rx
acquisition. Treat 15.361328125% RMS as point-correct but interval-reporting
unless a new physics/objective lever is introduced.
```

## 357: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise15.361328125 Acquisition-Geometry Rescue

Purpose:

```text
test a distinct acquisition-geometry lever after source-count escalation failed:
keep the baseline 4 sources and raise Tx/Rx offset from 45 mm to 50 mm for the
same seed34 close14 15.361328125% RMS boundary case.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p361328125_seed34|source_mismatch_noise15p361328125_seed34
  --update-case-label source_mismatch_noise15p361328125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/357_coordinate_optimizer_close14_seed34_sources4_txrx50_noise15p361328125_objectives
```

Result:

```text
elapsed: 1410.8 s
sources: 4
tx_rx_offset_mm: 50.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p361328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.38289e-03 worse (2.3291% relative) and clears the ambiguity
    cutoff by 4.92278e-04.
  x265/r8 is +2.00473e-03 worse (3.3764% relative).
  first non-r8 branch x265/r7.5 is +2.22991e-03 worse (3.7557% relative).

high-band objective, noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.57554e-03 worse (17.4923% relative).
  x265/r8 is +2.91816e-03 worse (32.3987% relative).
  first non-r8 branch x264/z85/r5 is +3.22520e-03 worse (35.8075% relative).

base objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.50918e-03 worse (2.7315% relative) and clears the ambiguity
    cutoff by 1.13127e-03.
  x265/r8 is +4.28195e-03 worse (4.6613% relative).
  first non-r8 branch x265/r7.5 is +4.55064e-03 worse (4.9538% relative).

high-band objective, source_mismatch_noise15p361328125_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.65974e-03 worse (18.4834% relative).
  x265/r8 is +5.53699e-03 worse (38.4783% relative).
  first non-r8 branch x264/r7.5 is +5.70055e-03 worse (39.6150% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(100.429,62.943,88.903), nonwhite fraction 0.277907
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
The 50 mm Tx/Rx acquisition geometry rescues the seed34 15.361328125% close14
boundary case where 45 mm with 4/5/7 sources remained interval-reporting. The
point estimate is true, both rows are strong, and both x ambiguity intervals
collapse to the single true x=264 mm point. The nominal x263/r8 competitor is
outside the ambiguity cutoff by 4.92e-04, so this is meaningfully cleaner than
the edge-clean 15.3515625% 45 mm result. Replicate Tx/Rx=50 on seeds 13 and
21 before promoting 15.361328125% RMS as a clean operating point under the
larger offset acquisition.
```

## 358: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise15.361328125 Replicate

Purpose:

```text
replicate the clean seed34 Tx/Rx=50 acquisition-geometry rescue on seed13
before promoting the larger-offset 15.361328125% RMS close14 operating point.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p361328125_seed13|source_mismatch_noise15p361328125_seed13
  --update-case-label source_mismatch_noise15p361328125_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/358_coordinate_optimizer_close14_seed13_sources4_txrx50_noise15p361328125_objectives
```

Result:

```text
elapsed: 1421.0 s
sources: 4
tx_rx_offset_mm: 50.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p361328125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p361328125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p361328125_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.56653e-03 worse (2.6109% relative) and clears the ambiguity
    cutoff by 6.66518e-04.
  x265/r8 is +1.78813e-03 worse (2.9802% relative).
  first non-r8 branch x265/r7.5 is +2.17772e-03 worse (3.6295% relative).

high-band objective, noise15p361328125_seed13:
  truth x264/r8 is best.
  x263/r8 is +1.77712e-03 worse (19.0350% relative).
  x265/r8 is +2.67052e-03 worse (28.6043% relative).
  first non-r8 branch x264/z85/r5 is +2.89944e-03 worse (31.0562% relative).

base objective, source_mismatch_noise15p361328125_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.62365e-03 worse (2.8426% relative) and clears the ambiguity
    cutoff by 1.23917e-03.
  x265/r8 is +4.20787e-03 worse (4.5590% relative).
  first non-r8 branch x265/r7.5 is +4.72250e-03 worse (5.1165% relative).

high-band objective, source_mismatch_noise15p361328125_seed13:
  truth x264/r8 is best.
  x263/r8 is +2.92186e-03 worse (19.1712% relative).
  x265/r8 is +5.35063e-03 worse (35.1071% relative).
  first non-r8 branch x265/r7.5 is +6.08894e-03 worse (39.9514% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.834,62.621,88.390), nonwhite fraction 0.273018
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean Tx/Rx=50 acquisition-geometry rescue. Both rows
are true, strong, and zero-ambiguity in x/z/r. The nearest x263/r8 competitor
clears the ambiguity cutoff by a larger nominal margin than seed34. Run seed21
at the same 4-source, 50 mm Tx/Rx, 15.361328125% RMS setting before aggregate
promotion.
```

## 359: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise15.361328125 Replicate

Purpose:

```text
complete the seed34/13/21 Tx/Rx=50 replicate set for the close14
15.361328125% RMS acquisition-geometry rescue before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p361328125_seed21|source_mismatch_noise15p361328125_seed21
  --update-case-label source_mismatch_noise15p361328125_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/359_coordinate_optimizer_close14_seed21_sources4_txrx50_noise15p361328125_objectives
```

Result:

```text
elapsed: 1395.1 s
sources: 4
tx_rx_offset_mm: 50.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p361328125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p361328125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p361328125_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.58751e-03 worse (2.6938% relative) and clears the ambiguity
    cutoff by 7.03537e-04.
  x265/r8 is +1.80664e-03 worse (3.0657% relative).
  first non-r8 branch x265/r7.5 is +2.08630e-03 worse (3.5402% relative).

high-band objective, noise15p361328125_seed21:
  truth x264/r8 is best.
  x263/r8 is +1.70327e-03 worse (20.6263% relative).
  x265/r8 is +2.80484e-03 worse (33.9661% relative).
  first non-r8 branch x265/r7.5 is +3.17453e-03 worse (38.4430% relative).

base objective, source_mismatch_noise15p361328125_seed21:
  truth x264/r8 is best.
  x263/r8 is +2.26086e-03 worse (2.4460% relative) and clears the ambiguity
    cutoff by 8.74399e-04.
  x265/r8 is +4.54734e-03 worse (4.9197% relative).
  first non-r8 branch x265/r7.5 is +4.68706e-03 worse (5.0709% relative).

high-band objective, source_mismatch_noise15p361328125_seed21:
  truth x264/r8 is best.
  x263/r8 is +2.19692e-03 worse (14.6876% relative).
  x265/r8 is +6.00544e-03 worse (40.1496% relative).
  first non-r8 branch x264/r7.5 is +5.58420e-03 worse (37.3334% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.532,62.459,88.130), nonwhite fraction 0.270578
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean Tx/Rx=50 replicate set: all seed21 rows are true,
strong, and zero-ambiguity in x/z/r. The nearest x263/r8 competitor clears the
ambiguity cutoff by meaningful margins in both nominal and source-mismatch
rows. Aggregate 357-359 next; if the aggregate confirms 6/6 true, strong,
zero-ambiguity rows, promote 50 mm Tx/Rx as the replicated larger-offset
rescue for the close14 15.361328125% RMS boundary.
```

## 360: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise15.361328125 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 Tx/Rx=50 replicate set and decide whether the
larger-offset acquisition should be promoted as a clean close14
15.361328125% RMS operating point.
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  outputs/experiments/357_coordinate_optimizer_close14_seed34_sources4_txrx50_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/358_coordinate_optimizer_close14_seed13_sources4_txrx50_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/359_coordinate_optimizer_close14_seed21_sources4_txrx50_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name coordinate_confidence_close14_sources4_txrx50_noise15p361328125_seed_replicates \
  --outdir outputs/experiments/360_coordinate_confidence_close14_sources4_txrx50_noise15p361328125_seed_replicates
```

Output:

```text
outputs/experiments/360_coordinate_confidence_close14_sources4_txrx50_noise15p361328125_seed_replicates
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 6 |
| Rows with true x/z/r | 6 |
| Strong labels | 6 |
| Fallback warning rows | 0 |
| Rows with nonzero x ambiguity | 0 |
| Max x/z/r ambiguity width | 0.0 / 0.0 / 0.0 mm |
| Radius margin min | 2.08630e-03 |
| Radius margin mean | 3.40902e-03 |
| Radius margin max | 4.72250e-03 |

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px,
  std=(80.556,55.560,72.624), nonwhite fraction 0.179731
coordinate_ambiguity_widths.png: 1720x971 px,
  std=(34.597,34.514,34.726), nonwhite fraction 0.053285
FIGURE_NOTES.md exists and reports 6 rows, strong=6, x-ambiguity rows=0.
```

Interpretation:

```text
Tx/Rx=50 mm is now a replicated clean larger-offset rescue for the close14
tangent 15.361328125% RMS boundary. It fixes the interval behavior that
remained under 45 mm Tx/Rx with 4, 5, and 7 sources: all six replicated rows
are truth geometry, all six are strong, and no row retains x/z/r ambiguity.
Promote 4 sources with 50 mm Tx/Rx as a clean operating point at
15.361328125% RMS, while keeping the cheaper 45 mm Tx/Rx guidance at
15.3125% RMS for replicated clean operation.
```

## 361: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise15.46875 Bracket Probe

Purpose:

```text
test whether the replicated Tx/Rx=50 acquisition can also clean the next old
45 mm ambiguous bracket, 15.46875% RMS noise on seed34.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p46875_seed34|source_mismatch_noise15p46875_seed34
  --update-case-label source_mismatch_noise15p46875_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/361_coordinate_optimizer_close14_seed34_sources4_txrx50_noise15p46875_objectives
```

Result:

```text
elapsed: 1390.3 s
sources: 4
tx_rx_offset_mm: 50.0
truth x positions: [190,250,264] mm
truth radii: [5,6,8] mm
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p46875_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p46875_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.38186e-03 worse (2.3010% relative) and clears the ambiguity
    cutoff by 4.81039e-04.
  x265/r8 is +2.00334e-03 worse (3.3359% relative).
  first non-r8 branch x265/r7.5 is +2.22819e-03 worse (3.7103% relative).

high-band objective, noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +1.57571e-03 worse (17.4723% relative).
  x265/r8 is +2.91800e-03 worse (32.3564% relative).
  first non-r8 branch x264/z85/r5 is +3.22666e-03 worse (35.7790% relative).

base objective, source_mismatch_noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.50676e-03 worse (2.6998% relative) and clears the ambiguity
    cutoff by 1.11404e-03.
  x265/r8 is +4.27705e-03 worse (4.6065% relative).
  first non-r8 branch x265/r7.5 is +4.54524e-03 worse (4.8953% relative).

high-band objective, source_mismatch_noise15p46875_seed34:
  truth x264/r8 is best.
  x263/r8 is +2.65980e-03 worse (18.4767% relative).
  x265/r8 is +5.53695e-03 worse (38.4633% relative).
  first non-r8 branch x264/r7.5 is +5.69971e-03 worse (39.5940% relative).
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.017,63.766,90.265), nonwhite fraction 0.291144
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
The 50 mm Tx/Rx acquisition cleans the 15.46875% RMS seed34 bracket that was
interval-reporting under 45 mm Tx/Rx. This is a seed34 bracket pass, not yet a
promoted operating point. Replicate 15.46875% RMS at Tx/Rx=50 on seeds 13 and
21 before promoting this higher noise level.
```

## 362: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise15.46875 Replicate

Purpose:

```text
replicate the clean seed34 15.46875% RMS Tx/Rx=50 bracket on seed13 before
promoting the higher-noise larger-offset operating point.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p46875_seed13|source_mismatch_noise15p46875_seed13
  --update-case-label source_mismatch_noise15p46875_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/362_coordinate_optimizer_close14_seed13_sources4_txrx50_noise15p46875_objectives
```

Result:

```text
elapsed: 1404.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p46875_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p46875_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p46875_seed13:
  x263/r8 is +1.56664e-03 worse (2.5815% relative) and clears the ambiguity
    cutoff by 6.56321e-04.
  first non-r8 branch x265/r7.5 is +2.17566e-03 worse (3.5850% relative).

base objective, source_mismatch_noise15p46875_seed13:
  x263/r8 is +2.62190e-03 worse (2.8106% relative) and clears the ambiguity
    cutoff by 1.22263e-03.
  first non-r8 branch x265/r7.5 is +4.71812e-03 worse (5.0578% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.77870e-03 worse nominal and +2.92374e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.465,63.466,89.788), nonwhite fraction 0.286256
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the 15.46875% RMS Tx/Rx=50 seed34 pass. Both rows are true,
strong, and zero-ambiguity in x/z/r, with x263/r8 comfortably outside the
ambiguity cutoff. Run seed21 next before aggregate promotion.
```

## 363: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise15.46875 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 15.46875% RMS Tx/Rx=50
close14 bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p46875_seed21|source_mismatch_noise15p46875_seed21
  --update-case-label source_mismatch_noise15p46875_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/363_coordinate_optimizer_close14_seed21_sources4_txrx50_noise15p46875_objectives
```

Result:

```text
elapsed: 1357.1 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p46875_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p46875_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p46875_seed21:
  x263/r8 is +1.58775e-03 worse (2.6636% relative) and clears the ambiguity
    cutoff by 6.93601e-04.
  first non-r8 branch x265/r7.5 is +2.08368e-03 worse (3.4955% relative).

base objective, source_mismatch_noise15p46875_seed21:
  x263/r8 is +2.25698e-03 worse (2.4159% relative) and clears the ambiguity
    cutoff by 8.55662e-04.
  first non-r8 branch x264/r7.5 is +4.68220e-03 worse (5.0119% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.70433e-03 worse nominal and +2.19374e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(100.994,63.213,89.383), nonwhite fraction 0.282189
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 15.46875% RMS Tx/Rx=50 replicate set. All seed21
rows are true, strong, and zero-ambiguity in x/z/r. Aggregate 361-363 next; if
the aggregate remains 6/6 true, strong, and zero-ambiguity, promote
15.46875% RMS under 4-source 50 mm Tx/Rx.
```

## 364: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise15.46875 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 15.46875% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this higher
noise bracket.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/361_coordinate_optimizer_close14_seed34_sources4_txrx50_noise15p46875_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/362_coordinate_optimizer_close14_seed13_sources4_txrx50_noise15p46875_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/363_coordinate_optimizer_close14_seed21_sources4_txrx50_noise15p46875_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise15p46875_seed_replicates
  --outdir outputs/experiments/364_coordinate_confidence_close14_sources4_txrx50_noise15p46875_seed_replicates
```

Output:

```text
outputs/experiments/364_coordinate_confidence_close14_sources4_txrx50_noise15p46875_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 2.08368e-03 / 3.40552e-03 / 4.71812e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(83.018,56.592,74.663), nonwhite fraction 0.189485
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(34.067,33.982,34.198), nonwhite fraction 0.050680
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 15.46875% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 15.46875% RMS as the current clean operating
point for the larger-offset acquisition. The next stress test is the 15.625%
RMS bracket under the same acquisition.
```

## 365: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise15.625 Probe

Purpose:

```text
test the next close14 tangent noise bracket, 15.625% RMS, after 15.46875% RMS
was replicated clean under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p625_seed34|source_mismatch_noise15p625_seed34
  --update-case-label source_mismatch_noise15p625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/365_coordinate_optimizer_close14_seed34_sources4_txrx50_noise15p625_objectives
```

Result:

```text
elapsed: 1405.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p625_seed34:
  x263/r8 is +1.38034e-03 worse (2.2610% relative) and clears the ambiguity
    cutoff by 4.64584e-04.
  first non-r8 branch x265/r7.5 is +2.22567e-03 worse (3.6456% relative).

base objective, source_mismatch_noise15p625_seed34:
  x263/r8 is +2.50321e-03 worse (2.6547% relative) and clears the ambiguity
    cutoff by 1.08882e-03.
  first non-r8 branch x265/r7.5 is +4.53734e-03 worse (4.8120% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.57596e-03 worse nominal and +2.65989e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.677,64.100,90.829), nonwhite fraction 0.296965
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 15.625% RMS under the 4-source, 50 mm Tx/Rx acquisition:
both rows selected the true x264/z90/r8 target-2 geometry, both were strong,
and x/z/r ambiguity widths were zero. This is not yet a promoted operating
point because it is only one seed. Replicate 15.625% RMS on seeds 13 and 21,
then aggregate 365 plus those replicates before promoting the bracket.
```

## 366: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise15.625 Replicate

Purpose:

```text
replicate the 15.625% RMS seed34 clean result on seed13 before deciding
whether the larger-offset acquisition can be promoted at this bracket.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p625_seed13|source_mismatch_noise15p625_seed13
  --update-case-label source_mismatch_noise15p625_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/366_coordinate_optimizer_close14_seed13_sources4_txrx50_noise15p625_objectives
```

Result:

```text
elapsed: 1410.1 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p625_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p625_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p625_seed13:
  x263/r8 is +1.56679e-03 worse (2.5396% relative) and clears the ambiguity
    cutoff by 6.41374e-04.
  first non-r8 branch x265/r7.5 is +2.17266e-03 worse (3.5217% relative).

base objective, source_mismatch_noise15p625_seed13:
  x263/r8 is +2.61934e-03 worse (2.7651% relative) and clears the ambiguity
    cutoff by 1.19842e-03.
  first non-r8 branch x265/r7.5 is +4.71172e-03 worse (4.9739% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.78099e-03 worse nominal and +2.92647e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.098,63.785,90.329), nonwhite fraction 0.291673
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 15.625% RMS Tx/Rx=50 result. Both seed13 rows are
true, strong, and zero-ambiguity in x/z/r. Run seed21 next; if it also remains
clean, aggregate 365-367 before promoting the 15.625% RMS bracket.
```

## 367: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise15.625 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 15.625% RMS Tx/Rx=50 close14
bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise15p625_seed21|source_mismatch_noise15p625_seed21
  --update-case-label source_mismatch_noise15p625_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/367_coordinate_optimizer_close14_seed21_sources4_txrx50_noise15p625_objectives
```

Result:

```text
elapsed: 1410.8 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise15p625_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise15p625_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise15p625_seed21:
  x263/r8 is +1.58810e-03 worse (2.6204% relative) and clears the ambiguity
    cutoff by 6.79034e-04.
  first non-r8 branch x265/r7.5 is +2.07985e-03 worse (3.4318% relative).

base objective, source_mismatch_noise15p625_seed21:
  x263/r8 is +2.25130e-03 worse (2.3731% relative) and clears the ambiguity
    cutoff by 8.28265e-04.
  first non-r8 branch x264/r7.5 is +4.67350e-03 worse (4.9263% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.70587e-03 worse nominal and +2.18912e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.780,63.616,90.055), nonwhite fraction 0.288825
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 15.625% RMS Tx/Rx=50 replicate set. All seed21
rows are true, strong, and zero-ambiguity in x/z/r. Aggregate 365-367 next; if
the aggregate remains 6/6 true, strong, and zero-ambiguity, promote
15.625% RMS under 4-source 50 mm Tx/Rx.
```

## 368: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise15.625 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 15.625% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this higher
noise bracket.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/365_coordinate_optimizer_close14_seed34_sources4_txrx50_noise15p625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/366_coordinate_optimizer_close14_seed13_sources4_txrx50_noise15p625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/367_coordinate_optimizer_close14_seed21_sources4_txrx50_noise15p625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise15p625_seed_replicates
  --outdir outputs/experiments/368_coordinate_confidence_close14_sources4_txrx50_noise15p625_seed_replicates
```

Output:

```text
outputs/experiments/368_coordinate_confidence_close14_sources4_txrx50_noise15p625_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 2.07985e-03 / 3.40012e-03 / 4.71172e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(84.341,57.131,75.755), nonwhite fraction 0.195244
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(33.714,33.628,33.847), nonwhite fraction 0.049537
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 15.625% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 15.625% RMS as the current clean operating
point for the larger-offset acquisition. The next stress test is 16.25% RMS
under the same acquisition.
```

## 369: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise16.25 Probe

Purpose:

```text
test the old 45 mm ambiguous 16.25% RMS close14 bracket under the larger
4-source, 50 mm Tx/Rx acquisition after 15.625% RMS was replicated clean.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise16p25_seed34|source_mismatch_noise16p25_seed34
  --update-case-label source_mismatch_noise16p25_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/369_coordinate_optimizer_close14_seed34_sources4_txrx50_noise16p25_objectives
```

Result:

```text
elapsed: 1402.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise16p25_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise16p25_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise16p25_seed34:
  x263/r8 is +1.37419e-03 worse (2.1104% relative) and clears the ambiguity
    cutoff by 3.97482e-04.
  first non-r8 branch x265/r7.5 is +2.21541e-03 worse (3.4024% relative).

base objective, source_mismatch_noise16p25_seed34:
  x263/r8 is +2.48872e-03 worse (2.4846% relative) and clears the ambiguity
    cutoff by 9.86205e-04.
  first non-r8 branch x265/r7.5 is +4.50528e-03 worse (4.4977% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.57695e-03 worse nominal and +2.66023e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(103.107,64.323,91.197), nonwhite fraction 0.300881
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 16.25% RMS under the 4-source, 50 mm Tx/Rx acquisition,
although the nominal x263/r8 ambiguity-clearance margin is smaller than at
15.625% RMS. This is evidence that the larger offset also rescues the old
45 mm ambiguous 16.25% bracket, but it is only one seed. Replicate on seeds 13
and 21 before promoting 16.25% RMS.
```

## 370: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise16.25 Replicate

Purpose:

```text
replicate the 16.25% RMS seed34 clean result on seed13 before deciding whether
the larger-offset acquisition can be promoted at this bracket.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise16p25_seed13|source_mismatch_noise16p25_seed13
  --update-case-label source_mismatch_noise16p25_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/370_coordinate_optimizer_close14_seed13_sources4_txrx50_noise16p25_objectives
```

Result:

```text
elapsed: 1404.1 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise16p25_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise16p25_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise16p25_seed13:
  x263/r8 is +1.56721e-03 worse (2.3819% relative) and clears the ambiguity
    cutoff by 5.80244e-04.
  first non-r8 branch x265/r7.5 is +2.16047e-03 worse (3.2835% relative).

base objective, source_mismatch_noise16p25_seed13:
  x263/r8 is +2.60875e-03 worse (2.5933% relative) and clears the ambiguity
    cutoff by 1.09980e-03.
  first non-r8 branch x265/r7.5 is +4.68555e-03 worse (4.6578% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.79016e-03 worse nominal and +2.93741e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.452,63.968,90.632), nonwhite fraction 0.294774
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 16.25% RMS Tx/Rx=50 result. Both seed13 rows are
true, strong, and zero-ambiguity in x/z/r. Run seed21 next; if it also remains
clean, aggregate 369-371 before promoting the 16.25% RMS bracket.
```

## 371: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise16.25 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 16.25% RMS Tx/Rx=50 close14
bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise16p25_seed21|source_mismatch_noise16p25_seed21
  --update-case-label source_mismatch_noise16p25_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/371_coordinate_optimizer_close14_seed21_sources4_txrx50_noise16p25_objectives
```

Result:

```text
elapsed: 1410.2 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise16p25_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise16p25_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise16p25_seed21:
  x263/r8 is +1.58931e-03 worse (2.4580% relative) and clears the ambiguity
    cutoff by 6.19416e-04.
  first non-r8 branch x265/r7.5 is +2.06439e-03 worse (3.1927% relative).

base objective, source_mismatch_noise16p25_seed21:
  x263/r8 is +2.22844e-03 worse (2.2116% relative) and clears the ambiguity
    cutoff by 7.17037e-04.
  first non-r8 branch x264/r7.5 is +4.63823e-03 worse (4.6032% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.71204e-03 worse nominal and +2.17061e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.140,63.801,90.364), nonwhite fraction 0.291926
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 16.25% RMS Tx/Rx=50 replicate set. All seed21
rows are true, strong, and zero-ambiguity in x/z/r. Aggregate 369-371 next; if
the aggregate remains 6/6 true, strong, and zero-ambiguity, promote
16.25% RMS under 4-source 50 mm Tx/Rx.
```

## 372: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise16.25 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 16.25% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this higher
noise bracket.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/369_coordinate_optimizer_close14_seed34_sources4_txrx50_noise16p25_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/370_coordinate_optimizer_close14_seed13_sources4_txrx50_noise16p25_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/371_coordinate_optimizer_close14_seed21_sources4_txrx50_noise16p25_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise16p25_seed_replicates
  --outdir outputs/experiments/372_coordinate_confidence_close14_sources4_txrx50_noise16p25_seed_replicates
```

Output:

```text
outputs/experiments/372_coordinate_confidence_close14_sources4_txrx50_noise16p25_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 2.06439e-03 / 3.37822e-03 / 4.68555e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(84.874,57.342,76.194), nonwhite fraction 0.197485
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(33.546,33.460,33.680), nonwhite fraction 0.048903
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 16.25% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 16.25% RMS as the current clean operating
point for the larger-offset acquisition. The next stress test is 17.5% RMS
under the same acquisition.
```

## 373: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise17.5 Probe

Purpose:

```text
test the old 45 mm x-ambiguous 17.5% RMS close14 bracket under the larger
4-source, 50 mm Tx/Rx acquisition after 16.25% RMS was replicated clean.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise17p5_seed34|source_mismatch_noise17p5_seed34
  --update-case-label source_mismatch_noise17p5_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/373_coordinate_optimizer_close14_seed34_sources4_txrx50_noise17p5_objectives
```

Result:

```text
elapsed: 1410.6 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise17p5_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise17p5_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise17p5_seed34:
  x263/r8 is +1.36135e-03 worse (1.8497% relative) and clears the ambiguity
    cutoff by 2.57343e-04.
  first non-r8 branch x265/r7.5 is +2.19405e-03 worse (2.9810% relative).

base objective, source_mismatch_noise17p5_seed34:
  x263/r8 is +2.45843e-03 worse (2.1879% relative) and clears the ambiguity
    cutoff by 7.72955e-04.
  first non-r8 branch x265/r7.5 is +4.43901e-03 worse (3.9505% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.57892e-03 worse nominal and +2.66089e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(103.441,64.489,91.482), nonwhite fraction 0.303935
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 17.5% RMS under the 4-source, 50 mm Tx/Rx acquisition,
turning the old 45 mm x-ambiguous bracket into a single-candidate interval.
The nominal x263/r8 clearance margin is only 2.57e-04, so this is a tight
clean result. Replicate on seeds 13 and 21 before promoting 17.5% RMS.
```

## 374: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise17.5 Replicate

Purpose:

```text
replicate the tight 17.5% RMS seed34 clean result on seed13 before deciding
whether the larger-offset acquisition can be promoted at this bracket.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise17p5_seed13|source_mismatch_noise17p5_seed13
  --update-case-label source_mismatch_noise17p5_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/374_coordinate_optimizer_close14_seed13_sources4_txrx50_noise17p5_objectives
```

Result:

```text
elapsed: 1403.4 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise17p5_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise17p5_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise17p5_seed13:
  x263/r8 is +1.56725e-03 worse (2.1074% relative) and clears the ambiguity
    cutoff by 4.51731e-04.
  first non-r8 branch x265/r7.5 is +2.13534e-03 worse (2.8713% relative).

base objective, source_mismatch_noise17p5_seed13:
  x263/r8 is +2.58603e-03 worse (2.2932% relative) and clears the ambiguity
    cutoff by 8.94461e-04.
  first non-r8 branch x265/r7.5 is +4.63075e-03 worse (4.1063% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.80849e-03 worse nominal and +2.95923e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.799,64.141,90.928), nonwhite fraction 0.297821
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 17.5% RMS Tx/Rx=50 result. Both seed13 rows are
true, strong, and zero-ambiguity in x/z/r. Run seed21 next; if it also remains
clean, aggregate 373-375 before promoting the 17.5% RMS bracket.
```

## 375: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise17.5 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 17.5% RMS Tx/Rx=50 close14
bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise17p5_seed21|source_mismatch_noise17p5_seed21
  --update-case-label source_mismatch_noise17p5_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/375_coordinate_optimizer_close14_seed21_sources4_txrx50_noise17p5_objectives
```

Result:

```text
elapsed: 1401.7 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise17p5_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise17p5_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise17p5_seed21:
  x263/r8 is +1.59089e-03 worse (2.1753% relative) and clears the ambiguity
    cutoff by 4.93889e-04.
  first non-r8 branch x265/r7.5 is +2.03284e-03 worse (2.7796% relative).

base objective, source_mismatch_noise17p5_seed21:
  x263/r8 is +2.18194e-03 worse (1.9311% relative) and clears the ambiguity
    cutoff by 4.87133e-04.
  first non-r8 branch x264/r7.5 is +4.56560e-03 worse (4.0408% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.72435e-03 worse nominal and +2.13358e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.536,64.000,90.702), nonwhite fraction 0.295381
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 17.5% RMS Tx/Rx=50 replicate set. All seed21 rows
are true, strong, and zero-ambiguity in x/z/r. Aggregate 373-375 next; if the
aggregate remains 6/6 true, strong, and zero-ambiguity, promote 17.5% RMS
under 4-source 50 mm Tx/Rx.
```

## 376: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise17.5 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 17.5% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this old
45 mm x-ambiguous bracket.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/373_coordinate_optimizer_close14_seed34_sources4_txrx50_noise17p5_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/374_coordinate_optimizer_close14_seed13_sources4_txrx50_noise17p5_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/375_coordinate_optimizer_close14_seed21_sources4_txrx50_noise17p5_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise17p5_seed_replicates
  --outdir outputs/experiments/376_coordinate_confidence_close14_sources4_txrx50_noise17p5_seed_replicates
```

Output:

```text
outputs/experiments/376_coordinate_confidence_close14_sources4_txrx50_noise17p5_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 2.03284e-03 / 3.33293e-03 / 4.63075e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1719x971 px, dynamic range 255,
  std=(85.488,57.581,76.699), nonwhite fraction 0.199960
coordinate_ambiguity_widths.png: 1719x971 px, dynamic range 255,
  std=(33.325,33.238,33.460), nonwhite fraction 0.048089
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 17.5% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 17.5% RMS as the current clean operating
point for the larger-offset acquisition. The next stress test is 20% RMS
under the same acquisition.
```

## 377: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise20 Probe

Purpose:

```text
test the old 45 mm point-correct but x-ambiguous 20% RMS close14 bracket under
the larger 4-source, 50 mm Tx/Rx acquisition after 17.5% RMS was replicated
clean.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise20_seed34|source_mismatch_noise20_seed34
  --update-case-label source_mismatch_noise20_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/377_coordinate_optimizer_close14_seed34_sources4_txrx50_noise20_objectives
```

Result:

```text
elapsed: 1411.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise20_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise20_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise20_seed34:
  x263/r8 is +1.33372e-03 worse (1.4511% relative), but remains inside the
    ambiguity cutoff by 4.49246e-05.
  first non-r8 branch x265/r7.5 is +2.14823e-03 worse (2.3373% relative).

base objective, source_mismatch_noise20_seed34:
  x263/r8 is +2.39318e-03 worse (1.7300% relative) and clears the ambiguity
    cutoff by 3.18133e-04.
  first non-r8 branch x265/r7.5 is +4.29904e-03 worse (3.1077% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.58283e-03 worse nominal and +2.66213e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(104.297,64.935,92.216), nonwhite fraction 0.312208
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
The 20% RMS close14 bracket under 4-source, 50 mm Tx/Rx is point-correct but
not clean. Both rows select the true x264/z90/r8 geometry and have strong
radius margins, but the nominal row keeps a 263-264 mm x interval because
x263/r8 remains just inside the ambiguity cutoff. Do not replicate 20% RMS as
a clean candidate. The clean-to-ambiguous transition is now bracketed between
replicated-clean 17.5% RMS and seed34 x-ambiguous 20% RMS. Run 18.75% RMS
seed34 next.
```

## 378: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise18.75 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 17.5% RMS and seed34 x-ambiguous
20% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise18p75_seed34|source_mismatch_noise18p75_seed34
  --update-case-label source_mismatch_noise18p75_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/378_coordinate_optimizer_close14_seed34_sources4_txrx50_noise18p75_objectives
```

Result:

```text
elapsed: 1411.4 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise18p75_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise18p75_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise18p75_seed34:
  x263/r8 is +1.34784e-03 worse (1.6329% relative) and clears the ambiguity
    cutoff by 1.09705e-04.
  first non-r8 branch x265/r7.5 is +2.17163e-03 worse (2.6309% relative).

base objective, source_mismatch_noise18p75_seed34:
  x263/r8 is +2.42653e-03 worse (1.9395% relative) and clears the ambiguity
    cutoff by 5.49909e-04.
  first non-r8 branch x265/r7.5 is +4.37016e-03 worse (3.4931% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.58088e-03 worse nominal and +2.66152e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(103.192,64.367,91.270), nonwhite fraction 0.301657
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 18.75% RMS under the 4-source, 50 mm Tx/Rx acquisition, but
the nominal x263/r8 ambiguity-clearance margin is very small: 1.10e-04. This
keeps 18.75% RMS in the clean-candidate branch, but it is too tight to promote
from one seed. Replicate on seeds 13 and 21 before promoting 18.75% RMS.
```

## 379: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise18.75 Replicate

Purpose:

```text
replicate the tight 18.75% RMS seed34 clean result on seed13 before deciding
whether the larger-offset acquisition can be promoted at this bracket.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise18p75_seed13|source_mismatch_noise18p75_seed13
  --update-case-label source_mismatch_noise18p75_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/379_coordinate_optimizer_close14_seed13_sources4_txrx50_noise18p75_objectives
```

Result:

```text
elapsed: 1418.6 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise18p75_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise18p75_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise18p75_seed13:
  x263/r8 is +1.56625e-03 worse (1.8781% relative) and clears the ambiguity
    cutoff by 3.15291e-04.
  first non-r8 branch x265/r7.5 is +2.10925e-03 worse (2.5292% relative).

base objective, source_mismatch_noise18p75_seed13:
  x263/r8 is +2.56141e-03 worse (2.0413% relative) and clears the ambiguity
    cutoff by 6.79216e-04.
  first non-r8 branch x265/r7.5 is +4.57292e-03 worse (3.6444% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.82679e-03 worse nominal and +2.98101e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.497,63.991,90.670), nonwhite fraction 0.295144
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 18.75% RMS Tx/Rx=50 result. Both seed13 rows are
true, strong, and zero-ambiguity in x/z/r. Run seed21 next; if it also remains
clean, aggregate 378-380 before promoting the 18.75% RMS bracket.
```

## 380: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise18.75 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 18.75% RMS Tx/Rx=50 close14
bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise18p75_seed21|source_mismatch_noise18p75_seed21
  --update-case-label source_mismatch_noise18p75_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/380_coordinate_optimizer_close14_seed21_sources4_txrx50_noise18p75_objectives
```

Result:

```text
elapsed: 1410.2 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise18p75_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise18p75_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise18p75_seed21:
  x263/r8 is +1.59138e-03 worse (1.9391% relative) and clears the ambiguity
    cutoff by 3.60376e-04.
  first non-r8 branch x265/r7.5 is +2.00052e-03 worse (2.4377% relative).

base objective, source_mismatch_noise18p75_seed21:
  x263/r8 is +2.13456e-03 worse (1.6974% relative) and clears the ambiguity
    cutoff by 2.48204e-04.
  first non-r8 branch x264/r7.5 is +4.49045e-03 worse (3.5707% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  x263/r8 is +1.73664e-03 worse nominal and +2.09652e-03 worse under
    source mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.164,63.786,90.377), nonwhite fraction 0.291890
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 18.75% RMS Tx/Rx=50 replicate set. All seed21 rows
are true, strong, and zero-ambiguity in x/z/r. Aggregate 378-380 next; if the
aggregate remains 6/6 true, strong, and zero-ambiguity, promote 18.75% RMS
under 4-source 50 mm Tx/Rx.
```

## 381: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise18.75 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 18.75% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this midpoint
between replicated-clean 17.5% and seed34-ambiguous 20%.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/378_coordinate_optimizer_close14_seed34_sources4_txrx50_noise18p75_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/379_coordinate_optimizer_close14_seed13_sources4_txrx50_noise18p75_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/380_coordinate_optimizer_close14_seed21_sources4_txrx50_noise18p75_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise18p75_seed_replicates
  --outdir outputs/experiments/381_coordinate_confidence_close14_sources4_txrx50_noise18p75_seed_replicates
```

Output:

```text
outputs/experiments/381_coordinate_confidence_close14_sources4_txrx50_noise18p75_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 2.00052e-03 / 3.28582e-03 / 4.57292e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(84.800,57.291,76.127), nonwhite fraction 0.196944
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(33.525,33.438,33.658), nonwhite fraction 0.048877
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 18.75% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 18.75% RMS as the current clean operating
point for the larger-offset acquisition. The clean-to-ambiguous transition is
now bracketed between replicated-clean 18.75% RMS and seed34 x-ambiguous
20% RMS. The next midpoint is 19.375% RMS seed34.
```

## 382: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.375 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 18.75% RMS and seed34 x-ambiguous
20% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p375_seed34|source_mismatch_noise19p375_seed34
  --update-case-label source_mismatch_noise19p375_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/382_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p375_objectives
```

Result:

```text
elapsed: 1399.6 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p375_seed34:
  x263/r8 is +1.34086e-03 worse (1.5381% relative) and clears the ambiguity
    cutoff by 3.32320e-05.
  first non-r8 branch x265/r7.5 is +2.16005e-03 worse (2.4778% relative).

base objective, source_mismatch_noise19p375_seed34:
  x263/r8 is +2.41003e-03 worse (1.8304% relative) and clears the ambiguity
    cutoff by 4.35046e-04.
  first non-r8 branch x265/r7.5 is +4.33487e-03 worse (3.2923% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.27972e-03 nominal and +5.66871e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.849,64.189,90.977), nonwhite fraction 0.298548
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 remains clean at 19.375% RMS under the 4-source, 50 mm Tx/Rx
acquisition, but this is the tightest clean seed34 midpoint so far. The
nominal x263/r8 competitor clears the ambiguity cutoff by only 3.32e-05,
smaller than the 18.75% seed34 clearance of 1.10e-04 and close to the
20% seed34 failure where x263/r8 stayed inside the cutoff by 4.49e-05.
Do not promote 19.375% RMS from one seed. Replicate seeds 13 and 21 before
deciding whether 19.375% RMS becomes the next clean bracket or the transition
narrows around this point.
```

## 383: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise19.375 Replicate

Purpose:

```text
replicate the very tight 19.375% RMS seed34 clean result on seed13 before
deciding whether the bracket can be promoted.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p375_seed13|source_mismatch_noise19p375_seed13
  --update-case-label source_mismatch_noise19p375_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/383_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p375_objectives
```

Result:

```text
elapsed: 1407.1 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p375_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p375_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p375_seed13:
  x263/r8 is +1.56536e-03 worse (1.7773% relative) and clears the ambiguity
    cutoff by 2.44255e-04.
  first non-r8 branch x265/r7.5 is +2.09587e-03 worse (2.3797% relative).

base objective, source_mismatch_noise19p375_seed13:
  x263/r8 is +2.54843e-03 worse (1.9304% relative) and clears the ambiguity
    cutoff by 5.68210e-04.
  first non-r8 branch x265/r7.5 is +4.54297e-03 worse (3.4413% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +2.86888e-03 nominal and +6.13471e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.096,63.781,90.327), nonwhite fraction 0.291623
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 19.375% RMS Tx/Rx=50 result. Both rows are true,
strong, and zero-ambiguity in x/z/r. Seed13 has more nominal cutoff clearance
than seed34, but the promoted claim still needs seed21 because seed34 was very
tight. Run seed21 next; if it remains clean, aggregate 382-384 before
promoting 19.375% RMS.
```

## 384: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise19.375 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 19.375% RMS Tx/Rx=50 close14
bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p375_seed21|source_mismatch_noise19p375_seed21
  --update-case-label source_mismatch_noise19p375_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/384_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p375_objectives
```

Result:

```text
elapsed: 1391.7 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p375_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p375_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p375_seed21:
  x263/r8 is +1.59123e-03 worse (1.8354% relative) and clears the ambiguity
    cutoff by 2.90779e-04.
  first non-r8 branch x265/r7.5 is +1.98410e-03 worse (2.2886% relative).

base objective, source_mismatch_noise19p375_seed21:
  x263/r8 is +2.11059e-03 worse (1.5950% relative) and clears the ambiguity
    cutoff by 1.25693e-04.
  first non-r8 branch x264/r7.5 is +4.45202e-03 worse (3.3644% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.12585e-03 nominal and +5.52140e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.813,63.622,90.080), nonwhite fraction 0.289186
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 19.375% RMS Tx/Rx=50 replicate set. Both rows are
true, strong, and zero-ambiguity in x/z/r. The tighter source-mismatch
x263/r8 clearance is 1.26e-04, still outside the ambiguity cutoff. Aggregate
382-384 next; if all six rows remain true, strong, and zero-ambiguity, promote
19.375% RMS under 4-source 50 mm Tx/Rx.
```

## 385: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise19.375 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 19.375% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this midpoint
between replicated-clean 18.75% and seed34-ambiguous 20%.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/382_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/383_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/384_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise19p375_seed_replicates
  --outdir outputs/experiments/385_coordinate_confidence_close14_sources4_txrx50_noise19p375_seed_replicates
```

Output:

```text
outputs/experiments/385_coordinate_confidence_close14_sources4_txrx50_noise19p375_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 1.98410e-03 / 3.26165e-03 / 4.54297e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(84.201,57.040,75.631), nonwhite fraction 0.194402
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(33.655,33.569,33.788), nonwhite fraction 0.049364
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 19.375% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 19.375% RMS as the current clean operating
point for the larger-offset acquisition. The clean-to-ambiguous transition is
now bracketed between replicated-clean 19.375% RMS and seed34 x-ambiguous
20% RMS. The next midpoint is 19.6875% RMS seed34.
```

## 386: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.6875 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.375% RMS and seed34
x-ambiguous 20% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p6875_seed34|source_mismatch_noise19p6875_seed34
  --update-case-label source_mismatch_noise19p6875_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/386_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p6875_objectives
```

Result:

```text
elapsed: 1403.4 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p6875_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p6875_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p6875_seed34:
  x263/r8 is +1.33731e-03 worse (1.4937% relative) but remains inside the
    ambiguity cutoff by 5.63989e-06.
  first non-r8 branch x265/r7.5 is +2.15417e-03 worse (2.4061% relative).

base objective, source_mismatch_noise19p6875_seed34:
  x263/r8 is +2.40165e-03 worse (1.7792% relative) and clears the ambiguity
    cutoff by 3.76838e-04.
  first non-r8 branch x265/r7.5 is +4.31702e-03 worse (3.1981% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28395e-03 nominal and +5.66620e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.506,64.021,90.684), nonwhite fraction 0.295479
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
The 19.6875% RMS close14 bracket under 4-source, 50 mm Tx/Rx is point-correct
but not clean. Both rows select the true x264/z90/r8 point and both radius
margins are strong, but the nominal row retains a 263-264 mm x interval
because x263/r8 remains just inside the ambiguity cutoff. Do not replicate
19.6875% RMS as a clean candidate. The clean-to-ambiguous transition is now
bracketed between replicated-clean 19.375% RMS and seed34 x-ambiguous
19.6875% RMS. The next midpoint is 19.53125% RMS seed34.
```

## 387: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.53125 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.375% RMS and seed34
x-ambiguous 19.6875% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p53125_seed34|source_mismatch_noise19p53125_seed34
  --update-case-label source_mismatch_noise19p53125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/387_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p53125_objectives
```

Result:

```text
elapsed: 1404.5 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p53125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p53125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p53125_seed34:
  x263/r8 is +1.33909e-03 worse (1.5157% relative) and clears the ambiguity
    cutoff by 1.38481e-05.
  first non-r8 branch x265/r7.5 is +2.15712e-03 worse (2.4416% relative).

base objective, source_mismatch_noise19p53125_seed34:
  x263/r8 is +2.40585e-03 worse (1.8045% relative) and clears the ambiguity
    cutoff by 4.06005e-04.
  first non-r8 branch x265/r7.5 is +4.32596e-03 worse (3.2447% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28184e-03 nominal and +5.66745e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(102.194,63.855,90.416), nonwhite fraction 0.292743
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 19.53125% RMS under the 4-source, 50 mm Tx/Rx acquisition,
but it is extremely close to the ambiguity boundary. The nominal x263/r8
competitor clears the ambiguity cutoff by only 1.38e-05, narrower than the
19.375% seed34 clean clearance of 3.32e-05 and only slightly above the
19.6875% seed34 ambiguous failure, where x263/r8 stayed inside by 5.64e-06.
Do not promote 19.53125% RMS from one seed. Replicate seeds 13 and 21 before
deciding whether 19.53125% RMS can become the next clean bracket.
```

## 388: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise19.53125 Replicate

Purpose:

```text
replicate the extremely tight 19.53125% RMS seed34 clean result on seed13
before deciding whether the bracket can be promoted.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p53125_seed13|source_mismatch_noise19p53125_seed13
  --update-case-label source_mismatch_noise19p53125_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/388_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p53125_objectives
```

Result:

```text
elapsed: 1413.6 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p53125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p53125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p53125_seed13:
  x263/r8 is +1.56510e-03 worse (1.7534% relative) and clears the ambiguity
    cutoff by 2.26213e-04.
  first non-r8 branch x265/r7.5 is +2.09250e-03 worse (2.3443% relative).

base objective, source_mismatch_noise19p53125_seed13:
  x263/r8 is +2.54512e-03 worse (1.9041% relative) and clears the ambiguity
    cutoff by 5.40129e-04.
  first non-r8 branch x265/r7.5 is +4.53538e-03 worse (3.3931% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +2.86768e-03 nominal and +6.13647e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.462,63.459,89.784), nonwhite fraction 0.286227
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 19.53125% RMS Tx/Rx=50 result. Both seed13 rows
are true, strong, and zero-ambiguity in x/z/r. Run seed21 next; if it also
remains clean, aggregate 387-389 before promoting 19.53125% RMS.
```

## 389: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise19.53125 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 19.53125% RMS Tx/Rx=50
close14 bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p53125_seed21|source_mismatch_noise19p53125_seed21
  --update-case-label source_mismatch_noise19p53125_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/389_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p53125_objectives
```

Result:

```text
elapsed: 1409.3 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p53125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p53125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p53125_seed21:
  x263/r8 is +1.59115e-03 worse (1.8108% relative) and clears the ambiguity
    cutoff by 2.73094e-04.
  first non-r8 branch x265/r7.5 is +1.97997e-03 worse (2.2533% relative).

base objective, source_mismatch_noise19p53125_seed21:
  x263/r8 is +2.10458e-03 worse (1.5707% relative) and clears the ambiguity
    cutoff by 9.47706e-05.
  first non-r8 branch x264/r7.5 is +4.44234e-03 worse (3.3155% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.12395e-03 nominal and +5.51894e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.168,63.291,89.527), nonwhite fraction 0.284191
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 19.53125% RMS Tx/Rx=50 replicate set. Both seed21
rows are true, strong, and zero-ambiguity in x/z/r. The tighter
source-mismatch x263/r8 clearance is 9.48e-05, still outside the ambiguity
cutoff. Aggregate 387-389 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.53125% RMS under 4-source 50 mm Tx/Rx.
```

## 390: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise19.53125 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 19.53125% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this midpoint
between replicated-clean 19.375% and seed34-ambiguous 19.6875%.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/387_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p53125_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/388_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p53125_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/389_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p53125_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise19p53125_seed_replicates
  --outdir outputs/experiments/390_coordinate_confidence_close14_sources4_txrx50_noise19p53125_seed_replicates
```

Output:

```text
outputs/experiments/390_coordinate_confidence_close14_sources4_txrx50_noise19p53125_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 1.97997e-03 / 3.25554e-03 / 4.53538e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(82.844,56.472,74.506), nonwhite fraction 0.188811
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(33.976,33.891,34.108), nonwhite fraction 0.050605
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 19.53125% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 19.53125% RMS as the current clean operating
point for the larger-offset acquisition. The clean-to-ambiguous transition is
now bracketed between replicated-clean 19.53125% RMS and seed34 x-ambiguous
19.6875% RMS. The next midpoint is 19.609375% RMS seed34.
```

## 391: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.609375 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.53125% RMS and seed34
x-ambiguous 19.6875% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p609375_seed34|source_mismatch_noise19p609375_seed34
  --update-case-label source_mismatch_noise19p609375_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/391_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p609375_objectives
```

Result:

```text
elapsed: 1406.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p609375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p609375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p609375_seed34:
  x263/r8 is +1.33820e-03 worse (1.5046% relative) and clears the ambiguity
    cutoff by 4.11709e-06.
  first non-r8 branch x265/r7.5 is +2.15564e-03 worse (2.4237% relative).

base objective, source_mismatch_noise19p609375_seed34:
  x263/r8 is +2.40375e-03 worse (1.7918% relative) and clears the ambiguity
    cutoff by 3.91437e-04.
  first non-r8 branch x265/r7.5 is +4.32149e-03 worse (3.2213% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28290e-03 nominal and +5.66683e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.793,63.656,90.074), nonwhite fraction 0.289273
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 19.609375% RMS under the 4-source, 50 mm Tx/Rx
acquisition, but the result is almost on the ambiguity boundary. The nominal
x263/r8 competitor clears the ambiguity cutoff by only 4.12e-06, smaller than
the 19.53125% seed34 clearance of 1.38e-05 and just across the boundary from
the 19.6875% seed34 ambiguous failure, where x263/r8 stayed inside by
5.64e-06. Do not promote 19.609375% RMS from one seed. Replicate seeds 13 and
21 before deciding whether 19.609375% RMS can become the next clean bracket.
```

## 392: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise19.609375 Replicate

Purpose:

```text
replicate the boundary-tight 19.609375% RMS seed34 clean result on seed13
before deciding whether the bracket can be promoted.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p609375_seed13|source_mismatch_noise19p609375_seed13
  --update-case-label source_mismatch_noise19p609375_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/392_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p609375_objectives
```

Result:

```text
elapsed: 1410.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p609375_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p609375_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p609375_seed13:
  x263/r8 is +1.56496e-03 worse (1.7417% relative) and clears the ambiguity
    cutoff by 2.17151e-04.
  first non-r8 branch x265/r7.5 is +2.09080e-03 worse (2.3269% relative).

base objective, source_mismatch_noise19p609375_seed13:
  x263/r8 is +2.54345e-03 worse (1.8911% relative) and clears the ambiguity
    cutoff by 5.26040e-04.
  first non-r8 branch x265/r7.5 is +4.53157e-03 worse (3.3693% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +2.86708e-03 nominal and +6.13735e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.046,63.251,89.430), nonwhite fraction 0.282757
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 19.609375% RMS Tx/Rx=50 result. Both seed13 rows
are true, strong, and zero-ambiguity in x/z/r. Run seed21 next; if it also
remains clean, aggregate 391-393 before promoting 19.609375% RMS.
```

## 393: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise19.609375 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 19.609375% RMS Tx/Rx=50
close14 bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p609375_seed21|source_mismatch_noise19p609375_seed21
  --update-case-label source_mismatch_noise19p609375_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/393_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p609375_objectives
```

Result:

```text
elapsed: 1400.6 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p609375_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p609375_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p609375_seed21:
  x263/r8 is +1.59110e-03 worse (1.7987% relative) and clears the ambiguity
    cutoff by 2.64209e-04.
  first non-r8 branch x265/r7.5 is +1.97790e-03 worse (2.2359% relative).

base objective, source_mismatch_noise19p609375_seed21:
  x263/r8 is +2.10157e-03 worse (1.5588% relative) and clears the ambiguity
    cutoff by 7.92667e-05.
  first non-r8 branch x264/r7.5 is +4.43748e-03 worse (3.2914% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.12300e-03 nominal and +5.51771e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(100.746,63.081,89.167), nonwhite fraction 0.280724
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 19.609375% RMS Tx/Rx=50 replicate set. Both seed21
rows are true, strong, and zero-ambiguity in x/z/r. The tighter
source-mismatch x263/r8 clearance is 7.93e-05, still outside the ambiguity
cutoff. Aggregate 391-393 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.609375% RMS under 4-source 50 mm Tx/Rx.
```

## 394: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise19.609375 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 19.609375% RMS Tx/Rx=50 close14 replicate set and
decide whether the larger-offset acquisition can be promoted at this midpoint
between replicated-clean 19.53125% and seed34-ambiguous 19.6875%.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/391_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p609375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/392_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p609375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/393_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p609375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise19p609375_seed_replicates
  --outdir outputs/experiments/394_coordinate_confidence_close14_sources4_txrx50_noise19p609375_seed_replicates
```

Output:

```text
outputs/experiments/394_coordinate_confidence_close14_sources4_txrx50_noise19p609375_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 1.97790e-03 / 3.25248e-03 / 4.53157e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(82.369,56.323,74.126), nonwhite fraction 0.186887
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(34.230,34.146,34.360), nonwhite fraction 0.051360
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 19.609375% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 19.609375% RMS as the current clean operating
point for the larger-offset acquisition. The clean-to-ambiguous transition is
now bracketed between replicated-clean 19.609375% RMS and seed34 x-ambiguous
19.6875% RMS. The next midpoint is 19.6484375% RMS seed34.
```

## 395: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.6484375 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.609375% RMS and seed34
x-ambiguous 19.6875% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p6484375_seed34|source_mismatch_noise19p6484375_seed34
  --update-case-label source_mismatch_noise19p6484375_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/395_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p6484375_objectives
```

Result:

```text
elapsed: 1394.1 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p6484375_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p6484375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p6484375_seed34:
  x263/r8 is +1.33775e-03 worse (1.4992% relative) but remains inside the
    ambiguity cutoff by 7.58164e-07.
  first non-r8 branch x265/r7.5 is +2.15491e-03 worse (2.4149% relative).

base objective, source_mismatch_noise19p6484375_seed34:
  x263/r8 is +2.40270e-03 worse (1.7855% relative) and clears the ambiguity
    cutoff by 3.84141e-04.
  first non-r8 branch x265/r7.5 is +4.31925e-03 worse (3.2097% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28342e-03 nominal and +5.66651e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.474,63.494,89.801), nonwhite fraction 0.286561
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
The 19.6484375% RMS close14 bracket under 4-source, 50 mm Tx/Rx is
point-correct but not clean. Both rows select the true x264/z90/r8 point and
both radius margins are strong, but the nominal row retains a 263-264 mm x
interval because x263/r8 remains just inside the ambiguity cutoff. Do not
replicate 19.6484375% RMS as a clean candidate. The clean-to-ambiguous
transition is now bracketed between replicated-clean 19.609375% RMS and seed34
x-ambiguous 19.6484375% RMS. The next midpoint is 19.62890625% RMS seed34.
```

## 396: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.62890625 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.609375% RMS and seed34
x-ambiguous 19.6484375% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p62890625_seed34|source_mismatch_noise19p62890625_seed34
  --update-case-label source_mismatch_noise19p62890625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/396_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p62890625_objectives
```

Result:

```text
elapsed: 1428.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p62890625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p62890625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p62890625_seed34:
  x263/r8 is +1.33798e-03 worse (1.5019% relative) and clears the ambiguity
    cutoff by 1.68027e-06.
  first non-r8 branch x265/r7.5 is +2.15528e-03 worse (2.4193% relative).

base objective, source_mismatch_noise19p62890625_seed34:
  x263/r8 is +2.40323e-03 worse (1.7886% relative) and clears the ambiguity
    cutoff by 3.87790e-04.
  first non-r8 branch x265/r7.5 is +4.32037e-03 worse (3.2155% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28316e-03 nominal and +5.66667e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(101.059,63.289,89.448), nonwhite fraction 0.283118
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 19.62890625% RMS under the 4-source, 50 mm Tx/Rx
acquisition, but this is the tightest clean seed34 result observed in the
transition bracket. The nominal x263/r8 competitor clears the ambiguity cutoff
by only 1.68e-06, just across the boundary from 19.6484375%, where x263/r8
stayed inside by 7.58e-07. Do not promote 19.62890625% RMS from one seed.
Replicate seeds 13 and 21 before deciding whether it can become the next clean
bracket.
```

## 397: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise19.62890625 Replicate

Purpose:

```text
replicate the boundary-tight 19.62890625% RMS seed34 clean result on seed13
before deciding whether the bracket can be promoted.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p62890625_seed13|source_mismatch_noise19p62890625_seed13
  --update-case-label source_mismatch_noise19p62890625_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/397_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p62890625_objectives
```

Result:

```text
elapsed: 1410.1 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p62890625_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p62890625_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p62890625_seed13:
  x263/r8 is +1.56493e-03 worse (1.7387% relative) and clears the ambiguity
    cutoff by 2.14881e-04.
  first non-r8 branch x265/r7.5 is +2.09038e-03 worse (2.3226% relative).

base objective, source_mismatch_noise19p62890625_seed13:
  x263/r8 is +2.54303e-03 worse (1.8879% relative) and clears the ambiguity
    cutoff by 5.22513e-04.
  first non-r8 branch x265/r7.5 is +4.53061e-03 worse (3.3635% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +2.86694e-03 nominal and +6.13757e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(100.287,62.872,88.782), nonwhite fraction 0.276603
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 replicates the clean 19.62890625% RMS Tx/Rx=50 result. Both seed13
rows are true, strong, and zero-ambiguity in x/z/r. Run seed21 next; if it
also remains clean, aggregate 396-398 before promoting 19.62890625% RMS.
```

## 398: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise19.62890625 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set for the 19.62890625% RMS Tx/Rx=50
close14 bracket before aggregate promotion.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p62890625_seed21|source_mismatch_noise19p62890625_seed21
  --update-case-label source_mismatch_noise19p62890625_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/398_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p62890625_objectives
```

Result:

```text
elapsed: 1408.7 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p62890625_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p62890625_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p62890625_seed21:
  x263/r8 is +1.59109e-03 worse (1.7957% relative) and clears the ambiguity
    cutoff by 2.61984e-04.
  first non-r8 branch x265/r7.5 is +1.97739e-03 worse (2.2316% relative).

base objective, source_mismatch_noise19p62890625_seed21:
  x263/r8 is +2.10081e-03 worse (1.5558% relative) and clears the ambiguity
    cutoff by 7.53863e-05.
  first non-r8 branch x264/r7.5 is +4.43627e-03 worse (3.2854% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.12276e-03 nominal and +5.51740e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.975,62.696,88.510), nonwhite fraction 0.274569
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the clean 19.62890625% RMS Tx/Rx=50 replicate set. Both
seed21 rows are true, strong, and zero-ambiguity in x/z/r. The tighter
source-mismatch x263/r8 clearance is 7.54e-05, still outside the ambiguity
cutoff. Aggregate 396-398 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.62890625% RMS under 4-source 50 mm Tx/Rx.
```

## 399: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise19.62890625 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 19.62890625% RMS Tx/Rx=50 close14 replicate set
and decide whether the larger-offset acquisition can be promoted at this
midpoint between replicated-clean 19.609375% and seed34-ambiguous
19.6484375%.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/396_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p62890625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/397_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p62890625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/398_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p62890625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise19p62890625_seed_replicates
  --outdir outputs/experiments/399_coordinate_confidence_close14_sources4_txrx50_noise19p62890625_seed_replicates
```

Output:

```text
outputs/experiments/399_coordinate_confidence_close14_sources4_txrx50_noise19p62890625_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 1.97739e-03 / 3.25172e-03 / 4.53061e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(81.025,55.816,73.028), nonwhite fraction 0.181641
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(34.671,34.588,34.800), nonwhite fraction 0.052833
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 19.62890625% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 19.62890625% RMS as the current clean
operating point for the larger-offset acquisition. The clean-to-ambiguous
transition is now bracketed between replicated-clean 19.62890625% RMS and
seed34 x-ambiguous 19.6484375% RMS. The next midpoint is 19.638671875% RMS
seed34.
```

## 400: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.638671875 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.62890625% RMS and seed34
x-ambiguous 19.6484375% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p638671875_seed34|source_mismatch_noise19p638671875_seed34
  --update-case-label source_mismatch_noise19p638671875_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/400_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p638671875_objectives
```

Result:

```text
elapsed: 1407.6 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p638671875_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p638671875_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p638671875_seed34:
  x263/r8 is +1.33786e-03 worse (1.5005% relative) and clears the ambiguity
    cutoff by 4.61257e-07.
  first non-r8 branch x265/r7.5 is +2.15509e-03 worse (2.4171% relative).

base objective, source_mismatch_noise19p638671875_seed34:
  x263/r8 is +2.40296e-03 worse (1.7870% relative) and clears the ambiguity
    cutoff by 3.85966e-04.
  first non-r8 branch x265/r7.5 is +4.31981e-03 worse (3.2126% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28329e-03 nominal and +5.66659e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(100.677,63.084,89.119), nonwhite fraction 0.279926
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 19.638671875% RMS under the 4-source, 50 mm Tx/Rx
acquisition, but it is effectively on the ambiguity boundary. The nominal
x263/r8 competitor clears the ambiguity cutoff by only 4.61e-07, smaller than
the 19.62890625% seed34 clearance of 1.68e-06 and just across the boundary
from the 19.6484375% seed34 ambiguous result. Do not promote 19.638671875%
RMS from one seed. Replicate seeds 13 and 21 before deciding whether it can
become the next clean bracket.
```

## 401: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise19.638671875 Replicate

Purpose:

```text
replicate the boundary-clean 19.638671875% RMS seed34 midpoint on seed13
under the 4-source, 50 mm Tx/Rx acquisition before deciding whether this
near-limit noise level can be promoted.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p638671875_seed13|source_mismatch_noise19p638671875_seed13
  --update-case-label source_mismatch_noise19p638671875_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/401_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p638671875_objectives
```

Result:

```text
elapsed: 1401.6 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p638671875_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p638671875_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p638671875_seed13:
  x263/r8 is +1.56491e-03 worse (1.7373% relative) and clears the ambiguity
    cutoff by 2.13745e-04.
  first non-r8 branch x265/r7.5 is +2.09017e-03 worse (2.3204% relative).

base objective, source_mismatch_noise19p638671875_seed13:
  x263/r8 is +2.54282e-03 worse (1.8863% relative) and clears the ambiguity
    cutoff by 5.20748e-04.
  first non-r8 branch x265/r7.5 is +4.53014e-03 worse (3.3605% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +2.86686e-03 nominal and +6.13768e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.889,62.658,88.439), nonwhite fraction 0.273410
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 also stays clean at 19.638671875% RMS under the 4-source, 50 mm
Tx/Rx acquisition. Unlike the seed34 row, seed13 is not right on the cutoff:
the nominal x263/r8 competitor clears the ambiguity threshold by 2.14e-04,
and the source-mismatch row clears it by 5.21e-04. This supports continuing
the replication instead of lowering the midpoint. Run seed21 next; if it also
remains true, strong, and zero-width in x/z/r, aggregate 400-402 before
promoting 19.638671875% RMS.
```

## 402: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise19.638671875 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set at 19.638671875% RMS under the
4-source, 50 mm Tx/Rx acquisition before aggregating the near-boundary clean
candidate.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p638671875_seed21|source_mismatch_noise19p638671875_seed21
  --update-case-label source_mismatch_noise19p638671875_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/402_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p638671875_objectives
```

Result:

```text
elapsed: 1414.7 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p638671875_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p638671875_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p638671875_seed21:
  x263/r8 is +1.59109e-03 worse (1.7942% relative) and clears the ambiguity
    cutoff by 2.60870e-04.
  first non-r8 branch x265/r7.5 is +1.97713e-03 worse (2.2295% relative).

base objective, source_mismatch_noise19p638671875_seed21:
  x263/r8 is +2.10044e-03 worse (1.5544% relative) and clears the ambiguity
    cutoff by 7.34455e-05.
  first non-r8 branch x264/r7.5 is +4.43566e-03 worse (3.2824% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.12264e-03 nominal and +5.51725e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.623,62.506,88.206), nonwhite fraction 0.271785
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the 19.638671875% RMS replicate set cleanly. Both seed21
rows selected truth x264/z90/r8, both were strong, and both ambiguity
intervals collapsed to a single x/z/r candidate. The tightest seed21
clearance is the source-mismatch x263/r8 competitor, which is still
7.34e-05 outside the ambiguity cutoff. Aggregate 400-402 next; if all six
rows remain true, strong, and zero-ambiguity, promote 19.638671875% RMS under
4-source 50 mm Tx/Rx.
```

## 403: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise19.638671875 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 19.638671875% RMS Tx/Rx=50 close14 replicate set
and decide whether this near-boundary level can be promoted above the
previous replicated-clean 19.62890625% RMS operating point.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/400_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p638671875_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/401_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p638671875_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/402_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p638671875_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise19p638671875_seed_replicates
  --outdir outputs/experiments/403_coordinate_confidence_close14_sources4_txrx50_noise19p638671875_seed_replicates
```

Output:

```text
outputs/experiments/403_coordinate_confidence_close14_sources4_txrx50_noise19p638671875_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 1.97713e-03 / 3.25133e-03 / 4.53014e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(80.415,55.528,72.514), nonwhite fraction 0.179197
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(34.707,34.623,34.835), nonwhite fraction 0.053370
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 19.638671875% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 19.638671875% RMS as the current clean
operating point for the larger-offset acquisition. The clean-to-ambiguous
transition is now bracketed between replicated-clean 19.638671875% RMS and
seed34 x-ambiguous 19.6484375% RMS. The next midpoint is 19.6435546875% RMS
seed34.
```

## 404: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.6435546875 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.638671875% RMS and seed34
x-ambiguous 19.6484375% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p6435546875_seed34|source_mismatch_noise19p6435546875_seed34
  --update-case-label source_mismatch_noise19p6435546875_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/404_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p6435546875_objectives
```

Result:

```text
elapsed: 1427.5 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p6435546875_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p6435546875_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p6435546875_seed34:
  x263/r8 is +1.33781e-03 worse (1.4998% relative) but remains inside the
    ambiguity cutoff by 1.48403e-07.
  first non-r8 branch x265/r7.5 is +2.15500e-03 worse (2.4160% relative).

base objective, source_mismatch_noise19p6435546875_seed34:
  x263/r8 is +2.40283e-03 worse (1.7862% relative) and clears the ambiguity
    cutoff by 3.85053e-04.
  first non-r8 branch x265/r7.5 is +4.31953e-03 worse (3.2111% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28336e-03 nominal and +5.66655e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(100.242,62.862,88.746), nonwhite fraction 0.276452
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 at 19.6435546875% RMS is point-correct but not clean. The best point
is still the true x264/z90/r8 and both radius labels are strong, but the
nominal near-best interval widens to 263-264 mm because x263/r8 remains
inside the ambiguity cutoff by 1.48e-07. Treat 19.6435546875% RMS as a new
seed34 ambiguous upper bound. Do not replicate this level. The clean-to-
ambiguous transition is now bracketed between replicated-clean 19.638671875%
RMS and seed34-ambiguous 19.6435546875% RMS. Run the lower midpoint
19.64111328125% RMS seed34 next.
```

## 405: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.64111328125 Midpoint

Purpose:

```text
test the lower midpoint between replicated-clean 19.638671875% RMS and
seed34 x-ambiguous 19.6435546875% RMS under the 4-source, 50 mm Tx/Rx
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p64111328125_seed34|source_mismatch_noise19p64111328125_seed34
  --update-case-label source_mismatch_noise19p64111328125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/405_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p64111328125_objectives
```

Result:

```text
elapsed: 1411.2 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p64111328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p64111328125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p64111328125_seed34:
  x263/r8 is +1.33784e-03 worse (1.5002% relative) and clears the ambiguity
    cutoff by 1.56439e-07.
  first non-r8 branch x265/r7.5 is +2.15504e-03 worse (2.4165% relative).

base objective, source_mismatch_noise19p64111328125_seed34:
  x263/r8 is +2.40290e-03 worse (1.7866% relative) and clears the ambiguity
    cutoff by 3.85510e-04.
  first non-r8 branch x265/r7.5 is +4.31967e-03 worse (3.2118% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28332e-03 nominal and +5.66657e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.795,62.622,88.362), nonwhite fraction 0.272841
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is clean at 19.64111328125% RMS under the 4-source, 50 mm Tx/Rx
acquisition, but only barely. The nominal x263/r8 competitor clears the
ambiguity cutoff by 1.56e-07, almost symmetric with the 19.6435546875%
ambiguous result where the same competitor was inside by 1.48e-07. Do not
promote this level from one seed. Replicate seeds 13 and 21 before deciding
whether 19.64111328125% RMS can become the next clean bracket.
```

## 406: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise19.64111328125 Replicate

Purpose:

```text
replicate the boundary-clean 19.64111328125% RMS seed34 midpoint on seed13
under the 4-source, 50 mm Tx/Rx acquisition before deciding whether this
near-limit noise level can be promoted.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p64111328125_seed13|source_mismatch_noise19p64111328125_seed13
  --update-case-label source_mismatch_noise19p64111328125_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/406_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p64111328125_objectives
```

Result:

```text
elapsed: 1424.9 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p64111328125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p64111328125_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p64111328125_seed13:
  x263/r8 is +1.56490e-03 worse (1.7369% relative) and clears the ambiguity
    cutoff by 2.13461e-04.
  first non-r8 branch x265/r7.5 is +2.09011e-03 worse (2.3199% relative).

base objective, source_mismatch_noise19p64111328125_seed13:
  x263/r8 is +2.54277e-03 worse (1.8859% relative) and clears the ambiguity
    cutoff by 5.20307e-04.
  first non-r8 branch x265/r7.5 is +4.53002e-03 worse (3.3598% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +2.86684e-03 nominal and +6.13771e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.027,62.207,87.699), nonwhite fraction 0.266745
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 stays clean at 19.64111328125% RMS under the 4-source, 50 mm Tx/Rx
acquisition. Both rows selected truth x264/z90/r8, both were strong, and both
near-best intervals collapsed to a single x/z/r candidate. Unlike the seed34
row, seed13 has a comfortable nominal x263/r8 ambiguity clearance of
2.13e-04. Run seed21 next; if it also remains clean, aggregate 405-407 before
promoting 19.64111328125% RMS.
```

## 407: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise19.64111328125 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set at 19.64111328125% RMS under the
4-source, 50 mm Tx/Rx acquisition before aggregating the near-boundary clean
candidate.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p64111328125_seed21|source_mismatch_noise19p64111328125_seed21
  --update-case-label source_mismatch_noise19p64111328125_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/407_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p64111328125_objectives
```

Result:

```text
elapsed: 1416.4 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p64111328125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p64111328125_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p64111328125_seed21:
  x263/r8 is +1.59108e-03 worse (1.7938% relative) and clears the ambiguity
    cutoff by 2.60592e-04.
  first non-r8 branch x265/r7.5 is +1.97706e-03 worse (2.2289% relative).

base objective, source_mismatch_noise19p64111328125_seed21:
  x263/r8 is +2.10034e-03 worse (1.5540% relative) and clears the ambiguity
    cutoff by 7.29602e-05.
  first non-r8 branch x264/r7.5 is +4.43551e-03 worse (3.2817% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.12262e-03 nominal and +5.51721e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(98.698,62.021,87.412), nonwhite fraction 0.264710
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the 19.64111328125% RMS replicate set cleanly. Both seed21
rows selected truth x264/z90/r8, both were strong, and both ambiguity
intervals collapsed to a single x/z/r candidate. The tightest seed21
clearance is the source-mismatch x263/r8 competitor, which is still
7.30e-05 outside the ambiguity cutoff. Aggregate 405-407 next; if all six
rows remain true, strong, and zero-ambiguity, promote 19.64111328125% RMS
under 4-source 50 mm Tx/Rx.
```

## 408: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise19.64111328125 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 19.64111328125% RMS Tx/Rx=50 close14 replicate
set and decide whether this near-boundary level can be promoted above the
previous replicated-clean 19.638671875% RMS operating point.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/405_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p64111328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/406_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p64111328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/407_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p64111328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise19p64111328125_seed_replicates
  --outdir outputs/experiments/408_coordinate_confidence_close14_sources4_txrx50_noise19p64111328125_seed_replicates
```

Output:

```text
outputs/experiments/408_coordinate_confidence_close14_sources4_txrx50_noise19p64111328125_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 1.97706e-03 / 3.25124e-03 / 4.53002e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(79.114,54.968,71.434), nonwhite fraction 0.174071
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(34.908,34.828,35.032), nonwhite fraction 0.054215
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 19.64111328125% RMS close14 tangent bracket is replicated clean under the
4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and nominal/source
mismatch rows, all six rows selected the true target-2 geometry x264/z90/r8,
all six radius labels were strong, and the near-best intervals collapsed to a
single x/z/r candidate. Promote 19.64111328125% RMS as the current clean
operating point for the larger-offset acquisition. The clean-to-ambiguous
transition is now bracketed between replicated-clean 19.64111328125% RMS and
seed34 x-ambiguous 19.6435546875% RMS. The next midpoint is
19.642333984375% RMS seed34.
```

## 409: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.642333984375 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.64111328125% RMS and seed34
x-ambiguous 19.6435546875% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p642333984375_seed34|source_mismatch_noise19p642333984375_seed34
  --update-case-label source_mismatch_noise19p642333984375_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/409_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p642333984375_objectives
```

Result:

```text
elapsed: 1424.5 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p642333984375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p642333984375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p642333984375_seed34:
  x263/r8 is +1.33782e-03 worse (1.5000% relative) and clears the ambiguity
    cutoff by 4.02121e-09.
  first non-r8 branch x265/r7.5 is +2.15502e-03 worse (2.4163% relative).

base objective, source_mismatch_noise19p642333984375_seed34:
  x263/r8 is +2.40286e-03 worse (1.7864% relative) and clears the ambiguity
    cutoff by 3.85282e-04.
  first non-r8 branch x265/r7.5 is +4.31960e-03 worse (3.2115% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28334e-03 nominal and +5.66656e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.497,62.477,88.108), nonwhite fraction 0.270655
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 is technically clean at 19.642333984375% RMS under the 4-source,
50 mm Tx/Rx acquisition, but it is numerically on the x-ambiguity boundary.
The nominal x263/r8 competitor clears the ambiguity cutoff by only 4.02e-09,
between the 19.64111328125% clean clearance of 1.56e-07 and the
19.6435546875% ambiguous miss of 1.48e-07. Do not promote this level from one
seed. Replicate seeds 13 and 21 before deciding whether 19.642333984375% RMS
can become the next clean bracket.
```

## 410: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed13 Noise19.642333984375 Replicate

Purpose:

```text
replicate the razor-thin clean 19.642333984375% RMS seed34 midpoint on
seed13 under the 4-source, 50 mm Tx/Rx acquisition before deciding whether
this boundary level can be promoted.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p642333984375_seed13|source_mismatch_noise19p642333984375_seed13
  --update-case-label source_mismatch_noise19p642333984375_seed13
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/410_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p642333984375_objectives
```

Result:

```text
elapsed: 1418.4 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p642333984375_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p642333984375_seed13: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p642333984375_seed13:
  x263/r8 is +1.56490e-03 worse (1.7367% relative) and clears the ambiguity
    cutoff by 2.13319e-04.
  first non-r8 branch x265/r7.5 is +2.09009e-03 worse (2.3196% relative).

base objective, source_mismatch_noise19p642333984375_seed13:
  x263/r8 is +2.54275e-03 worse (1.8857% relative) and clears the ambiguity
    cutoff by 5.20087e-04.
  first non-r8 branch x265/r7.5 is +4.52996e-03 worse (3.3594% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +2.86683e-03 nominal and +6.13772e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(98.721,62.058,87.439), nonwhite fraction 0.264552
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed13 stays clean at 19.642333984375% RMS under the 4-source, 50 mm Tx/Rx
acquisition. Both rows selected truth x264/z90/r8, both were strong, and both
near-best intervals collapsed to a single x/z/r candidate. Seed13 again has a
comfortable nominal x263/r8 ambiguity clearance of 2.13e-04 even though seed34
was only 4.02e-09 clear. Run seed21 next; if it also remains clean, aggregate
409-411 before promoting 19.642333984375% RMS.
```

## 411: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed21 Noise19.642333984375 Replicate

Purpose:

```text
complete the seed34/13/21 replicate set at 19.642333984375% RMS under the
4-source, 50 mm Tx/Rx acquisition before aggregating the boundary-clean
candidate.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p642333984375_seed21|source_mismatch_noise19p642333984375_seed21
  --update-case-label source_mismatch_noise19p642333984375_seed21
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/411_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p642333984375_objectives
```

Result:

```text
elapsed: 1399.7 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p642333984375_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8
  source_mismatch_noise19p642333984375_seed21: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p642333984375_seed21:
  x263/r8 is +1.59108e-03 worse (1.7936% relative) and clears the ambiguity
    cutoff by 2.60453e-04.
  first non-r8 branch x265/r7.5 is +1.97703e-03 worse (2.2287% relative).

base objective, source_mismatch_noise19p642333984375_seed21:
  x263/r8 is +2.10029e-03 worse (1.5538% relative) and clears the ambiguity
    cutoff by 7.27175e-05.
  first non-r8 branch x264/r7.5 is +4.43543e-03 worse (3.2813% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.12260e-03 nominal and +5.51719e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(98.333,61.841,87.102), nonwhite fraction 0.262109
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed21 completes the 19.642333984375% RMS replicate set cleanly. Both seed21
rows selected truth x264/z90/r8, both were strong, and both ambiguity
intervals collapsed to a single x/z/r candidate. The tightest seed21
clearance is the source-mismatch x263/r8 competitor, which is still
7.27e-05 outside the ambiguity cutoff. Aggregate 409-411 next; if all six
rows remain true, strong, and zero-ambiguity, promote 19.642333984375% RMS
under 4-source 50 mm Tx/Rx.
```

## 412: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise19.642333984375 Seed Aggregate

Purpose:

```text
aggregate the seed34/13/21 19.642333984375% RMS Tx/Rx=50 close14 replicate
set and decide whether this boundary-clean level can be promoted above the
previous replicated-clean 19.64111328125% RMS operating point.
```

Command:

```text
python -u run_coordinate_confidence_aggregate.py
  outputs/experiments/409_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p642333984375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/410_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p642333984375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/411_coordinate_optimizer_close14_seed21_sources4_txrx50_noise19p642333984375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --run-name coordinate_confidence_close14_sources4_txrx50_noise19p642333984375_seed_replicates
  --outdir outputs/experiments/412_coordinate_confidence_close14_sources4_txrx50_noise19p642333984375_seed_replicates
```

Output:

```text
outputs/experiments/412_coordinate_confidence_close14_sources4_txrx50_noise19p642333984375_seed_replicates
```

Result:

```text
row_count: 6
truth_geometry_count: 6
confidence_label_counts: strong=6
fallback_warning_count: 0
x_ambiguity_row_count: 0
max x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
radius_margin_abs min/mean/max: 1.97703e-03 / 3.25119e-03 / 4.52996e-03

acquisition summary:
  4 sources, Tx/Rx offset 50 mm: rows=6, truth rows=6, x ambiguity rows=0
```

Plot validation:

```text
coordinate_confidence_aggregate.png: 1720x971 px, dynamic range 255,
  std=(78.450,54.729,70.896), nonwhite fraction 0.171782
coordinate_ambiguity_widths.png: 1720x971 px, dynamic range 255,
  std=(35.145,35.063,35.271), nonwhite fraction 0.055218
FIGURE_NOTES.md exists and reports strong=6 and zero x-ambiguity rows.
```

Interpretation:

```text
The 19.642333984375% RMS close14 tangent bracket is replicated clean under
the 4-source, 50 mm Tx/Rx acquisition. Across seeds 34/13/21 and
nominal/source mismatch rows, all six rows selected the true target-2
geometry x264/z90/r8, all six radius labels were strong, and the near-best
intervals collapsed to a single x/z/r candidate. Promote 19.642333984375%
RMS as the current clean operating point for the larger-offset acquisition.
The clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34 x-ambiguous 19.6435546875% RMS. The next
midpoint is 19.6429443359375% RMS seed34.
```

## 413: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.6429443359375 Midpoint

Purpose:

```text
test the midpoint between replicated-clean 19.642333984375% RMS and seed34
x-ambiguous 19.6435546875% RMS under the 4-source, 50 mm Tx/Rx acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p6429443359375_seed34|source_mismatch_noise19p6429443359375_seed34
  --update-case-label source_mismatch_noise19p6429443359375_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/413_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p6429443359375_objectives
```

Result:

```text
elapsed: 1301.5 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p6429443359375_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p6429443359375_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p6429443359375_seed34:
  x263/r8 is +1.33782e-03 worse (1.4999% relative) but remains inside the
    ambiguity cutoff by 7.21902e-08.
  first non-r8 branch x265/r7.5 is +2.15501e-03 worse (2.4161% relative).

base objective, source_mismatch_noise19p6429443359375_seed34:
  x263/r8 is +2.40285e-03 worse (1.7863% relative) and clears the ambiguity
    cutoff by 3.85167e-04.
  first non-r8 branch x265/r7.5 is +4.31957e-03 worse (3.2113% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28335e-03 nominal and +5.66656e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(99.040,62.242,87.717), nonwhite fraction 0.267126
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 at 19.6429443359375% RMS is point-correct but not clean. The best
point is still the true x264/z90/r8 and both radius labels are strong, but
the nominal near-best interval widens to 263-264 mm because x263/r8 remains
inside the ambiguity cutoff by 7.22e-08. Treat 19.6429443359375% RMS as a
new seed34 ambiguous upper bound. Do not replicate this level. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.6429443359375% RMS. Run the
lower midpoint 19.64263916015625% RMS seed34 next.
```

## 414: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.64263916015625 Midpoint

Purpose:

```text
test the lower midpoint between replicated-clean 19.642333984375% RMS and
seed34 x-ambiguous 19.6429443359375% RMS under the 4-source, 50 mm Tx/Rx
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p64263916015625_seed34|source_mismatch_noise19p64263916015625_seed34
  --update-case-label source_mismatch_noise19p64263916015625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/414_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p64263916015625_objectives
```

Result:

```text
elapsed: 1289.5 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p64263916015625_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p64263916015625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p64263916015625_seed34:
  x263/r8 is +1.33782e-03 worse (1.5000% relative) but remains inside the
    ambiguity cutoff by 3.40843e-08.
  first non-r8 branch x265/r7.5 is +2.15502e-03 worse (2.4162% relative).

base objective, source_mismatch_noise19p64263916015625_seed34:
  x263/r8 is +2.40286e-03 worse (1.7864% relative) and clears the ambiguity
    cutoff by 3.85225e-04.
  first non-r8 branch x265/r7.5 is +4.31959e-03 worse (3.2114% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28335e-03 nominal and +5.66656e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(98.524,61.981,87.276), nonwhite fraction 0.263245
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 at 19.64263916015625% RMS is point-correct but not clean. The best
point is still the true x264/z90/r8 and both radius labels are strong, but
the nominal near-best interval widens to 263-264 mm because x263/r8 remains
inside the ambiguity cutoff by 3.41e-08. Treat 19.64263916015625% RMS as the
new seed34 ambiguous upper bound. Do not replicate this level. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.64263916015625% RMS. Run the
lower midpoint 19.642486572265625% RMS seed34 next.
```

## 415: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.642486572265625 Midpoint

Purpose:

```text
test the lower midpoint between replicated-clean 19.642333984375% RMS and
seed34 x-ambiguous 19.64263916015625% RMS under the 4-source, 50 mm Tx/Rx
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p642486572265625_seed34|source_mismatch_noise19p642486572265625_seed34
  --update-case-label source_mismatch_noise19p642486572265625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/415_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p642486572265625_objectives
```

Result:

```text
elapsed: 1291.0 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p642486572265625_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p642486572265625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p642486572265625_seed34:
  x263/r8 is +1.33782e-03 worse (1.5000% relative) but remains inside the
    ambiguity cutoff by 1.50315e-08.
  first non-r8 branch x265/r7.5 is +2.15502e-03 worse (2.4162% relative).

base objective, source_mismatch_noise19p642486572265625_seed34:
  x263/r8 is +2.40286e-03 worse (1.7864% relative) and clears the ambiguity
    cutoff by 3.85253e-04.
  first non-r8 branch x265/r7.5 is +4.31960e-03 worse (3.2114% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28334e-03 nominal and +5.66656e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(98.101,61.765,86.914), nonwhite fraction 0.260159
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 at 19.642486572265625% RMS is point-correct but not clean. The best
point is still the true x264/z90/r8 and both radius labels are strong, but
the nominal near-best interval widens to 263-264 mm because x263/r8 remains
inside the ambiguity cutoff by 1.50e-08. Treat 19.642486572265625% RMS as the
new seed34 ambiguous upper bound. Do not replicate this level. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.642486572265625% RMS. Run the
lower midpoint 19.6424102783203125% RMS seed34 next.
```

## 416: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.6424102783203125 Midpoint

Purpose:

```text
test the lower midpoint between replicated-clean 19.642333984375% RMS and
seed34 x-ambiguous 19.642486572265625% RMS under the 4-source, 50 mm Tx/Rx
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p6424102783203125_seed34|source_mismatch_noise19p6424102783203125_seed34
  --update-case-label source_mismatch_noise19p6424102783203125_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/416_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p6424102783203125_objectives
```

Result:

```text
elapsed: 1391.2 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p6424102783203125_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p6424102783203125_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p6424102783203125_seed34:
  x263/r8 is +1.33782e-03 worse (1.5000% relative) but remains inside the
    ambiguity cutoff by 5.50513e-09.
  first non-r8 branch x265/r7.5 is +2.15502e-03 worse (2.4163% relative).

base objective, source_mismatch_noise19p6424102783203125_seed34:
  x263/r8 is +2.40286e-03 worse (1.7864% relative) and clears the ambiguity
    cutoff by 3.85267e-04.
  first non-r8 branch x265/r7.5 is +4.31960e-03 worse (3.2114% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28334e-03 nominal and +5.66656e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(97.720,61.559,86.585), nonwhite fraction 0.257398
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 at 19.6424102783203125% RMS is point-correct but not clean. The best
point is still the true x264/z90/r8 and both radius labels are strong, but
the nominal near-best interval widens to 263-264 mm because x263/r8 remains
inside the ambiguity cutoff by 5.51e-09. Treat 19.6424102783203125% RMS as
the new seed34 ambiguous upper bound. Do not replicate this level. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.6424102783203125% RMS. Run the
lower midpoint 19.64237213134765625% RMS seed34 next.
```

## 417: Close-14 Sources=4, Tx/Rx Offset 50 mm, Seed34 Noise19.64237213134765625 Midpoint

Purpose:

```text
test the lower midpoint between replicated-clean 19.642333984375% RMS and
seed34 x-ambiguous 19.6424102783203125% RMS under the 4-source, 50 mm Tx/Rx
acquisition.
```

Command:

```text
python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml
  --grid-step-mm 1 --sources 4 --tx-rx-offset-mm 50 --frequency-ghz 1.5
  --true-x-values-mm 190,250,264 --true-z-values-mm 90,90,90
  --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,264
  --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6
  --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1
  --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5
  --replication-cases noise19p64237213134765625_seed34|source_mismatch_noise19p64237213134765625_seed34
  --update-case-label source_mismatch_noise19p64237213134765625_seed34
  --diagnostic-objective-variants base|highband --top-k 20
  --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets
```

Output:

```text
outputs/experiments/417_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p64237213134765625_objectives
```

Result:

```text
elapsed: 1413.1 s
sources: 4
tx_rx_offset_mm: 50.0
final state: x=[190,250,264], z=[90,90,90], r=[6,6,8]
objective top-candidate rows: 80
no radius-ambiguity revisit targets found.

confidence rows:
  noise19p64237213134765625_seed34: best x=264,z=90,r=8, strong,
    x interval 263-264, radius interval 8-8
  source_mismatch_noise19p64237213134765625_seed34: best x=264,z=90,r=8, strong,
    x interval 264-264, radius interval 8-8

base objective, noise19p64237213134765625_seed34:
  x263/r8 is +1.33782e-03 worse (1.5000% relative) but remains inside the
    ambiguity cutoff by 7.41956e-10.
  first non-r8 branch x265/r7.5 is +2.15502e-03 worse (2.4163% relative).

base objective, source_mismatch_noise19p64237213134765625_seed34:
  x263/r8 is +2.40286e-03 worse (1.7864% relative) and clears the ambiguity
    cutoff by 3.85274e-04.
  first non-r8 branch x265/r7.5 is +4.31960e-03 worse (3.2115% relative).

high-band objective:
  truth x264/r8 is best in both rows.
  radius margin is +3.28334e-03 nominal and +5.66656e-03 under source
    mismatch.
```

Plot validation:

```text
coordinate_confidence_margins.png: 1549x903 px, dynamic range 255,
  std=(97.279,61.326,86.207), nonwhite fraction 0.254226
FIGURE_NOTES.md exists and reports strong=2.
```

Interpretation:

```text
Seed34 at 19.64237213134765625% RMS is point-correct but not clean. The best
point is still the true x264/z90/r8 and both radius labels are strong, but
the nominal near-best interval widens to 263-264 mm because x263/r8 remains
inside the ambiguity cutoff by 7.42e-10. This is essentially the numerical
edge of the configured ambiguity rule. Treat 19.64237213134765625% RMS as the
final seed34 ambiguous upper bound for this bracket. The replicated-clean
level remains 19.642333984375% RMS; further bisection is not decision-useful
because the cutoff margin is already below 1e-09.
```

## 418: Close-14 Sources=4, Tx/Rx Offset 50 mm, Noise Boundary Summary

Purpose:

```text
package the final seed34 clean-to-ambiguous noise bracket for close-14 target 2
under 4-source, 50 mm Tx/Rx acquisition without running another FDTD sweep.
```

Command:

```text
python run_coordinate_noise_boundary_summary.py
  outputs/experiments/409_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p642333984375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/413_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p6429443359375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/414_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p64263916015625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/415_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p642486572265625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/416_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p6424102783203125_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  outputs/experiments/417_coordinate_optimizer_close14_seed34_sources4_txrx50_noise19p64237213134765625_objectives/data/multi_rebar_coordinate_optimizer_summary.json
  --clean-aggregate-json outputs/experiments/412_coordinate_confidence_close14_sources4_txrx50_noise19p642333984375_seed_replicates/data/coordinate_confidence_aggregate.json
  --promoted-clean-noise-rms-percent 19.642333984375
  --run-name coordinate_confidence_close14_txrx50_noise_boundary_summary
```

Output:

```text
outputs/experiments/418_coordinate_confidence_close14_txrx50_noise_boundary_summary
```

Result:

```text
rows summarized: 6
clean seed34 row count: 1
point-correct-not-clean row count: 5
promoted replicated-clean endpoint: 19.642333984375% RMS
final ambiguous upper endpoint: 19.642372131347656% RMS
final bracket width: 3.814697265625e-05% RMS
final ambiguous upper experiment: 417
final nominal x263/r8 margin to cutoff: -7.419559550081445e-10
stop tolerance: 1.0e-09
stop_due_to_numerical_edge: true

clean aggregate from experiment 412:
  rows=6
  truth_geometry_count=6
  x_ambiguity_row_count=0
  fallback_warning_count=0
  confidence_label_counts={strong: 6}
  radius_margin_abs min/mean/max =
    0.0019770301650875455 / 0.0032511884908621356 / 0.004529957610464208
```

Plot validation:

```text
noise_boundary_cutoff_margin.png: 1804x937 px, dynamic range 255,
  std=(31.696,31.880,32.332), nonwhite fraction 0.033482
noise_boundary_x_ambiguity_widths.png: 1804x903 px, dynamic range 255,
  std=(71.869,56.978,42.355), nonwhite fraction 0.203486
noise_boundary_radius_margins.png: 1923x937 px, dynamic range 255,
  std=(74.779,56.178,86.824), nonwhite fraction 0.380883
FIGURE_NOTES.md explains RMS, Tx/Rx, cutoff margin, x ambiguity widths, and
radius-margin evidence.
```

Interpretation:

```text
Experiment 418 turns the final bracket into a reusable decision artifact. The
cutoff-margin plot shows experiment 409 barely clean at +4.02121e-09, while
experiment 417 is barely ambiguous at -7.41956e-10. The ambiguity-width plot
confirms that only the nominal row opens to a 1 mm x interval above the clean
endpoint; the source-mismatch row stays collapsed. The radius-margin plot
confirms that radius evidence stays strong, so the boundary is a lateral
position ambiguity, not a radius failure. Keep 19.642333984375% RMS as the
promoted close-14 target-2 operating point under 4 sources and 50 mm Tx/Rx.
Do not spend more GPU time on this scalar noise bracket unless the ambiguity
rule itself changes.
```

## 419: Variable-Radius Staged Pipeline Replay Plan

Purpose:

```text
extend the packaged variable-radius staged summary with a dry-run replay plan
that captures the detection, assignment/location, focused polish, refined
focused polish, joint-radius, and summary commands from their run manifests.
```

Command:

```text
python run_variable_radius_staged_pipeline_summary.py
  --run-name variable_radius_staged_pipeline_seed13_21_34_sources7_replay_plan
  --case seed13|...216 detection...|...225 location...|...227 focused...|...222 joint...|...254 sources7 refined...
  --case seed21|...230 detection...|...233 location...|...234 focused...|...235 joint...|...255 sources7 refined...
  --case seed34_sources7|...239 detection...|...242 location...|...243 focused...|...247 joint...|...252 sources7 refined...
```

Output:

```text
outputs/experiments/419_variable_radius_staged_pipeline_seed13_21_34_sources7_replay_plan
```

Result:

```text
case count: 3
replay plan stage_count: 15
replay plan command_available_count: 15
replay command plan:
  data/staged_variable_radius_replay_commands.txt
replay plan JSON:
  data/staged_variable_radius_replay_plan.json

focused_policy by case:
  seed13: use_refined_focus_for_point_x
  seed21: use_refined_focus_for_point_x
  seed34_sources7: use_refined_focus_for_point_x

focused x ambiguity:
  standard 5-source focused stage: 2 x-ambiguity rows per seed
  refined 7-source focused stage: 0 x-ambiguity rows per seed

joint radius:
  truth tuple rank: 1 / 1 / 1
  joint max x/z/r error: 0 / 0 / 0 mm for all three cases
```

Plot validation:

```text
staged_variable_radius_pipeline_errors.png: 1753x971 px, dynamic range 255,
  std=(41.032,39.552,56.961), nonwhite fraction 0.101624
FIGURE_NOTES.md explains the staged error plot and per-case acquisition
settings.
```

Interpretation:

```text
Experiment 419 closes the packaging gap called out after the staged
variable-radius policy work. The summary still reports the same scientific
result as experiment 257: the economical 5-source focused stage carries a
target-2 x interval, the 7-source focused refinement collapses that interval
for all three seeds, and the joint-radius stage ranks the true [5,6,8] tuple
first. The new artifact is operational: a replay JSON and non-executable text
command plan list all 15 stage commands from their original manifests. This is
not a GPU rerun and should be treated as the dry-run orchestration package for
future staged variable-radius replications.
```
