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

### 061_source_profiled_geometry_window_exact_mismatch

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

Output:

```text
outputs/experiments/061_source_profiled_geometry_window_exact_mismatch
```

Runtime and count:

```text
325 geometry candidates
2 observed cases
3 modeled source-frequency scales per candidate
4987.25 s
```

GPU check during run:

```text
nvidia-smi reported NVIDIA GB10 at 88% GPU utilization.
The active process was /home/lam001/miniforge3/envs/FNO/bin/python with the
--backend gpu-cpml command.
```

Case summary:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin | Source profile |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| nominal | 250.0 | 90.0 | 6.0 | 6.2 | 9.815e-04 | fc=1.0, shift=0 ps, amp=1.000 |
| source_mismatch | 250.0 | 90.0 | 6.0 | 6.2 | 1.146e-03 | fc=1.1, shift=-50 ps, amp=1.100 |

Top candidates:

| Case | Rank | x [mm] | z [mm] | r [mm] | J |
| --- | ---: | ---: | ---: | ---: | ---: |
| nominal | 1 | 250.0 | 90.0 | 6.0 | 0.000e+00 |
| nominal | 2 | 250.0 | 90.0 | 6.2 | 9.815e-04 |
| nominal | 3 | 250.0 | 91.0 | 6.8 | 1.277e-03 |
| nominal | 4 | 250.0 | 91.0 | 7.0 | 1.718e-03 |
| source_mismatch | 1 | 250.0 | 90.0 | 6.0 | 1.295e-05 |
| source_mismatch | 2 | 250.0 | 90.0 | 6.2 | 1.159e-03 |
| source_mismatch | 3 | 250.0 | 91.0 | 6.8 | 1.456e-03 |
| source_mismatch | 4 | 250.0 | 91.0 | 7.0 | 1.976e-03 |

Plot validation:

```text
source_profiled_replication_radius_profiles.png: 1651x937 px, dynamic range 255, std 32.707
```

Interpretation:

```text
Stage 3A passes for exact data. The wider +/-2 mm x/z window does not move the
best solution away from x=250 mm, z=90 mm, r=6.0 mm. The closest wrong-radius
candidate remains r=6.2 at the correct x/z, followed by a deeper high-radius
candidate around z=91 mm and r=6.8-7.0 mm.
```

This result means the accepted source-profiled polish is not only a narrow
radius selector. In exact data it can reject nearby wrong x/z cells inside a
5 mm by 5 mm window. The next risk is whether 5-10% noise makes the deeper
high-radius candidate competitive.

## Stage 3A Decision

Stage 3A passes.

Next action:

```text
Run the same wider x/z/r window with 10% nominal noise and 10% source-mismatch
noise. If the z=91 mm, r=6.8-7.0 mm candidate overtakes the true radius under
noise, the final production workflow needs a narrower geometry window or a
confidence warning before reporting radius.
```

## Stage 3B Noisy Geometry-Window Plan

Purpose:

```text
Test whether 10% noise makes the deeper high-radius competitor from Stage 3A
overtake the true r=6.0 mm solution in the wider x/z/r window.
```

Cases:

```text
nominal_noise10_seed13:
  source fc scale 1.0, shift 0 ps, amp 1.0, noise 10%

source_mismatch_noise10_seed13:
  source fc scale 1.1, shift -50 ps, amp 1.1, noise 10%
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases "nominal_noise10_seed13:1.0,0.0,1.0,0.10,13|source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13" \
  --x-values-mm 248:252:1 \
  --z-values-mm 88:92:1 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name source_profiled_geometry_window_noise10
```

Decision gate:

```text
Pass if both cases select x=250 mm, z=90 mm, r=6.0 mm with a positive
distinct-radius margin. If either case selects the deeper high-radius candidate,
do not move to multi-rebar yet; first add window-size rules or confidence
warnings.
```
