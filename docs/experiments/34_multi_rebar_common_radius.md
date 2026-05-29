# Experiment 34: Multi-Rebar Common-Radius Profile

## Goal

Extend the accepted single-rebar source-profiled confidence workflow to the
existing 3-rebar scene.

This first multi-rebar stage is intentionally scoped:

```text
fixed known x/z positions,
one shared/common radius for all rebars,
source-profiled LS objective,
top-k candidates and distinct-radius margins.
```

This is not yet the full 9-parameter multi-rebar inversion. The purpose is to
test whether multi-rebar scattering preserves radius evidence before adding the
full combinatorial geometry search.

## Code Changes

Added:

```text
run_multi_rebar_common_radius_profile.py
tests/test_multi_rebar_common_radius_profile.py
```

Reused:

```text
core.geometry.build_rebar_model
gpu.fdtd_gpu_v2.FDTDSimulatorGPU_v2 with run_batch
inversion.source_profile.source_profiled_ls
run_single_rebar_source_profiled_replication.parse_replication_cases
```

## Validation Before GPU Run

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_multi_rebar_common_radius_profile.py \
  tests/test_source_profiled_replication_runner.py \
  tests/test_source_profile.py \
  -q
```

Result:

```text
14 passed
```

Compile check:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_multi_rebar_common_radius_profile.py \
  run_single_rebar_source_profiled_replication.py \
  inversion/source_profile.py
```

Result:

```text
passed
```

## Stage 4A Plan

Truth:

```text
3 rebars from config.py:
  x = 150, 250, 350 mm
  z = 90 mm
  radius = 6 mm
```

Candidate grid:

```text
common radius: 5.4-7.8 mm in 0.2 mm steps
```

Cases:

```text
nominal
noise10_seed13
source_mismatch
source_mismatch_noise10_seed13
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_common_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 2 \
  --run-name multi_rebar_common_radius_profile
```

Decision gate:

```text
Pass if every case selects common radius 6.0 mm and source-mismatch cases
recover source fc scale 1.1 and time shift -50 ps. If this fails, do not move
to full 9-parameter multi-rebar optimization; first diagnose whether radius
evidence is weakened by multi-rebar interactions.
```

## Running Log

### 063_multi_rebar_common_radius_profile

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_common_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 2 \
  --run-name multi_rebar_common_radius_profile
```

Output:

```text
outputs/experiments/063_multi_rebar_common_radius_profile
```

Runtime and count:

```text
13 common-radius candidates
4 observed cases
3 modeled source-frequency scales per candidate
190.03 s
```

Case summary:

| Case | Best r [mm] | Next r [mm] | Margin | Best J | Source profile |
| --- | ---: | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 1.122e-03 | 0.000e+00 | fc=1.0, shift=0 ps, amp=1.000 |
| noise10_seed13 | 6.0 | 6.2 | 9.930e-04 | 8.040e-02 | fc=1.0, shift=0 ps, amp=0.998 |
| source_mismatch | 6.0 | 6.2 | 1.221e-03 | 4.490e-06 | fc=1.1, shift=-50 ps, amp=1.100 |
| source_mismatch_noise10_seed13 | 6.0 | 6.2 | 1.090e-03 | 8.947e-02 | fc=1.1, shift=-50 ps, amp=1.100 |

Plot validation:

```text
multi_rebar_common_radius_profiles.png: 1617x920 px, dynamic range 255, std 34.142
```

Top-candidate note:

```text
The best radius is correct in every case. In source-mismatched cases, larger
radii around 7.2-7.4 mm appear in the top five with a -25 ps source shift, but
they remain well below the true r=6.0 candidate.
```

Interpretation:

```text
Stage 4A passes. With fixed true x/z positions and one shared radius, the
source-profiled confidence workflow transfers cleanly from one rebar to the
existing 3-rebar scene. Multi-rebar scattering did not erase common-radius
evidence in exact, 10% noisy, source-mismatched, or source-mismatched noisy
cases.
```

## Stage 4A Decision

Stage 4A passes.

Next action:

```text
Relax the common-radius assumption one controlled degree at a time. The next
test should sweep the radius of one rebar while holding the other two at the
true radius, starting with the center rebar and then checking the side rebars.
This tests per-rebar size identifiability before attempting full 9-parameter
multi-rebar optimization.
```

## Stage 4B Center-Rebar Radius Sweep Plan

Code extension:

```text
run_multi_rebar_common_radius_profile.py now supports:
  --sweep-rebar-index -1  common radius for all rebars
  --sweep-rebar-index N   sweep only rebar N and keep the others at truth
```

Focused validation:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_multi_rebar_common_radius_profile.py \
  tests/test_source_profile.py \
  -q
```

Result:

```text
12 passed
```

Compile check:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_multi_rebar_common_radius_profile.py \
  inversion/source_profile.py
```

Result:

```text
passed
```

Purpose:

```text
Sweep only the center rebar radius while side rebars remain fixed at 6.0 mm.
This is the hardest single-bar sweep because the center bar has neighbors on
both sides.
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_common_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --sweep-rebar-index 1 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 2 \
  --run-name multi_rebar_center_radius_profile
