# Experiment 44: Coordinate Optimizer Seed-Offset Stress

## Goal

Test whether the reporting-first coordinate optimizer still recovers the
multi-rebar geometry when the initial seed is farther from truth than the
compact replication matrix.

The compact four-seed matrix in Experiment 43 showed robust accuracy, but only
for a seed one grid step from truth:

```text
x/z initial error = 1 mm
radius initial error = 0.2 mm
```

This stage doubles the starting error:

```text
x/z initial error = 2 mm
radius initial error = 0.4 mm
```

## Planned Stress Run

Use a wider local coordinate window that still contains the truth:

```text
initial x = [148, 252, 348] mm
initial z = [92, 88, 92] mm
initial r = [6.4, 5.6, 6.4] mm
x offsets = [-2, -1, 0, 1, 2] mm
z offsets = [-2, -1, 0, 1, 2] mm
radius offsets = [-0.4, -0.2, 0, 0.2, 0.4] mm
```

This creates `125` candidates per target and `375` candidates for one pass
over three targets. At the current 1 mm GPU CPML runtime, the expected runtime
is roughly 1.5-2 hours.

## Decision Gates

Pass:

```text
all three targets update to exact x/z/r truth or within one 1 mm grid step,
confidence rows and ambiguity intervals remain present,
plots validate as nonblank and readable.
```

Branch:

```text
if a target stops at the seed instead of moving to truth, inspect top-k and run
a second coordinate pass before widening further.
if a target chooses the wrong radius but correct x/z, run a target-specific
dense radius profile around that final x/z.
if the search is accurate but very weak-confidence, keep the optimizer and
tighten reporting intervals rather than changing the objective.
```

## Planned Sequence

- [x] 090: seed 13 10% noise/source-mismatch with 2 mm x/z and 0.4 mm radius
  initial offset.
- [x] 091: focused target-0 revisit from the 090 post-pass state with a
  radius window spanning the selected high-radius branch and the true-radius
  branch.
- [x] Add tested helper logic for detecting weak high-radius branch updates
  and generating ambiguity-spanning revisit radius offsets.
- [x] 092: repeat the 2 mm stress with target order `1,2,0` to test whether
  correcting the stronger center/right targets before the left edge avoids the
  high-radius branch without an extra revisit.
- [x] 093: focused target-2 revisit from the 092 post-pass state with a
  radius window spanning the selected right-edge high-radius branch and the
  true-radius branch.
- [x] Add `--revisit-weak-high-radius-targets` to the coordinate optimizer
  runner and focused tests for the high-radius branch trigger.
- [x] 094: rerun the original 2 mm stress with the automated guarded revisit
  enabled.
- [x] 095: replicate guarded 2 mm stress on seed 21.
- [x] 096: aggregate guarded 2 mm stress runs for seeds 13 and 21.
- [ ] Replicate guarded 2 mm stress on seed 34.

## 090: 2 mm / 0.4 mm Seed-Offset Stress, Seed 13

Output:

```text
outputs/experiments/090_coordinate_optimizer_seed_offset2mm_noise10_seed13
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
  --initial-x-values-mm 148,252,348 \
  --initial-z-values-mm 92,88,92 \
  --initial-radius-values-mm 6.4,5.6,6.4 \
  --target-indices 0,1,2 \
  --passes 1 \
  --x-offsets-mm=-2:2:1 \
  --z-offsets-mm=-2:2:1 \
  --radius-offsets-mm=-0.4:0.4:0.2 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.10,13|source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13' \
  --update-case-label noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --progress-every 25 \
  --run-name coordinate_optimizer_seed_offset2mm_noise10_seed13
```

Result:

| Target | Final x/z/r [mm] | Nominal margin | Nominal label | Source-mismatch label | Ambiguity note |
| ---: | --- | ---: | --- | --- | --- |
| 0 | 150 / 91 / 6.8 | 3.323e-04 | weak | weak | interval spans z=90-91 mm and r=6.0-6.8 mm |
| 1 | 250 / 90 / 6.0 | 1.427e-03 | strong | strong | nominal interval includes small-radius branch |
| 2 | 350 / 90 / 6.0 | 2.711e-04 | weak | weak | interval spans z=90-91 mm and r=6.0-6.8 mm |

