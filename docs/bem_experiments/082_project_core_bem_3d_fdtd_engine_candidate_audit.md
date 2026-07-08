# BEM Experiment 082: 3D FDTD Engine Candidate Audit

Date: 2026-06-25

## Purpose

Choose the most defensible path for producing paired 3D FDTD
target/background data for the BEM comparison contract.

Runs `079-081` established that the repository has the comparison surface:
manifests, strict frequency-bin templates, an extractor contract, and a
synthetic extractor smoke. This run asks which execution path should fill that
surface with real 3D FDTD data.

This is a CPU-only audit. It does not launch 3D FDTD, field FWI, GPU/HPC work,
or neural-network training.

## Output

```text
outputs/bem_experiments/082_project_core_bem_3d_fdtd_engine_candidate_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_engine_candidate_audit.csv
data/project_core_bem_3d_fdtd_engine_candidate_implementation_order.csv
data/project_core_bem_3d_fdtd_engine_candidate_audit_summary.json
figures/project_core_bem_3d_fdtd_engine_candidate_audit.png
docs/PROJECT_CORE_BEM_3D_FDTD_ENGINE_CANDIDATE_AUDIT.md
scripts/run_project_core_bem_3d_fdtd_engine_candidate_audit.py
scripts/test_project_core_bem_3d_fdtd_engine_candidate_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
candidate paths:                    6
preferred next candidates:          1
supporting tooling candidates:      1
blocked research candidates:        2
reference-only candidates:          2
implementation steps:               4
top candidate:                      external_3d_fdtd_import
repo local 3D FDTD present:         false
repo 2D CPU FDTD present:           true
repo 2D GPU FDTD present:           true
external data request ready:        true
local 3D FDTD launch ready:         false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
```

Candidate classification:

| Priority | Candidate | Status | Role |
| ---: | --- | --- | --- |
| 1 | external_3d_fdtd_import | preferred_next | real paired target/background data |
| 2 | minimal_local_3d_fdtd_smoke_engine | supporting_tooling | plumbing smoke only |
| 3 | port_existing_gpu_2d_tmz_to_3d | blocked_research | long-term local engine project |
| 4 | port_existing_cpu_2d_tmz_to_3d | blocked_research | conventions/reference only |
| 5 | bempp_only_reference | reference_only | BEM side of comparison only |
| 6 | colleague_scarep_2d_fdtd_baseline | reference_only | 2D algorithm reference only |

## Interpretation

The fastest scientifically useful 3D comparison path is not a direct port of
the current local 2D TMz FDTD code. The immediate path is to request or
generate external full-Maxwell 3D FDTD target/background outputs that match the
existing run `073` manifest, run `080` trace schema, run `077` frequency-bin
templates, and run `075` comparator.

A tiny local 3D FDTD smoke engine may still be useful for plumbing, but it
would not be validation evidence. The current local CPU/GPU solvers are 2D TMz
and should be treated as convention/performance references, not as direct 3D
finite-rebar engines.

## Decision

Use external 3D FDTD import as the next validation data path. Keep local 3D
FDTD launch and any 3D validation claim blocked until real target/background
outputs fill the run `077` templates and pass the run `075` comparator.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_engine_candidate_audit.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_engine_candidate_audit.png
2140x854, dynamic range=255
```
