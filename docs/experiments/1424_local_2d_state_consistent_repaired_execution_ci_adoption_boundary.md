# Experiment 1424: Local 2D State-Consistent Repaired Execution CI Adoption Boundary

Date: 2026-06-28

## Purpose

Convert the guarded executed CPU command smoke from runs `1421`-`1423` into an
explicit CI adoption boundary. The goal is to state exactly which 2D regression
routes can now be used as CPU CI guards and which routes remain blocked from
physical, GPU, field-transfer, field-FWI, and 3D/HPC claims.

This run does not execute a new physical inversion, launch GPU work, transfer
to field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1424_local_2d_state_consistent_repaired_execution_ci_adoption_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_rows.csv
data/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_adoption_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ADOPTION_BOUNDARY.md
```

## Result

```text
boundary items:                    7
ready items:                       4
blocked items:                     3
executed commands:                 4 / 4
passed executable commands:        4
blocked routes not executed:       2
sensitivity scenarios:             26
sensitivity unexpected outcomes:   0
CI adoption boundary ready:        true
reduced sentinel adopted:          true
repaired full-core gate adopted:   true
full pack remains authoritative:   true
sentinel replaces full pack:       false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The ready CI items are:

| Item | Scope |
| --- | --- |
| Reduced sentinel fast-smoke execution | Consumer wiring, schema, parsing, plotting, and harmless row-order smoke |
| Repaired full-core gate execution | Row-key, digest, boundary, objective, margin, and token-sensitive changes |
| Execution sensitivity guard | Validator drift protection around the executed command rows |
| Full-pack authority rule | The 88-row repaired full-core pack remains authoritative for boundary-sensitive decisions |

The blocked items are:

| Item | Reason |
| --- | --- |
| Sentinel replaces full pack | The 11-row sentinel is fast smoke only |
| Physical or broad-radius claim | A new physical/acquisition design is required |
| GPU, field FWI, or 3D/HPC route | Current 2D evidence cannot promote these routes |

## Interpretation

The local 2D regression commands are ready for CPU CI adoption. The reduced
sentinel is a fast smoke route, and the repaired 88-row full-core table remains
the authoritative route for boundary-sensitive changes.

This is a software-quality and regression-readiness result. It does not create
new physical evidence and does not support GPU, field-transfer, field-FWI, or
3D/HPC escalation.

## Decision

Adopt the four passing CPU command routes as the guarded local 2D CI package.
Keep physical claims, broad-radius claims, GPU work, field transfer, field FWI,
and 3D/HPC blocked from this result.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_adoption_boundary.py
4 passed
```

Figure validation:

```text
3221x867, dynamic range=255
```
