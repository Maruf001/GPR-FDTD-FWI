# Experiment 43: Coordinate Optimizer Noise Replication

## Goal

Stress the Stage 8 reporting-first coordinate optimizer with noisy observed
data before widening search windows or adding more optimization passes.

The key question is not only whether the final x/z/r values are correct. The
run must also report whether radius confidence remains weak, whether ambiguity
intervals widen, and whether source-profile nuisance parameters absorb the
intended source mismatch.

## Method

Use the same compact coordinate windows from Experiment 42:

```text
initial x = [149, 251, 349] mm
initial z = [91, 89, 91] mm
initial r = [6.2, 5.8, 6.2] mm
x offsets = [-1, 0, 1] mm
z offsets = [-1, 0, 1] mm
radius offsets = [-0.2, 0, 0.2] mm
```

This keeps the truth inside each per-target window and tests whether noisy
observed data break the sequential update logic.

## Decision Gates

Pass:

```text
all three targets update to x/z/r truth or stay within one grid step of truth,
all rows emit confidence labels, fallback warnings, ambiguity intervals, and
source-profile fields,
plots validate as nonblank and readable.
```

Fail / branch:

```text
if any target moves away from truth, inspect that target's top-k candidates and
run a second pass or wider local window before adding more seeds.
if confidence is weak but the best candidate is correct, replicate across more
noise seeds instead of changing the optimizer.
```

## Planned Sequence

- [x] 083: 10% noise seed 13 plus source-mismatch noise seed 13.
- [x] 084: 10% noise seed 21 plus source-mismatch noise seed 21.
- [x] 085: aggregate coordinate optimizer confidence across seeds 13 and 21.
- [x] 086: repeat with seed 34 as an independent coordinate update path.
- [x] 087: aggregate coordinate optimizer confidence across seeds 13, 21, and 34.
- [x] 088: repeat with seed 55 as an independent coordinate update path.
- [x] 089: 4-seed aggregate for seeds 13, 21, 34, and 55.
- [x] Decision after four-seed aggregate: move to a harder seed-offset stress
  test before changing objective or adding another compact seed.

## 083: 10% Noise Seed 13

Output:

```text
outputs/experiments/083_coordinate_optimizer_noise10_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-mm 6.0 \
  --initial-x-values-mm 149,251,349 \
  --initial-z-values-mm 91,89,91 \
  --initial-radius-values-mm 6.2,5.8,6.2 \
  --target-indices 0,1,2 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.10,13|source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13' \
  --update-case-label noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --progress-every 9 \
  --run-name coordinate_optimizer_noise10_seed13
```

Result:

| Target | Final x/z/r [mm] | Nominal margin | Nominal label | Source-mismatch label | Ambiguity note |
| ---: | --- | ---: | --- | --- | --- |
| 0 | 150 / 90 / 6.0 | 3.219e-04 | weak | weak | radius interval includes 6.2 mm |
| 1 | 250 / 90 / 6.0 | 1.116e-03 | strong | strong | nominal interval includes 5.6 mm and z=89 mm |
| 2 | 350 / 90 / 6.0 | 4.766e-04 | weak | moderate | radius interval includes 6.2 mm |

Summary:

- Final state recovered exact truth from the perturbed seed:
  `x=[150,250,350] mm`, `z=[90,90,90] mm`, `r=[6,6,6] mm`.
- Confidence label counts across the two observed cases per target:
  `weak=3`, `moderate=1`, `strong=2`.
- Fallback warnings appeared on the 3 weak rows.
- The source profiler recovered the intended source parameters:
  nominal rows selected `fc=1.0`, `shift=0 ps`; source-mismatch rows selected
  `fc=1.1`, `shift=-50 ps`.
- Runtime was `1295.6 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `72.26`.

Interpretation:

The sequential coordinate optimizer is stable for seed 13 under 10% noise and
source mismatch, but radius must still be reported with confidence/fallback
fields. The ambiguity interval is doing useful work here: it exposes the nearby
6.2 mm radius candidate even when the best estimate is the true 6.0 mm.

Next decision:

Repeat the same compact noisy coordinate run with seed 21. If seed 21 also
recovers the exact target state, build an aggregate report before widening the
search or adding more coordinate passes.

## 084: 10% Noise Seed 21

Output:

```text
outputs/experiments/084_coordinate_optimizer_noise10_seed21
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-mm 6.0 \
  --initial-x-values-mm 149,251,349 \
  --initial-z-values-mm 91,89,91 \
  --initial-radius-values-mm 6.2,5.8,6.2 \
  --target-indices 0,1,2 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'noise10_seed21:1.0,0.0,1.0,0.10,21|source_mismatch_noise10_seed21:1.1,-50.0,1.1,0.10,21' \
  --update-case-label noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --progress-every 9 \
  --run-name coordinate_optimizer_noise10_seed21
