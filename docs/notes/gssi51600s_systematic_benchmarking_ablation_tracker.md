# GSSI51600S Systematic Benchmarking Ablation Tracker

## Purpose

This tracker governs cleanup and follow-on experiment work for
`outputs/gssi51600s_systematic_benchmarking_ablation`.

The immediate goal is to make the existing results interpretable before running
more experiments. New experiment runs should wait until the current figures,
metrics, and folder purposes are auditable.

## Current Cleanup Queue

| Step | Status | Notes |
| --- | --- | --- |
| Build folder-by-folder audit ledger | Pending | Record purpose, source script, inputs, metrics, figures, known issues, and fix status for every subfolder family. |
| Enforce plotting policy | Pending | Apply shared plotting rules across all summary and optimizer figures. |
| Regenerate existing figures from saved results | Pending | Regenerate before rerunning experiments, so presentation fixes are separated from scientific changes. |
| Diagnose optimizer and geometry behavior | Pending | Check whether parameters are optimized, pinned, guarded, or unit-misplotted. |
| Design compact rerun matrix | Pending | Only after cleanup: matched seeds, matched objective/window/budget, multiple seeds per optimizer. |

## Plotting Policy

All regenerated figures must follow these rules:

- Figure titles must identify the experiment family and key settings, including optimizer/backend where applicable.
- Do not silently mix incompatible units on one y-axis. If geometry parameters have different units or scales, use separate axes, normalized deltas, or tables.
- Bars that represent zero, ties, missing values, or non-applicable values must be explicitly labeled.
- Similar-height bars should use a comparison-oriented view, such as a zoomed y-axis or paired absolute-plus-delta view, so differences are readable.
- Absolute bars may start from zero when the absolute magnitude matters; close comparisons do not have to start from zero if that hides the result.
- Leave readable top headroom for labels and bar tops.
- Runtime totals and runtime components must not be plotted as if they are competing alternatives. Use decomposition naming or separate panels.
- Every final figure must be visually inspected before being accepted.

## Post-Cleanup Paper Review

After the cleanup queue above is complete, review this paper thoroughly:

`paper/FWI_twoParam_GPR_Quadratic-Wasserstein-Distance_2024.pdf`

Required deliverables:

- Save detailed reading notes as an IPython notebook:
  `docs/papers/FWI_twoParam_GPR_Quadratic-Wasserstein-Distance_2024_notes.ipynb`
- Extract implementable ideas from the paper, especially any two-parameter FWI,
  quadratic Wasserstein distance, objective shaping, or robustness concepts that
  could improve the real-field GSSI51600S workflow.
- Propose a small real-world-data test that keeps the existing fast CUDA
  accelerator approach intact.
- Treat any JAX, PyTorch, or CUDA changes as backend candidates behind the same
  scientific objective, not as a rewrite of the experiment logic.

## Accelerator Note

The current backend preflight figure suggests `jax_jit` has the best median
time for the tensor-kernel microbenchmark, even faster than `torch_cuda`.
That is plausible and consistent with the earlier acceleration checkpoint in
`docs/update/summary/249_2026-07-03_field_3d_0701_acceleration_backend_checkpoint.md`.

This does not yet prove JAX is the best full optimizer backend. The preflight is
a kernel-level benchmark, not a full forward/objective/backward/optimizer loop.
Before changing the main backend decision, compare:

- compilation warmup excluded versus included,
- host-device transfer costs,
- full objective and gradient runtime,
- memory use and batching behavior,
- numerical agreement with the existing CUDA/Fast-GPR path,
- end-to-end seconds per accepted optimizer iteration.

Until that full-loop comparison exists, keep the existing fast CUDA accelerator
path as the baseline and evaluate JAX as a candidate acceleration layer.
