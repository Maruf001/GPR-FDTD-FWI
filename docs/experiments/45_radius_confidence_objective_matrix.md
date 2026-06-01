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
