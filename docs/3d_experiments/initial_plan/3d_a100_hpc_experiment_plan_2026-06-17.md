# Initial 3D Experiments Plan for A100/NERSC HPC

Date: 2026-06-17

## Purpose

Create a research and execution plan for future 3D GPR FDTD/FWI experiments on
an HPC cluster with NVIDIA A100 GPUs, especially NERSC Perlmutter-style A100
nodes. This is an initial planning document, not a numbered 2D experiment
tracker and not a compute run. No new synthetic optimizer run, field-data
inversion, broad GPU sweep, or figure backfill was launched while preparing this
note.

This file deliberately lives under `docs/3d_experiments/initial_plan`. The
future 3D experiment tracker root is `docs/3d_experiments`; numbered 3D trackers
should live there when real 3D experiments begin. Do not put 3D planning or HPC
trackers under `docs/experiments`, which is the mature 2D synthetic tracker
stream.

The plan is intentionally conservative because the restored project has a mature
2D synthetic coordinate-optimizer archive, early field-data QC, and no current
3D solver implementation. The right next step is to preserve the 2D evidence,
keep field data separate, and design 3D as a staged capability rather than a
direct edit to the 2D runner.

## Inputs Audited

Project and migration documents:

```text
README.md
MIGRATION.md
SETUP.md
docs/update/summary
FIGURE_ANIMATION_TEMPLATE_INVENTORY.md
NEXT_DGX_SPARK_CHECKLIST.md
docs/dgx_spark_guide.md
docs/experiments/experiment_category_index.md
docs/experiments_consolidated/README.md
docs/experiments/756_marathon_stop_point_evaluation_seed2111485081748050_to_seed5527939710754757.md
docs/experiments/758_target1_confidence_policy_synthesis.md
```

Paper and positioning documents:

```text
docs/papers/00_paper_index.md
docs/papers/01_wavefield_reconstruction_2022.md
docs/papers/02_progressive_bandwidth_fwi_2021.md
docs/papers/03_optimal_transport_fwi_2025.md
docs/papers/04_quadratic_wasserstein_gpr_fwi_2024.md
docs/papers/05_implicit_multiparameter_gpr_fwi_2025.md
docs/papers/2026-06-07_literature_positioning_matrix.md
docs/papers/2026-06-07_literature_positioning_matrix.ipynb
docs/papers/2026-06-07_novelty-gap_analysis.md
docs/papers/rebar_fwi_strategy_from_papers.md
docs/papers/master_rebar_fwi_research_plan_from_5_papers.md
```

Neural-network paper inputs added under `paper/neural_network`:

```text
paper/neural_network/paper_index.md
paper/neural_network/1907.09997v1.pdf
paper/neural_network/1-s2.0-S0926580519301347-main.pdf
paper/neural_network/2207.06527v1.pdf
paper/neural_network/2305.05425v1.pdf
```

Synthetic archive and summary inputs:

```text
outputs/experiments
docs/experiments
docs/experiments_consolidated
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data
```

Field-data inputs:

```text
data/2026-06-09_GSSI_model_51600S
outputs/field_experiments/local_gssi_51600s_2026_06_09
docs/field_experiments/local_gssi_51600s_2026_06_09
```

Code areas checked for 3D/HPC relevance:

```text
config.py
core/fdtd.py
core/materials.py
core/geometry.py
core/scan.py
gpu/fdtd_gpu_v2.py
gpu/cpml_gpu.py
inversion/inversion_engine.py
inversion/geometry_inversion.py
inversion/source_profile.py
inversion/candidate_confidence.py
run_multi_rebar_coordinate_optimizer.py
core/run_outputs.py
tests
```

External primary/reference sources used for this plan:

- NERSC Perlmutter and Slurm/job policy documentation:
  https://docs.nersc.gov/systems/perlmutter/architecture/
  https://docs.nersc.gov/systems/perlmutter/running-jobs/
  https://docs.nersc.gov/jobs/
  https://docs.nersc.gov/jobs/policy/
- NVIDIA A100 product page and datasheet:
  https://www.nvidia.com/en-us/data-center/a100/
  https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-nvidia-us-2188504-web.pdf
- NVIDIA A100 80GB PCIe product brief:
  https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf
- NVIDIA CUDA Programming Guide:
  https://docs.nvidia.com/cuda/cuda-programming-guide/index.html
- NVIDIA NCCL overview:
  https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html
- Slurm GRES and sbatch documentation:
  https://slurm.schedmd.com/gres.html
  https://slurm.schedmd.com/sbatch.html
- gprMax documentation and publications:
  https://docs.gprmax.com/en/latest/gprmodelling.html
  https://www.gprmax.com/publications.shtml
  https://github.com/gprMax/gprMax
- h5py dataset/chunking documentation:
  https://docs.h5py.org/en/latest/high/dataset.html
- Jazayeri et al. 2019 rebar FWI paper:
  https://sajadjazayeri.github.io/papers/Jazayeri_etal_2019_rebar_FWI.pdf
- 3DInvNet paper and code:
  https://arxiv.org/abs/2305.05425
  https://github.com/qiqi-dai/3dinvnet

## Current Project State

### Synthetic Archive

The restored synthetic archive is internally consistent at the migration level:

```text
outputs/experiments direct dirs:       1219
numbered experiment dirs:              1218
run_manifest.json files:               1214
archive entries in migration inventory: 14538
```

The mature scientific result is the variable-depth, variable-radius, 3-rebar 2D
coordinate optimizer. The June 11 holistic table contains 425 parseable
coordinate-optimizer rows from runs 740-1218. All 425 reached exact final
x/z/r geometry in the tested bounded synthetic setting; 266 cleared the strict
base radius-confidence margin and 159 remained weak-but-exact.

