# Experiment Progression Summary, Experiments 270-433

Date: 2026-06-04

Scope: This summary reviews the current project state using the experiment
notes in `docs/experiments`, the previous update in
`docs/update/summary/001_2026-06-02_summary_update.md`, and the experiment
artifacts in `outputs/experiments`. The main focus is the work from experiment
270 through the latest completed experiment, 433. Experiment 434 exists and is
currently running, but it has not yet produced result files.

## Short Version

The project is building a two-dimensional ground-penetrating radar inversion
pipeline for rebar location and radius estimation. In plain terms, the system
simulates radar scans through concrete, compares simulated traces against an
observed scan, and searches for the rebar geometry that best explains the
data. The important change over the recent experiments is that the project is
no longer only asking "which candidate is best?" It is asking "is the best
candidate clearly better than nearby alternatives, and under what acquisition
and source assumptions?"

Around experiment 270, the central question was the resolution limit for a
three-rebar, variable-radius scene, especially the rightmost target with true
geometry `x=300 mm, z=90 mm, r=8 mm` in the close-50 setup. The system already
had confidence and ambiguity reporting, but the acquisition settings were still
being sorted out. Experiments 270-335 established a practical rule: four
sources are enough in the tested close-spacing branch when the transmit/receive
offset is adequate, but acquisition geometry matters strongly. With 35 mm
offset, close30 was the tightest replicated clean spacing. With 45 mm offset,
the tests reached the physical tangent case, close14, cleanly.

Experiments 337-418 then turned the close14 tangent case into a noise-boundary
study. Under 45 mm offset, the clean replicated endpoint was 15.3125 percent
root-mean-square noise. Adding more sources did not fix the next ambiguity. A
larger 50 mm transmit/receive offset did fix it and pushed the clean replicated
endpoint to 19.642333984375 percent root-mean-square noise. The final failure
above that point is not a radius failure: the radius evidence remains strong,
but the lateral position interval opens by 1 mm.

Experiments 421-433 moved into the current active branch: field-like source
shape calibration. A delayed secondary source pulse, called ringdown in the
notes, can make a fixed source model pick a wrong high-radius branch. A simple
source-basis fit, where the model fits both a primary pulse and a delayed
ringdown pulse, fixes that single-rebar failure and has now passed multi-rebar
local geometry gates for compact windows on all three targets. Dense Stage
4C-style source-shape radius sweeps have passed for the center target
(experiment 432) and left target (experiment 433). Experiment 434 is the same
dense sweep for the right target and is still in progress.

## Terms Used Here

Ground-penetrating radar, or GPR, means a radar pulse is sent into concrete and
the reflected signal is recorded. A B-scan is a collection of those reflected
traces across multiple source/receiver positions. In this project, a B-scan is
the main data object.

Finite-difference time-domain, or FDTD, is the forward simulator. It numerically
propagates the radar wave through concrete and around rebars. Full waveform
inversion, or FWI, is the inverse step: candidate rebar geometries are simulated
and compared against the observed scan to infer location and radius.

A source profile is a small set of nuisance parameters for the emitted radar
pulse, such as amplitude, timing shift, center frequency scale, and now delayed
ringdown. This matters because a wrong source model can look like a wrong rebar
size.

A confidence interval or ambiguity interval is the set of near-best candidates
that are too close to the best candidate to dismiss. A point estimate can be
correct but still not clean if a neighboring geometry is almost equally good.

Stage 4C, in these notes, refers to a dense local geometry/radius sweep around
a target. In the latest source-shape branch, the dense Stage 4C grid uses five
x positions, five z positions, and thirteen radius values.

Root-mean-square noise is reported as a percent level. For example, 10 percent
noise means synthetic noise scaled to 10 percent of the signal root-mean-square
level.

## The Project Objective

The project is trying to estimate rebar position and radius from GPR data in a
way that remains useful under realistic complications:

- source-wavelet mismatch, meaning the emitted radar pulse in the data is not
  exactly the pulse used by the model;
- noise;
- multiple neighboring rebars whose reflections overlap;
- variable radii, where different bars have different sizes;
- tight spacing, where adjacent bars become hard to distinguish;
- material uncertainty, where the same geometry can look similar under a
  slightly different material model.

The current research claim is therefore not "the best candidate is always
right." The stronger and more defensible claim is:

When the acquisition geometry is adequate, the tested two-dimensional pipeline
can recover the correct rebar locations and radii in controlled synthetic
single- and multi-rebar cases, while explicitly reporting ambiguity when the
objective cannot cleanly separate nearby candidates.