```

Result:

| Target | Final x/z/r [mm] | Nominal margin | Nominal label | Source-mismatch label | Ambiguity note |
| ---: | --- | ---: | --- | --- | --- |
| 0 | 150 / 90 / 6.0 | 6.093e-04 | moderate | weak | radius interval includes 6.2 mm |
| 1 | 250 / 90 / 6.0 | 1.282e-03 | strong | strong | nominal interval includes 5.6 mm and z=89 mm |
| 2 | 350 / 90 / 6.0 | 3.450e-04 | weak | weak | radius interval includes 6.2 mm |

Summary:

- Final state recovered exact truth from the perturbed seed:
  `x=[150,250,350] mm`, `z=[90,90,90] mm`, `r=[6,6,6] mm`.
- Confidence label counts: `weak=3`, `moderate=1`, `strong=2`.
- Fallback warnings appeared on the 3 weak rows.
- Source-profile selection again matched the intended nuisance source settings.
- Runtime was `1299.8 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `71.18`.

Interpretation:

Seed 21 independently confirms the seed-13 result. The coordinate update path
is stable, but edge-target radius confidence remains weaker than the center
target. The ambiguity intervals are therefore not cosmetic; they are part of
the valid result.

## 085: Seed 13/21 Aggregate

Output:

```text
outputs/experiments/085_coordinate_optimizer_noise_seed13_21_aggregate
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_coordinate_confidence_aggregate.py \
  outputs/experiments/083_coordinate_optimizer_noise10_seed13/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/084_coordinate_optimizer_noise10_seed21/data/multi_rebar_coordinate_optimizer_summary.json \
  --run-name coordinate_optimizer_noise_seed13_21_aggregate
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 12 |
| Rows with true x/z/r | 12 |
| Weak labels | 6 |
| Moderate labels | 2 |
| Strong labels | 4 |
| Fallback warning rows | 6 |
| Radius margin min | 3.184e-04 |
| Radius margin mean | 7.725e-04 |
| Radius margin max | 1.856e-03 |

Per-target aggregate:

| Target | Rows true x/z/r | Labels | Fallback rows | Margin mean |
| ---: | ---: | --- | ---: | ---: |
| 0 | 4/4 | 3 weak, 1 moderate | 3 | 4.399e-04 |
| 1 | 4/4 | 4 strong | 0 | 1.467e-03 |
| 2 | 4/4 | 3 weak, 1 moderate | 3 | 4.108e-04 |

Plot validation:

```text
size 1718x971, dynamic range 255, standard deviation 72.51
```

Decision:

The two-seed aggregate is strong enough to continue seed replication rather
than changing the optimizer. Run seed 34 next as an independent coordinate
update path. Do not batch multiple update seeds into one coordinate run unless
the goal is only to score extra observed cases on an already chosen path,
because the coordinate state is updated from one case label at a time.

## 086: 10% Noise Seed 34

Output:

```text
outputs/experiments/086_coordinate_optimizer_noise10_seed34
```

Result:

| Target | Final x/z/r [mm] | Nominal margin | Nominal label | Source-mismatch label | Ambiguity note |
| ---: | --- | ---: | --- | --- | --- |
| 0 | 150 / 90 / 6.0 | 4.322e-04 | weak | weak | radius interval includes 6.2 mm |
| 1 | 250 / 90 / 6.0 | 1.474e-03 | strong | strong | ambiguity interval stays at 6.0 mm |
| 2 | 350 / 90 / 6.0 | 2.930e-04 | weak | weak | source-mismatch interval reaches 6.4 mm |

Summary:

- Final state recovered exact truth from the perturbed seed:
  `x=[150,250,350] mm`, `z=[90,90,90] mm`, `r=[6,6,6] mm`.
- Confidence label counts: `weak=4`, `strong=2`.
- The weakest row so far is the right/source-mismatch case:
  margin `1.947e-04`, ambiguity radius interval `6.0-6.4 mm`.
- Runtime was `1299.4 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `72.35`.