The current synthetic decision point is not "run more GPUs". The target1
confidence-policy synthesis supports stopping blind source-density escalation
after 9 sources and, if explicitly approved, using exactly one narrow
Tx/Rx=52.5 mm probe for the current target1 weak-but-exact branch. That
synthetic policy remains separate from this 3D plan.

### Field Data

The local field dataset is in a separate dataset-local stream:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09
docs/field_experiments/local_gssi_51600s_2026_06_09
```

Four GSSI DZT/DZX profiles were imported and QC'd. They are useful for parser,
metadata, preprocessing, hyperbola, and common-offset calibration work, but they
are not sufficient for a defensible 3D FWI claim yet.

Known field constraints:

- No DZG/GPS/position sidecar was found.
- No complete 2D/3D survey layout is available.
- No independent as-built rebar geometry, cover, diameter, spacing, slab
  thickness, or material dielectric is confirmed.
- The short profiles 014 and 016 show strong shallow, repeated hyperbola-like
  events, but the velocity/depth calibration is unstable.
- Field run 004 selected a 60 mm effective Tx/Rx offset as a useful hypothesis,
  while producing implausibly shallow absolute depths in at least one profile.

Field data should therefore guide calibration priorities and future acquisition
requirements. It should not be folded into synthetic experiment trackers or
used as a 3D FWI validation target until geometry and ground-truth constraints
improve.

## Publication Framing from the Paper Corpus

The 3D program should not claim that GPR rebar detection, rebar sizing, or GPR
FWI for reinforced concrete is new. The local paper corpus and external checks
show mature prior work in:

- common-offset GPR FWI for rebar mapping and diameter estimation;
- hyperbola detection, theoretical-database matching, and ray/migration methods;
- MIMO/array GPR approaches for improved resolution and diameter estimation;
- inverse-scattering candidate localization for metallic bars in dielectrics;
- CNN/YOLO-style detection and 3D learned inversion from C-scan volumes;
- source-wavelet estimation, convolutional/source-independent objectives,
  progressive bandwidth, WRI, and optimal-transport FWI variants.

The defensible contribution is narrower and sharper:

```text
acquisition-aware 3D identifiability of closely spaced multi-rebar geometry,
reported with top-k competing branches, confidence margins, ambiguity intervals,
source/nuisance sensitivity, and clear unresolved labels.
```

The existing 2D archive is valuable because it already established the mechanics
of this claim: rank-1 truth selection, weak-but-exact branches, objective-variant
diagnostics, source-profile nuisance fitting, guarded local polish, and
target-specific acquisition policy. The 3D work should test which parts survive
when the problem includes finite bar length, crossed bars, crossline scattering,
full C-scan acquisition, and 3D Tx/Rx geometry.

Strong publishable angles to prioritize:

1. 2D-to-3D failure map: when long-bar 2D assumptions break under finite length,
   oblique/crossed bars, crossline scattering, or line-spacing changes.
2. Acquisition-design study: how scan direction, C-scan line spacing, Tx/Rx
   offset, source count/profile, frequency band, and noise affect the margin
   between true geometry and near-best wrong branches.
3. Confidence calibration: explicit labels for exact-clean, exact-weak,
   wrong-but-close, unresolved, and physically indistinguishable cases.
4. Parameterized 3D inversion before voxel FWI: show whether low-dimensional
   bar geometry can be recovered with interpretable margins before moving to
   full-volume inversion.
5. Baseline comparison: compare against at least simple hyperbola/migration or
   database-style baselines, plus a neural inversion baseline if 3DInvNet can be
   run cleanly.

Weak novelty claims to avoid:

- "FWI estimates rebar radius" without ambiguity and prior-art context.
- "3D simulation of rebars" without an inversion or acquisition-design question.
- "Deep learning reconstructs a 3D volume" without domain transfer,
  interpretability, and comparison to candidate-geometry margins.
- "Field-data validation" from the local GSSI profiles before independent
  geometry and survey layout are known.

Minimum paper-grade evidence should include:

- one-rebar, two-rebar, three-rebar, and crossed-grid synthetic scenes;
- isolated, moderate, close, and near-failure spacings;
- same-depth and variable-depth cases;
- same-radius and variable-radius cases;
- matched source, time-zero mismatch, amplitude mismatch, and ringdown mismatch;
- zero, moderate, and near-failure noise;
- top-k candidate tables, margin intervals, and unresolved flags, not only point
  estimates.

The first 3D paper should be framed as a controlled benchmark and acquisition
policy study. A later paper can pursue neural surrogates, voxel FWI, or real
field validation after stronger data and baselines exist.

## Neural-Network Paper Audit

The added `paper/neural_network` papers sharpen the baseline strategy.

### AlexNet Rebar Detection Paper

Xiang et al. use AlexNet to classify segmented GPR image windows into rebar
signature classes. Their testbed uses real StructureScan Mini XT data from a
column, shear wall, and slab, with 48 images split into smaller windows. The
best reported window setting reaches 94.51 percent accuracy, while dense and
uneven rebar arrangements remain harder because adjacent rebar signatures
interfere. The paper is useful as evidence that CNN-based rebar detection is
prior art, and as a simple classification baseline. It does not estimate x/z/r
with confidence margins; the authors explicitly leave size/depth recognition
for future work.

Planning consequence:

- Do not claim novelty for CNN recognition of rebar signatures.
- Use simple detector accuracy only as a front-end cue or baseline, not as a
  substitute for geometry identifiability.
- Dense/uneven layouts in that paper support making close-spacing and
  crossed-grid ambiguity a central experiment axis.

### Faster R-CNN + DCSE Hyperbola Detection Paper

Lei et al. propose a more directly useful B-scan pipeline: Faster R-CNN finds
candidate hyperbola regions, DCSE separates point clusters, CTFP extracts
fitting points, and a hyperbola fit estimates peaks. Their training data combine
gprMax synthetic B-scans and on-site data, expanded from 838 images to 5866
through augmentation. Their on-site highway data use a 400 MHz antenna with
16 cm Tx/Rx offset, and they report overall recall near 97.74 percent and
precision near 95.66 percent for rebar peak localization.

Planning consequence:

- Treat this as the strongest immediate classical/ML B-scan baseline for 2D and
  early 3D C-scan slice analysis.
- In the 3D plan, a detector-to-FWI workflow should compare our candidate
  initialization against a Faster R-CNN/DCSE-style hyperbola baseline.
- The baseline estimates peaks and localizes hyperbolas, but it does not report
  top-k physical geometry branches, radius ambiguity intervals, or acquisition
  policy margins.

### Deep-Learning 2D Forward-Solver Paper

Dai et al. train a bimodal encoder-decoder network to predict B-scans from 2D
permittivity and conductivity maps. Their gprMax-generated dataset uses a
1.5 m x 0.5 m domain, 2.5 mm pixels, a 1 GHz source, and common-offset scanning.
They report 1.28 percent mean relative error on regular tests and 12 ms
prediction time versus 4.5 minutes for one FDTD B-scan on the same GPU. Transfer
learning improves new soil and antenna scenarios, but the paper reports degraded
accuracy for multiple-object and concave-object cases.

Planning consequence:

- This is a future surrogate/candidate-screening idea, not an immediate
  replacement for FDTD verification.
- A paper-grade surrogate branch must quantify where speedups preserve or
  destroy rank ordering among near-best candidate geometries.
- Multiple-object degradation is directly relevant to close rebar ambiguity, so
  any surrogate must be tested on the same top-k competitor sets.

### 3DInvNet Paper

Dai et al.'s 3DInvNet reconstructs 3D permittivity maps from GPR C-scans using a
Denoiser plus Inverter architecture. The synthetic setup uses gprMax over a
1 m x 1 m x 0.26 m soil volume, 2.5 mm spacing, 1 GHz Ricker source, 10 cm
source-receiver offset, and 12 scan lines with 10 points per line. The workflow
uses 5850 synthetic training sets plus 150 tests for the initial dataset, then
285 fine-tuning sets plus 15 tests for harder heterogeneous cases. It resizes
C-scans and permittivity maps to 128 x 128 x 128 and runs in PyTorch. The real
measurement section uses a commercial GSSI 400 MHz system, a 1 m x 1 m scan
area, 21 B-scans, 5 cm line spacing, 88 A-scans per B-scan, 512 samples per
A-scan, and 220 measured sets.

The paper is highly relevant because it directly argues that 2D modeling misses
3D effects and demonstrates C-scan-to-volume inversion. Its limitations are also
important: supervised learning needs large datasets, down-sampled training data
can produce inaccurate mappings, strongly out-of-domain cases require
substantial retraining, hyperparameters are trial-driven, and tentative average
soil permittivity is needed for fine-tuning.

Planning consequence:

- 3DInvNet is a credible 3D learned-inversion baseline or scouting branch.
- It should not replace the parametric confidence workflow unless we add a
  bridge from predicted permittivity volumes to x/y/z/r/spacing and top-k
  ambiguity labels.
- Its C-scan acquisition design gives a useful starting point for the first
  NERSC C-scan scenes: 1 m square is too expensive for first smoke tests, but
  10 cm offset, 5 cm line spacing, and 128-cube network sizing are concrete
  reference points.
- A fair comparison should include touching/near-touching objects because that
  is where their real-data section reports more difficult interleaved patterns.

### Code Capability Baseline

The current implementation is 2D TMz, not 3D:

- `config.py` defines an x-z domain only.
- `core/fdtd.py` evolves `Ez`, `Hx`, and `Hy` arrays with shape `(Nz, Nx)`.
- `gpu/fdtd_gpu_v2.py` batches 2D CPML simulations over scan positions with
  arrays shaped like `(batch_size, Nz, Nx)`.
- `gpu/cpml_gpu.py` is 2D x-z CPML.
- `core/materials.py`, `core/geometry.py`, and `core/scan.py` build 2D
  concrete/rebar cross-sections and surface scan lines.
- `inversion/inversion_engine.py` and `inversion/regularization.py` are 2D
  pixel-inversion utilities.
- `run_multi_rebar_coordinate_optimizer.py` is the mature 2D bounded
  coordinate/radius optimizer and reporting path.

Reusable 2D assets for 3D:

- Experiment allocation and run manifests in `core/run_outputs.py`.
- Source-profile nuisance fitting in `inversion/source_profile.py`.
- Candidate-confidence and margin policy in `inversion/candidate_confidence.py`.
- Coordinate-optimizer reporting conventions.
- Figure notes and marker-section style from the figure inventory.
- Synthetic archive governance and skip-existing backfill discipline.

Non-reusable or requiring new implementations:

- 3D Maxwell update equations.
- 3D Yee grid material placement.
- 3D CPML on six faces, edges, and corners.
- 3D source/receiver and antenna footprint model.
- 3D scan grids, B-scan/C-scan extraction, and volume I/O.
- 3D adjoint/checkpointing if voxel FWI is attempted.
- Multi-GPU domain decomposition and halo exchange.
- Slurm/HPC job scripts and storage policy.

## Figure and Artifact Policy for Future 3D Work

The existing figure policy should be extended, not bypassed. For any compatible
future 3D experiment, preserve old outputs and use skip-existing generation
first. Do not overwrite figures unless a tracker explicitly records why.

Recommended core artifacts for each 3D run:

```text
run_manifest.json
README.md
data/experiment_config.json
data/runtime_memory_summary.json
data/receiver_traces.h5 or data/receiver_traces.npz
figures/acquisition_layout_3d.png
figures/scene_geometry_3d_overview.png
figures/scene_geometry_slices.png
figures/source_pulse_context.png
figures/bscan_cscan_summary.png
figures/FIGURE_NOTES.md
```

Additional core artifacts for 3D inversion or candidate-search runs:

```text
data/candidate_summary.csv
data/objective_variant_summary.csv
data/rank1_candidate_summary.csv
data/confidence_policy_summary.json
figures/coordinate_radius_decision_panel.png
figures/objective_candidate_cloud.png
figures/confidence_margin_panel.png
```

Additional core artifacts for HPC scaling runs:

```text
data/scaling_summary.csv
data/node_gpu_inventory.json
figures/runtime_memory_scaling.png
figures/throughput_per_gpu.png
```

Optional and selective artifacts only:

```text
figures/fdtd_wavefield_slice_animation.gif
figures/volume_snapshot_panel.png
figures/volume_render_preview.mp4
```

Rules for expensive visual media:

- Do not create full-volume animations for every run.
- Prefer still slice panels for auditability.
- Use animations only for selected validation examples, solver demos, and
  decision-critical failures.
- Always update `FIGURE_NOTES.md` so a later audit can distinguish geometry,
  acquisition, waveform, confidence, and performance figures.

Recommended 3D-specific marker sections for `FIGURE_NOTES.md`:

```text
<!-- acquisition_layout_3d:start -->
<!-- acquisition_layout_3d:end -->
<!-- scene_geometry_3d:start -->
<!-- scene_geometry_3d:end -->
<!-- bscan_cscan_summary:start -->
<!-- bscan_cscan_summary:end -->
<!-- fdtd_wavefield_3d:start -->
<!-- fdtd_wavefield_3d:end -->
<!-- hpc_scaling:start -->
<!-- hpc_scaling:end -->
```

## Archive Governance for 3D

Do not mix early 3D prototypes into the mature 2D synthetic archive. The 2D
tracker root remains `docs/experiments`; the 3D tracker root is
`docs/3d_experiments`. This `initial_plan` subdirectory is for planning material
that can be copied to NERSC before any experiment is launched.

Recommended roots:

```text
docs/3d_experiments/NNN_run_name.md
outputs/3d_experiments/NNN_run_name
```

Rationale:

- `outputs/experiments` is a large, mature 2D synthetic archive.
- `docs/experiments` is the 2D tracker sequence and should not receive 3D plan
  or 3D HPC tracker IDs.
- `outputs/field_experiments` already separates field/lab datasets.
- 3D development will initially contain solver validation, failed prototypes,
  memory benchmarks, and HPC scaling records that should not be counted as 2D
  coordinate-optimizer evidence.

Suggested 3D tracker numbering starts at `001` inside `docs/3d_experiments`;
those IDs are local to the 3D stream and do not consume 2D tracker IDs. On the
HPC copy of this repo, keep the same `docs/3d_experiments` structure and write
large run products under `outputs/3d_experiments`, which should stay local to
the machine unless explicitly archived.

## A100 and HPC Assumptions

Confirm the actual NERSC account, queue, filesystem, and module environment
before writing production scripts. NERSC Perlmutter GPU nodes are the primary
target: the NERSC architecture documentation describes GPU nodes with four
NVIDIA A100 GPUs and an AMD EPYC CPU. NERSC also documents Slurm use with the
GPU constraint, and 80GB A100 nodes can be selected with a site-specific
constraint such as `-C "gpu&hbm80g"` when available and justified.

General A100 details still matter. A100 appears in 40GB and 80GB variants, PCIe
and SXM form factors, and different node/network topologies. The official
NVIDIA datasheet reports high memory bandwidth and FP64 capability, but this
plan should rely on NERSC discovery commands for the actual node allocated to a
job.

Required HPC discovery commands:

```bash
nvidia-smi -L
nvidia-smi --query-gpu=name,memory.total,driver_version,pci.bus_id --format=csv
nvidia-smi topo -m
module avail cuda
module avail nccl
module avail openmpi
scontrol show nodes
sinfo -o "%P %D %G %m %f"
```

Required cluster questions:

- Which NERSC project/account should be charged with `#SBATCH -A`?
- Are allocated A100 GPUs 40GB or 80GB?
- Is the job on standard GPU nodes or explicitly requested `gpu&hbm80g` nodes?
- Which filesystem should hold short-lived output: `$SCRATCH`, `$PSCRATCH`, or a
  project directory?
