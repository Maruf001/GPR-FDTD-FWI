# Experiment 48: Research Handoff Matrix

## Purpose

Provide a compact handoff view that separates what is solved, what is only
interval-supported, which caveats matter, which visual artifacts should be
checked first, and where more GPU time is justified.

## Matrix

| Branch | Location accuracy | Radius confidence | Source/material caveat | Visualization evidence | Runtime/cost note | Handoff decision |
| --- | --- | --- | --- | --- | --- | --- |
| Single rebar, standard radius | Correct basin after staged/local refinement | Strongest with 1.5 GHz-only or carry-low-25 least squares; report top-k margins | Source amplitude/time/frequency profiling is required under mismatch | Frequency/source-profile plots in experiments 23 and 26; source branch GIFs in experiments 46/49 | Cheap enough for local profiling; avoid global search | Use source-profiled local radius evidence, not W2/OT or free material inversion |
| Single rebar, field-like source shape | Correct with source-basis coefficient fit across tested ringdown/noise/source rows | Existing amplitude/time/frequency profile and coarse ringdown grid can select r=7.8 mm | Delayed secondary-pulse source shape must be calibrated before field/lab radius claims | Experiment 50, runs 421-424 | Source-basis fit costs about the same as the modeled ringdown grid, around 1700 s for the 52-candidate matrix | Promote coefficient-fit source-shape diagnostics; multi-rebar gates 425-428 passed across all three targets |
| Multi-rebar source-shape compact/wide x/z gate | Left, center, and right targets correct over compact and dense Stage 4C radius windows; synthesis has 40/40 truth rows; compact seed replication adds 4/4 truth rows | Positive margins against 6.2 mm; weakest margin 1.006e-04 in center source-mismatch seed55 row | Source-basis coefficients recovered injected ringdown 0.20 and about 0.25; shifted z91/r6.8-7.0 branch appears but is not a near-tie | Experiment 51, runs 425-436 | 5 candidates cost 161 s; 27 candidates cost 849-882 s; 45 candidates cost 1472 s; 125 candidates cost 4076 s; dense 325 candidates cost about 10200-10500 s | Widen/high-radius check for seed55 before coupled-neighbor stress |
| Single rebar, shallow r=4 mm | Correct point estimate in tested high-band cases | Weak interval around the true radius remains after fine subcell sampling | Material/source changes can explain parts of the shallow objective valley | Fine-radius and material/source tradeoff plots from experiments 189-199; material branch GIF in experiment 49 | More fine sampling adds cost without collapsing the interval | Report radius as interval-supported; do not claim high-precision point size |
| Same-depth multi-rebar local x/z/r | True x/z/r recovered across the Stage 6 matrix | Mostly weak margins before coordinate-confidence upgrades | Source mismatch does not change point recovery but tightens margins | Experiment 40 confidence matrix | Robustness matrix already run | Confidence labels and ambiguity intervals are mandatory in all reports |
| Variable-radius close60 staged pipeline | Final x/z/r exact across seeds after staged policy | Joint radius tuple ranks truth first | Standard 5-source focused target-2 stage has x intervals; 7-source refinement collapses them | Experiment 419 staged error plot and replay plan | Replay plan captures 15 stage commands; reruns are heavy GPU work | Use 5-source interval reporting by default; use 7-source focused refinement when point x is required |
| Variable-radius close50 geometry | Close50 needed acquisition geometry changes to disambiguate target 2 | Radius remains strong while x ambiguity is the limiter | Do not hide missing Tx/Rx offset metadata | Experiments 271, 273, 280, 284, 289 aggregates | 4 sources with 35-40 mm Tx/Rx is the practical region | Use acquisition-aware summaries; 35 mm Tx/Rx is robust, 30 mm is margin-aware minimum |
| Tight variable-radius spacing under 35 mm Tx/Rx | Close30 is the tightest replicated clean result | Close28/25 require interval or larger-offset reporting | The coupled shifted-x/radius branch becomes competitive | Experiments 305, 310, 314 | More bisection below close30 is not useful without acquisition changes | Keep close30 as standard clean limit; use larger Tx/Rx for tighter spacing |
| Close14 tangent under 45 mm Tx/Rx | Clean at 10% and replicated up to 15.3125% RMS noise | Strong, zero-ambiguity at promoted clean levels | Higher noise becomes point-correct but x-interval-supported | Experiments 335, 349, 356 | Source-count escalation did not rescue the boundary | Use 4 sources; do not spend more GPU time on source-count escalation |
| Close14 tangent under 50 mm Tx/Rx | Clean replicated endpoint at 19.642333984375% RMS | Strong radius margins; boundary failure is lateral x ambiguity | Final seed34 upper is numerical-edge ambiguous at 19.642372131347656% RMS | Experiment 418 cutoff-margin and x-width plots | Single target-2 sweeps cost roughly 20-25 min each on GPU | Promote 19.642333984375% RMS; stop scalar bisection unless the ambiguity rule changes |

## Immediate Next Actions

```text
1. Do not run more close14 scalar bisection.
2. Do not spend GPU time on 5/7-source escalation for the closed close14 branch.
3. Use experiment 419's replay plan when a new staged variable-radius seed or
   geometry variation is needed.
4. Material/source branch animations are packaged in experiment 49/420; add
   more only when a new matrix exposes another actual competing branch.
5. For source-shape calibration, fixed-x/z, compact all-target, compact
   center hard-noise/high-radius, dense all-target, synthesis, and compact seed
   replication pass; next widen/high-radius check the seed55 weak row.
6. For the next non-source GPU branch, choose material perturbation tied to a
   known ambiguity branch or a staged variable-radius geometry not covered by
   close60/50/30/14.
```

## Plain Summary

The current result is not "we can always identify every rebar point exactly."
The result is more specific:

```text
When acquisition geometry is adequate, the pipeline recovers the correct
locations and radii in the tested synthetic multi-rebar cases. When the
objective has a near-tie, the system now reports that as an interval instead
of hiding it behind a single best point.
```

The strongest current engineering product is therefore:

```text
detector/assignment -> location-only correction -> focused target polish with
ambiguity reporting -> optional acquisition refinement -> joint radius tuple
estimation -> replayable summary package.
```
