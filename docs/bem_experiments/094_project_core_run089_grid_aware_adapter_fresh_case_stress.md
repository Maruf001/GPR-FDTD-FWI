# BEM Experiment 094: Project-Core Run089 Grid-Aware Adapter Fresh-Case Stress

Date: 2026-06-25

## Purpose

Stress the run `093` reusable adapter on fresh homogeneous dielectric-cylinder
cases outside the original run `089` geometry.

Run `093` proved that the run `092` contract can emit a full adapter payload
and reproduce the run `091` gate. This run asks whether that path survives
controlled changes in contrast, radius, and target position before any
layered, field, 3D, GPU, or `outputs/experiments` promotion is considered.

This is CPU-only. It reruns small matched project-core FDTD target/background
and target-cell field recordings for three homogeneous cases. It does not use
field data, GPU kernels, FWI, 3D/HPC work, neural-network training, or the
historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/094_project_core_run089_grid_aware_adapter_fresh_case_stress
```

Key artifacts:

```text
data/project_core_run089_grid_aware_adapter_fresh_case_stress_summary.json
data/project_core_run089_grid_aware_adapter_fresh_case_summary.csv
data/project_core_run089_grid_aware_adapter_fresh_case_variants.csv
data/project_core_run089_grid_aware_adapter_fresh_case_frequency_scales.csv
data/project_core_run089_grid_aware_adapter_fresh_case_arrays.npz
figures/project_core_run089_grid_aware_adapter_fresh_case_stress.png
docs/PROJECT_CORE_RUN089_GRID_AWARE_ADAPTER_FRESH_CASE_STRESS.md
scripts/run_project_core_run089_grid_aware_adapter_fresh_case_stress.py
scripts/test_project_core_run089_grid_aware_adapter_fresh_case_stress.py
scripts/script_snapshot_manifest.json
```

## Result

```text
case count:                         3
passed cases:                       3
failed cases:                       0
worst best-case L2:                 0.6662947067388982
all fresh cases pass:               true
ready for next stress design:       true
ready for half-space promotion:     false
ready for outputs/experiments promo: false
ready for field transfer:           false
ready for 3D validation:            false
ready for GPU work:                 false
```

Case table:

| Case | epsr | Radius m | Center x m | Center z m | Target cells | Best variant | Best L2 | Ready |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| lower_contrast_radius_25mm | 2.0 | 0.025 | 0.25 | 0.15 | 533 | product_no_div | 0.1885181142668548 | true |
| shifted_deeper_epsr4 | 4.0 | 0.03 | 0.23 | 0.17 | 753 | receiver_conjugate_div_source | 0.6662947067388982 | true |
| larger_high_contrast_epsr6 | 6.0 | 0.035 | 0.27 | 0.14 | 1013 | product_no_div | 0.5507342875625141 | true |

## Interpretation

The reusable run `093` adapter now has a positive homogeneous fresh-case
envelope. The weakest of the three cases is the shifted/deeper epsr-4 case at
0.6662947067388982 symmetric L2, still below the 0.75 acceptance line.

This supports designing the next layered or half-space smoke. It does not
itself promote half-space, field transfer, 3D validation, GPU work, FWI, or
historical `outputs/experiments` claims.

## Decision

Use this as the homogeneous fresh-case stress checkpoint. The next
duplicated-script branch can test a layered or half-space smoke, but promotion
must remain blocked until that branch passes.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test:

```text
scripts/run_project_core_run089_grid_aware_adapter_fresh_case_stress.py
scripts/test_project_core_run089_grid_aware_adapter_fresh_case_stress.py
scripts/script_snapshot_manifest.json
```

Recorded SHA-256 values:

```text
run_project_core_run089_grid_aware_adapter_fresh_case_stress.py
7c83f1c158ca9c1fc998301c600813e5f8b1702bafa943cbe351dced3db798bf

test_project_core_run089_grid_aware_adapter_fresh_case_stress.py
987af75fbcbd670a29679883cc14aff32fb8d0918ace642e3688a392765ae8ea
```

## Validation

Focused tests:

```text
tests/test_project_core_run089_grid_aware_adapter_fresh_case_stress.py
2 passed
```

Figure check:

```text
project_core_run089_grid_aware_adapter_fresh_case_stress.png  2536x718, dynamic range=255
```
