# Project State & Experiment Progression — Plain-English Audit (Experiments ~270 → 434)

Date: 2026-06-04
Scope: a coherent narrative of the multi-rebar work from roughly experiment **270** to the
current frontier (**433 complete, 434 in flight**), building on the prior summary that
covered the project up to ~experiment 310.
Basis: read end-to-end from `docs/experiments/` notes 40–51 (esp. 48 handoff matrix, 50
field-like source shape, 51 multi-rebar source-shape), the two prior `001_2026-06-02_*`
summaries, and a direct audit of the experiment `run_manifest.json` / `data/*summary*.json`
/ `figures/FIGURE_NOTES.md` files (e.g. 305, 310, 332, 335, 418, 421–434).

---

## 0. How to read this

This is one continuous technical story, not a run-by-run list. Section 1–2 define the
problem and every term. Section 3 recaps where things stood at ~270 (your existing
context). Section 4 is the heart: how the work evolved from 270 to today, in three
phases. Sections 5–10 answer the specific questions: decisions and why, compute cost
(including what "25/325" means), what worked/failed/stayed ambiguous, the current best
understanding, the open questions, and the sensible next steps. An appendix maps the
experiment-number ranges and lists a glossary.

---

## 1. What the project is trying to solve

The project simulates **ground-penetrating radar (GPR)** scanning of steel reinforcing
bars (**rebar**) buried in concrete, and runs that simulation *in reverse* to recover, for
each bar, three numbers:

```text
x = lateral position along the scan line   (mm)
z = cover depth below the surface          (mm)
r = bar radius (half the diameter)         (mm)
```

The **single-rebar** case (one bar) is mature. The active work is the harder
**multi-rebar** case: several bars are present at once, their radar echoes overlap, and
the inversion must decide *which bar is where, how deep, and how thick* — all together.

The defining difficulty is **ambiguity**. Two different geometries can produce almost
identical simulated radar data. The recurring villain in these experiments is a *coupled
shift*: the true bar at, say, `(x = 264 mm, r = 8.0 mm)` is hard to distinguish from a
competitor at `(x = 265 mm, r = 7.5 mm)` — move a bar 1 mm sideways and shrink it half a
millimetre, and the echoes barely change. So the research question is never just *"did the
optimizer pick the truth?"* It is *"was the truth **clearly** better than the nearest wrong
answer, and if not, did we report that honestly?"* Everything in the recent experiments
serves that second question.

---

## 2. The experimental setup (and every term defined)

**The forward simulator.** A 2-D finite-difference time-domain (FDTD) electromagnetic
solver on a **1 mm grid**, a **1.5 GHz** Ricker source pulse, run on the GPU with absorbing
boundaries (the `gpu-cpml` backend). One simulated scan over several transmit positions
produces a **B-scan** — a radar image of echo strength versus antenna position and
travel-time, in which each bar shows up as a hyperbola (arch).

**The scene.** Three steel bars at the same depth (`z = 90 mm`). Two different 3-bar scenes
are used for two different questions, and it matters not to confuse them:

- *Close-spacing scene* (used in experiments 270–418): bars at `x = [190, 250, 250+N]`
  with **unequal radii `r = [5, 6, 8] mm`** (left=5, centre=6, right=8). The left and
  centre bars are fixed; the **right `r = 8` bar** is pushed progressively toward the
  centre. The naming `closeN` means "right bar is `N` mm from the centre bar":

  ```text
  close50: x = [190, 250, 300]   (right bar 50 mm from centre)
  close30: x = [190, 250, 280]
  close25: x = [190, 250, 275]
  close14: x = [190, 250, 264]   ← only 14 mm apart
  ```

  At `close14`, an `r = 8 mm` bar (16 mm diameter) and an `r = 6 mm` bar (12 mm diameter)
  whose centres are 14 mm apart are **exactly tangent — physically touching**. That is why
  note 48 calls it "close14 tangent." It is the hardest separation the geometry allows.

- *Source-shape scene* (used in experiments 425–434): the original **wide, equal-radius**
  Stage-4C scene, bars at `x = [150, 250, 350]` (100 mm apart) with **`r = 6 mm` each**.
  Here spacing is easy; the question is a different kind of robustness (source pulse shape).

**The acquisition knobs.**

- **Sources** = the number of scan/transmit positions used to illuminate and measure the
  scene (typically 3, 4, 5, or 7). More positions = more information but more runtime.
