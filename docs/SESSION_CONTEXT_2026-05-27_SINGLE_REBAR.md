# Session Context: Single-Rebar Geometry Pipeline

Date: 2026-05-27

Read this file first when continuing work on DGX Spark or another machine.

## Current Direction

We are moving from the interview proof-of-concept toward a systematic GPR
inversion pipeline. The immediate target is deliberately simple:

```text
one circular rebar in 2D concrete
unknowns = [x_center, z_center, radius]
```

The reason for starting here is engineering discipline. Before estimating
multiple rebars, unequal depths, unequal radii, or non-circular shapes, we need
a clean forward/inverse loop whose objective, optimizer behavior, outputs, and
GPU path are easy to validate.

## Repository Choice

Continue development in `FTDT_Project`.

Previous inspection showed that `FTDT_Project` and `FTDT_Project_2` have
identical core development files (`core/`, `inversion/`, `gpu/`,
`visualization/`, tests, run scripts, config, requirements). `FTDT_Project_2`
looked like a presentation/artifact staging copy and had dirty/deleted tracked
documentation files. `FTDT_Project` was the clean repo and should be the base.

## What Changed This Session

Added a separate one-rebar pipeline instead of mutating the old three-rebar
interview path.

New files:

```text
run_single_rebar_inversion.py
inversion/single_rebar_pipeline.py
tests/test_single_rebar_pipeline.py
docs/experiments/11_single_rebar_pipeline.md
docs/SESSION_CONTEXT_2026-05-27_SINGLE_REBAR.md
```

Modified files:

```text
.gitignore
core/geometry.py
visualization/plot_inversion.py
```

Key implementation decisions:

- `core.geometry.build_rebar_model()` now accepts optional explicit rebar
  tuples while preserving the default three-rebar behavior.
- `core.geometry.build_single_rebar_model(x, z, radius)` builds the synthetic
  one-rebar scene.
- `inversion.single_rebar_pipeline.SingleRebarInversionEngine` synthesizes
  observed B-scan data and recovers `[x, z, radius]` using a normalized muted
  B-scan objective.
- The new CLI defaults to CPU but supports `--backend gpu-cpml` and
  `--backend auto`.
- The GPU production path is intended to use `gpu/fdtd_gpu_v2.py`, which has
  CPML. The older `gpu/fdtd_gpu.py` does not include CPML and should be treated
  as a benchmark artifact, not the scientific inversion path.
- `run_single_rebar_inversion.py` forces `MPLBACKEND=Agg` and local cache
  directories under `outputs/` so plotting works in terminal, DGX, and batch
  environments.
- `.gitignore` now ignores generated single-rebar outputs and local Matplotlib
  caches.

## Important Runtime Note

During local smoke testing on macOS, Python crashed with “Python quit
unexpectedly” when Matplotlib selected the macOS GUI backend. The inversion had
already completed; the crash happened while creating figures.

Fix applied:

```python
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "outputs/.matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "outputs/.cache")
```

This is the correct behavior for DGX Spark as well.

## Validation Completed

Syntax check:

```bash
python3 -m py_compile \
  core/geometry.py \
  visualization/plot_inversion.py \
  inversion/single_rebar_pipeline.py \
  run_single_rebar_inversion.py \
  tests/test_single_rebar_pipeline.py
```

Existing FDTD tests:

```bash
python3 tests/test_fdtd_basic.py
```

Result:

```text
6 passed, 0 failed
```

New one-rebar smoke tests:

```bash
python3 tests/test_single_rebar_pipeline.py
```

Result:

```text
2 passed, 0 failed
```

The new objective test confirmed:

```text
J(true geometry) = 0
J(wrong geometry) > J(true geometry)
```

CLI smoke run:

```bash
python3 -u run_single_rebar_inversion.py \
  --sources 1 \
  --max-iter 1 \
  --max-evals 3 \
  --outdir outputs/single_rebar_smoke_short
```

This intentionally stops early and is not an accuracy test. It verifies that
the CLI, optimizer call, data saving, and figure generation complete.

Generated smoke outputs:

```text
outputs/single_rebar_smoke_short/data/single_rebar_results.npz
outputs/single_rebar_smoke_short/data/single_rebar_summary.json
outputs/single_rebar_smoke_short/figures/single_rebar_convergence.png
outputs/single_rebar_smoke_short/figures/single_rebar_model_comparison.png
outputs/single_rebar_smoke_short/figures/single_rebar_observed_bscan.png
outputs/single_rebar_smoke_short/figures/single_rebar_recovered_bscan.png
```

## Recommended DGX Spark Continuation Plan

1. Pull the latest repo.

```bash
git pull
```

2. Verify the Python environment.

```bash
python3 -c "import numpy, scipy, matplotlib; print('core deps ok')"
python3 -c "import cupy as cp; print(cp.__version__); print(cp.cuda.runtime.getDeviceCount())"
```

3. Run CPU tests first.

```bash
python3 tests/test_fdtd_basic.py
python3 tests/test_single_rebar_pipeline.py
```

4. Run a CPU CLI smoke test.

```bash
python3 -u run_single_rebar_inversion.py \
  --sources 3 \
  --max-iter 1 \
  --max-evals 8 \
  --outdir outputs/single_rebar_cpu_smoke
```

5. Run a GPU-CPML smoke test.

```bash
python3 -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 3 \
  --max-iter 1 \
  --max-evals 8 \
  --outdir outputs/single_rebar_gpu_smoke
```

6. If CPU/GPU smoke tests complete, run a meaningful one-rebar inversion.

```bash
python3 -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 9 \
  --max-iter 20 \
  --max-evals 120 \
  --outdir outputs/single_rebar_gpu_run01
```

7. Only after the fixed-frequency run is stable, test a narrow frequency
   objective.

```bash
python3 -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 9 \
  --frequencies-ghz 1.4,1.5,1.6 \
  --max-iter 20 \
  --max-evals 180 \
  --outdir outputs/single_rebar_gpu_freq_1p4_1p6
```

## Frequency Sweep Position

Use frequency as a controlled second-stage knob, not the first thing to solve.

Reasoning:

- Each added frequency multiplies forward simulation cost.
- A narrow range such as 1.4, 1.5, 1.6 GHz may improve robustness and reduce
  geometry ambiguity once the single-frequency objective behaves.
- Starting with one frequency makes failures easier to diagnose: geometry,
  optimizer, source sampling, muting, or backend mismatch.

## gprMax Position

gprMax is relevant as a reference-quality external GPR/FDTD package, especially
for later validation and realistic antenna/material modeling. It should not
replace the current code at this stage.

Recommended use later:

- compare synthetic B-scans for a simple one-rebar scene,
- borrow modeling conventions for antennas/materials,
- validate whether our simplified solver produces plausible qualitative
  hyperbola behavior.

Do not introduce gprMax into the core pipeline until the current one-rebar
synthetic inversion is stable.

## Next Engineering Tasks

Highest priority:

- Run the one-rebar pipeline on DGX Spark with `--backend gpu-cpml`.
- Compare CPU vs GPU-CPML traces/objectives for the same candidate geometry.
- Run a real one-rebar inversion with enough evaluations to check whether
  `[x, z, radius]` converges toward truth.

Likely next code work:

- Add a formal CPU/GPU equivalence test for `FDTDSimulator` vs
  `FDTDSimulatorGPU_v2`.
- Add a result-summary plot/table for true vs initial vs recovered parameters.
- Add optimizer diagnostics if Powell stalls or radius is weakly identified.
- Once one rebar works, generalize to `N` independent circular rebars with
  explicit parameter ordering and constraints.
- Later extend shape parameterization: ellipse, rectangle, square.

## Mental Model of the Repo

Current project layers:

```text
config.py                 fixed physical/grid/source parameters
core/                     FDTD solver, CPML, material geometry, scanning
gpu/                      CuPy GPU solvers; v2 includes CPML
inversion/                old POC inversion plus new single-rebar pipeline
visualization/            plotting for models, B-scans, convergence
tests/                    lightweight correctness/smoke tests
run_*.py                  CLI entry points
docs/experiments/         experiment notes
```

For the current task, the main files are:

```text
run_single_rebar_inversion.py
inversion/single_rebar_pipeline.py
core/geometry.py
gpu/fdtd_gpu_v2.py
tests/test_single_rebar_pipeline.py
```

