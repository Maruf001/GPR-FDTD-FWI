# Plain Results Summary: Single-Rebar Pipeline

## What We Are Trying To Do

We are solving the smallest useful GPR inverse problem before moving to multiple
rebars:

```text
Find one circular rebar's x position, depth, and radius from a synthetic B-scan.
```

The unknowns are:

```text
x center, z center, radius
```

All are measured in meters internally and usually reported in millimeters.

## What Worked So Far

The current best workflow is:

```text
1. Run a cheaper 2 mm-grid global search to find the approximate basin.
2. Run a 1 mm-grid local Powell refinement to improve x and z.
3. Run a final deterministic 1 mm local grid polish to fix radius.
```

This matters because the 1 mm local Powell refinement found the location well
but still returned a radius that was too large:

```text
truth:     x=250.0 mm, z=90.0 mm, radius=6.0 mm
Powell:    x=249.5 mm, z=90.7 mm, radius=7.0 mm
```

The final grid polish corrected that:

```text
grid polish: x=250.0 mm, z=89.75 mm, radius=6.0 mm
data error:  0
model error: 0
```

The reported `z=89.75 mm` is not a scientific concern in this exact synthetic
case. On the 1 mm hard grid, several nearby z values produce the exact same
material mask as the true `z=90.0 mm` model.

## Why Radius Was Hard

Radius was not hard because the signal had no radius information. It was hard
because of the discrete grid.

The code represents the circular rebar on a finite grid. With a hard-grid
circle, small changes in physical radius or depth can produce the same grid-cell
mask, or a nearby mask with a very similar waveform. A smooth optimizer such as
Powell can stop in a nearby low-error depth/radius tradeoff.

The important observed tradeoff was:

```text
slightly deeper z + larger radius
```

This matched the waveform almost as well as the true geometry, even though the
radius was biased high.

## What The Radius Profiles Showed

At the Powell result from run 009:

```text
x=249.533 mm, z=90.653 mm
best radius ≈ 6.8 mm
```

At the same x but true depth:

```text
x=249.533 mm, z=90.000 mm
best radius = 6.0 mm
```

So the high radius was a depth/radius coupling, not a pure radius-estimation
failure.

## What Grid Polish Does

Grid polish takes the optimizer's approximate answer and tries a small set of
nearby candidates on an absolute millimeter grid.

Example:

```text
optimizer seed: x=249.533 mm, z=90.653 mm, radius=6.955 mm
grid candidates:
  x near 250 mm
  z from about 89.75 to 91.50 mm
  radius from about 6.0 to 7.9 mm
```

In the exact synthetic case, it found:

```text
x=250.0 mm, z=89.75 mm, radius=6.0 mm, objective=0
```

That means the recovered model produces the same B-scan as the synthetic
truth and the same rasterized material model.

## Important Warnings

Do not over-interpret sub-millimeter `z` differences in hard-grid runs. The
grid spacing is 1 mm, and the circle is rasterized.

Do not use `--polish-stop-misfit 0` on noisy or field data. It is only valid
for exact synthetic data where a perfect zero-error solution can exist.

For noisy data, grid polish should evaluate the local grid or stop at a
noise-aware threshold.

## What Happened With Noise

We added controlled Gaussian noise to the observed B-scans and repeated the
staged workflow.

At 1% RMS noise:

```text
Powell radius:  about 7.0 mm
polished radius: 6.0 mm
data error:      about 1.0%, matching the injected noise
model error:     0
```

At 5% RMS noise:

```text
Powell radius:  about 7.0 mm
polished radius: 6.0 mm
data error:      about 5.0%, matching the injected noise
model error:     0
```

So, for the current synthetic single-rebar case, grid polish still recovers the
correct rasterized geometry under moderate controlled noise.

## Making Grid Polish Cheaper

The first robust polish used a fine local grid:

```text
z step:      0.25 mm
radius step: 0.10 mm
candidates: 160
```

That worked, but took about 855 seconds for the polish step in the 5% noisy
run.

A coarser polish grid also worked on the same 5% noisy case:

```text
z step:      0.50 mm
radius step: 0.20 mm
candidates: 40
```

It recovered the same model and objective:

```text
fine polish:   x=250.0 mm, z=89.75 mm, radius=6.0 mm, data error=5.021%
coarse polish: x=250.0 mm, z=90.00 mm, radius=6.0 mm, data error=5.021%
```

The depth difference is only a grid representation detail. Both solutions have
zero model error on the 1 mm hard grid.

We repeated the coarse-polish run with a second 5% noise seed. It also
recovered the true rasterized geometry:

```text
seed 13: x=250.0 mm, z=90.0 mm, radius=6.0 mm, data error=5.021%
seed 21: x=250.0 mm, z=90.0 mm, radius=6.0 mm, data error=4.983%
```

At 10% RMS noise, the coarse polish still recovered the true rasterized model
for seed 13:

```text
seed 13: x=250.0 mm, z=90.0 mm, radius=6.0 mm, data error=10.005%
```

The 10% case had a small objective margin over the nearby high-radius basin, so
it should be treated as a stress case rather than a settled robustness result.

Current practical recommendation:

```text
Routine development: --grid-polish --grid-polish-preset coarse
Audit/final checks:  --grid-polish --grid-polish-preset fine
```

Grid-polish summaries now also save the best few local candidates, not just the
winner. That makes future reports clearer because we can say how close the next
best depth/radius tradeoff was to the selected model.

For the 10% stress case, the top candidates showed:

```text
best:        radius=6.0 mm, objective=1.9916e-01
next radius: radius=6.2 mm, objective=1.9972e-01
```

That is a small but still positive margin for the true radius.

## Where The Detailed Logs Are

Main single-rebar pipeline:

```text
docs/experiments/11_single_rebar_pipeline.md
```

Radius-refinement work:

```text
docs/experiments/12_radius_refinement_worklog.md
```

Robustness work after grid polish:

```text
docs/experiments/13_robust_grid_polish_worklog.md
```

Grid-polish speed work:

```text
docs/experiments/14_grid_polish_speed_worklog.md
```