- **Tx/Rx offset** = the lateral distance between transmitter and receiver antennas (20–50
  mm in these runs). Changing it changes *which part of the subsurface response is
  emphasized*; a larger offset can help separate the overlapping echoes of nearby bars.
  This knob turns out to be the single most important lever in the whole recent campaign.

**The search engine (important: this is not gradient FWI).** The robust rebar-sizing
results do **not** come from adjoint gradient descent. They come from a **source-profiled
candidate evaluation + staged coordinate optimizer**: it updates **one bar at a time** over
a small local grid of candidate `(x, z, r)` values, and *at each candidate* it fits a few
**source nuisance parameters** — a frequency-scale, a time-shift, and an amplitude — so a
slightly-wrong assumed source pulse cannot corrupt the geometry answer. For each target it
reports the best candidate **plus the runner-up candidates, the margin, a confidence label,
and an ambiguity interval**. Candidates are enumerated (not gradient-followed) precisely so
that near-ties become visible and reportable.

**Seeds and cases.** `seed13`, `seed21`, `seed34` are random-noise realizations — the same
experiment under three different noise patterns; a result that survives all three is real,
not luck. Each seed usually carries **two observed cases**: a *nominal* case (expected
source + noise) and a *source-mismatch* case (the source pulse is deliberately perturbed —
frequency +10 %, −50 ps timing, amplitude +10 %). So an aggregate over 3 seeds × 2 cases =
**6 rows**.

**The metrics (what "clean" means).**

- **Misfit / objective** = how badly a candidate disagrees with the data (lower is better).
- **Margin** = the objective gap between the best candidate and the next *distinct*
  competitor. Large margin ⇒ confident; tiny margin ⇒ fragile.
- **Confidence label** — `strong` (clearly separated), `moderate` (better but not by much),
  `weak` (barely better; report uncertainty).
- **Ambiguity interval** = the span of `x` (or `r`) values that remain close enough to the
  best to not be ruled out, e.g. "x = 264–265 mm."
- **"Clean"** = the gold standard for one acquisition setting: **all 6 rows select the true
  geometry, all are `strong`, and there is zero ambiguity interval.** "Point-correct but not
  clean" means the optimizer chose truth but a competitor was close enough to keep an
  interval/warning.

---

## 3. Where things stood around experiment 270

By ~270 the single-rebar problem was considered solved (source-profiled local radius polish,
with a high-frequency stage for size confidence, always reporting intervals). The
multi-rebar effort had built a **staged pipeline** for the variable-radius `[5, 6, 8]`
close-spacing scene:

```text
detect bars → assign one seed per bar → location-only correction (radii fixed)
            → focused polish of the hard target → joint radius-tuple estimation
            → confidence / ambiguity reporting → replayable summary
```

This worked cleanly for `close60`. But as the right `r = 8` bar was moved closer to the
centre, **its lateral position became the bottleneck**: the coupled `(x, r) → (x+1, r−0.5)`
competitor kept fitting almost as well. `close50` could only be disambiguated by *changing
the acquisition geometry*, and around 270 the team was probing how many sources and what
Tx/Rx offset were needed (experiment 276 was testing 4 sources at 40 mm Tx/Rx). The open
question entering this window was therefore precise: **how close can two bars be before the
inversion can no longer separate them cleanly — and what acquisition makes that limit
tighter?**

---

## 4. How the experiments evolved, 270 → 434

The arc has **three distinct phases**.

### Phase A — Lateral-resolution sweep (≈270–335): how close can bars get?

With **4 sources** adopted as the working source count, the team systematically tightened
the spacing — `close50, 45, 40, 35, 30, 25, 20, 15, 14` — while sweeping the **Tx/Rx
offset** (35, 40, 45 mm) and re-checking source count. Each setting was run on seeds
34/13/21 and aggregated into a `coordinate_confidence_*` summary. Audited outcomes:

| Spacing | Tx/Rx | Result (6 rows) | Min radius margin | x-ambiguity rows |
|---|---|---|---|---|
| close40 | 35 mm | 6/6 truth, **6 strong, clean** | 5.9e-3 | 0 |
| **close30** | **35 mm** | 6/6 truth, **6 strong, clean** | 1.5e-3 | 0 |
| close25 | 40 mm | 6/6 truth, **not clean** (strong 3 / moderate 2 / weak 1) | 4.9e-4 | **3** (1 mm) |
| close15 | 45 mm | 6/6 truth, **6 strong, clean** | 2.6e-3 | 0 |
| **close14 (tangent)** | **45 mm** | 6/6 truth, **6 strong, clean** | 2.6e-3 | 0 |

