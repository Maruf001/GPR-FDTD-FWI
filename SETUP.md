# Setup Guide

This project is intended to run on a Linux NVIDIA workstation or DGX Spark.
The current source machine was audited on 2026-06-14 with:

```text
GPU: NVIDIA GB10
NVIDIA driver: 580.95.05
CUDA shown by nvidia-smi: 13.0
CUDA compiler: 13.0.88
Git: 2.43.0
Codex CLI: 0.139.0
Claude Code: 2.1.177
```

## System Packages

Install or verify these first:

```bash
git --version
nvidia-smi
nvcc --version
python --version
```

Recommended baseline:

```text
Git
Miniforge or conda
NVIDIA driver and CUDA tools
Node.js 20 or newer for Codex/Claude CLI tools
zstd for restoring the local artifact archive
```

## Git And GitHub

Configure identity on the new machine:

```bash
git config --global user.name "Your Name"
git config --global user.email "55299535+Maruf001@users.noreply.github.com"
```

Verify GitHub access:

```bash
ssh -T git@github.com
git ls-remote https://github.com/Maruf001/GPR-FDTD-FWI.git refs/heads/master
```

HTTPS clone:

```bash
git clone https://github.com/Maruf001/GPR-FDTD-FWI.git
cd GPR-FDTD-FWI
```

Offline clone from the migration bundle:

```bash
git clone /path/to/GPR-FDTD-FWI_git_all_2026-06-14.bundle GPR-FDTD-FWI
cd GPR-FDTD-FWI
git remote add origin https://github.com/Maruf001/GPR-FDTD-FWI.git
```

## Python Environment

Conda path:

```bash
conda env create -f environment.yml
conda activate gpr-fdtd-fwi
python -m pytest -q
```

Pip path:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-gpu.txt
python -m pytest -q
```

The GPU requirements file installs `cupy-cuda12x==14.0.1`, matching the audited
current environment. If the new DGX Spark has a different CUDA/driver stack,
verify CuPy compatibility before long GPU runs.

## GPU Verification

```bash
python - <<'PY'
import cupy as cp
print("cupy", cp.__version__)
print("runtime", cp.cuda.runtime.runtimeGetVersion())
device = cp.cuda.Device(0)
print("device", device)
x = cp.arange(8)
print(cp.asnumpy(x * x))
PY
```

Project-level smoke checks:

```bash
python run_benchmark.py
python run_forward.py
```

For production experiment sweeps, prefer GPU-backed commands where supported.
Record command, output path, parameters, metrics, interpretation, and next
decision in `docs/experiments/`.

## Codex And Claude Code

The current machine has these CLIs on Node.js 20.20.0:

```bash
codex --version
claude --version
```

On the new machine, install and authenticate the tools through the same account
workflow used for this DGX Spark. Then verify:

```bash
which codex
codex --version
which claude
claude --version
```

Local Claude settings under `.claude/` are intentionally ignored and were not
placed in the artifact archive.

## Restore Local Experiment Outputs

Git does not restore ignored generated artifacts. To recreate this machine's
working copy, restore the archive described in `MIGRATION.md`:

```bash
tar --zstd -xf /path/to/GPR-FDTD-FWI_local_artifacts_2026-06-14.tar.zst
```

Run this from the repository root after cloning.