```

Decision gate:

```text
Pass if all cases select center-bar radius 6.0 mm. If the source-mismatch cases
prefer a large radius plus shifted source profile, the per-rebar workflow needs
additional source/geometry constraints before full multi-rebar inversion.
```

### 064_multi_rebar_center_radius_profile

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_common_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --sweep-rebar-index 1 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 2 \
  --run-name multi_rebar_center_radius_profile
```

Output:

```text
outputs/experiments/064_multi_rebar_center_radius_profile
```

Runtime and count:

```text
13 swept-radius candidates
sweep_rebar_index = 1
4 observed cases
3 modeled source-frequency scales per candidate
191.93 s
```

Case summary:

| Case | Best center r [mm] | Next r [mm] | Margin | Best J | Source profile |
| --- | ---: | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 4.145e-04 | 0.000e+00 | fc=1.0, shift=0 ps, amp=1.000 |
| noise10_seed13 | 6.0 | 6.2 | 3.194e-04 | 8.040e-02 | fc=1.0, shift=0 ps, amp=0.998 |
| source_mismatch | 6.0 | 6.2 | 4.591e-04 | 4.490e-06 | fc=1.1, shift=-50 ps, amp=1.100 |
| source_mismatch_noise10_seed13 | 6.0 | 6.2 | 3.314e-04 | 8.947e-02 | fc=1.1, shift=-50 ps, amp=1.100 |

Plot validation:

```text
multi_rebar_common_radius_profiles.png: 1617x920 px, dynamic range 255, std 33.672
```

Interpretation:

```text
The center rebar radius is individually identifiable in this controlled
fixed-position test, but the margin is much smaller than the common-radius
margin. This is expected: changing one bar perturbs only part of the B-scan,
while the common-radius sweep changes all three bars at once.
```

Decision:

```text
Run the same one-at-a-time sweep for side rebars 0 and 2. If side-bar margins
are similarly positive, per-rebar radius profiling is viable with mandatory
confidence reporting. If one side is weak, the multi-rebar workflow needs
position/radius coupling diagnostics before full optimization.
```

### 065_multi_rebar_left_radius_profile

Output:

```text
outputs/experiments/065_multi_rebar_left_radius_profile
```

Runtime and count:

```text
13 swept-radius candidates
sweep_rebar_index = 0
193.34 s
```

Case summary:

| Case | Best left r [mm] | Next r [mm] | Margin | Best J | Source profile |
| --- | ---: | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 3.737e-04 | 0.000e+00 | fc=1.0, shift=0 ps |
| noise10_seed13 | 6.0 | 6.2 | 2.263e-04 | 8.040e-02 | fc=1.0, shift=0 ps |
| source_mismatch | 6.0 | 6.2 | 4.235e-04 | 4.490e-06 | fc=1.1, shift=-50 ps |
| source_mismatch_noise10_seed13 | 6.0 | 6.2 | 3.117e-04 | 8.947e-02 | fc=1.1, shift=-50 ps |

Plot validation:

```text
multi_rebar_common_radius_profiles.png: 1617x920 px, dynamic range 255, std 33.696
```

### 066_multi_rebar_right_radius_profile

Output:

```text
outputs/experiments/066_multi_rebar_right_radius_profile
```

Runtime and count:

```text
13 swept-radius candidates
sweep_rebar_index = 2
191.98 s
```

Case summary:

| Case | Best right r [mm] | Next r [mm] | Margin | Best J | Source profile |
| --- | ---: | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 3.658e-04 | 0.000e+00 | fc=1.0, shift=0 ps |
| noise10_seed13 | 6.0 | 6.2 | 4.766e-04 | 8.040e-02 | fc=1.0, shift=0 ps |
| source_mismatch | 6.0 | 6.2 | 4.013e-04 | 4.490e-06 | fc=1.1, shift=-50 ps |
| source_mismatch_noise10_seed13 | 6.0 | 6.2 | 5.033e-04 | 8.947e-02 | fc=1.1, shift=-50 ps |

Plot validation:

```text
multi_rebar_common_radius_profiles.png: 1617x920 px, dynamic range 255, std 33.636
```

## Stage 4B Decision

Stage 4B passes with a confidence caveat.

Combined per-rebar result:

| Swept rebar | Nominal margin | 10% noise margin | Mismatch margin | Mismatch 10% noise margin |
| --- | ---: | ---: | ---: | ---: |
| left index 0 | 3.737e-04 | 2.263e-04 | 4.235e-04 | 3.117e-04 |
| center index 1 | 4.145e-04 | 3.194e-04 | 4.591e-04 | 3.314e-04 |
| right index 2 | 3.658e-04 | 4.766e-04 | 4.013e-04 | 5.033e-04 |

Interpretation:

```text
Individual rebar radius is identifiable in the fixed-position 3-rebar scene,
but the per-rebar margins are much weaker than the common-radius margins. The
left rebar under nominal 10% noise is the weakest tested case, with margin
2.263e-04.
```

Next action:

```text
Do not jump straight to full unconstrained 9-parameter optimization. First run
a one-rebar-at-a-time local x/z/r geometry coupling diagnostic in the 3-rebar
scene, starting with the weakest left rebar case. This tests whether nearby
position changes can erase the already smaller per-rebar radius margins.
```