The standout discovery: **the Tx/Rx offset is a far stronger lever than the spacing is a
penalty.** At the standard 35 mm offset, `close30` is the clean limit and `close25` fails.
But simply widening the offset to **45 mm makes even `close14` — bars physically touching —
clean at 10 % noise**, with strong margins. (Note the non-monotone clue: `close25` at 40 mm
was *ambiguous*, yet the *tighter* `close14` at 45 mm is *clean* — the extra 5 mm of offset
more than pays for the tighter geometry.) A parallel check confirmed that **escalating the
source count (5, 7) did not rescue the boundary**, so 4 sources is the validated minimum and
more sources are not worth the GPU time. The phase conclusion: **4 sources + 45 mm Tx/Rx
resolves the tightest geometry the scene allows.**

### Phase B — Noise-ceiling bisection (≈336–418): how much noise can the tangent case take?

Having maxed out *geometry*, the team turned the orthogonal knob: at the hardest scene
(`close14` tangent, 4 sources), **how much measurement noise before "clean" breaks?** They
ran a **binary search on the noise level** (RMS %). This is the explanation for the
bizarre-looking run names — the ever-finer noise values are successive bisection midpoints:

```text
15 → 17.5 → 16.25 → 15.625 → 15.3125 → … (at Tx/Rx 45 mm)
… raise offset to 50 mm …
19.375 → 19.53125 → 19.609375 → … → 19.642333984375 → 19.642372131347656
```

- At **45 mm** Tx/Rx, `close14` stayed clean up to **15.3125 % RMS** noise.
- Raising the offset to **50 mm** pushed the ceiling to **≈ 19.64 % RMS**.
- The `418` boundary summary records the converged result precisely:
  **promoted clean = 19.642333984375 % RMS** (3-seed clean, exp 409/412); the first
  **ambiguous** level above it is **19.642372131347656 %** (exp 417), where the nominal
  margin to the cutoff is `−7.4e-10`. The final bracket width is **3.8 × 10⁻⁵ %** — i.e.
  they bisected down to the **floating-point precision edge** and *stopped on purpose*
  (`stop_due_to_numerical_edge = true`), because narrowing further has no physical meaning.

Two things matter here. First, the **failure mode at the boundary is not radius** — radius
margins stay strong throughout; it is **lateral-x ambiguity** (the `x265/r7.5` competitor
finally creeps inside tolerance). So "above the ceiling" means *point-correct but
x-interval-supported*, not *wrong*. Second, this phase deliberately ended: note 48 records
the decision to **stop scalar noise bisection and stop source-count escalation** for this
closed branch.

*(Interlude, 419–420: consolidation, not new physics — a "replay plan" capturing the
15-stage variable-radius pipeline as reproducible commands, and packaged material/source
animations.)*

### Phase C — Source-shape / "ringdown" branch (≈421–434): a different robustness axis

The team then pivoted from *acquisition geometry* to the **shape of the source pulse**. Real
GPR sources are not a clean Ricker wavelet — they **ring down** (a delayed secondary pulse).
The accepted source-profiling only adjusts amplitude, timing, and frequency-scale; does it
survive a shaped source?

The single-rebar diagnostics (421–424) tell a tight story:

```text
421  inject ringdown into the data, keep the OLD profile model
       → FAILS: picks r = 7.8 mm (grid max) instead of 6.0, with a *positive* margin.
         The nuisance fit "explains" the ringing by faking a bigger bar
         (fc=1.1, +80 ps, amp≈0.767). A real warning for field data.
422  add a discrete modeled ringdown {0, 0.25}      → fixes the exact-0.25 cases.
423  but observed ringdown 0.20 (off the grid)      → FAILS again at r = 7.8 mm,
         because one global amplitude can't fit the primary and ringdown pulses separately.
424  replace the grid with a primary+ringdown BASIS-COEFFICIENT least-squares fit
       → ALL tested rows recover r = 6.0 mm, and the fitted ringdown coefficient
         matches what was injected (0.20, 0.25, 0.30). This is the fix.
```

In plain terms: instead of guessing the ringdown size from a short list, the model carries
**two source "building blocks" — a primary pulse and a delayed pulse — and solves for how
much of each best explains the data.** That small, physically interpretable fit stops source
ringing from being mistaken for a larger bar.

