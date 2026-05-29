# Experiment 19: Plotting And Baseline Infrastructure

## Goal

Start the autonomous research marathon by fixing infrastructure that can
mislead later decisions:

```text
plotting must be readable,
baseline summaries must be machine-readable,
and candidate margins must be easy to compare.
```

The user flagged several unacceptable plots:

```text
B-scan figures that render blank,
convergence figures with annotation text expanding the canvas,
model comparison colorbar overlapping the ground-truth panel.
```

## Plan

1. Add plotting helper functions with tests.
2. Replace fragile B-scan rendering with a robust image-based path.
3. Replace convergence arrow annotations with fixed in-axis summary text.
4. Put model-comparison colorbars in dedicated axes.
5. Validate generated figures before using them in experiments.
6. Then build the baseline result matrix and top-candidate margin extractor.

## Run Log

### Plotting helper implementation

Changed:

```text
visualization/plot_style.py
visualization/plot_bscan.py
visualization/plot_inversion.py
tests/test_plotting.py
```

Implemented:

```text
safe symmetric color limits,
single-column B-scan extents,
validated figure saving,
image-based B-scan plotting,
dedicated model-comparison colorbar axis,
convergence summary text instead of long arrow annotations.
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_plotting.py -q
5 passed
```

### 042 - plotting template validation smoke

Purpose: regenerate all standard single-rebar figures using the new plotting
path, including the one-source B-scan case that previously rendered blank.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 1 \
  --max-iter 1 \
  --max-evals 1 \
  --run-name plotting_template_validation_smoke \
  --optimizer powell
```

Output:

```text
outputs/experiments/042_plotting_template_validation_smoke/
```

Figure validation:

```text
single_rebar_convergence.png:       size=(2059, 835), dynamic_range=255
single_rebar_model_comparison.png:  size=(3079, 954), dynamic_range=255
single_rebar_observed_bscan.png:    size=(1715, 1209), dynamic_range=255
single_rebar_recovered_bscan.png:   size=(1715, 1209), dynamic_range=255
```

Interpretation:

```text
The plotting failures shown by the user are addressed at the template level.
Future experiment figures should use these helpers rather than ad hoc plotting.
```

## Current Decision

Proceed to the Day 1 baseline result matrix and top-candidate margin extractor.
