# Experiment 792: Close50 Effective Offset Policy

Date: 2026-06-17

## Purpose

CPU-only synthesis of the close50 target2 threshold branch after the requested
Tx/Rx 29.375 mm probe duplicated the requested 28.75 mm effective receiver
layout under 1 mm nearest receiver sampling.

No FDTD, FWI, GPU kernels, or new synthetic inversion runs were launched.

## Output

```text
outputs/experiments/1270_close50_effective_offset_policy
```

Artifacts:

```text
data/close50_effective_offset_rows.csv
data/close50_effective_offset_summary.json
data/figure_validation.csv
figures/close50_effective_offset_policy.png
run_manifest.json
```

## Inputs

```text
outputs/experiments/1268_close50_threshold_policy_after_txrx28p75_pilot/data/close50_threshold_by_txrx.csv
outputs/experiments/1269_coordinate_optimizer_close50_seed21_sources4_txrx29p375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

## Result

Policy label:

```text
close50_nearest_receiver_bisection_quantized_stop
```

Effective-offset table:

| Requested Tx/Rx | Effective offsets | Branch label |
| ---: | --- | --- |
| 25 mm | `[25, 25, 25, 25]` mm | `mixed_or_ambiguous` |
| 27.5 mm | `[28, 27, 28, 28]` mm | `single_seed_exact_but_nonclean` |
| 28.75 mm | `[29, 29, 29, 29]` mm | `single_seed_exact_but_nonclean` |
| 29.375 mm | `[29, 29, 29, 29]` mm | `duplicate_effective_geometry_check` |
| 30 mm | `[30, 30, 30, 30]` mm | `clean_replicated` |
| 35 mm | `[35, 35, 35, 35]` mm | `clean_replicated` |
| 40 mm | `[40, 40, 40, 40]` mm | `clean_replicated` |

Summary:

```text
duplicate requested offsets: 29.375 mm
last non-clean mean effective offset: 29 mm
first clean replicated mean effective offset: 30 mm
```

## Interpretation

Stop nearest-sampled sub-millimeter bisection on this close50 branch. The
requested 29.375 mm probe duplicates the effective 29 mm receiver layout from
28.75 mm, while requested 30 mm maps to effective 30 mm and is already clean in
the replicated aggregate.

If the below-30 transition must be studied, use one deliberately scoped linear
receiver-sampling pilot or a finer-grid pilot. Do not spend GPU time on more
nearest-sampled requested midpoint offsets between 28.75 and 30 mm.

## Validation

Focused tests:

```text
tests/test_close50_effective_offset_policy.py: 3 passed
```

The effective-offset figure was validated as nonblank:

```text
close50_effective_offset_policy.png nonwhite=0.0675, dynamic range=255
```
