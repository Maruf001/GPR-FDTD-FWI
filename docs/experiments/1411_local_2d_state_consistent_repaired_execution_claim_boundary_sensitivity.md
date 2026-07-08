# Local 2D Experiment 1411: State-Consistent Repaired Execution Claim Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1410` claim-boundary validator with damaged claim-boundary
summaries.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote downstream states.

## Output

```text
outputs/experiments/1411_local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity_scenarios.csv
data/local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity_summary.json
figures/local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CLAIM_BOUNDARY_SENSITIVITY.md
scripts/run_local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity.py
scripts/test_local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity.py
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected failure scenarios:        17
observed pass scenarios:           1
observed failure scenarios:        17
unexpected outcomes:               0
sensitivity ready:                 true
full pack remains authoritative:   true
sentinel replaces full pack:       false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The exact claim boundary passes. Damaged cases fail for claim-count drift,
missing or duplicated recommended guard, wrong repaired row count, repaired
sensitivity not ready, original packet mismatch drift, original packet marked
ready, sentinel row-count drift, sentinel/full-pack authority drift, physical
claim readiness, and downstream GPU/field/FWI/3D readiness.

## Interpretation

Runs `1409`-`1411` now form a guarded claim-boundary package for the repaired
local 2D regression execution packet.

This package resolves a table-execution boundary. It does not create a new
physical inversion result and does not justify GPU work, field transfer, field
FWI, or 3D/HPC.

## Decision

Use runs `1409`-`1411` as the guarded repaired local 2D execution
claim-boundary package.

Keep physical claims, GPU work, field transfer, field FWI, and 3D/HPC blocked
from this table-execution repair.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity.py
5 passed
```

Python compile check:

```text
run_local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity.py: pass
tests/test_local_2d_state_consistent_repaired_execution_claim_boundary_sensitivity.py: pass
```

Figure check:

```text
3041x879, dynamic range=255
```