- What are the limits for QOS, walltime, job arrays, and charging factors?
- Are MIG slices enabled or disabled by default?
- Are CUDA-aware MPI and NCCL installed and supported?
- Are long-running jobs preemptible?

NERSC and Slurm documentation should govern the final job syntax. Treat every
example script in this plan as a template that must be adapted to actual NERSC
account, QOS, module, filesystem, and allocation policy.

## Local DGX vs NERSC Work Split

Keep the local DGX Spark/GB10 stream and the NERSC A100 stream separate.

Local DGX Spark work should prioritize:

- finishing the 2D target1 confidence-policy synthesis without broad GPU runs;
- skip-existing figure/table backfills for existing 2D artifacts;
- CPU-side summary, branch labeling, and policy documentation;
- local field-data QC, metadata extraction, preprocessing, and hyperbola cues;
- small 3D budget calculations, unit tests, and tiny CPU reference cases.

NERSC A100 work should prioritize:

- Phase 0 cluster readiness and environment validation;
- tiny 3D CPU/GPU parity cases;
- one short single-GPU forward run at a time;
- small job arrays only after single-case correctness is proven;
- 3DInvNet/code-data smoke tests if licensing and dependencies are clean;
- no broad synthetic matrix until budget, parity, and publication question pass.

The two streams should exchange documents, not raw experiment folders by default.
Copy `docs/3d_experiments` to the HPC repo so the NERSC agent has the same plan.
Keep heavy products in the machine-local output root until selected artifacts are
curated for archive.