That reporting discipline is central. Several recent experiments would look
better if only the best point were reported. The confidence reports show that
some of those best points are not clean because a nearby shifted x position or
nearby radius is almost tied.

## Experimental Setup

The main multi-rebar setup used in the recent close-spacing branch has three
rebars at the same depth, with different radii. The standard true radii are
`[5, 6, 8] mm`. The rightmost target is often the difficult one because it is
the larger bar and is placed close to the middle bar in the tight-spacing
experiments.

The coordinate optimizer usually starts from a partially wrong target state.
For the right-target close-spacing runs, the x location is correct but the
depth and radius start too shallow/small, for example `z=85 mm, r=6 mm` for a
true `z=90 mm, r=8 mm`. The optimizer then searches a small local grid in x,
z, and radius.

The recent close-spacing coordinate runs commonly used:

- grid step: 1 mm;
- frequency: 1.5 GHz;
- target: the rightmost rebar, target index 2;
- x offsets: five candidates from -2 mm to +2 mm;
- z offsets: three candidates, usually 0, 5, and 10 mm from the initial depth;
- radius offsets: seven candidates from -1 mm to +2 mm in 0.5 mm steps;
- two observed cases per seed: a nominal noisy case and a source-mismatch
  noisy case;
- diagnostic objectives: a base objective and often a high-band objective;
- confidence reporting through best candidate, label, and ambiguity interval.

That makes 105 geometry candidates for one target pass, and because there are
usually two observed cases per run, the candidate table usually has 210 rows.
When the logs print progress such as `25/325`, that number is the geometry-grid
progress, not the total table rows. In a four-case dense source-shape run,
325 geometries become 1,300 candidate rows.

The latest source-shape branch uses a different but related local geometry
runner. It keeps neighboring rebars fixed at truth, varies one target's local
x/z/r grid, and fits the source shape for each candidate. The field-like source
shape being tested is a delayed secondary pulse 180 ps after the primary pulse,
with 0.8 frequency scale. The source-basis fit estimates a primary coefficient
and a delayed-ringdown coefficient instead of forcing one global source
amplitude to explain both pulses.

## Hardware And Runtime Context

The observed runtimes below were measured on the local machine, not estimated
from theory. The current machine reports:

- GPU: NVIDIA GB10;
- driver: 580.95.05;
- CUDA compute capability: 12.1;
- PyTorch-visible GPU memory: about 128.5 GB;
- Linux memory: 119 GiB total;
- CPU: 20 ARM cores, reported as 10 Cortex-X925 cores and 10 Cortex-A725 cores.

The cost pattern is important:

| Run type | Typical grid | Candidate rows | Observed wall time |
| --- | ---: | ---: | ---: |
| Close-spacing coordinate optimizer, 4 sources | 105 geometries x 2 cases | 210 | about 21-24 min per seed |
| Close14 source-count test, 3 sources | 105 geometries x 2 cases | 210 | about 18-21 min |
| Close14 source-count test, 5 sources | 105 geometries x 2 cases | 210 | about 28 min |
| Close14 source-count test, 7 sources | 105 geometries x 2 cases | 210 | about 39 min |
| Source-shape narrow gate | 5 geometries x 4 cases | 20 | 161 s |
| Source-shape compact x/z/r gate | 27 geometries x 4 cases | 108 | 873-882 s |
| Source-shape high-radius compact gate | 45 geometries x 4 cases | 180 | 1472 s |
| Source-shape wider x/z high-radius gate | 125 geometries x 4 cases | 500 | 4076 s |
| Source-shape dense Stage 4C gate | 325 geometries x 4 cases | 1,300 | about 10,500 s, or 2.9 h |

The coordinate optimizer scan from experiments 270-417 has 113 measured runs.
Across those runs, the mean wall time is about 1,404 s, or 23.4 minutes. For
the common four-source, 35-50 mm offset runs, the mean is about 1,395 s, or
23.25 minutes. The 50 mm noise-boundary runs are not much slower than the 45
mm runs; the bigger cost increase comes from source count and grid size.

This is why the project moved toward staged and guarded workflows. A broad
dense grid is possible, but it is expensive enough that the experiment design
must be selective. The dense Stage 4C source-shape runs are almost three hours
per target on this hardware.

## Where The Project Stood Around Experiment 270

Before experiment 270, the project had already made several important
transitions.

First, single-rebar radius estimation had moved away from plain fixed-source
least squares. Earlier tests showed that source-wavelet mismatch can push the
objective toward a wrong high-radius candidate. The source-profiled approach,
which searches over source amplitude, time shift, and center-frequency scale,
became mandatory for radius claims under mismatch.

