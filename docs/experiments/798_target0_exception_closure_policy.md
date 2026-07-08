# Experiment 798: Target0 Exception Closure Policy

Date: 2026-06-17

## Purpose

CPU-only synthesis of the seed2504730781961 target0 weak-exact follow-up chain:

```text
1136: 8 sources, Tx/Rx=60.0 mm baseline control
1137: 8 sources, Tx/Rx=52.5 mm spacing probe
1138: 8 sources, Tx/Rx=50.0 mm spacing probe
1139: 8 sources, Tx/Rx=45.0 mm spacing probe
1140: 9 sources, Tx/Rx=60.0 mm source-density probe
```

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1276_target0_exception_closure_policy
```

Artifacts:

```text
data/target0_exception_closure_summary.json
data/target0_exception_closure_rows.csv
data/figure_validation.csv
figures/target0_exception_closure_policy.png
run_manifest.json
```

## Result

Policy label:

```text
target0_exception_closed_by_source_density
```

Summary:

```text
runs synthesized:                    1136, 1137, 1138, 1139, 1140
baseline base margin:                3.872998e-04
best 8-source spacing margin:        4.842585e-04 at Tx/Rx=45 mm
accepted source-density margin:      5.296469e-04 at 9 sources, Tx/Rx=60 mm
baseline to best spacing delta:      9.695872e-05
baseline to accepted rescue delta:   1.423471e-04
accepted run ids:                    1140
all runs truth exact:                true
all objective variants truth exact:  true
gpu priority:                        none
```

The spacing ladder was monotone and truth-preserving but did not cross the
base 5e-4 confidence cutoff. The existing 9-source Tx/Rx=60 run crosses the
base cutoff and closes the target0 exception without further GPU work.

## Interpretation

Do not run more target0 GPU work for this exception. Existing follow-ups show
that source-density, not smaller Tx/Rx spacing alone, is the effective rescue
mechanism for seed2504730781961 target0 under ringdown050.

Keep the recurring target0 late-window caveat: run 1140 passes base, highband,
veryhigh, and early_high, but late and late_high remain below the moderate
cutoff. That caveat is not a reason for another target0 sweep because all
objective variants preserve the exact target geometry.

## Validation

Focused tests:

```text
tests/test_target0_exception_closure_policy.py: 3 passed
```

Figure validation:

```text
target0_exception_closure_policy.png: 1804x835,
nonwhite=0.3908, dynamic range=255
```
