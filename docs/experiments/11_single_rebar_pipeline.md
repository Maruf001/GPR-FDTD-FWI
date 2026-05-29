# Experiment 11: Single-Rebar Geometry Pipeline

## Goal

Build the simplest reliable inversion problem before returning to multiple
rebars: one circular rebar, three unknowns, and synthetic observed data from
the same forward model.

Unknown parameter vector:

```text
[x_center, z_center, radius]
```

All values are in meters internally and reported in millimeters by the CLI.

## Command

Quick local CPU run:

```bash
python run_single_rebar_inversion.py --sources 5 --max-evals 25
```

More complete local or DGX Spark run:

```bash
python run_single_rebar_inversion.py --backend auto --sources 15 --max-evals 120
```

Multi-frequency objective:

```bash
python run_single_rebar_inversion.py --frequencies-ghz 1.4,1.5,1.6 --sources 15
```

## Outputs

```text
outputs/single_rebar/
  data/single_rebar_results.npz
  data/single_rebar_summary.json
  figures/single_rebar_model_comparison.png
  figures/single_rebar_convergence.png
  figures/single_rebar_observed_bscan.png
  figures/single_rebar_recovered_bscan.png
```

## Frequency Plan

Start with a fixed 1.5 GHz source. A small multi-frequency objective
(for example 1.4, 1.5, 1.6 GHz) is useful once the single-frequency inversion
is stable because it can reduce geometry ambiguity and test robustness.

Do not start with a broad sweep. Each extra frequency multiplies the forward
simulation count, so it is better used as a second-stage validation knob.

## GPU Plan

The systematic path uses the CPU solver by default and the CPML-capable GPU
solver when requested with `--backend gpu-cpml` or `--backend auto` on a CUDA
machine. The older GPU solver without CPML should be treated as a benchmark
artifact, not the production scientific path.

## DGX GPU Continuation Notes

The DGX Spark development path now prioritizes `--backend gpu-cpml`. CPU is
kept as a correctness reference, not the heavy inversion path.

Added GPU checks and workflow:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python tests/test_gpu_cpml_parity.py
```

This verifies that `gpu/fdtd_gpu_v2.py` matches the CPU CPML solver for both a
single trace and the batched B-scan path used by the inversion objective.

The GPU solver now supports batched scan simulation, so one objective evaluation
advances all scan positions together on the GPU instead of serializing each
trace. On this DGX run, the same 3-source/8-evaluation smoke changed from about
51 s on CPU to about 10 s with GPU batching.

A useful starter command for the current one-rebar problem is:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 9 \
  --optimizer differential-evolution \
  --de-popsize 5 \
  --max-evals 120 \
  --z-bounds-mm 60,130 \
  --radius-bounds-mm 4,10 \
  --outdir outputs/single_rebar_gpu_de_run03_9src_120eval_bounded
```

Result from that diagnostic:

```text
truth:     x=250.0 mm, z=90.0 mm, radius=6.0 mm
recovered: x=252.5 mm, z=91.8 mm, radius=6.8 mm
best J:    4.8008e-02
NRMS data: 4.3853e-02
runtime:   149.8 s for 120 evaluations with 9 sources
```

The broad default depth bound still permits deep, weak-scatterer false basins.
For the starter one-rebar pipeline, use physically realistic bounds while the
objective and optimizer are being developed.

## Objective Landscape Diagnostic

Added a reusable diagnostic entry point:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_objective_landscape.py \
  --backend gpu-cpml \
  --sources 9 \
  --xz-count 9 \
  --zr-count 9 \
  --radius-count 13 \
  --x-half-window-mm 60 \
  --z-half-window-mm 30 \
  --z-bounds-mm 60,130 \
  --radius-bounds-mm 4,10 \
  --radius-sweep-bounds-mm 4,10 \
  --compare-summary-json outputs/single_rebar_gpu_de_run03_9src_120eval_bounded/data/single_rebar_summary.json \
  --outdir outputs/single_rebar_landscape_9src_run01
