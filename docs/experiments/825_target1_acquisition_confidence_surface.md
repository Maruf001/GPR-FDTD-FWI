# Experiment 825: Target1 Acquisition-Confidence Surface

Date: 2026-06-18

## Purpose

Build a CPU-only target1 acquisition-confidence surface from the existing
700-1259 archive tables. This clarifies the remaining 2D target1 work without
launching FDTD, FWI, optimizer, or GPU experiments.

## Output

```text
outputs/experiments/1312_target1_acquisition_confidence_surface
```

Artifacts:

```text
data/target1_acquisition_confidence_surface.csv
data/target1_source_density_branch_policy.csv
data/target1_acquisition_confidence_surface_summary.json
data/figure_validation.csv
figures/target1_acquisition_confidence_surface.png
run_manifest.json
```

## Result

Policy label:

```text
target1_acquisition_confidence_surface_exact_but_nonmonotonic_cpu_no_gpu
```

Summary:

```text
canonical target1 rows:              133
exact target1 geometry rows:         133
base accepted rows:                   90
base weak-exact rows:                 43
late_high truth rows:                133
late_high accepted rows:             132
source-count settings:                 5
Tx/Rx settings:                        7
best source count, min n=5:             5 sources
best Tx/Rx, min n=3:                   60 mm
source-density series:                 17
all-accepted source series:             1
all-weak source series:                 3
source escalation helped:              10
lower source count was best:            7
last source worse than first:           8
terminal 11-source branches:            2 / 2 worse
gpu priority:                           none_now
```

## Interpretation

The target1 archive is not a localization failure: every canonical target1 row
recovers the exact x/z/r geometry. The unresolved behavior is confidence-policy
behavior under the strict canonical base gate.

Source density is not a monotonic rescue rule. Some branches improve at 9
sources, but 7 source-density branches are best at the lower source count and
both terminal 11-source branches get worse. The diagnostic `late_high`
objective confirms almost every target1 row, but it should remain a secondary
diagnostic rather than replacing the canonical base confidence gate.

No broad target1 GPU sweep is justified from this archive surface. Future GPU
work would need a new target1 hypothesis, not a repeat of source-count
escalation.

## Validation

Focused tests:

```text
tests/test_target1_acquisition_confidence_surface.py
4 passed
```

Figure validation:

```text
target1_acquisition_confidence_surface.png: 2654x1481,
nonwhite=0.3358, dynamic range=255
```