## 3D Memory and Runtime Budget

3D FDTD is memory-bandwidth dominated and grows quickly. The full 3D Yee update
needs six field components:

```text
Ex, Ey, Ez, Hx, Hy, Hz
```

For equal spatial steps, the 3D CFL limit is:

```text
dt <= dx / (c * sqrt(3))
```

With Courant factor 0.9, example single-GPU memory estimates are:

| Case | Physical domain before PML | dx | PML | Grid incl. PML | Cells | dt ps | Nt for 8 ns | 6 fields f32 | 1 scalar saved all time f32 | 6 fields saved all time f32 |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| coarse single A100 | 0.50 x 0.30 x 0.30 m | 2.0 mm | 15 | 280 x 180 x 180 | 9.07M | 3.466 | 2308 | 0.203 GiB | 78.0 GiB | 468.0 GiB |
| medium single A100 | 0.50 x 0.30 x 0.25 m | 1.5 mm | 20 | 374 x 240 x 207 | 18.58M | 2.600 | 3078 | 0.415 GiB | 213.1 GiB | 1278.3 GiB |
| fine warning case | 0.50 x 0.30 x 0.25 m | 1.0 mm | 30 | 560 x 360 x 310 | 62.50M | 1.733 | 4616 | 1.397 GiB | 1074.7 GiB | 6448.1 GiB |
| larger field patch | 0.90 x 0.60 x 0.30 m | 2.0 mm | 15 | 480 x 330 x 180 | 28.51M | 3.466 | 2308 | 0.637 GiB | 245.1 GiB | 1470.9 GiB |

