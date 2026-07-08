# Experiment 1425: Local 2D State-Consistent Repaired Execution CI Adoption Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `1424` CI adoption boundary from saved artifacts. The goal is
to confirm that a downstream consumer can read the boundary rows and summary
and recover the same decision: four CPU CI guard items are ready, three claim
promotion items remain blocked, and the 88-row full-core pack remains
authoritative.

This run does not execute a new physical inversion, launch GPU work, transfer
to field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1425_local_2d_state_consistent_repaired_execution_ci_adoption_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_validator_checks.csv
data/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_validator_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ADOPTION_BOUNDARY_VALIDATOR.md
```

## Result

```text
validation checks:                 5
validation checks passed:          5
blocking failures:                 0
boundary validation ready:         true
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

The five validation checks confirm:

| Check | Result |
| --- | --- |
| Boundary counts are consistent | pass |
| CPU CI routes are scoped and adopted | pass |
| Execution evidence is passed and guarded | pass |
| Full-pack authority is preserved | pass |
| Physical, GPU, field, and 3D claims are blocked | pass |

## Interpretation

The saved CI adoption boundary is internally consistent. The reduced sentinel
is ready only as a fast smoke route, the repaired full-core route is ready for
boundary-sensitive CI checks, and the full 88-row pack remains authoritative.

Physical claims, broad-radius claims, GPU work, field transfer, field FWI, and
3D/HPC remain blocked.

## Decision

Use runs `1424`-`1425` as the consumer-validated local 2D CI adoption
boundary. Sensitivity remains required before treating it as fully guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_adoption_boundary_validator.py
5 passed
```

Figure validation:

```text
2717x821, dynamic range=255
```
