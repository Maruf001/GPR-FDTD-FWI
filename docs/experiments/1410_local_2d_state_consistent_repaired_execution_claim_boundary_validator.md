# Local 2D Experiment 1410: State-Consistent Repaired Execution Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `1409` repaired execution claim boundary from a consumer
perspective.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote downstream states.

## Output

```text
outputs/experiments/1410_local_2d_state_consistent_repaired_execution_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_claim_boundary_validation_checks.csv
data/local_2d_state_consistent_repaired_execution_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_repaired_execution_claim_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CLAIM_BOUNDARY_VALIDATOR.md
scripts/run_local_2d_state_consistent_repaired_execution_claim_boundary_validator.py
scripts/test_local_2d_state_consistent_repaired_execution_claim_boundary_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
validation ready:                   true
recommended guard:                  repaired_regression_execution_packet_guard
materialized core rows:             88
full pack remains authoritative:    true
sentinel replaces full pack:        false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The validator confirms exactly one recommended guard, the 88-row repaired core
table, the four row-count mismatches that block the original packet, the
11-row sentinel fast-smoke-only role, and blocked downstream states.

## Interpretation

The run `1409` claim boundary is internally consistent. It is now positively
validated, but not yet stress-tested by negative controls.

## Decision

Use run `1410` as the positive validator for the repaired local 2D execution
claim boundary.

Run sensitivity testing before treating this claim boundary as fully guarded.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_claim_boundary_validator.py
5 passed
```

Python compile check:

```text
run_local_2d_state_consistent_repaired_execution_claim_boundary_validator.py: pass
tests/test_local_2d_state_consistent_repaired_execution_claim_boundary_validator.py: pass
```

Figure check:

```text
2645x841, dynamic range=255
```