Summary:

- Final state:
  `x=[150,250,350] mm`, `z=[91,90,90] mm`, `r=[6.8,6.0,6.0] mm`.
- Center and right recovered exact truth despite the wrong left-edge state.
- Left target selected the deeper/larger-radius branch. The true
  `150/90/6.0` candidate was rank 2 in the nominal target-0 profile, only
  `3.323e-04` objective units worse than the selected `150/91/6.8` candidate.
- Confidence label counts: `weak=4`, `strong=2`.
- Fallback warnings appeared on all weak edge-target rows.
- Runtime was `6047.5 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `70.56`.

Interpretation:

The wider seed-offset stress did not fail by losing horizontal location. It
failed through a weak-confidence edge ambiguity between the true radius/depth
and a deeper/larger-radius branch. This matches the earlier single-rebar radius
bias problem and is exactly why the optimizer must not commit weak edge updates
without a fallback or confirmation rule.

Next decision:

Run a focused target-0 revisit from the post-pass state:

```text
current state: x=[150,250,350], z=[91,90,90], r=[6.8,6.0,6.0]
target: 0 only
x offsets: [-1,0,1]
z offsets: [-1,0,1]
radius offsets: [-0.8,-0.6,-0.4,-0.2,0.0]
```

If the revisit returns `150/90/6.0`, then the next implementation should add a
weak-margin confirmatory revisit for edge targets. If it still returns the high
radius branch, the next implementation should be conservative reporting rather
than automatic correction.

## 091: Focused Target-0 Revisit

Output:

```text
outputs/experiments/091_coordinate_optimizer_seed_offset2mm_target0_revisit_seed13
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
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 91,90,90 \
  --initial-radius-values-mm 6.8,6.0,6.0 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.8:0:0.2 \
  --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.10,13|source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13' \
  --update-case-label noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --progress-every 15 \
  --run-name coordinate_optimizer_seed_offset2mm_target0_revisit_seed13
```

Result:

| Case | Final target-0 x/z/r [mm] | Margin | Label | Ambiguity interval |
| --- | --- | ---: | --- | --- |
| noise10_seed13 | 150 / 90 / 6.0 | 2.263e-04 | weak | z=90-91 mm, r=6.0-6.8 mm |
| source_mismatch_noise10_seed13 | 150 / 90 / 6.0 | 3.117e-04 | weak | z=90-91 mm, r=6.0-6.8 mm |

Summary:

- Starting from the 090 post-pass state
  `x=[150,250,350]`, `z=[91,90,90]`, `r=[6.8,6.0,6.0]`, the focused revisit
  recovered exact truth:
  `x=[150,250,350]`, `z=[90,90,90]`, `r=[6.0,6.0,6.0]`.
- The revisit is still weak-confidence, so the correct output remains an
  interval/warning, not an unqualified radius.
- Runtime was `719.7 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `63.87`.

Implementation follow-up:

Added tested helpers in `inversion.multi_rebar_coordinate`:

```text
is_weak_high_radius_branch
weak_high_radius_revisit_targets
interval_offsets
revisit_radius_offsets_from_row
```

Focused validation passed:

```text
py_compile for coordinate modules
22 focused tests across coordinate, optimizer, confidence, and aggregate helpers
```

Interpretation:

The high-radius target-0 branch in 090 is recoverable after the other targets
are corrected. The next experiment should test whether target ordering can
avoid the extra revisit: run the same 2 mm stress as `target_indices=1,2,0`.
If that succeeds, the pipeline can use center/strong-target-first ordering plus
the weak high-radius revisit trigger as a safety net.

## 092: 2 mm Stress With Target Order 1,2,0

Output:

```text
outputs/experiments/092_coordinate_optimizer_seed_offset2mm_order120_noise10_seed13
```

Result:

