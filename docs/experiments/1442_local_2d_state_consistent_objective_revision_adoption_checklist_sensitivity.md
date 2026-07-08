# Experiment 1442: Local 2D Objective-Revision Adoption Checklist Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1441` validator for the local 2D objective-revision
adoption checklist.

This run checks whether the validator accepts the exact saved run `1440`
checklist and rejects controlled damage to route partitions, local-use flags,
`veryhigh` diagnostic evidence, blocked-route flags, guard readiness, and
downstream readiness states.

This run uses saved artifacts only. It does not execute new FDTD simulations,
launch GPU work, transfer to field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1442_local_2d_state_consistent_objective_revision_adoption_checklist_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_adoption_checklist_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_adoption_checklist_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_adoption_checklist_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_ADOPTION_CHECKLIST_SENSITIVITY.md
scripts/run_local_2d_state_consistent_objective_revision_adoption_checklist_sensitivity.py
scripts/test_local_2d_state_consistent_objective_revision_adoption_checklist_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         37
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        36
observed failure scenarios:        36
unexpected outcomes:               0
sensitivity ready:                 true
adoption validation ready:         true
adoption checklist ready:          true
drop-veryhigh ready:               true
majority-vote ready:               true
promote revised objective now:     false
broad radius tolerance promoted:   false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Interpretation

The adoption-checklist validator accepts the exact run `1440` checklist and
rejects 36 damaged variants. The rejected cases cover route-count drift, route
status drift, local-use flag drift, missing `veryhigh` failure labels,
blocked-route flag drift, guard-readiness drift, and false
broad/physical/GPU/field/FWI/3D readiness.

## Decision

Use runs `1440-1442` as the guarded local 2D objective-revision adoption
checklist. Broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims
remain blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_adoption_checklist_sensitivity.py
5 passed
```

Figure validation:

```text
4337x887, dynamic range=255
```
