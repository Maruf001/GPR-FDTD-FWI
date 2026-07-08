# BEM Experiment 125: scarep GPU MFS Dependency Recheck

Date: 2026-06-27

## Purpose

Recheck the optional CuPy/CUDA dependency path needed by the colleague
`scarep` GPU MFS demo.

This run does not run heavy GPU work, train neural networks, launch local 3D
FDTD, make a 3D validation claim, or change the CPU BEM/Bempp paths.

## Output

```text
outputs/bem_experiments/125_scarep_gpu_mfs_dependency_recheck
```

Key artifacts:

```text
data/scarep_gpu_mfs_dependency_recheck_rows.csv
data/scarep_gpu_mfs_dependency_recheck_summary.json
figures/scarep_gpu_mfs_dependency_recheck.png
docs/SCAREP_GPU_MFS_DEPENDENCY_RECHECK.md
scripts/run_scarep_gpu_mfs_dependency_recheck.py
scripts/test_scarep_gpu_mfs_dependency_recheck.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                     3
passes:                     2
blocking failures:          1
CuPy import ready:          true
CUDA runtime ready:         true
CuPy linalg ready:          false
GPU MFS dependencies ready: false
CPU BEM path blocked:       false
Bempp 3D path blocked:      false
real BEM/FDTD comparison:   false
GPU/HPC ready:              false
```

Dependency checks:

| Check | Status | Detail |
| --- | --- | --- |
| cupy_import | pass | 14.0.1 |
| cuda_runtime_version | pass | 12090 |
| cupy_linalg_solve | fail | ImportError: libcublas.so.12: cannot open shared object file: No such file or directory |

## Interpretation

The optional `scarep` GPU MFS demo path remains blocked by `libcublas.so.12`.
This does not affect the validated `scarep` CPU 2D BEM path or the Bempp 3D
prototype path.

## Decision

Do not block BEM/FDTD work on the optional `scarep` GPU MFS dependency path.
Use the CPU `scarep` BEM evidence and the Bempp 3D path unless a specific need
for the `scarep` GPU MFS demo appears.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_scarep_gpu_mfs_dependency_recheck.py
sha256: 86566e94585c05193529b1b9a6cfd98edeb851c7ff27adac41c7ed153ff83c20

test_scarep_gpu_mfs_dependency_recheck.py
sha256: 7266b9ea024cc28d4a5eed9f4e5f8ea4d4bd48572da152e546884b11ccb9fc69
```

Subsequent related BEM experiments should start from a duplicated
run-specific script.

## Validation

Focused dependency tests:

```text
tests/test_scarep_gpu_mfs_dependency_recheck.py
3 passed
```

Figure check:

```text
scarep_gpu_mfs_dependency_recheck.png
1961x771, dynamic range=255
```