```

Outputs:

```text
outputs/single_rebar_landscape_9src_run01/data/objective_landscape.npz
outputs/single_rebar_landscape_9src_run01/data/objective_landscape_summary.json
outputs/single_rebar_landscape_9src_run01/data/point_comparison.csv
outputs/single_rebar_landscape_9src_run01/data/radius_sweep.csv
outputs/single_rebar_landscape_9src_run01/data/xz_landscape.csv
outputs/single_rebar_landscape_9src_run01/data/z_radius_landscape.csv
outputs/single_rebar_landscape_9src_run01/figures/xz_landscape.png
outputs/single_rebar_landscape_9src_run01/figures/z_radius_landscape.png
outputs/single_rebar_landscape_9src_run01/figures/radius_sweep.png
```

Result:

```text
true:       J=0, x=250.0 mm, z=90.0 mm, radius=6.0 mm
initial:    J=1.4950, x=235.0 mm, z=80.0 mm, radius=8.0 mm
comparison: J=0.0480, x=252.5 mm, z=91.8 mm, radius=6.8 mm
```

All sampled diagnostic slices had their minimum at the true geometry. The
radius sweep is shallow and quantized around the true value:

```text
r=5.5 mm -> J=3.7920e-02
r=6.0 mm -> J=0
r=6.5 mm -> J=1.0942e-02
r=7.0 mm -> J=1.0942e-02
r=7.5 mm -> J=4.9268e-02
```

Interpretation: current single-frequency data identifies location well in the
local landscape, but radius is only stable to roughly grid-cell scale. This is
consistent with the 2 mm grid and rasterized circular inclusion: several nearby
radii produce very similar material masks and B-scans. The next objective work
should focus on radius resolution and false-basin rejection before moving to
multiple rebars.

## False Basin and Multi-Frequency Diagnostics

The landscape tool can now scan custom slice centers, which is useful for
checking false basins from broad optimizers:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_objective_landscape.py \
  --backend gpu-cpml \
  --sources 9 \
  --xz-count 7 \
  --zr-count 7 \
  --radius-count 11 \
  --x-bounds-mm 50,450 \
  --z-bounds-mm 50,200 \
  --radius-bounds-mm 3,8 \
  --xz-center-x-mm 109.10964773777393 \
  --xz-center-z-mm 176.228209550857 \
  --xz-radius-mm 3.520727976764159 \
  --zr-x-mm 109.10964773777393 \
  --zr-center-z-mm 176.228209550857 \
  --radius-sweep-x-mm 109.10964773777393 \
  --radius-sweep-z-mm 176.228209550857 \
  --compare-summary-json outputs/single_rebar_gpu_de_run01_9src_60eval/data/single_rebar_summary.json \
  --outdir outputs/single_rebar_landscape_false_basin_9src_run01
```

The false basin around the broad-search candidate is real but much worse than
the true basin:

```text
false candidate: J=8.3912e-01, x=109.1 mm, z=176.2 mm, radius=3.5 mm
local x-z min:   J=7.8599e-01, x=50.0 mm,  z=200.0 mm, radius=3.5 mm
true candidate:  J=0
```

A narrow multi-frequency diagnostic with 1.4, 1.5, and 1.6 GHz did not
materially sharpen radius identification on the current 2 mm grid. The radius
sweep values remained nearly the same as the 1.5 GHz-only run:

```text
single frequency: r=6.5 mm -> J=1.0942e-02, r=7.0 mm -> J=1.0942e-02
multi frequency:  r=6.5 mm -> J=1.0601e-02, r=7.0 mm -> J=1.0601e-02
```

Interpretation: the main radius limit is probably geometry rasterization and
2 mm grid resolution, not lack of nearby source frequencies. The next radius
resolution test should compare the current 2 mm grid with a finer-grid forward
configuration or a sub-cell/smoothed geometry parameterization.

## Numbered Output Convention

New runs should default to numbered directories under:

```text
outputs/experiments/NNN_<run_name>/
```

Both `run_single_rebar_inversion.py` and
`run_single_rebar_objective_landscape.py` now allocate the next number when
`--outdir` is omitted. Each numbered run writes `run_manifest.json` with the
command, timestamp, git commit/status, backend, source count, frequencies, and
summary path. Explicit `--outdir` still works for reproducing old commands or
writing a named diagnostic directory.

## Grid Resolution Probe

A small one-source diagnostic compared the current 2 mm grid against a temporary
1 mm grid override using identical radius sweep samples from 4 to 8 mm:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_objective_landscape.py \
  --backend gpu-cpml \
  --sources 1 \
  --radius-count 9 \
  --radius-sweep-bounds-mm 4,8 \
  --run-name radius_grid2mm_probe

/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_objective_landscape.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 1 \
  --radius-count 9 \
  --radius-sweep-bounds-mm 4,8 \
  --run-name radius_grid1mm_probe
```

Outputs:

```text
outputs/experiments/002_radius_grid2mm_probe/
outputs/experiments/003_radius_grid1mm_probe/
```

Radius sweep comparison:

```text
2 mm grid:
  r=4.5,5.0,5.5 mm -> J=1.1538e-03  (identical)
  r=6.5,7.0 mm     -> J=3.3941e-04  (identical)

1 mm grid:
  r=4.5 mm -> J=2.2584e-03
  r=5.0 mm -> J=9.8218e-04
  r=5.5 mm -> J=3.2800e-04
  r=6.0 mm -> J=0
  r=6.5 mm -> J=3.7501e-04
  r=7.0 mm -> J=1.0385e-03
```

Interpretation: the finer grid removes the repeated-radius objective plateaus,
so radius ambiguity is substantially a geometry rasterization issue. A full
1 mm-grid inversion will be more expensive, but it is the clean next validation
path before adding more rebars. A cheaper alternative is sub-cell/smoothed
circle geometry on the 2 mm grid; that is tested below.

## Sub-Cell Geometry Probe

Added opt-in sub-cell circular geometry with `--geometry-mode subcell` and
`--subcell-samples`. The implementation estimates the fraction of each Ez-cell
control volume occupied by the circular rebar. Epsilon and permeability are
linearly blended; conductivity is log-blended so partial steel cells do not
immediately behave like full steel cells.

One-source diagnostic command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_objective_landscape.py \
  --backend gpu-cpml \
  --sources 1 \
  --run-name radius_subcell2mm_s9_logsigma_probe \
  --geometry-mode subcell \
  --subcell-samples 9 \
  --radius-count 9 \
  --radius-sweep-bounds-mm 4,8 \
  --xz-count 2 \
  --zr-count 2 \
  --progress-every 0
```