Interpretation:

- Resident forward fields are not the main problem by themselves.
- Coefficients, material arrays, CPML auxiliary arrays, temporaries, source
  state, receiver buffers, and diagnostics can multiply resident memory by
  several times.
- Storing all forward fields for adjoint inversion is not viable for realistic
  3D. Even one scalar field at all time steps can exceed a 40GB A100 for modest
  domains.
- 3D adjoint or voxel FWI will require checkpointing, recomputation, boundary
  saving, compression, or a different inversion strategy.

Practical memory rules:

- Keep initial single-GPU resident memory below 25 GB on 40GB A100 nodes and
  below 50 GB on 80GB nodes.
- Use `float32` for production forward runs after parity tests; keep `float64`
  reference tests on tiny domains.
- Do not save full fields by default. Save receiver traces, sparse snapshot
  panels, and selected validation slices.
- Write a budget estimate before every 3D job and store it in
  `data/runtime_memory_summary.json`.

## Implementation Strategy

### Solver Direction

Do not patch 3D into `core/fdtd.py` or `gpu/fdtd_gpu_v2.py` in place. Preserve
the 2D solver and add new modules so the current archive remains reproducible.

Proposed module layout:

```text
core3d/
  config3d.py
  materials3d.py
  geometry3d.py
  scan3d.py
  fdtd3d_reference.py
gpu3d/
  fdtd3d_gpu.py
  cpml3d_gpu.py
  kernels.py
inversion3d/
  coordinate_search3d.py
  confidence3d.py
  checkpointing.py
run_3d_forward.py
run_3d_coordinate_optimizer.py
run_3d_hpc_scaling.py
tools/estimate_3d_fdtd_budget.py
```

The CPU reference can be slow because it is for correctness only. The GPU
solver should use fused kernels or carefully controlled CuPy kernels to avoid
large temporary arrays. The current 2D CuPy style is useful for readability, but
3D production will likely need lower-level CUDA/CuPy RawKernel style updates to
control memory bandwidth and temporary allocation.

### Physics Scope

The first 3D forward solver should implement:

- Cartesian Yee grid.
- Six field components.
- Non-dispersive epsilon/sigma materials.
- PEC masks for metallic rebars.
- Simple point or small dipole source.
- Monostatic and bistatic receiver sampling.
- Six-face CPML or a deliberately documented first absorbing-boundary
  approximation for smoke tests only.

Do not start with:

- Full realistic commercial antenna CAD.
- Dispersive concrete.
- Rough surfaces.
- Corrosion, chlorides, moisture gradients, or rebar ribs.
- Voxel FWI over all permittivity cells.
- Multi-node MPI.

Those can be staged after the solver passes the core tests.

### Material and Geometry Model

Minimum useful 3D geometry features:

- Air/concrete half-space or slab.
- Finite cylindrical PEC rebars along x or y.
- Crossed rebar grids.
- Variable cover depth, radius, spacing, and bar length.
- Optional homogeneous conductivity.
- Optional surface layer or thin air gap.

Important numerical issue: staircasing of small radii becomes severe at coarse
grid spacing. A 6 mm radius target at 2 mm grid spacing has only 3 cells per
radius. Use this only for early feasibility. For radius-confidence claims,
compare 2 mm, 1.5 mm, and 1 mm grids on at least a small domain before
interpreting radius margins.

### Source and Receiver Model

The field QC currently suggests a 60 mm effective Tx/Rx offset for the local
GSSI 51600S data, but that is a hypothesis, not confirmed antenna geometry.

3D synthetic work should therefore start with explicit source models:

- `point_ez` or `point_current_z` for parity with 2D intuition.
- `short_dipole_x` or `short_dipole_y` for polarization studies.
- Bistatic source/receiver offsets of 0, 40, 60, 80, and 100 mm.
- Time-zero and ringdown nuisance parameters stored separately from geometry.

Only after this works should the project consider a calibrated 51600S antenna
model or external solver comparison.

### Inversion Direction

Start with 3D parameter inversion, not voxel FWI:

- Single-bar centerline position, cover depth, radius, and orientation.
- Three-bar or small-grid coordinate/radius inversion.
- Concrete epsilon and source/time-zero nuisance parameters.
- Bounded candidate grids and local refinement.
- Confidence margins based on top candidate separation, adapted from the 2D
  coordinate optimizer.

Voxel FWI should be deferred until:

- Forward solver correctness is proven.
- Checkpointing is implemented.
- 3D synthetic coordinate inversion exposes a question that parameter inversion
  cannot answer.
- The field-data geometry is good enough to justify it.

## Validation Ladder

Each phase must leave a small, reproducible artifact and a tracker note.

### Phase 0: HPC Readiness

Purpose: confirm the cluster can support controlled 3D development.

Deliverables:

- `docs/3d_experiments/001_hpc_readiness.md`
- `outputs/3d_experiments/001_hpc_readiness/data/node_gpu_inventory.json`
- Cluster module and Slurm notes.
- Environment lock or container decision.

Stop criteria:

- Do not proceed to production if A100 memory size, GPU request syntax, scratch
  policy, or driver/CUDA compatibility is unknown.

### Phase 1: 3D Budget Planner

Purpose: estimate grid, CFL, memory, output size, and runtime before allocating
expensive jobs.

Deliverables:

- `tools/estimate_3d_fdtd_budget.py`
- Unit tests for memory/CFL calculations.
- Saved budget JSON for every proposed run.

Acceptance:

- Budget tool reproduces known 2D scaling order and the example 3D estimates in
  this plan.
- It warns when full time-field storage exceeds available GPU memory.

### Phase 2: Tiny CPU Reference Solver

Purpose: establish correctness independent of GPU optimization.

Experiments:

- Vacuum propagation smoke test.
- Homogeneous concrete propagation speed test.
- PEC reflection from a plane or cylinder on a tiny grid.
- CFL stability/instability bracket.

Acceptance:

- Energy remains bounded under stable CFL.
- Travel times match expected velocity within documented grid error.
- PEC mask produces a clear reflection.
- Tests run in CI without GPU.

### Phase 3: Single-GPU 3D Forward Kernel

Purpose: run the validated equations on one A100.

Experiments:

- Same smoke tests as Phase 2.
- Compare CPU and GPU on tiny domains.
- Measure throughput in cells-step/s.
- Confirm no hidden host-device synchronization inside the time loop.

Acceptance:

- CPU/GPU traces agree within tolerance on tiny grids.
- Memory stays inside the budget estimate.
- The code emits runtime/memory summaries and minimal figures.

### Phase 4: 3D Synthetic GPR Forward Scenes

Purpose: create interpretable 3D B-scan/C-scan evidence before inversion.

Initial scenes:

1. Homogeneous concrete with one long PEC cylinder perpendicular to the scan.
2. Same cylinder with finite length to expose out-of-plane effects.
3. Three parallel rebars with the existing 2D truth geometry lifted into 3D.
4. Crossed grid of rebars.
5. Offset/polarization sweep over 0, 40, 60, 80, and 100 mm Tx/Rx.

Acceptance:

- B-scan hyperbolas are visually and numerically sensible.
- Long-cylinder central slices approximate the 2D solver trend where expected.
- Finite-length and crossed-grid scenes show clear differences from 2D.
- Figures and `FIGURE_NOTES.md` are complete.

### Phase 5: Multi-GPU and HPC Scaling

Purpose: scale only after the single-GPU solver is trusted.

Path:

- Begin with embarrassingly parallel job arrays over candidate geometries.
- Use one GPU per candidate before building domain decomposition.
- Add multi-GPU domain decomposition only when a single candidate no longer fits
  or runtime blocks the science.

Domain decomposition requirements:

- Halo exchange for field components across subdomain boundaries.
- CPML only on global outer boundaries, not internal halos.
- Reproducible single-GPU vs multi-GPU parity on small grids.
- NCCL or CUDA-aware MPI decision documented from actual cluster support.

Acceptance:

- Strong/weak scaling tables show real benefit over job arrays.
- Communication overhead is measured, not assumed.
- Multi-GPU parity tests pass before production science.

### Phase 6: 3D Coordinate/Radius Inversion

Purpose: lift the strongest 2D result into a 3D parameterized inverse problem.

Initial inversion sequence:

1. One known synthetic bar, fixed epsilon and source.
2. One bar with epsilon/time-zero nuisance fitting.
3. One bar with Tx/Rx offset uncertainty.
4. Three parallel bars matching the 2D truth.
5. Crossed-grid bars with known truth.

Acceptance:

- Exact geometry is recovered in clean synthetic cases.
- Confidence margins are reported using a documented 3D policy.
- Weak-but-exact cases are not relabeled as accepted.
- Objective variants are recorded for every decision-critical branch.

### Phase 7: Field Bridge

Purpose: use local field data to constrain hypotheses without overstating
claims.

Allowed uses of the local GSSI field dataset:

- Parser validation.
- Time axis, trace spacing, and profile metadata checks.
- Preprocessing and hyperbola cue comparison.
- Common-offset sensitivity comparison.
- Synthetic overlay against short profiles 014 and 016 as a calibration
  exercise.

Not allowed yet:

- Full 3D field FWI.
- Radius/cover claims from local data alone.
- Treating local profiles as a known 3D survey volume.
- Mixing field-data outputs into synthetic experiment trackers.

Field prerequisites before real 3D inversion:

- Profile layout with line order, direction, spacing, start/end coordinates.
- Antenna Tx/Rx offset, polarization, and time-zero convention.
- Independent cover depth, bar spacing, bar diameter, slab thickness, and
  material constraints.
- A repeatable raw/minimally processed/analysis-ready data split.

### Phase 8: Production A100 Experiment Matrix

