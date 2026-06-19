# Experiment 799: Modern Ringdown050 Exception Status

Date: 2026-06-17

## Purpose

CPU-only synthesis of the weak-exact secondary-confirmation exception state
after the target0 closure in experiment 798. This checks whether any modern
ringdown050 exception still justifies local GPU work.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1277_modern_ringdown050_exception_status
```

Artifacts:

```text
data/modern_ringdown050_exception_status_rows.csv
data/modern_ringdown050_exception_status_summary.json
data/figure_validation.csv
figures/modern_ringdown050_exception_status.png
run_manifest.json
```

## Inputs

```text
outputs/experiments/1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259
outputs/experiments/1263_coordinate_weak_exact_exception_triage_700_1259
outputs/experiments/1276_target0_exception_closure_policy
```

## Result

Policy label:

```text
modern_ringdown050_no_open_exception_gpu_priority_none
```

Summary:

```text
exception rows:                    2
modern ringdown050 exceptions:     1
modern ringdown050 closed:         1
modern ringdown050 open:           0
legacy exceptions:                 1
gpu priority:                      none
```

Per-target status:

| Target | Exception | Status |
| --- | --- | --- |
| target0 | run 1136, ringdown050 | closed by existing source-density follow-up 1140 |
| target1 | run 785, ringdown025 | legacy archive caveat, no GPU priority |
| target2 | none | no secondary exception |

## Interpretation

No modern ringdown050 weak-exact exception remains open after the target0
source-density closure. Keep legacy ringdown025 run 785 as an archive caveat,
not a local GPU priority.

Do not launch a synthetic GPU exception probe from the current weak-exact
policy state.

## Validation

Focused tests:

```text
tests/test_modern_ringdown050_exception_status.py: 5 passed
```

Figure validation:

```text
modern_ringdown050_exception_status.png: 1515x835,
nonwhite=0.3371, dynamic range=255
```
