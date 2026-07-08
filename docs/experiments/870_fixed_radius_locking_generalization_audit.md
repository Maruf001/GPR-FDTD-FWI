# Experiment 870: Fixed-Radius Locking Generalization Audit

Date: 2026-06-22

## Purpose

Test whether the fixed-radius target-locking mechanism validated by run `1358`
appears elsewhere in the saved detector candidate tables.

This is a CPU-only audit. It reads existing candidate tables from the guarded
fixed-radius detector pilots and does not run FDTD, GPU kernels, field FWI,
3D/HPC work, or neural-network training.

The scientific question is narrow:

```text
Was the successful 1358 unlock a general update-order policy signal,
or only a single-branch mechanism result?
```

## Output

```text
outputs/summary_tables/134_local_2d_detector_fixed_radius_locking_generalization_audit
```

Key artifacts:

```text
data/local_2d_detector_fixed_radius_locking_generalization_rows.csv
data/local_2d_detector_fixed_radius_locking_generalization_validation.csv
data/local_2d_detector_fixed_radius_locking_generalization_gates.csv
data/local_2d_detector_fixed_radius_locking_generalization_summary.json
figures/local_2d_detector_fixed_radius_locking_generalization.png
figures/FIGURE_NOTES.md
```

## Result

```text
design runs audited:                 3
candidate-table steps audited:        9
near-tie threshold:                   5%
eligible lock opportunities:          1
validated lock opportunities:         1
unvalidated lock opportunities:       0
validation run:                       1358
validation final L-infinity error:    0 mm
validation guard within caps:         true
new guarded GPU probe ready:          false
broad GPU queue ready:                false
detector-seeded FWI ready:            false
field transfer ready:                 false
```

The only eligible lock opportunity is the already validated `1357` target-1
step:

```text
greedy candidate: [251, 89] mm
lock candidate:   [250, 90] mm
lock rank:        2
relative penalty: 3.4146%
```

That lock is exactly the mechanism tested by `1358`, where target 2 then moved
to exact truth.

## Interpretation

The result strengthens the mechanism claim but weakens the general-policy
claim.

The validated statement is:

```text
In the repaired target2 close14 seed21 nominal branch, a near-tie target-1
lock removes the downstream non-overlap exclusion and allows target 2 to
recover exact geometry.
```

The unsupported statement is:

```text
The current detector should use a general target-locking policy across cases.
```

The saved candidate tables do not expose another unresolved eligible lock
opportunity. Therefore no new GPU probe is justified from this audit.

## Validation

Focused tests:

```text
tests/test_local_2d_detector_fixed_radius_locking_generalization_audit.py
3 passed
```

Figure validation:

```text
local_2d_detector_fixed_radius_locking_generalization.png:
2653x903, dynamic range=255
```

## Decision

Stop the fixed-radius locking branch at a single-branch mechanism claim. The
next work should either update paper-facing synthesis tables or move to
independent field-QC/provenance work. Do not launch a new detector GPU probe,
broad GPU queue, detector-seeded FWI, or field transfer from this result.