Then 425–434 carried this into the **wide, equal-radius 3-bar scene** (`x = [150, 250, 350]`,
`r = 6 mm` each), with the two neighbours **fixed at truth**, testing each target in turn:

```text
425  left, fixed x/z, 5 radii ...................... all 4 ringdown cases correct
426/427/428  left/centre/right, compact 3×3×3 window  all correct; competitor = r 6.2 at true x/z
429  centre, hard noise (10% noisy ringdown + mismatch)  correct; weakest margin 1.813e-4
430  centre + high-radius decoys r 7.4/7.8 ......... decoys never reach the top candidates
431  centre, wider 5×5 x/z window ................. correct; high-radius only ranks 9–12
432  centre, DENSE Stage-4C radius grid (325 cand) . correct; a shifted-depth z91/r6.8–7.0
                                                      branch appears ~rank 3 but stays secondary
433  left,  DENSE Stage-4C grid .................... correct, same secondary branch
434  right, DENSE Stage-4C grid .................... ** CURRENTLY RUNNING ** (completes coverage)
```

So the source-shape fix is now validated for **all three targets in compact windows**, and
**for the centre and left targets on the dense radius grid**; experiment **434 (right,
dense) is executing right now** to finish the all-target dense coverage that note 51 listed
as the next step.

---

## 5. The major decisions, and why (grounded in the evidence)

1. **Acquisition geometry (Tx/Rx offset) is the primary disambiguation lever — over source
   count.** Evidence: 45 mm makes the tangent case clean while 40 mm leaves `close25`
   ambiguous, and adding sources (5, 7) did not move the boundary. So the policy is "use 4
   sources; widen the offset," not "throw more scan positions at it."
2. **Reporting must be acquisition-aware.** Summaries now record the Tx/Rx offset and source
   count explicitly (added around 272–273) so that a 35 mm result is never silently compared
   to a 50 mm result. Mixing them would hide the dominant lever.
3. **Confidence labels and ambiguity intervals are mandatory.** Because the optimizer
   routinely picks the truth *while a competitor sits within the noise floor*, "picked
   truth" is not a result on its own — the honest product is "picked truth **and** here is
   how separated it was."
4. **Stop scalar noise bisection at the numerical edge.** Once the clean/ambiguous bracket
   reaches ~10⁻⁹ in objective margin (3.8 × 10⁻⁵ % in noise), further bisection measures
   floating-point arithmetic, not physics. The promoted ceiling (19.642333984375 %) is the
   honest endpoint.
5. **Scale one step at a time; narrow windows before broad sweeps.** Repeatedly stated in the
   notes — compact 27-candidate gates precede 325-candidate dense grids — because a dense
   grid costs ~3 GPU-hours and a broad blind sweep wastes that.
6. **Source-shape fitting is a calibration *diagnostic*, not the default production
   objective.** The basis fit fixes the ringdown failure, but the team deliberately refuses
   to carry a large, free-form source model in production — the same caution that earlier
   rejected optimal-transport and free material parameters: a flexible-enough source model
   could itself *absorb* radius error and make the size estimate meaningless.

---

## 6. How many simulations per cycle, and how long it takes

**One forward B-scan** ≈ one FDTD solve per transmit position. On the DGX Spark (GB10) GPU
at the 1 mm / 1.5 GHz production grid, that is **≈ 1 s per transmit position**, so **≈ 4–5 s
for a 4–5-source B-scan**.