Second, reporting had become confidence-aware. Notes 40 and 41 are especially
important here. Experiment 079 showed that the Stage 6 all-target matrix
recovered all 24 tested multi-rebar rows correctly, but 22 of those 24 rows
were weak confidence. Experiment 080 then added ambiguity interval reporting.
That changed the interpretation from "the point estimate is always enough" to
"the point estimate is useful, but the uncertainty interval is part of the
result."

Third, the coordinate optimizer had become reporting-first. Experiments 082-089
showed that the optimizer could recover the target x/z/r values across seeds
and noise cases, but also that margins were often weak. The aggregate in
experiment 089 had 24 truth rows, but 14 weak labels and 14 fallback warnings.
This again reinforced that reporting intervals are not cosmetic; they are
needed to avoid overclaiming.

Fourth, seed-offset stress tests in experiments 090-098 showed a useful rescue
pattern. Guarded revisits could recover targets that a main pass failed, but
the aggregate intentionally retained failed main rows. That made the reporting
more honest: a rescue can be useful, but it does not erase the fact that the
main objective had a vulnerable branch.

By experiment 270, the active question had narrowed to acquisition design and
spacing limits in a variable-radius multi-rebar setting. The main target was
the rightmost bar, and the core question was:

How few source positions and how much transmit/receive separation are needed
to recover the correct x/z/r cleanly when bars are close together?

## Experiments 270-280: Four Sources Became The Practical Minimum For Close50

The close50 branch first tested source count and transmit/receive offset. The
initial evidence showed that five sources with a 40 mm transmit/receive offset
worked cleanly. Experiment 271 aggregated earlier close50 runs and found all
six rows clean and strong under the five-source, 40 mm setup.

The important design fix in experiment 272 was metadata, not physics. The
summaries were updated to record acquisition settings, because mixing runs with
different source counts or transmit/receive offsets can hide the real cause of
a pass or failure. Experiment 273 made that point directly: source count alone
did not explain the results unless the transmit/receive offset was also
grouped correctly.

Three sources then failed. Experiment 274, with three sources and 40 mm offset,
selected a shifted and smaller-radius branch instead of the truth. Experiment
275 aggregated the source-count comparison and showed that the three-source
group had zero truth rows and four x-ambiguity rows, while the five-source
group was clean.

Experiment 276 then tested the practical middle ground: four sources, 40 mm
offset. It passed for seed 34, and experiments 278 and 279 replicated that for
seeds 13 and 21. Experiment 280 aggregated the three four-source seeds:

- 6 rows;
- 6 truth rows;
- 6 strong labels;
- 0 x-ambiguity rows;
- maximum x ambiguity width: 0 mm;
- radius-margin mean: about 0.00638.

This established four sources with 40 mm offset as the cheaper validated
close50 setting. Five sources remained a conservative backup, and three
sources were not enough.

## Experiments 281-289: 35 mm Offset Became The Robust Close50 Default

After source count, the next question was transmit/receive offset. Offset is
not just a mechanical setting. It changes the angular and timing information in
the B-scan, and in tight multi-rebar cases that can decide whether two nearby
geometries are separable.

The 30 mm offset experiments, 281-284, were point-correct and officially
strong, but the margins were much thinner. The aggregate in experiment 284 had
all six truth rows and no ambiguity, but its minimum radius margin was about
0.00170, much smaller than the 40 mm aggregate.

The 25 mm offset failed in experiment 285. The best candidate shifted laterally
to `x=301 mm`, while the true `x=300 mm` candidate was nearly tied. That made
25 mm a lower bound failure, not a practical choice.

The 35 mm offset runs, experiments 286-289, gave the better tradeoff. The
aggregate in experiment 289 had:

- 6 rows;
- 6 truth rows;
- 6 strong labels;
- 0 x-ambiguity rows;
- radius-margin mean: about 0.00519.

The conclusion was that 35 mm is the robust close50 default, 30 mm is a
margin-aware minimum, and 25 mm is too small.

## Experiments 290-305: Tightening Under 35 mm Offset Reached Close30 Cleanly

The next branch kept four sources and 35 mm offset, then tightened the spacing
between the middle and right rebars. The goal was to find the smallest spacing
that still stayed clean without changing acquisition geometry.

Close45, close40, and close35 all passed cleanly across seeds 34, 13, and 21.
Their aggregates were experiments 293, 297, and 301. Each had six truth rows,
six strong labels, and zero x ambiguity.

