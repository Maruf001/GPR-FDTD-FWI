# BEM Experiment 360: Real-Pair Packet Gap Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `359` BEM real-pair packet gap claim boundary from
artifacts.

This run checks the claim counts, guarded support blocks, claim-row order,
blocked claim rows, packet gap counts, downstream blocked states, figure output,
and script snapshots.

It does not stage packet files, execute BEM/FDTD comparison, calibrate
thresholds, launch GPU work, transfer to field evidence, run field FWI, or start
3D/HPC work.

## Output

```text
outputs/bem_experiments/360_project_core_bem_real_pair_packet_gap_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_real_pair_packet_gap_claim_boundary_validator_checks.csv
data/project_core_bem_real_pair_packet_gap_claim_boundary_validator_summary.json
figures/project_core_bem_real_pair_packet_gap_claim_boundary_validator.png
docs/PROJECT_CORE_BEM_REAL_PAIR_PACKET_GAP_CLAIM_BOUNDARY_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:               9
passed checks:                   9
failed checks:                   0
validation ready:                true
claims:                          11
guarded claims:                  8
blocked claims:                  3
packet items:                    34
missing packet items:            34
missing projected traces:        26
missing metadata/control items:  8
open action groups:              4
real packet files present:       false
real pair execution ready:       false
broad BEM replacement ready:     false
field transfer ready:            false
3D validation ready:             false
GPU work ready:                  false
```

## Interpretation

The saved claim boundary is internally consistent. The four real-pair packet
support blocks are guarded, the packet gap counts are stable, and every
execution-scale downstream state remains blocked.

## Decision

Use run `360` as the validator for the run `359` claim boundary. The branch
remains a packet-staging problem, not a ready BEM/FDTD comparison problem.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_packet_gap_claim_boundary_validator.py
3 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_packet_gap_claim_boundary_validator.py: pass
tests/test_project_core_bem_real_pair_packet_gap_claim_boundary_validator.py: pass
```

Figure validation:

```text
3689x933, dynamic range=255
```