**A coordinate-optimizer target sweep** (the unit of Phases A–B). It updates one bar over a
local grid of **x-offsets {−2,−1,0,1,2} (5) × z-offsets {0,5,10} (3) × radius-offsets
{−1 … +2} (7) = 105 candidate geometries** per observed case, and at each candidate
simulates **3 modeled frequency-scales** (the time-shift and amplitude are fit in trace
space, no re-solve). That is **≈ 315 modeled B-scans (≈ 1,260 single-source FDTD solves)**
per run, reused across the 2 observed cases. Measured: **≈ 1,400 s ≈ 23 min per run**
(consistent with note 48's "20–25 min each"). The progress prints you see — `25/210`,
`50/210` — are the *candidate index* across the 105×2 = 210-row case grid, emitted every
`--progress-every` candidates.

**Cost of the phases.** The noise bisection (336–418) was roughly **60+ optimizer runs plus
~15 aggregates** — on the order of **25–30 GPU-hours** for that phase alone, to pin a single
noise number. The source-shape runs scale directly with candidate count and carry **6
modeled B-scans per candidate** (3 frequency-scales × primary+ringdown bases, ≈ 32 s/cand):

```text
  5 candidates  →   161 s
 27 candidates  →   873–882 s
 45 candidates  →  1,472 s
125 candidates  →  4,076 s
325 candidates  → 10,526 s  (≈ 2.9 h)   ← the dense Stage-4C grids (432/433/434)
```

This is the literal source of your **"25/325 checkpoint"**: the dense grids run
`--progress-every 25` over **325 candidates** (x 248:252 ×5, z 88:92 ×5, r 5.4:7.8:0.2 ×13),
so each checkpoint is ~25 candidates ≈ ~13 min, and a full dense run is ~2.9 h. (For
comparison, the single-rebar source-shape matrices in 421–424 were 52–candidate × 7-case
grids at ~1,700 s each.)

---

## 7. What worked, what did not, what stayed ambiguous

**Worked.**
- 4 sources + **45 mm** Tx/Rx cleanly separates **tangent** bars (`close14`) at 10 % noise.
- Widening Tx/Rx offset as the disambiguation lever (geometry beats source count).
- A **noise ceiling of ≈ 19.64 % RMS** at 50 mm offset for the tangent case.
- The **primary+ringdown basis-coefficient fit** recovers the true radius under source
  ringing where the old profile failed — validated across all 3 targets (compact) and
  centre/left (dense).

**Did not work.**
- 35 mm Tx/Rx below `close30`; `close25` clean even at 40 mm.
- **Source-count escalation** (5, 7) to push the resolution/noise boundary.
- The **old amplitude/time/frequency source profile under ringdown** (selects a fake big
  bar) and the **discrete ringdown grid** for off-grid ringing (e.g. observed 0.20).

**Ambiguous / still soft.**
- The coupled **`(x, r) → (x+1, r−0.5)`** competitor is the persistent fragile branch near
  every limit — it is *managed by reporting*, not eliminated.
- In the dense source-shape grids, a **shifted-depth `z ≈ 91 mm, r ≈ 6.8–7.0 mm`** branch
  reappears at ~rank 3 — secondary, not a tie, but a recurring near-degeneracy worth
  watching.
- The noise-ceiling's final bracket is a **numerical-precision artefact**, not a physically
  meaningful resolution of the boundary.

---

## 8. Current best understanding

The pipeline does **not** claim "we always recover every rebar exactly." It claims something
more precise and more defensible:

> When the acquisition geometry is adequate, the pipeline recovers the correct `x/z/r` for
> the tested synthetic multi-rebar scenes; and when the objective has a near-tie, it
> **reports that as an interval instead of hiding it behind a single best point.**

Concretely, as of today:

- **Lateral separation:** with 4 sources + 45 mm Tx/Rx, the variable-radius `[5,6,8]` scene
  is cleanly separable down to **tangent bars (14 mm centre spacing)** at 10 % noise;
  `close30` is the clean limit at the standard 35 mm offset.
- **Noise robustness:** the tangent case stays clean to **≈ 19.64 % RMS** at 50 mm offset;
  beyond that it is point-correct with a lateral-x interval, never silently wrong.
- **Source-pulse robustness:** a small interpretable **primary+ringdown source basis**
  prevents source ringing from masquerading as a larger bar, and it behaves the same with
  neighbouring rebars present (compact and dense windows).
- **Strongest engineering product** (note 48): *detector/assignment → location-only
  correction → focused target polish with ambiguity reporting → optional acquisition
  refinement → joint radius-tuple estimation → replayable summary package.*

---

## 9. Limitations, bottlenecks, and unresolved questions

- **All synthetic, all 2-D.** No lab or field data yet; 3-D is out of scope. Every "clean"
  statement is a statement about controlled synthetic scenes.
- **Source-shape multi-rebar gates fix the neighbours at truth.** They are *not yet a joint
  multi-bar + source-shape inversion*; the two neighbouring bars are assumed perfectly
  known. Note 51 is explicit that this is "not yet a full multi-rebar source-shape
  validation."
- **The two hard axes have not been combined.** Lateral resolution was studied on the
  variable-radius close-spacing scene; source-shape was studied on the easy wide scene.
  Source ringing in a *tightly-spaced* scene is untested.
- **The clean tangent limit depends on a 45–50 mm Tx/Rx offset.** Whether that offset is
  physically realizable / standard for real GPR antennas is an open grounding question — the
  result may be partly an artefact of an idealized acquisition.
- **The ringdown basis is a single fixed shape** (180 ps delay, 0.8 frequency-scale). Real
  source shapes are richer, and a more flexible source model risks absorbing radius — which
  is exactly why it is kept as a diagnostic, not promoted to production.
- **Compute is the throughput bottleneck:** dense grids are ~3 GPU-hours each; full
  multi-target dense coverage and any joint extension multiply that. Cost grows as
  `candidates × source-bases × sources`.

---

## 10. The most sensible next steps

1. **Let 434 finish** (right-target dense Stage-4C source-shape) → all-three-target dense
   coverage of the source-shape branch is then complete; record the right-target margins and
   whether the same secondary `z91/r6.8–7.0` branch behaves.
2. **Relax the "neighbours fixed at truth" assumption** — a first *joint* multi-rebar
   source-shape test, even on a compact window, to move from "diagnostic on an easy scene" to
   a genuine multi-bar result.
3. **Combine the two hard axes** — run the source-shape (ringdown) stress on the
   *close-spacing* `[5,6,8]` scene, where lateral ambiguity and source ringing could
   interact. This is the most informative untested corner.
4. **Ground the acquisition assumption** — check whether 45–50 mm Tx/Rx offsets correspond to
   realistic field GPR hardware, or document the result as an idealized-acquisition limit.
5. **Do not** resume scalar noise bisection, and **do not** spend GPU time on 5/7-source
   escalation for the closed `close14` branch (both explicitly retired in note 48). The next
   non-source GPU branch flagged by the handoff matrix is either a **material perturbation
   tied to a known ambiguity branch** or a **staged variable-radius geometry not covered by
   close60/50/30/14**.
6. **Begin the path toward lab/field data** once the joint source-shape result exists, since
   the source-shape work was explicitly motivated as the pre-field-data calibration step.

---

## Appendix A — Experiment-number map (≈270 → 434)

```text
270–271      close50, 4 src, 40 mm Tx/Rx, seed replicates + summary
272–273      acquisition-metadata + acquisition-aware aggregate (don't mix Tx/Rx silently)
274–280      close50 source-count study (3 vs 4 vs 5), settle on 4 sources
281–289      close50 Tx/Rx study (25/30/35 mm), settle on 35 mm robust region
290–305      LATERAL SWEEP at 35 mm Tx/Rx: close45→40→35→30→25  (clean limit = close30)
306–335      Tx/Rx widened to 40/45 mm; push close25→20→15→14   (45 mm ⇒ close14 tangent clean)
336–355      NOISE BISECTION at close14, 45 mm Tx/Rx (+ a 3/5/7-source re-check)
357–418      NOISE BISECTION at close14, 50 mm Tx/Rx → ceiling 19.642333984375 % RMS (418 summary)
419–420      consolidation: replay plan + material/source animations (no new physics)
421–424      SINGLE-REBAR source ringdown: fail → discrete grid → basis-coefficient fit (the fix)
425–428      MULTI-REBAR source-shape gates: left/centre/right, compact windows
429–431      centre hard-noise / high-radius decoys / wider x-z window
432–434      DENSE Stage-4C source-shape grids: centre (432), left (433), right (434, RUNNING)
```

## Appendix B — Glossary

- **GPR / FDTD / B-scan** — ground-penetrating radar; the finite-difference time-domain
  forward simulator; the position-vs-time radar image it produces.
- **x / z / r** — a bar's lateral position, cover depth, and radius (the three unknowns).
- **closeN** — the right `r = 8` bar is `N` mm from the centre bar (`close14` = tangent).
- **Sources / Tx-Rx offset** — number of scan positions; transmitter–receiver separation
  (the dominant lever for separating nearby bars).
- **Seed / case / row** — a noise realization; a nominal vs source-mismatch observation; one
  confidence result. 3 seeds × 2 cases = 6 rows per aggregate.
- **Misfit / margin / confidence / ambiguity interval** — data disagreement (lower better);
  gap to the next competitor; strong/moderate/weak label; the span of values not ruled out.
- **Clean** — all 6 rows truth, all strong, zero ambiguity interval.
- **Ringdown** — a delayed secondary pulse in the source wavelet (source "ringing"); the
  basis-coefficient fit models it as primary + delayed pulse and solves their weights.
- **Coupled competitor** — the recurring fragile near-tie `(x, r) ↔ (x+1, r−0.5)`.
- **DGX Spark / GB10** — the NVIDIA Grace-Blackwell GPU platform (128 GB unified memory) on
  which all production simulations run.
```
