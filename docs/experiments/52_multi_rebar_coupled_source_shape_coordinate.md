# Experiment 52: Coupled Multi-Rebar Source-Shape Coordinate Stress

## Goal

Move beyond fixed-neighbor local source-shape profiles.

Experiments 425-439 showed that one target at a time selects the true x/z/r
when the neighboring rebars stay fixed at truth. This tracker starts the next
question:

```text
If neighboring rebar radii are initially wrong and the coordinate optimizer
updates targets sequentially, does the source-shape coefficient-fit objective
still recover the true multi-rebar state?
```

## Implementation

Extended the reporting-first coordinate optimizer so it can reuse the
source-shape model that fixed the single-rebar and fixed-neighbor multi-rebar
ringdown cases:

```text
run_multi_rebar_coordinate_optimizer.py
inversion/candidate_confidence.py
tests/test_multi_rebar_coordinate_optimizer.py
tests/test_candidate_confidence.py
```

New coordinate-optimizer controls:

```text
--fit-ringdown-coefficient
--source-ringdown-delay-ps
--source-ringdown-frequency-scale
```

The coordinate confidence report now preserves fitted source-shape fields:

```text
source_ringdown_scale
source_ringdown_delay_ps
source_ringdown_frequency_scale
source_primary_coefficient
source_ringdown_coefficient
```

Validation after the implementation patch:

```text
44 passed in 0.37 s
```

## 440: Seed55 Coupled Compact Pass

Output:

```text
outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --initial-radius-values-mm 6.2,6.2,6.2 \
  --target-indices 1,0,2 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --update-case-label source_mismatch_ringdown025_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0' \
  --top-k 12 \
  --progress-every 9 \
  --run-name multi_rebar_coupled_source_shape_seed55_compact_pass
```

Purpose:

```text
Start all three radii at 6.2 mm, then update center, left, right. The center
target is updated first so it is evaluated while both neighbors are wrong.
```

Runtime and count:

```text
2642.63 s
3 coordinate steps
27 candidates per step
1 observed source-mismatch/ringdown/noise case
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
```

State history:

| Step | Target | State radii before [mm] | Updated x/z/r [mm] | Margin | Label |
| ---: | ---: | --- | --- | ---: | --- |
| 1 | 1 | 6.2 / 6.2 / 6.2 | 250 / 90 / 6.0 | 1.228e-04 | weak |
| 2 | 0 | 6.2 / 6.0 / 6.2 | 150 / 90 / 6.0 | 2.948e-04 | weak |
| 3 | 2 | 6.0 / 6.0 / 6.2 | 350 / 90 / 6.0 | 2.185e-04 | weak |

Final state:

```text
x = [150.0, 250.0, 350.0] mm
z = [90.0, 90.0, 90.0] mm
r = [6.0, 6.0, 6.0] mm
```

Source-shape recovery:

| Target | Fitted fc scale | Fitted shift [ps] | Fitted ringdown scale | Ringdown coefficient |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1.1 | -50 | 0.2510 | 0.2748 |
| 0 | 1.1 | -50 | 0.2505 | 0.2753 |
| 2 | 1.1 | -50 | 0.2503 | 0.2756 |

Top-candidate pattern:

```text
All three coordinate steps ranked true r=6.0 first and r=6.2 second at true
x/z. The ambiguity interval is therefore a local 6.0-6.2 mm radius interval,
not a shifted-location or high-radius branch.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1545x903 px, dynamic range 255, grayscale std 51.2725
```

Figure notes:

```text
outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass/figures/FIGURE_NOTES.md
```

## Interpretation

Experiment 440 is the first coupled-neighbor source-shape pass. It starts with
all three radii wrong at 6.2 mm and recovers the exact true all-target state in
one sequential coordinate pass.

The important caveat is confidence, not point accuracy. All three rows are
weak because r=6.2 mm remains close to r=6.0 mm. This means the result should
be reported as a correct point estimate with a narrow radius ambiguity interval,
not as a high-confidence exact-size claim.

## Next Decision

Run one of these, in order of value:

```text
1. Repeat the coupled source-shape coordinate pass from a harder x/z/r
   perturbed seed so neighboring locations are also initially wrong.
2. If that passes, aggregate coupled source-shape coordinate rows before moving
   to dense or two-pass variants.
3. Do not run a dense coupled Stage 4C source-shape sweep yet; the compact
   coupled seed should be stressed first because dense coupled grids are much
   more expensive.
```
