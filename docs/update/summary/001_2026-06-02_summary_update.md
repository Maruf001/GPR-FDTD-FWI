

## User: 

From your key reults I could not understand much, especially your conclusion. please try to explain it plainly (without dumbing down or lack of technical details, but if tehcnical detaisl included, explain those too -- it's the meaning of explaining things plainly) and also give me a holistic view. so basically we finalized the single rebar case, and now are doing multi-rebar case? what's the gist of the matter? what's going on?


## Codex: 

## Multi-Rebar Inversion Status Summary

The active work has moved from **single-rebar inversion** into the harder **multi-rebar inversion** case.

The single-rebar case is the baseline: one buried circular steel target, where the goal is to recover its location, depth, and radius from GPR-like simulated data. That case is much cleaner because there is only one object producing reflections.

The current multi-rebar work asks:

> When several rebars are close together, can the inversion still tell which object is where, how deep it is, and what radius it has?

## Key Issue: Ambiguity

The key issue now is **ambiguity**. In multi-rebar scenes, two nearby geometries can produce very similar GPR responses.

For example, the true target may be:

```text
x = 275 mm, radius = 8.0 mm
```

but a nearby wrong candidate like:

```text
x = 276 mm, radius = 7.5 mm
```

can sometimes fit the data almost as well. This is the repeated competing branch we keep seeing.

So the question is not only:

> Did the optimizer pick the true answer?

It is also:

> Was the true answer clearly better than nearby wrong answers?

That distinction is the whole point of the recent experiments.

## Terminology

**Source count** means how many scan/source positions we use. More sources usually give more information, but cost more runtime.

**Tx/Rx offset** means the spacing between transmitter and receiver. Changing this changes the measurement geometry. A larger offset can sometimes help separate overlapping responses from nearby rebars.

**close50, close30, close25, close28** describe how close the right rebar is to the middle rebar. For example:

```text
close50: x = [190, 250, 300] mm
close30: x = [190, 250, 280] mm
close25: x = [190, 250, 275] mm
close28: x = [190, 250, 278] mm
```

So smaller “close” numbers mean a harder scene.

## Current Gist

The robust multi-rebar acquisition we were testing is:

```text
4 sources + 35 mm Tx/Rx offset
```

With that setup:

```text
close50 passed cleanly
close45 passed cleanly
close40 passed cleanly
close35 passed cleanly
close30 passed, but margins became tighter
close25 failed as a clean result
```

So right now:

> **close30 is the tightest replicated clean result under 35 mm Tx/Rx.**

“Clean” here means all seeds recovered truth, confidence was strong, and there was no lateral ambiguity interval.

## close25 Rescue Attempt

Then we asked whether **close25** could be rescued by a more conservative acquisition.

We tried:

```text
close25 + 4 sources + 40 mm Tx/Rx offset
```

That did recover the true point across seeds, but it was not clean. The aggregate result was:

```text
6/6 rows selected truth geometry
3/6 rows still had x ambiguity
1 row was weak
minimum margin was very small
```

Meaning: the optimizer picked the right answer, but nearby wrong answers were too close in objective value.

So:

> **close25 at 40 mm is recoverable with warning/interval reporting, not a reliable clean resolution limit.**

## close28 Bracketing Experiment

Then we bracketed between **close30** and **close25** using **close28**:

```text
close28 + 4 sources + 35 mm Tx/Rx offset
```

Experiments **311** and **312** both selected the true answer, but the nominal rows still kept a near-best ambiguity:

```text
truth:      x278/r8
competitor: x279/r7.5
```

So **close28** looks like a transition zone. It may be point-recoverable, but it is not yet proven clean. We need **seed21** plus aggregate before making a firm policy statement.

## Holistic Conclusion

```text
Single rebar:
    Baseline problem is effectively mature.

Multi rebar:
    Active work is finding the practical resolution limit.

Current clean replicated limit:
    close30 with 4 sources and 35 mm Tx/Rx.

Below that:
    close28/close25 can still pick the true point in some settings,
    but ambiguity becomes significant.
```

## Next Logical Experiment

The next logical experiment is:

```text
run close28 seed21 with 4 sources, 35 mm Tx/Rx
then aggregate 311–313
```

If the **close28 aggregate** has ambiguity, then **close30 remains the clean limit**.

If **close28** surprisingly aggregates cleanly, then we can promote **close28** as a tighter validated limit.
