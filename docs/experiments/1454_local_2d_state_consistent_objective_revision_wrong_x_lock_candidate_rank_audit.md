# Experiment 1454: Wrong-X Lock Candidate Rank Audit

Date: 2026-06-28

## Purpose

Audit the candidate-rank structure behind the all-objective wrong-x locks
identified in run `1453`.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1454_local_2d_state_consistent_objective_revision_wrong_x_lock_candidate_rank_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_wrong_x_lock_candidate_rank_rows.csv
data/local_2d_state_consistent_objective_revision_wrong_x_lock_case_summary.csv
data/local_2d_state_consistent_objective_revision_wrong_x_lock_candidate_rank_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_wrong_x_lock_candidate_rank_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_WRONG_X_LOCK_CANDIDATE_RANK_AUDIT.md
scripts/run_local_2d_state_consistent_objective_revision_wrong_x_lock_candidate_rank_audit.py
scripts/test_local_2d_state_consistent_objective_revision_wrong_x_lock_candidate_rank_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
wrong-lock perturbations:            2
wrong-lock objective rows:          12
187-188-189 plateau rows:           12
all rows share 187-188-189 plateau: true
lowest-plateau x selected rows:     12
truth rank min:                      4
truth rank max:                      5
truth inside top plateau rows:       0
median truth gap to best:            0.007440443830871349
max truth gap to best:               0.023872185127222008
rank audit ready:                    true
promote revised objective now:       false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The all-objective wrong lock is a candidate-rank plateau: every audited
objective has x=187, 188, and 189 mm tied at the best misfit, while the truth
x=190 mm sits just outside that plateau at rank 4 or 5. The reported x=187
selection is the lowest-x representative of the plateau, not a unique isolated
minimum.

## Decision

Use run `1454` to target the next 2D design: the branch needs a disambiguator
that separates x=187-189 from x=190, not another objective-filtering policy.
Keep broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_wrong_x_lock_candidate_rank_audit.py
3 passed
```

Figure validation:

```text
3116x1384, dynamic range=255
```
