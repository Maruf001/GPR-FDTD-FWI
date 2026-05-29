# Experiment 15: Trace-Shift Diagnostics

## Goal

Use the diagnostic idea from the 2025 optimal-transport FWI paper before
changing the inversion objective.

The question is:

```text
Does the radius-biased Powell basin have worse trace alignment than the
true-radius polished candidate, even when least-squares misfit is close?
```

If yes, trace-shift diagnostics can guide a later hybrid objective:

```text
OT-like or shift-aware basin search -> least-squares refinement -> grid polish
```

## Plain Terms

- **Least-squares misfit**: current waveform amplitude error objective.
- **Trace shift**: time shift that best aligns one synthetic trace with the
  observed trace by cross-correlation.
- **Dominant period**: period of the strongest frequency in the observed trace
  spectrum after muting.
- **RCCC**: absolute trace shift divided by dominant period.
- **NRCCC**: fraction of traces with `RCCC < 0.5`.

The optimal-transport paper uses the half-period criterion as a practical
signal that least-squares fitting is safe from cycle skipping.

## Planned Work

1. Add a small trace-distance diagnostics module.
2. Save final recovered trace-shift diagnostics in future
   `single_rebar_summary.json` outputs.
3. Add a post-hoc candidate diagnostic runner for existing single-rebar runs.
4. Compare the known Powell high-radius result against polished true-radius
   candidates.

## Run Log

### Code changes

Added:

```text
inversion/trace_distances.py
tests/test_trace_distances.py
run_single_rebar_trace_diagnostics.py
```

Updated:

```text
inversion/single_rebar_pipeline.py
run_single_rebar_inversion.py
```

Future `run_single_rebar_inversion.py` summaries now include:

```text
trace_shift_by_frequency
```

The post-hoc runner can evaluate arbitrary saved candidates or
`grid_polish.top_candidates` from previous runs.

### 024 - exact synthetic Powell vs polished candidates

Purpose: compare the known run 009 high-radius Powell result against exact
true-radius polished candidates.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_trace_diagnostics.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --run-name trace_shift_exact_powell_vs_polish \
  --summary-candidate powell009:outputs/experiments/009_single_rebar_grid1mm_powell_refine_from_2mm/data/single_rebar_summary.json:recovered \
  --summary-candidate polish014:outputs/experiments/014_single_rebar_grid1mm_gridpolish_from_run009/data/single_rebar_summary.json:recovered \
  --summary-candidate polish015:outputs/experiments/015_single_rebar_grid1mm_powell_gridpolish_from_2mm/data/single_rebar_summary.json:recovered \
  --candidate-mm true:250.0,90.0,6.0 \
  --candidate-mm high_radius_same_xz:249.5333604898392,90.65264829814728,6.954785108476757
```

Output:

```text
outputs/experiments/024_trace_shift_exact_powell_vs_polish/
```

Result:

```text
candidate             J           NRCCC  median RCCC  max RCCC  radius
polish014             0           1.000  0.000        0.000     6.000 mm
polish015             0           1.000  0.000        0.000     6.000 mm
true                  0           1.000  0.000        0.000     6.000 mm
powell009             2.0828e-03  1.000  0.003        0.003     6.955 mm
high_radius_same_xz   2.0828e-03  1.000  0.003        0.003     6.955 mm
```

Interpretation: trace shift is not the main reason run 009 is wrong. The
high-radius Powell candidate is already well phase-aligned by the paper's
half-period criterion. The radius problem is a subtler amplitude/shape and
hard-grid depth-radius ambiguity.

### 025 - 10% noise top-candidate diagnostics

Purpose: evaluate trace-shift diagnostics for the ranked top candidates from
the 10% noisy stress run.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_trace_diagnostics.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --run-name trace_shift_noise10_top_candidates \
  --observed-noise-rms-fraction 0.10 \
  --noise-seed 13 \
  --summary-candidate optimizer023:outputs/experiments/023_single_rebar_grid1mm_noise10_coarsepolish_topk/data/single_rebar_summary.json:optimizer_final \
  --summary-candidate recovered023:outputs/experiments/023_single_rebar_grid1mm_noise10_coarsepolish_topk/data/single_rebar_summary.json:recovered \
  --summary-top-candidates top023:outputs/experiments/023_single_rebar_grid1mm_noise10_coarsepolish_topk/data/single_rebar_summary.json:8
```

Output:

