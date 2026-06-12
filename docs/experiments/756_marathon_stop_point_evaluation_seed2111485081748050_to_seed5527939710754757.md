# Experiment 756: Marathon Stop-Point Evaluation Seed2111485081748050 to Seed5527939710754757

## Purpose

Stop the autonomous GPU marathon at a clean decision boundary after completing
the current seed branch. This note summarizes what was completed before
starting another seed or field-data goal.

## Completed Runs

This stop-point covers runs 1204-1218:

```text
1204 seed2111485081748050 target2 sources=7  Tx/Rx=60   accepted
1205 seed2111485081748050 target1 sources=5  Tx/Rx=60   accepted
1206 seed3416454629006707 target0 sources=8  Tx/Rx=60   accepted
1207 seed3416454629006707 target2 sources=5  Tx/Rx=60   weak
1208 seed3416454629006707 target2 sources=7  Tx/Rx=60   weak near-miss
1209 seed3416454629006707 target2 sources=9  Tx/Rx=60   accepted rescue
1210 seed3416454629006707 target1 sources=5  Tx/Rx=60   accepted
1211 seed5527939710754757 target0 sources=8  Tx/Rx=60   weak
1212 seed5527939710754757 target0 sources=8  Tx/Rx=52.5 weak near-miss
1213 seed5527939710754757 target0 sources=8  Tx/Rx=50   accepted thin
1214 seed5527939710754757 target0 sources=8  Tx/Rx=45   accepted best bracket
1215 seed5527939710754757 target2 sources=5  Tx/Rx=60   accepted
1216 seed5527939710754757 target1 sources=5  Tx/Rx=60   weak
1217 seed5527939710754757 target1 sources=9  Tx/Rx=60   weak near-miss
1218 seed5527939710754757 target1 sources=11 Tx/Rx=60   weak negative escalation
```

## Accomplishments

Three branch-level decisions were completed:

```text
seed2111485081748050: closed accepted
  target0: accepted at 8-source Tx/Rx=60 with late-window caveat
  target2: accepted after 7-source Tx/Rx=60 rescue with early-window caveat
  target1: accepted cleanly at 5-source Tx/Rx=60

seed3416454629006707: closed accepted
  target0: accepted at 8-source Tx/Rx=60 with late-window caveat
  target2: accepted after 9-source Tx/Rx=60 rescue
  target1: accepted cleanly at 5-source Tx/Rx=60

seed5527939710754757: closed as mixed/partially unresolved
  target0: accepted after acquisition bracket, best tested point Tx/Rx=45
  target2: accepted at 5-source Tx/Rx=60 with early-window caveat
  target1: exact geometry but unresolved radius confidence after 5/9/11-source ladder
```

## Technical Findings

The useful policy signals from this block are:

```text
target0 weak controls:
  Tx/Rx acquisition bracketing remains useful.
  For seed5527939710754757, margins improved from 4.505e-04 at 60 mm
  to 4.930e-04 at 52.5 mm, 5.024e-04 at 50 mm, and 5.150e-04 at 45 mm.

target2 weak controls:
  source-density rescue remains effective.
  Seed3416454629006707 required 9 sources after weak 5- and 7-source rows.
  Seed2111485081748050 was rescued at 7 sources.

target1 weak controls:
  source-density rescue is not uniformly sufficient.
  Seed5527939710754757 improved from 4.516e-04 at 5 sources to 4.875e-04
  at 9 sources, but worsened to 3.632e-04 at 11 sources.
```

All runs preserved exact x/z/r geometry in the final state and in rank-1
diagnostic objective candidates. The unresolved issue is confidence separation
against the next radius, not localization failure.

## Stop Rationale

Do not launch another Fibonacci seed yet. The current evidence has enough new
structure to justify a synthesis step before more GPU time:

```text
1. target0 acquisition bracketing has repeated value but should not be swept
   indefinitely without a policy threshold for stopping.
2. target2 source-density rescue is still productive, usually at 7 or 9 sources.
3. target1 needs a clearer rule when 9 sources is near-miss and 11 sources
   worsens; more source density alone is not a reliable remedy.
```

## Recommended Next Decision

Before another marathon, decide one of these:

```text
A. target1 acquisition-offset probe:
   Test seed5527939710754757 target1 at 5-source Tx/Rx=52.5 before more seeds.

B. confidence-policy synthesis:
   Aggregate recent target1 weak/rescue branches and define when near-miss
   exact geometry is carried versus rescued.

C. field-data intake track:
   Keep separate from synthetic runs and start only with DZT/QC/calibration,
   not GPU FWI, until geometry and acquisition metadata are reliable.
```

Recommended immediate choice: run the CPU-side confidence-policy synthesis
first, then choose whether seed5527939710754757 target1 deserves a Tx/Rx=52.5
probe or should be carried as exact geometry with unresolved radius confidence.
