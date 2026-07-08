# BEM Experiment 079: 3D FDTD Execution Readiness Audit

Date: 2026-06-25

## Purpose

Audit whether the local repository can produce real paired 3D FDTD
target/background outputs for the run `075` comparator today.

This is CPU-only readiness analysis. It does not launch 3D FDTD, field FWI,
GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/079_project_core_bem_3d_fdtd_execution_readiness_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_execution_readiness_audit.csv
data/project_core_bem_3d_fdtd_execution_readiness_audit_summary.json
figures/project_core_bem_3d_fdtd_execution_readiness_audit.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXECUTION_READINESS_AUDIT.md
```

## Result

```text
readiness checks:                   10
pass / partial / fail:              6 / 1 / 3
blocking gaps:                      3
local 3D FDTD launch ready:         false
real comparison ready:              false
3D validation claim ready:          false
```

Blocking gaps:

```text
local_3d_fdtd_engine
frequency_bin_extractor
paired_real_fdtd_outputs
```

## Interpretation

The BEM-side acceptance surface is now ready through manifest templates,
manifest validation, comparator schema, strict import templates, and synthetic
smoke tests.

The local execution side is not ready. The repository has a 2D TMz FDTD engine,
but no local 3D FDTD engine or real receiver-to-frequency-bin extractor for the
finite-rebar target/background pair.

## Decision

Do not launch a local 3D FDTD comparison from this repository yet. The next
implementation task is a real 3D FDTD engine/import path plus an extractor that
fills the run `077` templates and passes the run `075` comparator.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_execution_readiness_audit.py
2 passed
```

Figure check:

```text
2032x810, dynamic range=255
```