Interpretation:

Seed 34 still passes the accuracy gate, but it strengthens the conclusion that
the right target can be correct and still low-confidence under source-mismatch
noise. The final report must not collapse this to only `r=6.0 mm`; it must
include the ambiguity interval.

## 087: Seed 13/21/34 Aggregate

Output:

```text
outputs/experiments/087_coordinate_optimizer_noise_seed13_21_34_aggregate
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 18 |
| Rows with true x/z/r | 18 |
| Weak labels | 10 |
| Moderate labels | 2 |
| Strong labels | 6 |
| Fallback warning rows | 10 |
| Radius margin min | 1.947e-04 |
| Radius margin mean | 7.786e-04 |
| Radius margin max | 1.856e-03 |

Per-target aggregate:

| Target | Rows true x/z/r | Labels | Fallback rows | Margin mean |
| ---: | ---: | --- | ---: | ---: |
| 0 | 6/6 | 5 weak, 1 moderate | 5 | 4.517e-04 |
| 1 | 6/6 | 6 strong | 0 | 1.529e-03 |
| 2 | 6/6 | 5 weak, 1 moderate | 5 | 3.552e-04 |

Plot validation:

```text
size 2222x971, dynamic range 255, standard deviation 73.96
```

Decision:

Run seed 55 as the fourth independent coordinate update path. If it also
recovers all three targets, build a 4-seed aggregate before moving to harder
tests such as wider seed offsets, second coordinate passes, or broader local
windows.

## 088: 10% Noise Seed 55

Output:

```text
outputs/experiments/088_coordinate_optimizer_noise10_seed55
```

Result:

| Target | Final x/z/r [mm] | Nominal margin | Nominal label | Source-mismatch label | Ambiguity note |
| ---: | --- | ---: | --- | --- | --- |
| 0 | 150 / 90 / 6.0 | 3.579e-04 | weak | weak | radius interval includes 6.2 mm |
| 1 | 250 / 90 / 6.0 | 1.504e-03 | strong | strong | source-mismatch interval includes 5.6 mm and z=89 mm |
| 2 | 350 / 90 / 6.0 | 2.619e-04 | weak | weak | radius interval includes 6.2 mm |

Summary:

- Final state recovered exact truth from the perturbed seed:
  `x=[150,250,350] mm`, `z=[90,90,90] mm`, `r=[6,6,6] mm`.
- Confidence label counts: `weak=4`, `strong=2`.
- Fallback warnings appeared on the 4 weak rows.
- Runtime was `1300.8 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `74.49`.

Interpretation:

Seed 55 matches the prior noisy seeds: exact geometry recovery, strong center
target, and weak edge targets. This completes the planned compact four-seed
coordinate replication.

## 089: Four-Seed Coordinate Aggregate

Output:

```text
outputs/experiments/089_coordinate_optimizer_noise_seed13_21_34_55_aggregate
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 24 |
| Rows with true x/z/r | 24 |
| Weak labels | 14 |
| Moderate labels | 2 |
| Strong labels | 8 |
| Fallback warning rows | 14 |
| Radius margin min | 1.947e-04 |
| Radius margin mean | 7.615e-04 |
| Radius margin max | 1.856e-03 |

Per-target aggregate:

| Target | Rows true x/z/r | Labels | Fallback rows | Margin mean |
| ---: | ---: | --- | ---: | ---: |
| 0 | 8/8 | 7 weak, 1 moderate | 7 | 4.418e-04 |
| 1 | 8/8 | 8 strong | 0 | 1.508e-03 |
| 2 | 8/8 | 7 weak, 1 moderate | 7 | 3.344e-04 |

Plot validation:

```text
size 2957x971, dynamic range 255, standard deviation 73.73
```

Decision:

The compact 10% noise/source-mismatch coordinate optimizer is robust across
seeds 13, 21, 34, and 55. The next best experiment is not another compact seed.
Move to a harder seed-offset stress test with a 2 mm x/z initial error and a
0.4 mm radius initial error, using wider local coordinate windows that still
contain the truth.
