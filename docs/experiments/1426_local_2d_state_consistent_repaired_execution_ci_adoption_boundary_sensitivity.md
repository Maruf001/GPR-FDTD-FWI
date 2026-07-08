# Experiment 1426: Local 2D State-Consistent Repaired Execution CI Adoption Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1425` CI adoption boundary validator. The goal is to
verify that the validator accepts the exact run `1424` boundary and rejects
controlled damage to boundary counts, CPU route adoption, execution evidence,
full-pack authority, and false physical/GPU/field/3D readiness.

This run does not execute a new physical inversion, launch GPU work, transfer
to field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1426_local_2d_state_consistent_repaired_execution_ci_adoption_boundary_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_sensitivity_scenarios.csv
data/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_sensitivity_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_adoption_boundary_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ADOPTION_BOUNDARY_SENSITIVITY.md
```

## Result

```text
scenarios:                         23
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        22
observed failure scenarios:        22
unexpected outcomes:               0
sensitivity ready:                 true
CI adoption boundary ready:        true
reduced sentinel adopted:          true
repaired full-core gate adopted:   true
full pack remains authoritative:   true
sentinel replaces full pack:       false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The exact run `1424` CI adoption boundary passes. All 22 damaged variants fail
as expected for missing boundary rows, count drift, CI-boundary readiness drift,
reduced-sentinel adoption drift, full-core route drift, execution-count drift,
sensitivity guard drift, full-pack authority drift, sentinel-replacement
promotion, physical-claim promotion, GPU/field route promotion, field-transfer
promotion, field-FWI promotion, and 3D/HPC promotion.

## Interpretation

The local 2D CI adoption boundary is now guarded. The four passing CPU command
routes can be used as the local 2D CI package, with the reduced sentinel kept
as fast smoke and the repaired 88-row full-core table kept authoritative for
boundary-sensitive changes.

The package remains a regression and software-quality result only. Physical
claims, broad-radius claims, GPU work, field transfer, field FWI, and 3D/HPC
remain blocked.

## Decision

Use runs `1424`-`1426` as the guarded local 2D CI adoption boundary. Do not
promote physical, GPU, field-transfer, field-FWI, or 3D/HPC claims from this
package.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_adoption_boundary_sensitivity.py
6 passed
```

Figure validation:

```text
3671x887, dynamic range=255
```