Close30 also passed cleanly, but the margin was much thinner. Experiment 305
aggregated the close30 seed set:

- 6 rows;
- 6 truth rows;
- 6 strong labels;
- 0 x-ambiguity rows;
- radius-margin mean: about 0.00243;
- radius-margin minimum: about 0.00150.

That made close30 the tightest replicated clean result under the standard
35 mm offset. The reason it matters is that close30 passed, but the nearest
competitor was already becoming a coupled shifted-x and radius branch. The
result was clean, but it was near the edge of the acquisition's resolving
power.

## Experiments 306-323: Close25 And Close28 Needed Larger Offset Or Interval Reporting

Experiment 306 tested close25 under the same four-source, 35 mm offset setup.
It did not stay clean. The best point shifted to a neighboring x/radius branch,
and the truth was close enough that the right interpretation was ambiguity,
not a clean failure of radius physics.

The next rescue was a 40 mm transmit/receive offset. Experiments 307-310 tested
close25 at 40 mm. The aggregate in experiment 310 selected the truth in all
six rows, but it was still not clean:

- labels: 3 strong, 2 moderate, 1 weak;
- x-ambiguity rows: 3 of 6;
- maximum x ambiguity width: 1 mm;
- maximum radius ambiguity width: 0.5 mm.

This is a good example of why point accuracy and clean separability are
different claims. The point estimate was right, but the ambiguity interval had
to be reported.

Experiments 311-314 tested close28 at 35 mm. Again, the aggregate selected the
truth in all six rows, but three rows had x ambiguity and two rows were weak.
Close28 under 35 mm was therefore a transition-zone result: recoverable, but
not a clean operating point.

Experiments 316-319 then tested close28 with a larger 45 mm offset. The
aggregate in experiment 319 was clean:

- 6 rows;
- 6 truth rows;
- 6 strong labels;
- 0 x-ambiguity rows.

Experiments 320-323 repeated that for close25 with 45 mm offset, and it also
passed cleanly. This established the main acquisition lesson:

If the spacing is tighter than close30, the standard 35 mm offset is not enough
for a clean point claim. Larger offset can recover clean separation.

## Experiments 324-335: 45 mm Offset Reached The Physical Tangent Case

After close25 passed at 45 mm, the branch pushed spacing even tighter:
close20, close15, and close14. Close14 is the tangent case, where the middle
and right bars physically touch if their radii are 6 mm and 8 mm. Going closer
would overlap the circles.

Experiments 324-327 showed close20 was clean. Experiments 328-331 showed
close15 was clean. Experiments 332-335 showed close14 was also clean at 45 mm
offset.

Experiment 335, the close14 aggregate, had:

- 6 rows;
- 6 truth rows;
- 6 strong labels;
- 0 x-ambiguity rows;
- radius-margin mean: about 0.00398.

This was a strong result, but it should be read with the acquisition setting
attached. The standard 35 mm branch had a clean limit at close30. The larger
45 mm branch reached the tangent geometry cleanly.

## Experiments 336-356: Source Count Did Not Rescue The 45 mm Noise Boundary

Experiment 336 asked whether close14 at 45 mm could be made cheaper with three
sources. It could not. The run was faster, but the result was not clean; it
opened a 1 mm x interval. This reinforced the four-source minimum for the
tangent branch.

The next question was noise tolerance. Experiment 337 tested 20 percent
root-mean-square noise at close14 and 45 mm offset. It was point-correct, but
not clean because the x interval opened. Experiments 338-341 showed that 15
percent noise was replicated clean.

Experiments 342-353 then bisected between 15 and 17.5 percent noise. The
replicated clean endpoint under 45 mm offset became 15.3125 percent noise,
aggregated in experiment 349:

- 6 rows;
- 6 truth rows;
- 6 strong labels;
- 0 x-ambiguity rows;
- radius-margin mean: about 0.00374.

Above that, the system remained point-correct in several seed-34 probes, but
the nominal row repeatedly opened a 1 mm x interval. The ambiguity was lateral
position, not radius.

Experiments 354-356 tested whether increasing source count to five or seven
could rescue the boundary at 15.361328125 percent noise. It did not. The
aggregate in experiment 356 had six truth rows and six strong radius labels,
but four of six rows had x ambiguity. More sources increased runtime and did
not solve the specific near-tie.

The design lesson was that source count is not a universal fix. At this
boundary, acquisition geometry was more important than simply adding more
source positions.

## Experiments 357-418: 50 mm Offset Raised The Close14 Noise Endpoint

