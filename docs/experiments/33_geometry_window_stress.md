# Experiment 33: Geometry Window Stress

## Goal

Stress the accepted source-profiled local radius polish with a wider x/z/r
candidate window.

The Stage 2 result is strong at a fixed local x/z window. Stage 3 asks:

```text
How wide can the final local polish window be before x/z/r ambiguity or hard
grid snapping creates misleading top candidates?
```

## Current Evidence Entering Stage 3

Passed:

```text
Stage 1:
  exact and combined source-mismatch smoke gates

Stage 2A:
  compact exact/noise/source-mismatch matrix

Stage 2B:
  16-case noise/source seed replication matrix
```

Important limitation:

```text
Those tests used x=250 mm and z near 90-91.5 mm. They prove radius robustness
inside a good local basin, not how wide the basin can safely be.
```

## Stage 3A Plan

Use the existing source-profiled replication runner with a wider geometry grid:

```text
x:      248, 249, 250, 251, 252 mm
z:      88, 89, 90, 91, 92 mm
radius: 5.4-7.8 mm in 0.2 mm steps
cases:  nominal exact, combined source mismatch exact
```

Candidate count:

```text
5 x values * 5 z values * 13 radii = 325 geometry candidates
3 modeled source-frequency scales per candidate
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases "nominal:1.0,0.0,1.0,0.0,13|source_mismatch:1.1,-50.0,1.1,0.0,13" \
  --x-values-mm 248:252:1 \
  --z-values-mm 88:92:1 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name source_profiled_geometry_window_exact_mismatch
```

Decision gate:

```text
Pass if both cases select x=250 mm, z=90 mm or a known equivalent hard-grid
cell, and r=6.0 mm with a positive distinct-radius margin.
```

If this fails:

```text
inspect top-k candidates by x/z/r,
separate location ambiguity from radius ambiguity,
then decide whether subcell geometry or a narrower final polish window is the
right next intervention.
```

## Running Log

No Stage 3 GPU run has been completed yet.