Purpose: run a narrow, scientifically motivated matrix after all earlier phases
pass.

Candidate matrix:

| Family | Variables | Why it matters |
| --- | --- | --- |
| Grid resolution | 2.0, 1.5, 1.0 mm on small domains | Quantifies radius staircasing and convergence |
| Tx/Rx offset | 0, 40, 60, 80, 100 mm | Bridges synthetic policy and field offset hypothesis |
| Source model | point, dipole, fitted ringdown | Tests waveform nuisance transfer |
| Bar geometry | infinite-like, finite, crossed grid | Establishes when 2D breaks |
| Noise/ringdown | current 2D stress patterns | Compares confidence policy to 2D archive |
| Objective variants | base, early/late, source-profiled | Preserves rank/confidence reporting discipline |

Production stop rules:

- Stop if exact geometry fails in clean one-bar synthetic cases.
- Stop if grid convergence changes radius decision labels.
- Stop if multi-GPU parity fails.
- Stop if the field-data hypothesis depends on unknown survey geometry.
- Stop if runtime/memory exceeds budget by more than 25 percent without a clear
  explanation.

## 3DInvNet and Neural-Network Scout Path

3DInvNet is relevant but not plug-and-play for this project. The paper describes
a two-stage learned inversion pipeline for reconstructing 3D permittivity volumes
from GPR C-scans: a denoising network followed by a U-shaped 3D inverter with
multiscale feature aggregation. The published workflow uses gprMax-generated
3D C-scan/permittivity-map pairs, resized 128 x 128 x 128 volumes, staged
training, and PyTorch. The GitHub repository provides code and dataset links,
but license, dependency, and data-access details must be verified before any
integration.

Potential value for this project:

- baseline: compare learned 3D volume inversion against parameterized
  top-k geometry inversion on the same synthetic scenes;
- scout: identify whether C-scan volumes carry enough information for finite
  length, crossed-grid, and close-spacing ambiguity questions;
- denoising/surrogate: later assist with preprocessing or candidate proposal;
- negative result: document where supervised volume inversion fails under source
  mismatch, unseen geometries, or close-spacing ambiguity.

Limits:

- 3DInvNet outputs permittivity volumes, not direct x/y/z/r/top-k candidate
  margins.
- Domain transfer from published synthetic/real data to this rebar geometry is
  unknown.
- A neural result without ambiguity labels does not answer the core
  identifiability question.
- Training a large model should not happen before small inference and tiny-data
  smoke tests prove the workflow is usable on NERSC.

Recommended neural scout phases:

### NN-0: License, Data, and Environment Audit

- Record repository license status, dataset access, expected disk size, and
  package requirements.
- Run only import/tests or dry-run scripts.
- Save notes in `docs/3d_experiments/nn_000_3dinvnet_audit.md`.

### NN-1: Provided Example or Tiny Synthetic Smoke

- If pretrained weights and a small example are available, run inference only.
- If not, train a deliberately tiny synthetic subset for a few iterations to
  validate I/O, GPU memory, and tensor shapes.
- Write outputs under `outputs/3d_experiments/nn_001_3dinvnet_smoke`.
- Stop if the workflow needs large downloads, long training, or unclear license
  decisions before the audit is complete.

### NN-2: Geometry Extraction Bridge

- Convert predicted permittivity volumes into bar centerline, cover, radius,
  spacing, and orientation estimates.
- Compare those estimates with the parameterized candidate-search top-k table.
- Record whether the volume prediction supports, contradicts, or obscures the
  ambiguity-margin decision.

### NN-3: Paper Baseline Decision

Include 3DInvNet in a paper only if it provides one of these:

- a fair baseline on the same synthetic C-scan scenes;
- a learned denoising/proposal stage that improves a documented metric;
- a useful failure-mode comparison showing why explicit confidence margins are
  needed.

Do not let neural-network work displace the first 3D FDTD parity and
parameterized inversion ladder. It is a parallel scout branch, not the main
scientific core yet.

## First Concrete 3D Experiment Set

These are proposed future runs, not commands executed now.

### 3D-001: HPC Readiness

Goal: validate NERSC account, filesystem, module, CUDA/CuPy, Slurm, and GPU
allocation details before any science run.

Outputs:

```text
docs/3d_experiments/001_hpc_readiness.md
outputs/3d_experiments/001_hpc_readiness/data/node_gpu_inventory.json
```

### 3D-002: Budget and CFL Smoke

Goal: produce a no-FDTD budget report for candidate domains.

Outputs:

```text
outputs/3d_experiments/002_budget_cfl_smoke/data/budget_cases.csv
outputs/3d_experiments/002_budget_cfl_smoke/data/budget_cases.json
docs/3d_experiments/002_budget_cfl_smoke.md
```

### 3D-003: CPU Vacuum Reference

Goal: validate 3D CFL, propagation, and receiver sampling on a tiny grid.

No GPU required.

### 3D-004: GPU Vacuum and Homogeneous Concrete Parity

Goal: compare CPU and A100 traces on tiny domains.

Slurm template:

```bash
#!/bin/bash
#SBATCH --job-name=gpr3d_004
#SBATCH -A <nersc_project>
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 1
#SBATCH --gpus=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=00:30:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail
module load python
conda activate gpr-fdtd-fwi
srun -n 1 -c 32 --gpus-per-task=1 python run_3d_forward.py \
  --case homogeneous_concrete_parity \
  --backend gpu \
  --outdir outputs/3d_experiments/004_gpu_homogeneous_parity
```

Adapt the account, QOS, environment setup, and filesystem to the actual NERSC
allocation. For an 80GB A100 request, use the documented NERSC constraint form,
for example `#SBATCH -C "gpu&hbm80g"`, only when the memory budget proves it is
needed. Do not run this before 3D-001 and 3D-002 have tracker notes.

