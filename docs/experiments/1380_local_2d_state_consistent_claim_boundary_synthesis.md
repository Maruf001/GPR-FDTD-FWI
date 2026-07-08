# Experiment 1380: Local 2D State-Consistent Claim-Boundary Synthesis

Date: 2026-06-27

## Purpose

Synthesize runs `1374`-`1379` into one result-driven decision boundary for the
local 2D state-consistency branch.

Those runs tested whether the target recovery only worked under a fragile fixed
neighbor state, or whether there is a defensible local mechanism result after
the fixed-neighbor geometry is made internally consistent.

This run does not rerun the optimizer, launch broad batches, run GPU work, use
field data, run field FWI, perform 3D/HPC work, or train neural networks.

## Output

```text
outputs/experiments/1380_local_2d_state_consistent_claim_boundary_synthesis
```

Key artifacts:

```text
data/local_2d_state_consistent_claim_boundary_stage_rows.csv
data/local_2d_state_consistent_claim_boundary_normalized_results.csv
data/local_2d_state_consistent_claim_boundary_radius_boundaries.csv
data/local_2d_state_consistent_claim_boundary_synthesis_summary.json
figures/local_2d_state_consistent_claim_boundary_synthesis.png
docs/LOCAL_2D_STATE_CONSISTENT_CLAIM_BOUNDARY_SYNTHESIS.md
scripts/run_local_2d_state_consistent_claim_boundary_synthesis.py
scripts/test_local_2d_state_consistent_claim_boundary_synthesis.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source runs:                              6
stage rows:                               6
normalized result rows:                   116
radius-boundary rows:                     4
failure rows:                             32
correct-state rows:                       18
expanded-window correct-state rows:       6
expanded-window correct-state truth rows: 6
minimum wrong-minus-truth misfit:         -0.013784677258736597
state-consistency guard enforced:         true
objective ladder all truth:               true
expanded correct state all truth:         true
state-consistent mechanism promoted:      true
wide radius tolerance promoted:           false
strict expanded-window tolerance promoted:false
broad batch ready:                        false
GPU work ready:                           false
field transfer ready:                     false
field FWI ready:                          false
```

Stage progression:

| Run | Stage | Tested rows | Truth rows | Failure rows | Stage passed |
| ---: | --- | ---: | ---: | ---: | --- |
| 1374 | guard enforcement | 3 | 1 | 2 | true |
| 1375 | objective ladder | 6 | 6 | 0 | true |
| 1376 | small neighbor tolerance | 16 | 16 | 0 | true |
| 1377 | wide radius ladder | 32 | 26 | 6 | false |
| 1378 | radius boundary refinement | 20 | 11 | 9 | false |
| 1379 | expanded x-window | 24 | 13 | 11 | false |

Radius boundary summary:

| Run | Window | Direction | Last all-objectives pass mm | First any-objective fail mm |
| ---: | --- | --- | ---: | ---: |
| 1378 | narrow x-window, two objectives | near neighbor radius increase | 2.0 | 2.25 |
| 1378 | narrow x-window, two objectives | far neighbor radius decrease | 1.5 | 1.75 |
| 1379 | expanded x-window, six objectives | near neighbor radius increase |  | 2.0 |
| 1379 | expanded x-window, six objectives | far neighbor radius decrease |  | 1.5 |

## Interpretation

The corrected-state mechanism survives the strongest tested target-window
challenge. With fixed-neighbor geometry made internally consistent, the target
remains:

```text
x = 190 mm
z = 90 mm
radius = 5 mm
```

across the six-objective ladder and the expanded x-window from 186 mm to
194 mm.

The radius-tolerance claim does not survive as a broad statement. Under the
narrower two-objective window, the recovery remains stable through near-neighbor
radius +2.0 mm and far-neighbor radius -1.5 mm. Under the expanded x-window and
six-objective audit, failures begin at those same perturbation sizes. The
failures move the selected target below truth, to x=188 mm in runs `1377`-`1378`
and x=187 mm in run `1379`.

The result supports a local mechanism claim, not broad local 2D sweeps, GPU
work, field transfer, or field FWI.

## Decision

Promote only the corrected-state local 2D mechanism:

```text
With consistent fixed-neighbor geometry, the target remains x=190 mm,
z=90 mm, radius=5 mm across the tested objective ladder and expanded x-window.
```

Do not promote broad radius tolerance. Do not launch broad local 2D batches,
GPU work, field transfer, or field FWI from this branch.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_claim_boundary_synthesis.py
sha256: 03e61ae34dca29db03f4bc98c134f7e9886814e4b065de17f8c68390020d3a63

test_local_2d_state_consistent_claim_boundary_synthesis.py
sha256: 97efafac921731fe1ab5e38cbe0459b10a35efffcc2037344badde487263b2a7
```

Subsequent related local 2D state-consistency experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_claim_boundary_synthesis.py
3 passed
```

Figure check:

```text
local_2d_state_consistent_claim_boundary_synthesis.png
2356x1458, dynamic range=255
```
