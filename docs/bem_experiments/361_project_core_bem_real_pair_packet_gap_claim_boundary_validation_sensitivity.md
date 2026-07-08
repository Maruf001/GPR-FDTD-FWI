# BEM Experiment 361: Real-Pair Packet Gap Claim Boundary Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `360` claim-boundary validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `359` claim boundary
and rejects damaged variants covering claim counts, guarded support states,
claim-row order, guarded and blocked claim rows, packet gap counts, false
downstream promotion, figure validation, and script snapshots.

It does not stage packet files, execute BEM/FDTD comparison, calibrate
thresholds, launch GPU work, transfer to field evidence, run field FWI, or start
3D/HPC work.

## Output

```text
outputs/bem_experiments/361_project_core_bem_real_pair_packet_gap_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_packet_gap_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_real_pair_packet_gap_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_packet_gap_claim_boundary_validation_sensitivity.png
docs/PROJECT_CORE_BEM_REAL_PAIR_PACKET_GAP_CLAIM_BOUNDARY_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                  22
expected pass:              1
observed pass:              1
expected failures:          21
observed failures:          21
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 359:      true
rejects damaged variants:   true
real packet files present:  false
real pair execution ready:  false
broad BEM replacement ready:false
field transfer ready:       false
3D validation ready:        false
GPU work ready:             false
```

## Interpretation

The validator accepts the exact run `359` claim boundary and rejects controlled
damaged variants covering claim counts, guarded support states, claim rows,
packet gap counts, false promotion, figure validation, and script snapshots.

## Decision

Use runs `359-361` as the guarded BEM real-pair packet gap claim-boundary
block. The next actionable BEM step is still packet staging, not
execution-scale comparison.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_packet_gap_claim_boundary_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_packet_gap_claim_boundary_validation_sensitivity.py: pass
tests/test_project_core_bem_real_pair_packet_gap_claim_boundary_validation_sensitivity.py: pass
```

Figure validation:

```text
3689x922, dynamic range=255
```
