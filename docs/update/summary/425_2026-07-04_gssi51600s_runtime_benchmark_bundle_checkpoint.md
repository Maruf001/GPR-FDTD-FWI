# GSSI 51600S Runtime Benchmark Bundle Checkpoint

## Scope

- Added `run_gssi51600s_runtime_benchmark_card.py`.
- Generated a compact speed benchmark for the current trusted GSSI 51600S CUDA Fast-GPR optimizer path.
- Wired the runtime benchmark card and figure into the current GSSI prediction bundle.

## Runtime Benchmark

- Artifact:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/127_gssi51600s_runtime_benchmark_card_current`
- Decision:
  `gssi51600s_current_runtime_benchmark_ready`
- Scope:
  CUDA Fast-GPR optimizer loop only; excludes one-time setup, archive unpacking, plotting, and report packaging.

Current measured optimizer-loop timing:

- profiles 0-2 at 0.22 m spacing:
  - mean iteration runtime: `3.431 s`
  - 6-iteration optimizer-loop estimate: `20.587 s`
- profiles 1-3 at 0.22 m spacing:
  - mean iteration runtime: `3.515 s`
  - 6-iteration optimizer-loop estimate: `21.088 s`
- two-subset optimizer-loop estimate:
  - `41.676 s`
  - `0.695 min`

## Updated Bundle

- Artifact:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/130_gssi51600s_current_prediction_bundle_product_readme`
- Bundle now includes:
  - runtime benchmark summary path
  - runtime benchmark figure copy
  - runtime script snapshot
  - compact runtime fields in the summary JSON
  - README entries for the prediction text, summary JSON, release-style figure, spacing figure, and runtime figure

## Validation

- Focused GSSI suite:
  `84 passed in 4.66s`
- Diff hygiene:
  `git diff --check` passed for touched runtime, bundle, release-card, query, planner, test, and daily-update files.

## Product Interpretation

The current GSSI predictor bundle now reports both prediction quality and speed. The current 3D measured-offset two-subset fit is fast enough for interactive iteration after setup, but the timing should be rerun after changes to domain size, number of profile subsets, optimizer schedule, or iteration count.
