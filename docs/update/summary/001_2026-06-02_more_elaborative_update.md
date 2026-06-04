# Plain Explanation Summary - Multi-Rebar Transition

Date: 2026-06-02

## Future Explanation Style

When asked for a plain explanation after a research marathon, explain the work
without dumbing it down. Keep the technical details, but define what each term
means and why it matters. Start with the big picture, then explain the current
result, then explain the next step.

## Holistic View

The project has mostly moved from the single-rebar case into the harder
multi-rebar case.

The single-rebar case is the baseline problem: one buried circular steel target
is present, and the inversion tries to recover its location, depth, and radius
from GPR-like simulated data. That case is much cleaner because only one object
is producing the main reflected signal.

The multi-rebar case is harder because several buried steel bars are present at
the same time. Their signals can overlap. The inversion now has to decide not
only where one target is, but which nearby target configuration best explains
the whole simulated scan.

The main research question is:

```text
How close can two rebars be before the inversion can no longer separate them
cleanly?
```

That is why the recent experiments use names like `close50`, `close30`,
`close25`, and `close28`. These describe how close the right rebar is to the
middle rebar.

For example:

```text
close50: x = [190, 250, 300] mm
close30: x = [190, 250, 280] mm
close25: x = [190, 250, 275] mm
close28: x = [190, 250, 278] mm
```

Smaller numbers mean the rebars are closer together, so the problem is harder.

## What Is Being Tested

The current robust multi-rebar setup is:

```text
4 source positions
35 mm Tx/Rx offset
1.5 GHz center frequency
```

`source positions` means how many scan positions are used to illuminate and
measure the scene. More source positions usually provide more information, but
they cost more runtime.

`Tx/Rx offset` means the distance between the transmitter and receiver in the
GPR acquisition geometry. Changing this spacing changes what parts of the
subsurface response are emphasized. A larger Tx/Rx offset can sometimes help
separate overlapping responses from nearby rebars.

With the 4-source, 35 mm Tx/Rx setup, the recent evidence is:

```text
close50 passed cleanly
close45 passed cleanly
close40 passed cleanly
close35 passed cleanly
close30 passed cleanly, but with tighter margins
close25 failed as a clean result
```

So the current clean replicated limit is:

```text
close30 with 4 sources and 35 mm Tx/Rx offset
```

In plain terms: with this acquisition setup, the system can reliably separate
the tested rebars when the center/right spacing is 30 mm. At 25 mm, the
standard 35 mm Tx/Rx acquisition is no longer clean.

## Why "Clean" Matters

The optimizer can sometimes pick the true answer even when a nearby wrong
answer fits almost as well.

For example, the truth may be:

```text
x = 275 mm, radius = 8.0 mm
```

but a competing candidate may be:

```text
x = 276 mm, radius = 7.5 mm
```

If both candidates produce very similar simulated GPR responses, then the
optimizer picking the truth is not enough by itself. We also need to know
whether the truth was clearly better than the nearby competitor.

That is why the experiments track confidence labels, ambiguity intervals, and
objective margins.

## What Seed Means

`seed13`, `seed21`, and `seed34` are random-noise seeds.

The simulations add noise to the synthetic data so that the inversion is tested
under more realistic conditions. A seed controls the exact random noise pattern.

For example:

```text
seed13: one specific noise realization
seed21: a different noise realization
seed34: another different noise realization
```

Running multiple seeds asks:

```text
Does the result still hold when the noise changes?
```

A result from one seed is only a probe. A result that survives seeds 13, 21,
and 34 is stronger evidence.

## What Rows Mean

A `row` in these reports is one confidence result for one observed case.

Each seed usually has two observed cases:

```text
nominal noise case
source-mismatch noise case
```

The nominal case uses the expected source model plus noise.

The source-mismatch case deliberately changes the source wavelet slightly, for
example by changing frequency scale or timing. This tests whether the inversion
is robust when the assumed source pulse is not perfectly correct.

So when three seeds are aggregated, there are usually:

```text
3 seeds x 2 cases per seed = 6 rows
```

That is what `6/6 rows selected truth geometry` means:

```text
all six seed/case combinations selected the true x, z, and radius
```

That sounds good, but it does not automatically mean the result is clean.

For example:

```text
3/6 rows had x ambiguity
```

means that in three of the six seed/case combinations, another lateral position
was still close enough to the best answer that the report kept an ambiguity
interval.

If the truth is `x=275 mm`, an ambiguity interval like:

```text
x = 275-276 mm
```

means:

```text
the best answer is x=275 mm, but x=276 mm is still too plausible to ignore
```

## What Weak, Moderate, and Strong Mean

The confidence label describes how clearly the selected radius is separated
from the next competing radius.

The basic idea is:

```text
strong: the selected radius is clearly better than nearby radii
moderate: the selected radius is better, but the separation is not large
weak: the selected radius is barely better, so report uncertainty
```

So:

```text
1 row was weak
```

means one seed/case combination picked the truth, but the objective gap between
the selected radius and the next competing radius was too small to trust the
point estimate without qualification.

In this project, a weak row is not the same as a total failure. It means:

```text
do not report this as a clean single answer; report an interval or ambiguity
warning
```

## What Margin Means

The objective value is the misfit: how badly a candidate geometry disagrees
with the observed/synthetic data. Lower is better.

The `margin` is the difference between the best candidate and the next serious
competitor.

For example:

```text
truth misfit:      0.05060
competitor misfit: 0.05109
margin:            0.00049
```

That means the competitor is only slightly worse than the truth.

When the minimum margin is very small, it means at least one seed/case
combination had a very close competitor. The optimizer may still choose the
truth, but the data does not strongly rule out the competitor.

Plainly:

```text
a small margin means the answer is fragile
```

The repeated fragile competitor in the recent close cases is a coupled shift:

```text
truth:      x = 275 or 278 mm, radius = 8.0 mm
competitor: x + 1 mm, radius = 7.5 mm
```

That means the inversion can confuse a slightly shifted lateral position with a
slightly smaller radius.

## Recent Result: Close25

The standard 35 mm Tx/Rx acquisition failed clean close25 recovery.

Then a more conservative acquisition was tried:

```text
close25
4 sources
40 mm Tx/Rx offset
```

That result was better:

```text
6/6 rows selected truth geometry
```

But it was not clean:

```text
3/6 rows had x ambiguity
confidence labels were mixed: strong=3, moderate=2, weak=1
minimum margin was very small
```

So the conclusion is:

```text
close25 at 40 mm Tx/Rx is point-recoverable, but ambiguous.
```

In plain terms: the optimizer picked the right answer across seeds, but nearby
wrong answers were still too close. This should be reported with uncertainty
intervals, not as a clean resolution limit.

## Recent Result: Close28

After close30 passed and close25 failed cleanly, close28 was tested to bracket
the transition.

Experiments 311 and 312 tested:

```text
close28
4 sources
35 mm Tx/Rx offset
seeds 34 and 13
```

Both runs selected the true geometry and did not require a revisit.

But both still showed a near-best competing branch:

```text
truth:      x = 278 mm, radius = 8.0 mm
competitor: x = 279 mm, radius = 7.5 mm
```

Seed34 had a weak nominal row. Seed13 improved to moderate, but still retained
the same ambiguity interval:

```text
x = 278-279 mm
radius = 7.5-8.0 mm
```

So close28 currently looks like a transition-band result:

```text
it may be point-recoverable, but it is not yet a clean validated limit
```

## Current Gist

The current state is:

```text
single rebar: baseline problem is mature
multi rebar: active work is finding the practical separation limit
clean replicated multi-rebar limit so far: close30 with 4 sources and 35 mm Tx/Rx
close25 with 40 mm Tx/Rx: truth-selected but ambiguous
close28 with 35 mm Tx/Rx: truth-selected for two seeds, but still ambiguous
```

The next logical step is:

```text
run close28 seed21 with 4 sources and 35 mm Tx/Rx
then aggregate experiments 311-313
```

If the close28 aggregate still has ambiguity, then close30 remains the clean
validated geometry-separation limit. If close28 aggregates cleanly, it can be
promoted as a tighter validated limit.