```text
outputs/experiments/025_trace_shift_noise10_top_candidates/
```

Result:

```text
candidate      J           NRCCC  median RCCC  max RCCC  radius
recovered023   1.9916e-01  1.000  0.000        0.003     6.000 mm
top023_top1    1.9916e-01  1.000  0.000        0.003     6.000 mm
top023_top2    1.9916e-01  1.000  0.000        0.003     6.000 mm
top023_top3    1.9972e-01  1.000  0.003        0.003     6.200 mm
top023_top4    1.9972e-01  1.000  0.003        0.003     6.200 mm
optimizer023   2.0142e-01  1.000  0.003        0.006     6.991 mm
top023_top5    2.0142e-01  1.000  0.003        0.006     6.800 mm
top023_top6    2.0183e-01  1.000  0.003        0.006     7.000 mm
top023_top7    2.0241e-01  1.000  0.006        0.010     6.400 mm
top023_top8    2.0241e-01  1.000  0.006        0.010     6.400 mm
```

Interpretation: the finer RCCC statistics weakly follow the least-squares
ranking, but the paper's main `NRCCC` switch criterion is saturated at 1.0 for
every candidate. That means all candidates are already in a least-squares-safe
phase-aligned basin. Trace-shift diagnostics alone will not resolve this
single-rebar radius ambiguity.

### 026 - 5% noise optimizer vs recovered candidate

Purpose: repeat the comparison at the moderate 5% noise level.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_trace_diagnostics.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --run-name trace_shift_noise05_optimizer_vs_recovered \
  --observed-noise-rms-fraction 0.05 \
  --noise-seed 13 \
  --summary-candidate optimizer020:outputs/experiments/020_single_rebar_grid1mm_noise05_coarsepolish/data/single_rebar_summary.json:optimizer_final \
  --summary-candidate recovered020:outputs/experiments/020_single_rebar_grid1mm_noise05_coarsepolish/data/single_rebar_summary.json:recovered
```

Output:

```text
outputs/experiments/026_trace_shift_noise05_optimizer_vs_recovered/
```

Result:

```text
candidate      J           NRCCC  median RCCC  max RCCC  radius
recovered020   5.8565e-02  1.000  0.000        0.000     6.000 mm
optimizer020   6.0876e-02  1.000  0.003        0.006     6.973 mm
```

Interpretation: the result matches the 10% case. The true-radius model is
better, but the high-radius model is also safely phase-aligned.

### 027 - summary-writing smoke run

Purpose: verify that future `single_rebar_summary.json` outputs include
`trace_shift_by_frequency`.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 1 \
  --max-iter 1 \
  --max-evals 1 \
  --run-name trace_shift_summary_smoke \
  --optimizer powell
```

Output:

```text
outputs/experiments/027_trace_shift_summary_smoke/
```

Result: `data/single_rebar_summary.json` contains `trace_shift_by_frequency`.

## Conclusion

Trace-shift diagnostics are now implemented and useful as a safety diagnostic,
but they do not explain the current single-rebar radius bias. In all tested
cases, including the high-radius Powell basin, `NRCCC = 1.0`, meaning the
candidate traces are already within the half-period alignment criterion from
the optimal-transport paper.

Practical consequence:

```text
Do not jump straight to OT-LS optimization for the current one-rebar radius
problem. The evidence says this is not primarily cycle skipping.
```

The better next paper-backed step is the progressive-bandwidth objective
schedule from the 2021 PEBDD paper. That method can change amplitude/detail
weighting across stages, which is more relevant to the observed radius/depth
tradeoff than trace-shift correction alone.

## Validation

Passed after implementing trace diagnostics:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  core/geometry.py core/materials.py gpu/fdtd_gpu_v2.py \
  inversion/single_rebar_pipeline.py inversion/trace_distances.py \
  run_single_rebar_inversion.py run_single_rebar_trace_diagnostics.py \
  run_single_rebar_objective_landscape.py run_single_rebar_radius_profile.py \
  core/run_outputs.py tests/test_gpu_cpml_parity.py \
  tests/test_single_rebar_pipeline.py tests/test_fdtd_basic.py \
  tests/test_grid_polish.py tests/test_trace_distances.py

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_trace_distances.py
# 3 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_grid_polish.py
# 5 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_fdtd_basic.py
# 6 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_single_rebar_pipeline.py
# 2 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_gpu_cpml_parity.py
# 2 passed, 0 failed

git diff --check
# no whitespace errors
```