| Target order step | Target | Final x/z/r [mm] | Nominal margin | Nominal label | Ambiguity note |
| ---: | ---: | --- | ---: | --- | --- |
| 1 | 1 | 250 / 90 / 6.0 | 1.485e-03 | strong | center target still robust |
| 2 | 2 | 350 / 91 / 6.6 | 2.252e-05 | weak | interval spans z=90-91 mm and r=6.0-6.8 mm |
| 3 | 0 | 150 / 90 / 6.0 | 2.751e-04 | weak | left recovers after center/right order change |

Summary:

- Final state:
  `x=[150,250,350] mm`, `z=[90,90,91] mm`, `r=[6.0,6.0,6.6] mm`.
- Reordering corrected the left edge but moved the high-radius/deeper branch to
  the right edge.
- The right-target true candidate `350/90/6.0` was rank 3 in the nominal
  profile, only `1.186e-04` objective units worse than the selected
  `350/91/6.6` branch.
- Confidence label counts: `weak=4`, `strong=2`.
- Runtime was `6022.5 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `66.61`.

Interpretation:

Target order alone is not a sufficient fix. It can decide which edge target
gets corrected first, but a weak edge update can still choose the high-radius
branch when the ambiguity interval contains the true lower-radius branch.

Next decision:

Run a focused target-2 revisit from the 092 post-pass state:

```text
current state: x=[150,250,350], z=[90,90,91], r=[6.0,6.0,6.6]
target: 2 only
x offsets: [-1,0,1]
z offsets: [-1,0,1]
radius offsets: [-0.6,-0.4,-0.2,0.0,0.2]
```

If target 2 recovers truth, the evidence supports a general rule: after a
larger-offset pass, revisit any weak edge target whose selected radius is the
high end of its ambiguity interval.

## 093: Focused Target-2 Revisit

Output:

```text
outputs/experiments/093_coordinate_optimizer_seed_offset2mm_target2_revisit_seed13
```

Result:

| Case | Final target-2 x/z/r [mm] | Margin | Label | Ambiguity interval |
| --- | --- | ---: | --- | --- |
| noise10_seed13 | 350 / 90 / 6.0 | 4.766e-04 | weak | z=90-91 mm, r=6.0-6.8 mm |
| source_mismatch_noise10_seed13 | 350 / 90 / 6.0 | 5.033e-04 | moderate | z=90-91 mm, r=6.0-6.8 mm |

Summary:

- Starting from the 092 post-pass state
  `x=[150,250,350]`, `z=[90,90,91]`, `r=[6.0,6.0,6.6]`, the focused revisit
  recovered exact truth:
  `x=[150,250,350]`, `z=[90,90,90]`, `r=[6.0,6.0,6.0]`.
- Runtime was `722.0 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `72.03`.

Interpretation:

The same confirmatory revisit mechanism works on both edge targets. Target
order alone is not enough, but weak high-radius edge branches are recoverable
when revisited with a radius window that spans the ambiguity interval after the
other target estimates have improved.

Implementation:

`run_multi_rebar_coordinate_optimizer.py` now supports:

```text
--revisit-weak-high-radius-targets
--revisit-x-offsets-mm
--revisit-z-offsets-mm
--revisit-radius-step-mm
```

The guarded mode detects weak rows that selected the high-radius endpoint of
their ambiguity interval, then appends a revisit step using radius offsets
derived from that interval. Default behavior is unchanged unless the flag is
passed.

Focused validation:

```text
py_compile passed for coordinate modules
23 focused tests passed
```

Next decision:

Run the original target order `0,1,2` stress with
`--revisit-weak-high-radius-targets` enabled. If it reproduces `090 + 091` in a
single automated run and ends at true x/z/r, promote guarded revisit as the
default policy for wider-offset coordinate searches.

## 094: Automated Guarded Revisit, 2 mm Seed 13

Output:

```text
outputs/experiments/094_coordinate_optimizer_seed_offset2mm_guarded_revisit_seed13
```

Command difference from 090:

```text
--revisit-weak-high-radius-targets
--revisit-x-offsets-mm=-1:1:1
--revisit-z-offsets-mm=-1:1:1
--revisit-radius-step-mm 0.2
```

Result:

| Step kind | Target | Final x/z/r [mm] | Nominal margin | Label | Note |
| --- | ---: | --- | ---: | --- | --- |
| main | 0 | 150 / 91 / 6.8 | 3.323e-04 | weak | high-radius branch reproduced |
| main | 1 | 250 / 90 / 6.0 | 1.427e-03 | strong | center corrected |
| main | 2 | 350 / 90 / 6.0 | 2.711e-04 | weak | right corrected but weak |
| revisit | 0 | 150 / 90 / 6.0 | 2.263e-04 | weak | guard recovered truth |

Summary:

- Initial state:
  `x=[148,252,348]`, `z=[92,88,92]`, `r=[6.4,5.6,6.4]`.
- Final state after automated revisit:
  `x=[150,250,350]`, `z=[90,90,90]`, `r=[6.0,6.0,6.0]`.
- The guard selected exactly one revisit target: target 0.
- Confidence rows: 8 total; 6 main rows plus 2 revisit rows.
- Runtime was `6693.9 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `66.22`.

Interpretation:

The guarded revisit reproduces the manual `090 + 091` recovery in a single
runner invocation. It should be promoted for wider-offset coordinate searches,
but it needs replication on another noise seed before being treated as stable.

Next decision:

Run the same guarded 2 mm stress on another seed, starting with seed 21. If it
also reaches the true final state, aggregate guarded stress runs and then move
to a targeted radius-confidence improvement branch rather than more coordinate
plumbing.

## 095: Automated Guarded Revisit, 2 mm Seed 21

Output:

```text
outputs/experiments/095_coordinate_optimizer_seed_offset2mm_guarded_revisit_seed21
```

Result:

| Step kind | Target | Final x/z/r [mm] | Nominal margin | Label | Note |
| --- | ---: | --- | ---: | --- | --- |
| main | 0 | 150 / 91 / 6.8 | 3.369e-04 | weak | high-radius branch reproduced |
| main | 1 | 250 / 90 / 6.0 | 1.660e-03 | strong | center corrected |
| main | 2 | 350 / 90 / 6.0 | 1.426e-04 | weak | right corrected but very weak |
| revisit | 0 | 150 / 90 / 6.0 | 5.112e-04 | moderate | guard recovered truth |

Summary:

- Initial state:
  `x=[148,252,348]`, `z=[92,88,92]`, `r=[6.4,5.6,6.4]`.
- Final state after automated revisit:
  `x=[150,250,350]`, `z=[90,90,90]`, `r=[6.0,6.0,6.0]`.
- The guard selected exactly one revisit target: target 0.
- Confidence rows: 8 total; 6 main rows plus 2 revisit rows.
- Runtime was `6741.3 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `64.41`.

Interpretation:

Seed 21 replicates seed 13: the main pass falls into the same weak high-radius
left-edge branch, then the guarded revisit recovers exact truth. The right edge
is correct but has very weak margin, so reporting still needs fallback warnings
and ambiguity intervals.

## 096: Guarded 2 mm Aggregate, Seeds 13 And 21

Output:

```text
outputs/experiments/096_coordinate_optimizer_seed_offset2mm_guarded_seed13_21_aggregate
```

Aggregate row result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 16 |
| Rows with true x/z/r | 12 |
| Weak labels | 11 |
| Moderate labels | 1 |
| Strong labels | 4 |
| Fallback warning rows | 11 |
| Radius margin min | 1.170e-04 |
| Radius margin mean | 6.964e-04 |
| Radius margin max | 2.262e-03 |

Per-target aggregate:

| Target | True rows | Labels | Fallback rows | Margin mean |
| ---: | ---: | --- | ---: | ---: |
| 0 | 4/8 | 7 weak, 1 moderate | 7 | 3.645e-04 |
| 1 | 4/4 | 4 strong | 0 | 1.849e-03 |
| 2 | 4/4 | 4 weak | 4 | 2.075e-04 |

Note:

The aggregate row count includes failed main-pass target-0 rows as intended.
Both full guarded runs end with true final x/z/r after the revisit step.

Plot validation:

```text
size 1977x971, dynamic range 255, standard deviation 62.87
```

Decision:

Continue one more guarded 2 mm seed replication with seed 34. If seed 34 also
passes final-state truth, treat guarded revisit as stable enough for this stage
and move to radius-confidence improvement rather than more coordinate plumbing.

## 097: Automated Guarded Revisit, 2 mm Seed 34

Output:

```text
outputs/experiments/097_coordinate_optimizer_seed_offset2mm_guarded_revisit_seed34
```

Result:

| Step kind | Target | Case | Final x/z/r [mm] | Radius margin | Label | Note |
| --- | ---: | --- | --- | ---: | --- | --- |
| main | 0 | noise10_seed34 | 150 / 91 / 6.8 | 5.618e-04 | weak | high-radius branch reproduced |
| main | 0 | source_mismatch_noise10_seed34 | 150 / 91 / 6.8 | 5.719e-04 | weak | same high-radius branch |
| main | 1 | noise10_seed34 | 250 / 90 / 6.0 | 1.653e-03 | strong | center corrected |
| main | 1 | source_mismatch_noise10_seed34 | 250 / 90 / 6.0 | 2.236e-03 | strong | center robust |
| main | 2 | noise10_seed34 | 350 / 90 / 6.0 | 9.039e-05 | weak | exact but very weak |
| main | 2 | source_mismatch_noise10_seed34 | 350 / 90 / 6.2 | 5.894e-06 | weak | mismatch almost flat between 6.0 and 6.2 |
| revisit | 0 | noise10_seed34 | 150 / 90 / 6.0 | 3.417e-04 | weak | guard recovered truth |
| revisit | 0 | source_mismatch_noise10_seed34 | 150 / 90 / 6.0 | 4.672e-04 | weak | guard recovered truth |

Summary:

- Initial state:
  `x=[148,252,348]`, `z=[92,88,92]`, `r=[6.4,5.6,6.4]`.
- Final state after automated revisit:
  `x=[150,250,350]`, `z=[90,90,90]`, `r=[6.0,6.0,6.0]`.
- The guard selected exactly one revisit target: target 0.
- Confidence rows: 8 total; 6 weak rows and 2 strong rows.
- Runtime was `6741.0 s`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `66.17`.

Interpretation:

Seed 34 confirms the guarded-revisit pattern from seeds 13 and 21. The main
pass again falls into the weak high-radius branch on the left edge, then the
guarded revisit recovers the true final state. The right edge remains a
radius-confidence problem: the nominal update case is exact, but the
source-mismatch case is almost flat and selects 6.2 mm by only `5.894e-06`.

## 098: Guarded 2 mm Aggregate, Seeds 13, 21, And 34

Output:

```text
outputs/experiments/098_coordinate_optimizer_seed_offset2mm_guarded_seed13_21_34_aggregate
```

Aggregate row result:

| Metric | Value |
| --- | ---: |
| Confidence rows | 24 |
| Rows with true x/z/r | 17 |
| Weak labels | 17 |
| Moderate labels | 1 |
| Strong labels | 6 |
| Fallback warning rows | 17 |
| Radius margin min | 5.894e-06 |
| Radius margin mean | 7.112e-04 |
| Radius margin max | 2.262e-03 |

Per-target aggregate:

| Target | True rows | Labels | Fallback rows | Margin mean |
| ---: | ---: | --- | ---: | ---: |
| 0 | 6/12 | 11 weak, 1 moderate | 11 | 4.049e-04 |
| 1 | 6/6 | 6 strong | 0 | 1.881e-03 |
| 2 | 5/6 | 6 weak | 6 | 1.544e-04 |

Note:

The aggregate row count includes failed main-pass target-0 rows before guarded
revisit. All three full guarded runs end with true final x/z/r after the
revisit step.

Plot validation:

```text
size 2956x971, dynamic range 255, standard deviation 64.12
```

Decision:

The guarded coordinate optimizer is stable enough for this 2 mm seed-offset
stage. The next stage should stop adding coordinate plumbing and instead attack
radius confidence directly. The immediate target is an edge-rebar
radius-confidence objective comparison that reuses the existing GPU candidate
framework and tests paper-backed weighting ideas against the current
source-profiled least-squares objective.
