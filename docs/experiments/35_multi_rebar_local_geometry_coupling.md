# Experiment 35: Multi-Rebar Local Geometry Coupling

## Goal

Test whether the weaker per-rebar radius margins from Experiment 34 survive
local x/z/r variation in the 3-rebar scene.

The first target is the left rebar because it had the weakest fixed-position
10% noise margin:

```text
left rebar, nominal 10% noise margin: 2.263e-04
```

## Code Changes

Added:

```text
run_multi_rebar_local_geometry_profile.py
tests/test_multi_rebar_local_geometry_profile.py
```

Reused:

```text
run_multi_rebar_common_radius_profile.py GPU CPML simulation helpers
inversion.source_profile.source_profiled_ls
```

## Validation Before GPU Run

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_multi_rebar_local_geometry_profile.py \
  tests/test_multi_rebar_common_radius_profile.py \
  tests/test_source_profile.py \
  -q
```

Result:

```text
16 passed
```

Compile check:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_multi_rebar_local_geometry_profile.py \
  run_multi_rebar_common_radius_profile.py \
  inversion/source_profile.py
```

Result:

```text
passed
```

## Stage 4C Plan

Fixed scene:

```text
3 rebars:
  x = 150, 250, 350 mm
  z = 90 mm
  radius = 6 mm
```

Target:

```text
left rebar, index 0
```

Local target grid:

```text
x:      148, 149, 150, 151, 152 mm
z:      88, 89, 90, 91, 92 mm
radius: 5.4-7.8 mm in 0.2 mm steps
```

Cases:

```text
noise10_seed13
source_mismatch_noise10_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 0 \
  --target-x-values-mm 148:152:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name multi_rebar_left_local_geometry_noise10
```

Decision gate:

```text
Pass if both cases select x=150 mm, z=90 mm, r=6.0 mm with positive
distinct-radius margins. If a neighboring x/z and wrong radius wins, full
multi-rebar optimization should wait for stronger confidence/window rules.
```

## Running Log

### 067_multi_rebar_left_local_geometry_noise10

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 0 \
  --target-x-values-mm 148:152:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name multi_rebar_left_local_geometry_noise10
```

Output:

```text
outputs/experiments/067_multi_rebar_left_local_geometry_noise10
```

Runtime and count:

```text
325 target x/z/r candidates
2 observed cases
3 modeled source-frequency scales per candidate
4811.28 s
```

Case summary:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin | Source profile |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| noise10_seed13 | 150.0 | 90.0 | 6.0 | 6.2 | 2.263e-04 | fc=1.0, shift=0 ps, amp=0.998 |
| source_mismatch_noise10_seed13 | 150.0 | 90.0 | 6.0 | 6.2 | 3.117e-04 | fc=1.1, shift=-50 ps, amp=1.100 |

Top candidates:

| Case | Rank | x [mm] | z [mm] | r [mm] | J |
| --- | ---: | ---: | ---: | ---: | ---: |
| noise10_seed13 | 1 | 150.0 | 90.0 | 6.0 | 8.040e-02 |
| noise10_seed13 | 2 | 150.0 | 90.0 | 6.2 | 8.062e-02 |
| noise10_seed13 | 3 | 150.0 | 91.0 | 6.8 | 8.127e-02 |
| noise10_seed13 | 4 | 150.0 | 91.0 | 7.0 | 8.147e-02 |
| source_mismatch_noise10_seed13 | 1 | 150.0 | 90.0 | 6.0 | 8.947e-02 |
| source_mismatch_noise10_seed13 | 2 | 150.0 | 90.0 | 6.2 | 8.978e-02 |
| source_mismatch_noise10_seed13 | 3 | 150.0 | 91.0 | 6.8 | 9.044e-02 |
| source_mismatch_noise10_seed13 | 4 | 150.0 | 91.0 | 7.0 | 9.077e-02 |

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png: 1617x920 px, dynamic range 255, std 32.222
```

Interpretation:

```text
The left-rebar local x/z/r coupling test passes. The best target geometry
stays at the true x=150 mm, z=90 mm, r=6.0 mm under nominal 10% noise and
source-mismatched 10% noise.
```

Important caveat:

```text
The margins remain small. The local x/z/r freedom did not erase the left-rebar
radius evidence, but production reporting still needs top-k ambiguity and
confidence fields before full multi-rebar optimization can be trusted.
```

## Stage 4C Interim Decision

The weakest fixed-position per-rebar case passed the x/z/r coupling test.

Next action:

```text
Run the same local x/z/r coupling matrix for the center rebar. If center also
passes, the remaining right-rebar test can be treated as a symmetry/edge check
or deferred behind confidence-layer implementation.
```