The next rescue changed transmit/receive offset from 45 mm to 50 mm while
keeping four sources. This worked.

Experiments 357-360 showed that the previously ambiguous
15.361328125 percent noise level became clean under 50 mm offset. Experiments
361-364 promoted 15.46875 percent. Experiments 365-368 promoted 15.625
percent. Experiments 369-372 promoted 16.25 percent. Experiments 373-376
promoted 17.5 percent. Experiments 378-381 promoted 18.75 percent. Experiments
382-385 promoted 19.375 percent.

The branch then used bisection near 20 percent noise. Clean replicated
aggregates were produced at:

- 19.53125 percent, experiment 390;
- 19.609375 percent, experiment 394;
- 19.62890625 percent, experiment 399;
- 19.638671875 percent, experiment 403;
- 19.64111328125 percent, experiment 408;
- 19.642333984375 percent, experiment 412.

Experiment 412 is the promoted clean endpoint:

- 6 rows;
- 6 truth rows;
- 6 strong labels;
- 0 x-ambiguity rows;
- radius-margin mean: about 0.00325;
- radius-margin minimum: about 0.00198.

Experiments 413-417 then tested just above that endpoint on seed 34. These
runs stayed point-correct and radius-strong, but the nominal row opened a
1 mm x interval. The final ambiguous upper endpoint was
19.642372131347656 percent. The bracket between the clean endpoint and the
ambiguous endpoint is only 0.00003814697265625 percentage points wide, and the
final margin to the ambiguity cutoff is below `1e-9`. Experiment 418 packaged
this as a noise-boundary summary.

The interpretation is precise:

Four sources with 50 mm transmit/receive offset cleanly resolve the close14
tangent target through 19.642333984375 percent root-mean-square noise in the
tested seed set. Above that, the radius remains strong and the truth remains
the best point, but lateral x ambiguity appears. Further scalar bisection is
not useful unless the ambiguity rule changes.

## Experiments 419-420: Packaging And Visualization

Experiment 419 did not run a new GPU inversion. It packaged the variable-radius
staged pipeline into a replay plan. The plan records detection, location,
focused polish, refined focused polish, joint-radius, and summary commands for
three seeds. The key scientific result is unchanged from the earlier staged
branch:

- the economical five-source focused stage can carry a target-2 x interval;
- the seven-source focused refinement collapses that interval;
- the joint-radius stage ranks the true `[5, 6, 8] mm` tuple first for all
  three seeds.

This matters because it converts a successful but scattered branch into a
replayable workflow.

Experiment 420 packaged material/source branch animations. It is not a new
optimizer claim. It visualizes two previously observed ambiguity mechanisms:

- material branch: lower effective steel conductivity can look similar at the
  same geometry;
- source branch: source-wavelet mismatch can create wrong high-radius
  candidates when source profiling is not used.

The decision from experiment 420 was to add future animations only when a real
objective matrix exposes a meaningful competing branch. This keeps
visualization tied to evidence rather than decoration.

## Experiments 421-424: Source Shape Became The Current Active Problem

The next major branch asked a field-like question: what happens when the
observed source wavelet has a delayed secondary pulse?

Experiment 421 used the existing source profile, which could adjust amplitude,
time shift, and center-frequency scale, but did not model delayed ringdown.
The nominal and controlled source-mismatch cases recovered the correct
6.0 mm radius. The ringdown cases failed badly: they selected the upper tested
radius bound, 7.8 mm. The best nuisance profile tried to compensate with a high
frequency scale, late time shift, and lower amplitude.

This was an important negative result. It showed that source profiling is
necessary but not sufficient for field-like source shape errors.

Experiment 422 added a simple discrete modeled ringdown option, with modeled
ringdown scales 0.0 and 0.25. That fixed the exact 0.25 ringdown cases without
hurting the nominal or controlled mismatch cases.

Experiment 423 then tested a broader amplitude/noise/source-mismatch matrix.
The discrete ringdown grid passed many cases, including 0.25 ringdown with
noise and 0.30 ringdown, but it failed the observed 0.20 ringdown case. The
reason is physically clear: using a modeled 0.25 delayed pulse plus one global
amplitude scale changes the primary pulse too much, so the objective can again
prefer a larger bar.

Experiment 424 fixed that by fitting source-basis coefficients. Instead of one
global amplitude, the model fits a primary pulse coefficient and a delayed
ringdown coefficient. This recovered all tested single-rebar rows:

- nominal: correct radius 6.0 mm;
- ringdown 0.20: recovered from the earlier failure;
- ringdown 0.30: correct;
- ringdown 0.25 with 5 and 10 percent noise: correct;
- source mismatch plus ringdown: correct;
- source mismatch plus ringdown and noise: correct.

The branch decision was to promote source-basis coefficient fitting as the
source-shape calibration diagnostic. The discrete ringdown-grid version is too
brittle to scale.

## Experiments 425-433: Multi-Rebar Source-Shape Gates

Experiments 425-433 carried the source-basis fit into multi-rebar local
geometry tests. These tests are not yet full end-to-end multi-rebar inversion.
The neighboring rebars are fixed at truth, and one target is swept locally.
That limitation matters, but the results are still valuable because they test
whether the source-shape fix remains stable when neighboring rebar reflections
are present.

Experiment 425 was a narrow left-target gate at fixed x/z with five radius
candidates. It passed all four cases in 161 s. The former failure case,
ringdown 0.20, recovered `r=6.0 mm`, and the fitted ringdown coefficient was
approximately 0.20.

Experiments 426-428 expanded to compact x/z/r windows for the left, center,
and right targets:

- 3 x positions;
- 3 z positions;
- 3 radii;
- 27 geometries;
- 4 observed cases;
- 108 candidate rows;
- about 14.6 minutes per run.

All three targets selected the true `x/z/r` in every tested case. The nearest
competitor was not a shifted location; it was the adjacent radius `r=6.2 mm`
at the true x/z location. The weakest compact-window margin was in the center
target noisy-ringdown row, about `2.353e-04`.

Experiment 429 stressed the center target with harder noisy cases. It still
selected the true geometry in all four rows, but the weakest margin dropped to
about `1.813e-04`. That is a pass, but it is not a wide-margin pass.

Experiment 430 reintroduced high-radius candidates, including `r=7.4 mm` and
`r=7.8 mm`, into the compact center-target grid. This directly tested whether
the old source-shape failure branch would return. It did not. All four rows
selected `x=250 mm, z=90 mm, r=6.0 mm`, and high-radius candidates did not
enter the top eight.

Experiment 431 widened the center-target high-radius window to a 5 x 5 x 5
grid, or 125 geometries. It again selected the true geometry in all four rows.
High-radius candidates appeared around ranks 9-12, mostly at `z=92 mm`, but
they were not near-ties.

Experiment 432 ran the dense Stage 4C-style center-target source-shape grid:

- x values: 248-252 mm;
- z values: 88-92 mm;
- radius values: 5.4-7.8 mm in 0.2 mm steps;
- 325 geometries;
- 4 observed cases;
- 1,300 candidate rows;
- 10,526 s wall time.

The center dense run passed. All four rows selected `x=250 mm, z=90 mm,
r=6.0 mm`. A secondary shifted-depth branch around `z=91 mm` and `r=6.8-7.0
mm` became visible in the top candidates, but it stayed behind the truth and
the adjacent `r=6.2 mm` candidate at the true x/z location.

Experiment 433 repeated the dense Stage 4C-style grid for the left target:

- x values: 148-152 mm;
- z values: 88-92 mm;
- radius values: 5.4-7.8 mm in 0.2 mm steps;
- 325 geometries;
- 4 observed cases;
- 1,300 candidate rows;
- 10,487 s wall time.

It also passed. All four rows selected `x=150 mm, z=90 mm, r=6.0 mm`. The
same shifted-depth branch appeared but remained secondary.

Experiment 434 is the right-target dense Stage 4C-style source-shape run. At
the time of this summary, a Python process is still running this command. The
folder exists, but no result files or figure notes are available yet. The
latest completed source-shape result is therefore experiment 433.

## What Worked

The confidence-reporting stack worked. It repeatedly prevented overclaiming by
showing when a correct best point was still interval-supported rather than
clean.

The acquisition-aware summaries worked. The close50 branch showed that source
count cannot be interpreted without transmit/receive offset. Once metadata was
explicit, the conclusions became cleaner: four sources with 35-40 mm offset
were practical for close50, while 25 mm offset failed.

The four-source acquisition worked well in the tested multi-rebar close-spacing
branch. Three sources failed in important cases. Five and seven sources were
sometimes useful in earlier staged refinement, but in the close14 noise
boundary they did not fix the lateral ambiguity. Four sources with better
offset was the better solution there.

The larger transmit/receive offsets worked. Under 35 mm offset, close30 was
the tightest clean standard-spacing result. Under 45 mm offset, the tangent
close14 geometry was clean. Under 50 mm offset, the close14 tangent case stayed
clean up to 19.642333984375 percent noise.

