# Experiment 190: Candidate Confidence Non-Finite Hardening

## Purpose

Harden the shared candidate confidence helper so non-finite margins and
misfits are reported as missing/unavailable instead of weak evidence.

## 657: Candidate Confidence Non-Finite Hardening

Output:

```text
outputs/experiments/657_candidate_confidence_nonfinite_hardening
```

Command:

```text
Patch inversion/candidate_confidence.py so confidence_label() treats NaN,
infinity, and non-numeric margins as missing, and ambiguity_interval() ignores
candidates with non-finite misfits. Add focused regression tests.
```

Artifacts:

```text
README.md
data/candidate_confidence_nonfinite_hardening.json
run_manifest.json
```

Validation:

```text
tests/test_candidate_confidence.py: 7 passed in 0.02 s
tests/test_coordinate_objective_diagnostic_report.py tests/test_coordinate_confidence_aggregate.py: 22 passed in 0.29 s
full pytest: 265 passed in 24.40 s
git diff --check: clean after run 657
```

## Interpretation

The objective-confidence and profile-confidence paths now match the broader
reporting hardening: non-finite numeric margins become missing confidence
labels, and non-finite candidate misfits do not define ambiguity intervals.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 657.

