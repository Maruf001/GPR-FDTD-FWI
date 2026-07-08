# Experiment 1427: Local 2D State-Consistent Physical Claim Design Gap Audit

Date: 2026-06-28

## Purpose

Convert the blocked physical and broad-radius claims into a concrete next-design
matrix for the local 2D FDTD branch.

The source evidence says the corrected-state mechanism is stable inside the
tested local setup, but broad radius and physical claims remain blocked by
expanded-window failures and negative wrong-minus-truth margins.

This run does not execute new FDTD simulations, launch GPU work, transfer to
field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1427_local_2d_state_consistent_physical_claim_design_gap_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_physical_claim_design_gap_evidence.csv
data/local_2d_state_consistent_physical_claim_design_matrix.csv
data/local_2d_state_consistent_physical_claim_design_gap_audit_summary.json
figures/local_2d_state_consistent_physical_claim_design_gap_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_PHYSICAL_CLAIM_DESIGN_GAP_AUDIT.md
scripts/run_local_2d_state_consistent_physical_claim_design_gap_audit.py
scripts/test_local_2d_state_consistent_physical_claim_design_gap_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source runs:                         5
evidence rows:                       11
design rows:                         6
CPU design-ready rows:               5
new finite-difference data required: 4
corrected-state mechanism promoted:  true
wide radius tolerance promoted:      false
physical claim ready:                false
broad batch ready:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The next design matrix has six blocks:

| Priority | Design block | Current decision |
| ---: | --- | --- |
| 1 | expanded window near-radius bracket | CPU design ready |
| 2 | expanded window far-radius bracket | CPU design ready |
| 3 | objective-family disambiguation | CPU design ready |
| 4 | noise and time-zero replicates | CPU design ready |
| 5 | geometry-window resolution check | CPU design ready |
| 6 | GPU or broad-batch escalation | blocked from current evidence |

## Interpretation

The useful next 2D work is not another CI wrapper or a broad GPU batch. The
data-driven next branch is a CPU bracket/replicate design around the expanded
x-window failures:

```text
near-neighbor radius increase: +0.50, +1.00, +1.25, +1.50, +1.75 mm
far-neighbor radius decrease:  -0.50, -0.75, -1.00, -1.25 mm
```

Those cases should be checked under the expanded x-window and six-objective
audit before any broad radius, physical, GPU, field-transfer, field-FWI, or
3D/HPC escalation.

## Decision

Use run `1427` as the next local 2D design matrix. Run CPU bracket and
replicate studies before considering broad batches, GPU work, field transfer,
field FWI, or 3D/HPC escalation.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_physical_claim_design_gap_audit.py
4 passed
```

Figure validation:

```text
3256x894, dynamic range=255
```