The source-basis fit worked. It fixed a real source-shape failure that the old
amplitude/time/frequency profile could not fix, and it passed the first
multi-rebar local geometry gates.

The replay and visualization packaging worked. Experiment 419 makes the staged
variable-radius workflow repeatable. Experiment 420 ties animations to actual
known ambiguity branches instead of creating disconnected visuals.

## What Did Not Work

Three sources did not work as a clean acquisition for the close50 and close14
branches tested here. It reduced runtime but opened lateral ambiguity or picked
the wrong branch.

The 25 mm transmit/receive offset did not work for close50. It made the
shifted x candidate too competitive.

Close25 at 35 mm offset did not work cleanly. Close25 at 40 mm became
point-correct but still interval-supported. Close28 at 35 mm was also
point-correct but interval-supported. These are useful results, but they are
not clean-resolution claims.

More sources did not rescue the close14, 45 mm, 15.361328125 percent noise
boundary. Five and seven sources increased runtime but left x ambiguity.

The old source profile did not handle delayed source ringdown. Experiment 421
selected `r=7.8 mm` for ringdown cases. The discrete ringdown grid helped, but
it failed observed ringdown 0.20 in experiment 423. The coefficient-fit source
basis was needed.

Further scalar bisection of the final 50 mm close14 noise boundary is not
useful. The clean-to-ambiguous bracket is already at a numerical edge of the
configured ambiguity rule.

## What Remains Ambiguous

Some best points are correct but not clean. This is the most important
interpretation rule for the project. A correct point estimate under a weak
label or nonzero x interval should be reported as interval-supported.

The source-shape dense branch has visible secondary shifted-depth candidates
around `z=91 mm` and `r=6.8-7.0 mm`. They are not near-ties in experiments 432
and 433, but they are a real branch and should be tracked in the right-target
dense result when experiment 434 finishes.

The source-shape branch is still local. Neighboring rebars are fixed at truth,
and the target windows are manually chosen. This is not yet a full
detector-to-source-shape multi-rebar pipeline.

The source-shape model is still simple. It fits a primary pulse plus one
delayed ringdown pulse at fixed delay and frequency scale. That is a useful
field-like diagnostic, but not a complete arbitrary source-wavelet inversion.

The project is still two-dimensional and synthetic. The results are strong for
the tested controlled cases, but they are not yet field-data validation.

## Current Best Understanding

The project now has a strong synthetic 2D story built around three principles.

First, acquisition geometry matters as much as the optimizer. In the tested
multi-rebar close-spacing cases, lateral ambiguity was often solved by
transmit/receive offset, not by adding more sources or changing the objective
alone.

Second, source calibration is mandatory for radius claims. Simple source
amplitude/time/frequency profiling handles many controlled mismatches, but
field-like ringdown can still look like a wrong larger radius. The
primary-plus-ringdown coefficient fit is the current best source-shape
diagnostic.

Third, uncertainty reporting is part of the result. The pipeline's most
defensible output is not just one recovered geometry. It is a recovered
geometry plus margins, labels, ambiguity intervals, acquisition metadata, and
source/material caveats.

As of the latest completed artifacts, the strongest current claims are:

- close50 variable-radius target recovery is clean with four sources and
  35-40 mm transmit/receive offset;
- under 35 mm offset, close30 is the tightest replicated clean spacing;
- under 45 mm offset, the close14 tangent case is clean at low noise and up to
  15.3125 percent noise;
- under 50 mm offset, close14 is clean up to 19.642333984375 percent noise;
- the close14 failure above that endpoint is lateral x ambiguity, not radius
  failure;
- source-basis coefficient fitting fixes the delayed-ringdown radius bias in
  the tested single-rebar cases;
- source-basis fitting has passed multi-rebar compact gates for all three
  targets and dense Stage 4C gates for center and left targets.

## Current Bottlenecks

The main bottleneck is GPU time for dense grids. A 325-geometry, four-case
dense source-shape run takes about 2.9 hours per target on the current GB10
system. Broad sweeps over multiple targets, seeds, materials, source shapes,
and acquisition settings can therefore become expensive quickly.

The second bottleneck is experimental scope. The project has many strong local
results, but each broader claim needs careful packaging: fixed benchmark
matrix, acquisition metadata, source assumptions, confidence intervals, and
runtime.

The third bottleneck is integration. The source-shape work currently lives in
local geometry sweeps. The detector-seeded pipeline and the multi-rebar
source-shape branch have not yet been fully joined into one end-to-end
multi-rebar workflow.

