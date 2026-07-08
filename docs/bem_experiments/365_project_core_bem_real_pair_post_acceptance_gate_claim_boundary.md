# BEM Experiment 365: Real-Pair Post Acceptance Gate Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the BEM real-pair claim boundary after the guarded return-packet
acceptance gate from runs `362-364`.

This run adds the return-packet acceptance gate as a guarded claim while keeping
real packet files, real comparison, threshold calibration, broad BEM
replacement, field transfer, GPU work, and 3D validation blocked.

## Output

```text
outputs/bem_experiments/365_project_core_bem_real_pair_post_acceptance_gate_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_real_pair_post_acceptance_gate_claim_boundary_claim_rows.csv
data/project_core_bem_real_pair_post_acceptance_gate_claim_boundary_summary.json
figures/project_core_bem_real_pair_post_acceptance_gate_claim_boundary.png
scripts/
```

## Result

```text
claims:                         12
guarded claims:                 9
blocked claims:                 3
base claims:                    11
base guarded claims:            8
base blocked claims:            3
acceptance gates:               8
ready acceptance gates:         2
blocked acceptance gates:       6
missing packet items:           34
missing projected traces:       26
missing metadata/control:       8
real packet files present:      false
real comparison ready:          false
threshold calibration ready:    false
broad BEM replacement ready:    false
field transfer ready:           false
GPU work ready:                 false
3D validation ready:            false
```

## Interpretation

The BEM claim boundary now includes the guarded return-packet acceptance gate.
The branch is ready to accept and validate a future returned packet, but not to
run the real BEM/FDTD comparison.

## Decision

Use run `365` as the current BEM claim boundary after the return-packet
acceptance gate. Do not run real comparison or threshold calibration until the
packet is present and passes the gate.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_post_acceptance_gate_claim_boundary.py
3 passed
```

Figure validation:

```text
3761x953, dynamic range=255
```
