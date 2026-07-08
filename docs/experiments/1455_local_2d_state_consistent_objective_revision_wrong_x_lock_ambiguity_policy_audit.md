# Experiment 1455: Wrong-X Lock Ambiguity Policy Audit

Date: 2026-06-28

## Purpose

Test whether the x=187-189 wrong-lock plateau can be repaired by selection
policy alone.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1455_local_2d_state_consistent_objective_revision_wrong_x_lock_ambiguity_policy_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_wrong_x_lock_ambiguity_policy_rows.csv
data/local_2d_state_consistent_objective_revision_wrong_x_lock_ambiguity_policy_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_wrong_x_lock_ambiguity_policy_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_WRONG_X_LOCK_AMBIGUITY_POLICY_AUDIT.md
scripts/run_local_2d_state_consistent_objective_revision_wrong_x_lock_ambiguity_policy_audit.py
scripts/test_local_2d_state_consistent_objective_revision_wrong_x_lock_ambiguity_policy_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
wrong-lock objective rows:          12
policies audited:                   11
point policies audited:              3
best point-policy truth recovery:    0
smallest top-k truth set:            5
smallest tolerance truth set:        0.025
truth-containing set policies:       2
ambiguity policy audit ready:        true
unique point repair ready:           false
ambiguity set possible:              true
promote revised objective now:       false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

Policy result:

| Policy family | Best result |
| --- | --- |
| point selection | 0 of 12 rows recover truth |
| top-k ambiguity set | top-5 includes truth in 12 of 12 rows |
| misfit tolerance set | 0.025 tolerance includes truth in 12 of 12 rows |

## Interpretation

No point-selection rule tested here recovers the truth from the wrong-x
plateau. Truth can be included only by accepting a nonunique set, such as the
top five ranked candidates or a 0.025 misfit-tolerance band.

## Decision

Do not repair the wrong-x lock with tie-breaking or objective filtering. Treat
top-k or tolerance acceptance only as an ambiguity flag, and require new
disambiguating data or model design before broad-radius or physical-transfer
claims.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_wrong_x_lock_ambiguity_policy_audit.py
3 passed
```

Figure validation:

```text
3184x1130, dynamic range=255
```