Output:

```text
outputs/experiments/006_radius_subcell2mm_s9_logsigma_probe/
```

Radius sweep comparison:

```text
2 mm hard:
  r=4.5,5.0,5.5 mm -> J=1.1538e-03  (identical)
  r=6.5,7.0 mm     -> J=3.3941e-04  (identical)

2 mm subcell, 9 samples, linear conductivity blend:
  r=5.5 mm -> J=4.6644e-04
  r=6.5 mm -> J=6.6691e-11
  r=7.0 mm -> J=7.7024e-11

2 mm subcell, 9 samples, log conductivity blend:
  r=4.5 mm -> J=1.0115e-03
  r=5.0 mm -> J=1.0536e-03
  r=5.5 mm -> J=8.9106e-04
  r=6.0 mm -> J=0
  r=6.5 mm -> J=4.5352e-04
  r=7.0 mm -> J=4.9792e-04
```

Interpretation: log conductivity blending removes the worst linear-blend
artifact where 6.5 and 7.0 mm were nearly indistinguishable from the true
6.0 mm radius. It is still less clean than the 1 mm hard-grid sweep, especially
on the smaller-radius side. For production inversion validation, prefer a
1 mm-grid forward configuration; keep sub-cell geometry as a cheaper diagnostic
or fallback, not the primary evidence that radius is identifiable.


## 1 mm Inversion CLI Smoke

`run_single_rebar_inversion.py` now also accepts `--grid-step-mm`, matching the
landscape diagnostic. This keeps the numbered inversion pipeline usable for the
higher-resolution forward configuration that best separated nearby radii.

Smoke command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 1 \
  --max-iter 1 \
  --max-evals 1 \
  --run-name single_rebar_grid1mm_cli_smoke \
  --z-bounds-mm 60,130 \
  --radius-bounds-mm 4,10
```

Output:

```text
outputs/experiments/007_single_rebar_grid1mm_cli_smoke/
```

Result:

```text
grid:      dx=dz=1.0 mm, NX=560, NZ=360, NT=3769, NPML=30
runtime:   2.9 s
objective: J=9.4436e-02 at the initial guess
success:   false, expected because the smoke was capped at one evaluation
```

Interpretation: this was not intended to recover the rebar. It validates that
the 1 mm GPU inversion path builds, runs, writes plots/data, and records grid
metadata in both the summary JSON and run manifest. The next substantive run is
a bounded 1 mm-grid differential-evolution inversion with enough evaluations to
estimate x, z, and radius.


## 1 mm Staged Inversion Runs

A direct broad 1 mm-grid DE run with 5 sources and about 60 evaluations did not
find the true basin:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer differential-evolution \
  --de-popsize 4 \
  --max-evals 60 \
  --run-name single_rebar_grid1mm_de_5src_60eval_bounded \
  --z-bounds-mm 60,130 \
  --radius-bounds-mm 4,10
```

Output:

```text
outputs/experiments/008_single_rebar_grid1mm_de_5src_60eval_bounded/
recovered: x=105.7 mm, z=127.8 mm, radius=7.8 mm
best J:    1.0447
NRMS data: 0.1773
runtime:   319.2 s for 60 evaluations
```

Interpretation: 60 evaluations is too small for broad 1 mm global search over
the full lateral range. The result is a search-budget failure, not evidence
against the 1 mm forward model.

A staged run using the previous 2 mm coarse recovery as the 1 mm initial guess
worked much better:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 10 \
  --max-evals 50 \
  --run-name single_rebar_grid1mm_powell_refine_from_2mm \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10
```

Output:

```text
outputs/experiments/009_single_rebar_grid1mm_powell_refine_from_2mm/
truth:     x=250.0 mm, z=90.0 mm, radius=6.0 mm
recovered: x=249.5 mm, z=90.7 mm, radius=7.0 mm
best J:    2.0828e-03
NRMS data: 7.8896e-03
runtime:   266.6 s for 50 evaluations
```

Interpretation: the staged coarse-to-fine path is the right pipeline direction.
The 1 mm local refinement recovers x and z accurately and greatly improves data
fit, but radius remains biased high. The next radius-specific step should not
be another broad global search; it should profile or optimize radius separately
near the recovered x-z location, possibly with more sources and a radius prior,
before expanding to multiple rebars.

## Radius Refinement Continuation

The follow-up radius-specific work is tracked in:

```text
docs/experiments/12_radius_refinement_worklog.md
```

Current conclusion from runs 010-016: the staged single-rebar path should use a
2 mm bounded global search, a 1 mm local continuous refinement, and a final
1 mm deterministic local grid polish. The grid polish resolves the remaining
radius bias caused by hard-grid rasterization and the z-radius tradeoff near
the optimum.