### 3D-005: Single Long Rebar Forward

Goal: generate a 3D B-scan for a long PEC cylinder and compare its central
profile with the 2D synthetic intuition.

Core figures:

```text
scene_geometry_3d_overview.png
scene_geometry_slices.png
acquisition_layout_3d.png
bscan_cscan_summary.png
```

### 3D-006: Finite-Length Rebar and Crossline Sensitivity

Goal: quantify when 2D assumptions fail because of finite bar length or
off-profile scattering.

### 3D-007: Three Parallel Bars with 2D Truth Lifted to 3D

Goal: reproduce the known 2D target geometry in a 3D scene and measure whether
the same acquisition concepts preserve rank-1 exact geometry.

### 3D-008: One-Bar Coordinate/Radius Inversion

Goal: first 3D parameter inversion with truth known.

Decision rule:

- Exact x/y/z/r accepted only if base margin clears the documented 3D cutoff.
- Exact geometry with weak radius margin remains weak-but-exact.

### 3D-009: Crossed-Grid Coordinate/Radius Inversion

Goal: test the first scene where 2D cross-sections are structurally inadequate.

This run should not happen until 3D-008 is stable.

## Data Format Plan

For 3D, raw arrays must not be casual `.npy` dumps with undocumented axes.

Recommended layout:

```text
data/
  experiment_config.json
  runtime_memory_summary.json
  receiver_traces.h5
    /traces/amplitude[shot, receiver, time]
    /axes/time_s[time]
    /axes/source_xyz_m[shot, 3]
    /axes/receiver_xyz_m[receiver, 3]
    /geometry/material_summary
    /processing_log
  sparse_snapshots.h5
    /Ez[t_index, z, y, x] or selected slices only
```

h5py/HDF5 chunking and compression are appropriate for large datasets, but the
dependency is not currently in `environment.yml`. Add it only when the first 3D
I/O implementation needs chunked/resizable arrays. Until then, use compact
`.npz` for small validation traces and JSON/CSV for summaries.

## Environment Plan

The local conda environment `gpr-fdtd-fwi` currently validates the 2D project
and has CuPy 14.0.1 with CUDA runtime 12090 on lam002. Do not assume the HPC
cluster can reproduce Python 3.13 and the same CUDA stack without testing.

Recommended HPC path:

1. Capture current local environment:

   ```bash
   conda env export -n gpr-fdtd-fwi > environment.local-lam002-2026-06-17.yml
   ```

2. On the cluster, prefer a new reproducible environment or container:

   ```bash
   conda env create -f environment.yml
   conda activate gpr-fdtd-fwi
   python -m pytest -q
   python - <<'PY'
   import cupy as cp
   print(cp.__version__)
   print(cp.cuda.runtime.runtimeGetVersion())
   print(cp.cuda.Device(0))
   PY
   ```

3. If Python 3.13 causes solver/tooling friction on HPC, create a cluster
   environment with Python 3.11 or 3.12 and validate the full test suite before
   running any experiment.

4. Record driver, CUDA, CuPy, MPI/NCCL, Slurm, and Git commit in every 3D
   manifest.

## Research Questions

The 3D program should answer specific questions:

- When does the current 2D coordinate/radius confidence policy transfer to 3D?
- Which failures are caused by finite bar length, crossed bars, or crossline
  scattering?
- Does 60 mm effective Tx/Rx offset remain useful in 3D synthetic scenes, or
  was it a field-preprocessing artifact?
- How fine must the grid be before 6 mm and 8 mm radii have stable margins?
- Can parameterized 3D inversion recover radius without voxel FWI?
- What information does a second scan direction or dense C-scan add over a
  single B-scan?
- What field metadata is mandatory before local GSSI 51600S data can be used
  for 3D inversion?

## Risks

Major risks and controls:

| Risk | Control |
| --- | --- |
| Treating 3D as a small patch to 2D | New `core3d`/`gpu3d` modules and explicit tests |
| GPU time lost to unbudgeted memory growth | Budget JSON before every run |
| Full-field adjoint storage exceeds A100 memory | Parameter inversion first; checkpointing before voxel FWI |
| Radius claims depend on staircasing | Grid convergence at 2.0, 1.5, and 1.0 mm |
| Field-data overclaiming | Field stream remains separate; require geometry/ground truth |
| Multi-GPU complexity distracts from science | Job arrays first; domain decomposition only after need is proven |
| Figure archive becomes unauditable | Core figure list and `FIGURE_NOTES.md` markers |
| Environment drift on HPC | Manifest driver/CUDA/CuPy/commit; cluster validation before runs |

## Recommended Immediate Next Actions

Do these before any A100 production run:

1. Finish the current 2D synthetic confidence-policy decision separately:
   either stop with run 1217 as exact-but-unresolved or run one explicitly
   approved target1 Tx/Rx=52.5 probe.
2. Keep using `docs/3d_experiments` as the 3D tracker root and create
   `outputs/3d_experiments` with a README before the first 3D run.
3. Implement `tools/estimate_3d_fdtd_budget.py` and tests.
4. Draft Phase 0 HPC readiness tracker after actual cluster access details are
   known.
5. Build the tiny CPU 3D reference solver and tests.
6. Only then request a short single-A100 interactive or batch allocation for
   GPU parity.

## Bottom-Line Recommendation

The 3D A100 program is justified as a future research direction, but not as an
immediate broad GPU marathon. The current project has strong 2D synthetic
coordinate/radius evidence and early field-data QC. A defensible 3D program
should first prove a 3D forward solver, memory budgeting, figures, and
single-GPU parity, then lift the existing coordinate-confidence policy into
parameterized 3D synthetic inversions. Field data should shape calibration and
future acquisition requirements, not drive full 3D FWI until survey geometry and
ground truth are available.
