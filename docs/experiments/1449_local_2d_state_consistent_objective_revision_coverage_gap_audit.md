# Experiment 1449: Objective Revision Coverage Gap Audit

Date: 2026-06-28

## Purpose

Audit what the guarded local 2D objective-revision materialization from runs
`1446`-`1448` actually covers, and what it still leaves open.

This run does not execute new FDTD simulations. It turns the saved
materialization result into a coverage boundary and a next-design matrix.

It does not launch GPU work, transfer to field evidence, run field FWI, or
start 3D/HPC work.

## Output

```text
outputs/experiments/1449_local_2d_state_consistent_objective_revision_coverage_gap_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_coverage_axes.csv
data/local_2d_state_consistent_objective_revision_next_design_matrix.csv
data/local_2d_state_consistent_objective_revision_coverage_gap_audit_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_coverage_gap_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_COVERAGE_GAP_AUDIT.md
scripts/run_local_2d_state_consistent_objective_revision_coverage_gap_audit.py
scripts/test_local_2d_state_consistent_objective_revision_coverage_gap_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
prospective perturbations:             5
objectives per case:                   6
materialized routes:                   3
drop-veryhigh truth recovered:         5
drop-veryhigh failures:                0
majority-vote truth recovered:         5
majority-vote failures:                0
veryhigh diagnostic failures:          3
source cases:                          2
noise seeds:                           1
coverage axes:                         12
partial or blocked axes:               6
next design blocks:                    6
CPU design blocks ready:               4
coverage gap audit ready:              true
expanded CPU stress design ready:      true
promote revised objective now:         false
broad radius promoted:                 false
physical claim ready:                  false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

The four CPU-ready next-design blocks are:

| Priority | Design block | Status | Purpose |
| ---: | --- | --- | --- |
| 1 | independent geometry CPU holdout | ready to design | Test the revised objective policy away from the same local geometry family. |
| 2 | source/noise policy stress | ready to design | Test source timing, amplitude, frequency, and random-seed robustness. |
| 3 | near-radius boundary refinement | ready to design | Refine the near-neighbor +2.00 mm failure boundary. |
| 4 | far-radius boundary extension | ready to design | Test deeper far-neighbor radius decreases under the revised policy. |

## Interpretation

The revised local 2D objective policy is well guarded for the saved five-case
materialization. In that narrow scope, drop-`veryhigh` recovers truth on all
five cases, majority vote recovers truth on all five cases, and `veryhigh`
remains diagnostic with three failures.

The evidence is still narrow. It covers one local geometry family, one noise
seed, nominal source frequency and amplitude, two time-shift states, and a
small near/far radius perturbation set. That is enough to define the next CPU
stress design, but it is not enough to promote broad-radius, physical-transfer,
GPU, field-FWI, or 3D/HPC claims.

## Decision

Use run `1449` as the coverage-gap boundary after the objective-revision
materialization. The next 2D work should be an independent CPU stress design
before any stronger local objective-policy claim is made.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_coverage_gap_audit.py
3 passed
```

Figure validation:

```text
3581x1115, dynamic range=255
```
