# BEM Experiment 224: scarep GPU MFS Fix Priority Audit

Date: 2026-06-28

## Purpose

Decide whether the optional colleague `scarep` GPU MFS dependency path should be
fixed now.

This run does not install packages, modify CUDA libraries, run heavy GPU work,
launch FDTD/FWI, use field data, or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/224_scarep_gpu_mfs_fix_priority_audit
```

Key artifacts:

```text
data/scarep_gpu_mfs_fix_priority_dependency_rows.csv
data/scarep_gpu_mfs_fix_priority_rows.csv
data/scarep_gpu_mfs_fix_priority_audit_summary.json
figures/scarep_gpu_mfs_fix_priority_audit.png
docs/SCAREP_GPU_MFS_FIX_PRIORITY_AUDIT.md
scripts/run_scarep_gpu_mfs_fix_priority_audit.py
scripts/test_scarep_gpu_mfs_fix_priority_audit.py
```

## Result

```text
dependency checks:                 3
dependency passes:                 2
dependency blocking failures:      1
CuPy import ready:                 true
CUDA runtime ready:                true
CuPy linalg ready:                 false
GPU MFS dependency ready:          false
scarep CPU BEM ready:              true
tabulated scaling guard ready:     true
fix GPU MFS now recommended:       false
GPU MFS fix priority:              low
current BEM work blocked:          false
GPU/HPC ready:                     false
field transfer ready:              false
3D validation ready:               false
field FWI ready:                   false
```

The current dependency check reproduces the prior blocker:

```text
cupy.linalg.solve -> ImportError: libcublas.so.12
```

This affects only the optional `scarep` GPU MFS demo path. The validated
`scarep` CPU BEM path and the guarded tabulated-surface BEM path remain ready.

## Interpretation

Fixing cuBLAS would unlock an optional demo branch. It is not required for the
current CPU BEM evidence, Bempp 3D reference path, or guarded tabulated-surface
work.

## Decision

Do not spend the current BEM marathon on CUDA/cuBLAS repair.

Keep the fix priority low and continue with CPU `scarep` evidence, Bempp 3D
references, and guarded tabulated-surface work unless a specific GPU MFS
requirement appears.

## Validation

Focused tests:

```text
tests/test_scarep_gpu_mfs_fix_priority_audit.py
3 passed
```

Python compile check:

```text
run_scarep_gpu_mfs_fix_priority_audit.py: pass
tests/test_scarep_gpu_mfs_fix_priority_audit.py: pass
```

Figure check:

```text
2465x811, dynamic range=255
```
