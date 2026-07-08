# Experiment 1433: Local 2D Far-Radius Veryhigh Tie-Policy Audit

Date: 2026-06-28

## Purpose

Test whether the run `1432` wrong-x plateau can be repaired by selection policy
alone.

This run uses saved candidate profiles only. It does not execute new FDTD
simulations, launch GPU work, transfer to field data, run field FWI, or promote
3D/HPC work.

## Output

```text
outputs/experiments/1433_local_2d_state_consistent_far_radius_veryhigh_tie_policy_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_far_radius_veryhigh_exact_tie_policy_rows.csv
data/local_2d_state_consistent_far_radius_veryhigh_top_k_policy_rows.csv
data/local_2d_state_consistent_far_radius_veryhigh_tolerance_policy_rows.csv
data/local_2d_state_consistent_far_radius_veryhigh_tie_policy_audit_summary.json
figures/local_2d_state_consistent_far_radius_veryhigh_tie_policy_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_FAR_RADIUS_VERYHIGH_TIE_POLICY_AUDIT.md
scripts/run_local_2d_state_consistent_far_radius_veryhigh_tie_policy_audit.py
scripts/test_local_2d_state_consistent_far_radius_veryhigh_tie_policy_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
failed veryhigh perturbations:               5
exact tie policies tested:                   3
exact tie selections:                        15
exact tie selections landing on truth:       0
top-k required to include truth:             4 to 4
absolute tolerance required to include truth:0.0035579159181040702 to 0.0035579159181040702
relative tolerance required to include truth:0.15926191548530105 to 0.15926191548530105
truth-band candidate count:                  4 to 4
truth-band x span:                           3.0 to 3.0 mm
tie-only repair ready:                       false
tolerance unique repair ready:               false
objective revision needed:                   true
broad radius tolerance promoted:             false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

Exact tie-breaking cannot repair the failure because the truth is not part of
the best-misfit plateau. The truth appears only when the accepted set is widened
to four candidates or by allowing an absolute misfit tolerance of about
`0.0035579159181040702`, which creates a four-candidate x interval from 187 to
190 mm instead of a unique location.

## Decision

Use run `1433` to block tie-policy-only promotion of the `veryhigh` objective.
Future 2D work should revise or downweight the `veryhigh` observable rather
than treating the far-radius failure as a harmless tie.

Broad radius, physical, GPU, field-transfer, field-FWI, and 3D/HPC claims remain
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_far_radius_veryhigh_tie_policy_audit.py
5 passed
```

Figure validation:

```text
3076x863, dynamic range=255
```