The fourth bottleneck is model realism. Material uncertainty and source-shape
uncertainty are being handled as bounded diagnostic/reporting branches, not as
unlimited free variables. That is a good design choice for stability, but it
means field-data claims need careful calibration.

## Sensible Next Steps

The immediate next step is to let experiment 434 finish and then inspect its
summary, case CSVs, objective candidates, figure notes, and plots. If it
passes, the project should package an all-target dense source-shape summary for
experiments 432-434. If it fails or shows a near-tie, the top candidates should
be inspected before running any new sweep.

After 434, the next useful source-shape work is aggregation and reporting, not
immediate expansion. The project should summarize all source-shape gates
425-434 in one artifact that reports target, grid size, cases, best geometry,
next radius, margin, fitted ringdown coefficient, runtime, and any shifted
x/z/r branches.

The close14 scalar noise bisection should stay closed. Experiment 418 already
shows the boundary at a numerical edge. More runs there are unlikely to change
the scientific conclusion.

The close-spacing acquisition story should be preserved as a table in future
reports. The clean limits depend on offset: close30 at 35 mm, close14 at
45 mm, and close14 with much higher noise tolerance at 50 mm.

The next non-source GPU branch should be chosen carefully. Good candidates are:

- a material perturbation tied to a known ambiguity branch;
- a detector-seeded multi-rebar run that uses the same confidence discipline;
- a variable-radius staged geometry not already covered by close60, close50,
  close30, or close14;
- an efficiency pass that reduces dense-grid cost through staged screening,
  caching, or better batching.

## Evidence Index

Key notes:

- `docs/update/summary/001_2026-06-02_summary_update.md`
- `docs/experiments/40_stage6_all_target_confidence_synthesis.md`
- `docs/experiments/41_ambiguity_interval_reporting.md`
- `docs/experiments/42_reporting_first_coordinate_optimizer.md`
- `docs/experiments/43_coordinate_optimizer_noise_replication.md`
- `docs/experiments/44_coordinate_optimizer_seed_offset_stress.md`
- `docs/experiments/45_radius_confidence_objective_matrix.md`
- `docs/experiments/47_detection_to_fwi_pipeline.md`
- `docs/experiments/48_research_handoff_matrix.md`
- `docs/experiments/49_material_source_branch_animation_summary.md`
- `docs/experiments/50_field_like_source_shape_calibration.md`
- `docs/experiments/51_multi_rebar_source_shape_basis_fit.md`

Key aggregate artifacts:

- `outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/289_coordinate_confidence_close50_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/305_coordinate_confidence_close30_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/310_coordinate_confidence_close25_sources4_txrx40_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/314_coordinate_confidence_close28_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/319_coordinate_confidence_close28_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/323_coordinate_confidence_close25_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/335_coordinate_confidence_close14_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/349_coordinate_confidence_close14_sources4_txrx45_noise15p3125_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/356_coordinate_confidence_close14_seed34_noise15p361328125_sources4_5_7_aggregate/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/412_coordinate_confidence_close14_sources4_txrx50_noise19p642333984375_seed_replicates/data/coordinate_confidence_aggregate.json`
- `outputs/experiments/418_coordinate_confidence_close14_txrx50_noise_boundary_summary/data/noise_boundary_summary.json`

Key current source-shape artifacts:

- `outputs/experiments/421_source_shape_ringdown_profiled_replication/data/source_profiled_replication_summary.json`
- `outputs/experiments/424_source_shape_ringdown_basis_fit_matrix/data/source_profiled_replication_summary.json`
- `outputs/experiments/425_multi_rebar_left_source_shape_basis_fit_narrow/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/426_multi_rebar_left_source_shape_basis_fit_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/427_multi_rebar_center_source_shape_basis_fit_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/428_multi_rebar_right_source_shape_basis_fit_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/429_multi_rebar_center_source_shape_basis_fit_hard_noise_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/430_multi_rebar_center_source_shape_basis_fit_high_radius_compact_xzr/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/431_multi_rebar_center_source_shape_basis_fit_high_radius_wide_xz/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/432_multi_rebar_center_source_shape_basis_fit_stage4c_dense_radius/data/multi_rebar_local_geometry_summary.json`
- `outputs/experiments/433_multi_rebar_left_source_shape_basis_fit_stage4c_dense_radius/data/multi_rebar_local_geometry_summary.json`

Current in-flight experiment:

- `outputs/experiments/434_multi_rebar_right_source_shape_basis_fit_stage4c_dense_radius`
- status at summary time: process running, result files not yet available.
