# NERSC HPC Handoff for Initial 3D Work

Date: 2026-06-17

This is a short handoff note for a Codex agent running in a NERSC/HPC checkout
of this repository. The full plan is:

```text
docs/3d_experiments/initial_plan/3d_a100_hpc_experiment_plan_2026-06-17.md
```

## Boundary Conditions

- Do not use `docs/experiments` for 3D work. That is the 2D synthetic tracker
  stream.
- Use `docs/3d_experiments` for 3D trackers and planning notes.
- Use `outputs/3d_experiments` for 3D run products.
- Keep field data under `docs/field_experiments` and `outputs/field_experiments`.
- Do not launch broad 3D sweeps, broad neural-network training, or full-matrix
  A100 jobs before readiness and budget checks pass.
- The first publication target is a controlled 3D identifiability and
  acquisition-design study, not a generic "we detect rebars" claim.

## Start Here on NERSC

1. Confirm repo and branch:

   ```bash
   pwd
   git status --short --branch
   git remote -v
   ```

2. Confirm node, GPU, CUDA, and Slurm conventions:

   ```bash
   nvidia-smi -L
   nvidia-smi --query-gpu=name,memory.total,driver_version,pci.bus_id --format=csv
   nvidia-smi topo -m
   module avail cuda
   module avail python
   sinfo -o "%P %D %G %m %f"
   ```

3. Create the first 3D tracker only after collecting actual NERSC details:

   ```text
   docs/3d_experiments/001_hpc_readiness.md
   outputs/3d_experiments/001_hpc_readiness/data/node_gpu_inventory.json
   ```

4. Validate the Python environment before any experiment:

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

If the existing environment does not build cleanly on NERSC, document the issue
in `001_hpc_readiness.md` and create a cluster-specific environment only after
recording the exact Python/CUDA/CuPy choices.

## First Allowed Work Items

### 3D-001: HPC Readiness

Goal: collect NERSC account, QOS, filesystem, module, Slurm, CUDA, GPU memory,
and CuPy compatibility facts.

This step is documentation and environment validation only.

### 3D-002: Budget and CFL Smoke

Goal: implement or run a no-FDTD budget calculator for candidate 3D domains.

Expected future outputs:

```text
docs/3d_experiments/002_budget_cfl_smoke.md
outputs/3d_experiments/002_budget_cfl_smoke/data/budget_cases.csv
outputs/3d_experiments/002_budget_cfl_smoke/data/budget_cases.json
```

### NN-0: 3DInvNet Audit

Goal: inspect the 3DInvNet code/data/license/dependencies and decide whether it
is usable as a baseline or scout branch.

Expected future tracker:

```text
docs/3d_experiments/nn_000_3dinvnet_audit.md
```

Do not train a large model in NN-0. Run only import checks, dry runs, metadata
inspection, and very small examples if they are already available.

## First GPU Job Shape

Use a short single-node, single-GPU job only after 3D-001 and 3D-002 exist.
Adapt account, QOS, module, and filesystem details to the real allocation.

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

Use `#SBATCH -C "gpu&hbm80g"` only if the budget note proves 80GB memory is
needed.

## Paper Framing to Preserve

Do not frame the work as first rebar detection, first rebar sizing, or first
GPR neural inversion. Those claims are not credible given the local literature
and neural-network paper set.

The stronger claim is:

```text
controlled acquisition-aware 3D identifiability of close multi-rebar geometry,
with top-k competing branches, confidence margins, ambiguity intervals, and
explicit unresolved labels.
```

Useful comparison branches:

- Faster R-CNN/DCSE-style B-scan hyperbola detection as a detector baseline.
- 3DInvNet as a C-scan-to-volume learned inversion baseline if it can be run
  cleanly and fairly.
- A learned forward-solver/surrogate only after it preserves candidate ranking
  among near-best geometries.

## Stop Conditions

Stop and document before spending A100 time if any of these happen:

- NERSC account, QOS, GPU constraint, or filesystem policy is unclear.
- CUDA/CuPy compatibility is not validated.
- No budget estimate exists for the proposed 3D domain.
- The job would write full 3D fields for all time steps by default.
- The proposed run is a broad sweep rather than one narrow readiness/parity case.
- The plan starts mixing 3D outputs with `outputs/experiments` or 3D notes with
  `docs/experiments`.
