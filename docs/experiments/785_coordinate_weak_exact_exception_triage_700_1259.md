# Experiment 785: Weak-Exact Exception Triage 700-1259

Date: 2026-06-17

## Purpose

CPU-only triage of the two exception runs identified by experiment 784. This
checks whether the remaining secondary-confirmation misses are substantive
enough to justify a narrow GPU follow-up, using only existing objective and
top-candidate artifacts.

No FDTD, FWI, or GPU command was run.

## Output

```text
outputs/experiments/1263_coordinate_weak_exact_exception_triage_700_1259
```

Artifacts:

```text
data/weak_exact_exception_triage.csv
data/weak_exact_exception_triage_summary.json
data/figure_validation.csv
figures/weak_exact_exception_triage.png
run_manifest.json
```

## Inputs

```text
outputs/experiments/1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259
outputs/experiments/785_coordinate_optimizer_variable_depth_radius_seed89_target1_sources7_txrx60_ringdown025_objectives
outputs/experiments/1136_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources8_txrx60_ringdown050_objectives
```

## Result

Policy label:

```text
weak_exact_exception_triage
```

Exception summary:

| Run | Target | Ringdown | Best secondary | Margin | Deficit from 5e-4 | Classification |
| ---: | --- | ---: | --- | ---: | ---: | --- |
| 1136 | target0 | 0.50 | `highband` | 4.953100e-4 | 4.690041e-6 | near-threshold modern monitor |
| 785 | target1 | 0.25 | `late` | 4.208206e-4 | 7.917944e-5 | legacy archive, no GPU priority |

Both exception rows still preserve the exact target geometry under their best
secondary objective. The difference is margin strength, not point recovery.

## Interpretation

Do not launch broad GPU sweeps for these exceptions.

Run 1136 is a modern target0/ringdown050 row, but its highband secondary margin
misses the cutoff by less than 1% of the cutoff. It is better treated as a
near-threshold monitor case than as a reason for a broad target0 sweep.

Run 785 is a legacy target1/ringdown025 row. It is useful as an archive caveat,
but it should not drive modern ringdown050 policy or immediate GPU use.

If a later paper table requires closing every exception, the only defensible
GPU work would be one narrow targeted probe for run 1136 or run 785, not an
unconstrained target sweep.

## Validation

Focused tests:

```text
tests/test_coordinate_weak_exact_exception_triage.py: 4 passed
```

The triage figure was validated as nonblank:

```text
weak_exact_exception_triage.png nonwhite=0.3597, dynamic range=255
```
