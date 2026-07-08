# Experiment 1432: Local 2D Far-Radius Veryhigh Plateau Diagnosis

Date: 2026-06-28

## Purpose

Diagnose the wrong-x plateau behind the run `1430` far-radius `veryhigh`
failures using saved candidate profiles.

This run does not execute new FDTD simulations, launch GPU work, transfer to
field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1432_local_2d_state_consistent_far_radius_veryhigh_plateau_diagnosis
```

Key artifacts:

```text
data/local_2d_state_consistent_far_radius_veryhigh_candidate_profiles.csv
data/local_2d_state_consistent_far_radius_veryhigh_plateau_summary.csv
data/local_2d_state_consistent_far_radius_veryhigh_plateau_diagnosis_summary.json
figures/local_2d_state_consistent_far_radius_veryhigh_plateau_diagnosis.png
docs/LOCAL_2D_STATE_CONSISTENT_FAR_RADIUS_VERYHIGH_PLATEAU_DIAGNOSIS.md
scripts/run_local_2d_state_consistent_far_radius_veryhigh_plateau_diagnosis.py
scripts/test_local_2d_state_consistent_far_radius_veryhigh_plateau_diagnosis.py
scripts/script_snapshot_manifest.json
```

## Result

```text
failed veryhigh perturbations:       5
plateau candidate count range:       3 to 3
truth rank range:                    4 to 4
truth-minus-best misfit range:       0.0035579159181040702 to 0.0035579159181040702
truth outside plateau:               true
veryhigh plateau diagnosis ready:    true
broad radius tolerance promoted:     false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

For every failed far-radius perturbation, the plateau is identical:

```text
x = 187.0, 188.0, and 189.0 mm tie at the best veryhigh misfit.
x = 190.0 mm, the truth, ranks fourth.
truth-minus-best misfit = 0.0035579159181040702
```

## Interpretation

The far-radius `veryhigh` failure is not a single wrong candidate. It is a flat
wrong-x plateau immediately left of truth. This explains why the selected x
sticks at 187 mm while several neighboring wrong x candidates have the same
misfit.

## Decision

Use run `1432` to focus future 2D diagnostics on the `veryhigh` objective
plateau and tie behavior. Broad radius, physical, GPU, field-transfer,
field-FWI, and 3D/HPC claims remain blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_far_radius_veryhigh_plateau_diagnosis.py
4 passed
```

Figure validation:

```text
2824x863, dynamic range=255
```
