# Experiment 1445: Objective-Revision Execution Manifest Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1444` validator for the run `1443` local 2D
objective-revision execution manifest.

This run checks whether the validator accepts the exact saved run `1443`
manifest and rejects controlled damage to primary objective selection,
majority-vote cross-check objective coverage, `veryhigh` diagnostic status,
blocked-route executability, objective-role metadata, summary counts,
downstream readiness, figure validation, and script snapshots.

It does not run new FDTD simulations, launch GPU work, transfer to field data,
run field FWI, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1445_local_2d_state_consistent_objective_revision_execution_manifest_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_execution_manifest_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_execution_manifest_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_execution_manifest_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_EXECUTION_MANIFEST_SENSITIVITY.md
scripts/run_local_2d_state_consistent_objective_revision_execution_manifest_sensitivity.py
scripts/test_local_2d_state_consistent_objective_revision_execution_manifest_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          37
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         36
observed failure scenarios:         36
unexpected outcomes:                0
sensitivity ready:                  true
exact run 1443 accepted:            true
damaged variants rejected:          true
promote revised objective now:      false
broad radius promoted:              false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The execution-manifest validator accepts the exact run `1443` manifest and
rejects every damaged variant. The rejected cases cover `veryhigh`
primary-policy promotion, cross-check objective drift, diagnostic flag drift,
blocked-route executability drift, objective-role drift, summary drift,
downstream promotion, figure validation drift, and script-snapshot drift.

## Decision

Use runs `1443-1445` as the guarded local 2D objective-revision execution
manifest. Keep `veryhigh` out of primary selection and keep broad/physical/GPU/
field/FWI/3D routes blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_execution_manifest_sensitivity.py
3 passed
```

Figure validation:

```text
4031x887, dynamic range=255
```
