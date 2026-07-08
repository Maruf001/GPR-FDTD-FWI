# BEM Experiment 491: Post Real Return-File Acceptance-Gate Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded real return-file acceptance gate from runs `488-490` into the
BEM claim boundary.

## Output

```text
outputs/bem_experiments/491_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      34
guarded claims:                              31
blocked claims:                              3
acceptance gate ready:                       true
acceptance-gate validation ready:            true
acceptance-gate sensitivity ready:           true
required real return files:                  4
accepted real return files:                  0
required real entries:                       1116
accepted real entries:                       0
required real scorecard rows:                279
accepted real scorecard rows:                0
source-hash requirements:                    558
scattered-norm requirements:                 558
real return packet accepted:                 false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The BEM boundary now records the exact real-file acceptance gate. The gate is
ready to evaluate a future return packet, but the current state has zero
accepted real files, zero accepted real entries, and no accepted real packet.

## Decision

Use this as the current BEM claim boundary after the real return-file
acceptance-gate block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary.py
4 passed
```

Figure check:

```text
3977x894, dynamic range=255
```
