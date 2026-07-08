# BEM Experiment 314: Bempp Fine-Mesh FDTD Archive Receiver Operator Holdout Readiness Audit

Date: 2026-06-28

## Purpose

Audit whether the current archive already contains independent data suitable
for validating the guarded run `311-313` receiver-operator diagnostic.

This run does not run FDTD, run a new BEM solve, validate a physical operator,
calibrate BEM/FDTD amplitude agreement, validate 3D physics, transfer to field
evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/314_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_readiness_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_candidates.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_readiness_audit_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_readiness_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
candidate count:                         7
target/background pair candidates:       5
independent schema-compatible candidates:0
holdout-ready candidates:                0
receiver-operator holdout ready:         false
holdout design ready:                    true
physical operator claim ready:           false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
field FWI ready:                         false
```

Candidate audit:

| Candidate | Rows | Frequencies | Receivers | Holdout ready | Blocker |
| --- | ---: | ---: | ---: | --- | --- |
| run117 fine-mesh BEM reference | 279 | 9 | 31 | false | BEM reference only and also used by the current run 311 fit |
| run303 training proxy pair | 279 | 9 | 31 | false | Same proxy pair used to fit and diagnose the receiver operator |
| run118 synthetic sensitivity | 837 | 9 | 31 | false | Synthetic rows generated from the same BEM reference |
| run124 synthetic preflight pass | 279 | 9 | 31 | false | Synthetic BEM-derived frequency bins, not independent FDTD |
| run247 half-space synthetic pairwise | 117 | 9 | 13 | false | Different scalar half-space schema and receiver grid |
| run262 trace-root negative control | 117 | 9 | 13 | false | Negative-control table and half-space scalar trace-root schema |
| run299 2D archive convertible B-scans | 80 | 0 | 0 | false | Convertible B-scans, but zero strict fine-mesh target/background frequency-export pairs |

## Interpretation

The current archive does not contain an independent fine-mesh target/background
BEM/FDTD holdout pair for the receiver-operator diagnostic. The available
candidates are either the training pair, synthetic rows derived from the same
BEM reference, different scalar half-space schemas, negative-control rows, or
raw 2D B-scans without strict fine-mesh target/background frequency exports.

## Decision

Do not promote the receiver-operator diagnostic to a physical operator or
calibrated agreement claim.

The next required artifact is an independent fine-mesh target/background
frequency-export pair on the `31 receiver x 9 frequency` grid with a matching
BEM reference and no reuse of the run `311` fitted receiver operator.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_readiness_audit.py
3 passed
```

Figure validation:

```text
3492x1091, dynamic range=255
```
