# BEM Experiment 359: Real-Pair Packet Gap Claim Boundary

Date: 2026-06-28

## Purpose

Refresh the current BEM claim boundary after the guarded real-pair packet
filesystem gap audit.

This run folds four recent BEM real-pair checkpoints into one decision state:

```text
347-349  real-pair execution readiness gate
350-352  file-level FDTD export packet contract
353-355  non-executed packet staging command plan
356-358  current filesystem gap audit
```

This is a saved-artifact synthesis run. It does not stage real packet files,
execute BEM/FDTD comparison, calibrate thresholds, launch GPU work, transfer to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/359_project_core_bem_real_pair_packet_gap_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_real_pair_packet_gap_claim_boundary_claim_rows.csv
data/project_core_bem_real_pair_packet_gap_claim_boundary_summary.json
figures/project_core_bem_real_pair_packet_gap_claim_boundary.png
docs/PROJECT_CORE_BEM_REAL_PAIR_PACKET_GAP_CLAIM_BOUNDARY.md
scripts/
```

## Result

```text
claims:                         11
guarded claims:                 8
blocked claims:                 3
real-pair gate guarded:         true
packet contract guarded:        true
staging plan guarded:           true
filesystem gap audit guarded:   true
packet items:                   34
missing packet items:           34
missing projected traces:       26
missing metadata/control items: 8
open action groups:             4
real packet files present:      false
real pair execution ready:      false
broad BEM replacement ready:    false
field transfer ready:           false
3D validation ready:            false
GPU work ready:                 false
field FWI ready:                false
```

The claim boundary now records that the real-pair handoff is structurally
defined and validator-hardened, but not executable. The expected packet is still
empty: all 34 expected files are missing, including 26 projected FDTD traces and
eight metadata/control artifacts.

## Decision

Use run `359` as the current BEM real-pair packet claim boundary.

The next BEM-side action remains staging the required projected FDTD traces and
metadata/control packet files, then rerunning the packet gap audit and
acceptance checks. Do not promote the current branch to real BEM/FDTD
comparison, broad BEM replacement, field transfer, 3D validation, GPU work, or
field FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_packet_gap_claim_boundary.py
3 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_packet_gap_claim_boundary.py: pass
tests/test_project_core_bem_real_pair_packet_gap_claim_boundary.py: pass
```

Figure validation:

```text
3761x948, dynamic range=255
```
