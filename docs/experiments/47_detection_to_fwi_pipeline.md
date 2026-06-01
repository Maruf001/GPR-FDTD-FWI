# Detection-To-FWI Pipeline

## Goal

Build a 2D end-to-end pipeline for rebar location and size estimation:

```text
B-scan -> candidate detection windows -> source-profiled FWI refinement ->
confidence/ambiguity reporting
```

3D is deliberately out of scope for this stage. The current priority is a
research-grade 2D pipeline with enough scenario coverage to judge whether a
paper-quality contribution is plausible.

## Current Evidence Base

Single-rebar experiments:

```text
001-062
```

Multi-rebar experiments:

```text
063-106
```

Navigation view:

```text
outputs/experiments/_by_category_symlinks/
```

The symlink view is for browsing only. Canonical outputs remain
`outputs/experiments/NNN_run_name`.

## Stage 10 Plan

### 10A: Detection Seed Layer

Purpose:

```text
estimate likely rebar x/z windows from a B-scan before FWI refinement
```

Method:

```text
background-remove the B-scan,
compute an envelope/absolute-energy image,
score physically plausible two-way TX/RX hyperbolas over x/z candidates,
return top candidates with non-maximum suppression and confidence scores.
```

Important boundary:

```text
the detector estimates x/z seed windows, not radius. Radius is still resolved
by the source-profiled FWI/refinement and confidence machinery.
```

### 10B: Single-Rebar Detector Benchmark

Scenarios:

```text
depths: 60, 90, 120, 150 mm
radii: 4, 6, 8, 10 mm
noise: 0%, 5%, 10%
source: nominal first, then source mismatch
```

Metrics:

```text
top-1 x/z error,
top-3 hit rate,
candidate-window contains truth,
detector score margin,
runtime.
```

### 10C: Detection + Existing FWI Refinement

Use detector top-k candidates to choose local x/z windows, then run the
existing source-profiled geometry/radius refinement.

Metrics:

```text
final x error,
final z error,
final radius error,
confidence label,
ambiguity interval,
runtime.
```

### 10D: Multi-Rebar Same-Depth Benchmark

Start with current three-rebar same-depth setup, then expand:

```text
count: 2, 3
spacing: wide, medium, close
noise/source mismatch: same cases as single-rebar benchmark
```

The detector must avoid collapsing multiple rebars into one broad detection.

### 10E: Future Scenario Families

After same-depth 2D works:

```text
variable-depth multi-rebar,
mixed-radius multi-rebar,
material/shape variants,
lab or field data branch if available.
```

## Paper-Oriented Success Criteria

A publishable claim needs more than selected successful runs. Minimum evidence:

```text
fixed benchmark matrix,
baseline/ablation comparison,
generalization across noise/source mismatch/depth/radius/spacing,
uncertainty calibration,
runtime analysis,
negative/failure mode reporting.
```

Possible paper claim:

```text
a source-profiled, confidence-aware 2D GPR-FWI pipeline for rebar
location/radius estimation with explicit ambiguity reporting under source
mismatch, noise, and multi-rebar interference.
```

## Current Status

- [x] Created Stage 10 tracker.
- [x] Add tested hyperbola-energy detector.
- [x] Add detector CLI/runner.
- [x] Run first single-rebar detector smoke.
- [x] Run first multi-rebar same-depth detector smoke.
- [x] Run first detection-to-refinement smoke.
- [x] Interpret results and choose next benchmark expansion.

## Implementation

Files:

```text
inversion/rebar_detection.py
run_rebar_detection_pipeline.py
tests/test_rebar_detection.py
```

Detector behavior:

```text
median background removal,
Hilbert-envelope scoring when scipy is available,
TX/RX two-leg hyperbola model,
optional detector time-offset grid,
non-maximum suppression in x/z,
candidate windows for downstream FWI.
```

Validation:

```text
tests/test_rebar_detection.py: 5 passed
py_compile passed for detector and runner
git diff --check: passed before GPU smoke runs
```

## 107: Single-Rebar Detector Without Time Offset

Output:

```text
outputs/experiments/107_detection_single_rebar_default_smoke
```

Result:

| Rank | x [mm] | z [mm] | Normalized score |
| ---: | ---: | ---: | ---: |
| 1 | 250 | 125 | 1.898 |
| 2 | 222 | 110 | 1.307 |
| 3 | 278 | 110 | 1.299 |

Truth:

```text
x=250 mm, z=90 mm
```

Interpretation:

The detector found the correct lateral location but a depth that was too deep
by 35 mm. This was caused by the hyperbola model using zero source-time offset
while the Ricker source has a delayed peak. Keep this failed smoke as evidence
that time-offset calibration is mandatory.

## 108: Single-Rebar Detector With Source-Delay Offset

Output:

```text
outputs/experiments/108_detection_single_rebar_source_delay_smoke
```

Result:

| Rank | x [mm] | z [mm] | Normalized score |
| ---: | ---: | ---: | ---: |
| 1 | 250 | 80 | 2.124 |
| 2 | 250 | 65 | 1.713 |
| 3 | 250 | 95 | 1.501 |

Truth was inside tolerance:

```text
top truth match: rank 3, x error 0 mm, z error 5 mm
```

Interpretation:

Using the nominal Ricker source delay fixes the large depth bias, but the top
rank is still shallow. The detector should treat source-time offset as a small
nuisance grid, not as a fixed constant.

## 109: Single-Rebar Detector With Offset Grid

Output:

```text
outputs/experiments/109_detection_single_rebar_offset_grid_smoke
```

Detector time offsets:

```text
400, 500, 600, 667 ps
```

Result:

| Rank | x [mm] | z [mm] | Time offset [ps] | Normalized score |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 250 | 95 | 500 | 2.160 |
| 2 | 250 | 80 | 667 | 2.123 |
| 3 | 250 | 110 | 400 | 1.870 |

Truth match:

```text
rank 1, x error 0 mm, z error 5 mm, within tolerance
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.94
```

Interpretation:

The offset-grid detector gives a good seed window for the true single rebar.
It should be the default detection setting for synthetic Ricker-source
benchmarks until a data-driven direct-wave calibration is added.

## 110: Multi-Rebar Same-Depth Detector Smoke

Output:

```text
outputs/experiments/110_detection_multi_rebar_same_depth_smoke
```

Truth:

```text
x=[150,250,350] mm, z=[90,90,90] mm, r=[6,6,6] mm
```

Result:

| Rank | x [mm] | z [mm] | Time offset [ps] | Normalized score |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 248 | 90 | 500 | 0.954 |
| 2 | 352 | 90 | 500 | 0.870 |
| 3 | 148 | 90 | 500 | 0.831 |

Truth matches:

```text
left:   rank 3, x error 2 mm, z error 0 mm
center: rank 1, x error 2 mm, z error 0 mm
right:  rank 2, x error 2 mm, z error 0 mm
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.21
```

Interpretation:

This is the first end-to-end detection evidence that the hyperbola-energy
seed stage can find multiple same-depth rebars without being given target
locations. The next multi-rebar detector tests should vary spacing, depth, and
noise before promoting it to a general seed layer.

## 111: Detection-Seeded Source-Profiled Polish

Output:

```text
outputs/experiments/111_detection_seeded_source_profiled_polish_smoke
```

Detection seed used:

```text
x=250 mm, local z window 80-105 mm, radius window 5.4-7.4 mm
```

Source-profile grid:

```text
frequency scales: 0.9, 1.0, 1.1
time shifts: -50, 0, 50 ps
amplitude: fitted
```

Result:

```text
best: x=250 mm, z=90 mm, r=6.0 mm
radius margin: 9.814769770963429e-04
candidate count: 66
runtime: 1060.8 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.05
```

Interpretation:

The detection seed can drive the existing source-profiled radius polish and
recover the true radius. Runtime is too high for a large benchmark if every
detected seed gets a full 1 mm source-profiled grid. The next development step
should be a two-stage detector-to-FWI refinement:

```text
cheap 2 mm coarse source-profiled/nominal screen,
then narrow 1 mm source-profiled polish only for surviving seed windows.
```

## Next Decision

Proceed to Stage 10B with detector benchmarks, but keep the benchmark cheap:

```text
1. add a detector summary/aggregate helper for many synthetic scenarios;
2. run single-rebar depth/radius/noise detector-only matrix;
3. add two-stage refinement only after detector-only hit rates are known;
4. avoid full 1 mm source-profiled polish for every scenario until the coarse
   screen is implemented.
```

## Stage 10B Implementation

File:

```text
run_rebar_detection_benchmark.py
```

Purpose:

```text
run detector-only synthetic matrices before spending 1 mm FWI refinement
compute on every scenario.
```

Validation:

```text
tests/test_rebar_detection.py: 6 passed
py_compile passed for benchmark runner
full test suite: 133 passed in 23.65 s
git diff --check: passed
```

## 112: Single-Rebar Depth/Radius/Noise Detector Benchmark

Output:

```text
outputs/experiments/112_single_rebar_detection_depth_radius_noise_benchmark
```

Matrix:

```text
depths: 70, 90, 110, 130 mm
radii: 4, 6, 8, 10 mm
noise: 0%, 5%, 10%
source: nominal
scenarios: 48
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| detected count | 48 / 48 |
| hit count | 48 / 48 |
| hit rate | 1.000 |
| median x error | 0.0 mm |
| median z error | 5.0 mm |
| max x error | 4.0 mm |
| max z error | 10.0 mm |

Interpretation:

The offset-grid detector is robust across the first single-rebar depth/radius
matrix under up to 10% observed noise. This supports promoting it to the seed
stage for more scenario coverage.

## 113: Single-Rebar Source-Mismatch Detector Benchmark

Output:

```text
outputs/experiments/113_single_rebar_detection_source_mismatch_benchmark
```

Matrix:

```text
depths: 70, 90, 110, 130 mm
radii: 4, 6, 8, 10 mm
noise: 0%, 5%, 10%
source: frequency scale 1.1, time shift -50 ps, amplitude scale 1.1
scenarios: 48
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| detected count | 48 / 48 |
| hit count | 48 / 48 |
| hit rate | 1.000 |
| median x error | 0.0 mm |
| median z error | 2.5 mm |
| max x error | 0.0 mm |
| max z error | 10.0 mm |

Interpretation:

Source mismatch did not harm detector-only seeding in this matrix. This is
important because source mismatch has been a major radius-refinement failure
driver. It suggests the detector can provide stable x/z windows while source
profiling handles the refinement objective.

## 114: Close-Spacing Multi-Rebar Detector Smoke

Output:

```text
outputs/experiments/114_detection_multi_rebar_close_spacing_source_mismatch_noise10
```

Scenario:

```text
x=[190,250,310] mm, z=[90,90,90] mm, r=[6,6,6] mm
source mismatch: frequency scale 1.1, time shift -50 ps, amplitude 1.1
noise: 10%
```

Top true matches:

| Truth | Matched rank | x error | z error |
| --- | ---: | ---: | ---: |
| left | 3 | 2 mm | 0 mm |
| center | 1 | 2 mm | 0 mm |
| right | 2 | 2 mm | 0 mm |

Interpretation:

The detector separates three same-depth rebars at 60 mm spacing under source
mismatch and 10% noise. This is a stronger multi-target seed result than the
current same-depth 100 mm spacing case.

## 115: Variable-Depth Multi-Rebar Detector Smoke

Output:

```text
outputs/experiments/115_detection_multi_rebar_variable_depth_source_mismatch_noise10
```

Scenario:

```text
x=[150,250,350] mm, z=[80,100,120] mm, r=[6,6,6] mm
source mismatch: frequency scale 1.1, time shift -50 ps, amplitude 1.1
noise: 10%
```

Top true matches:

| Truth | Matched rank | x error | z error |
| --- | ---: | ---: | ---: |
| left shallow | 1 | 2 mm | 5 mm |
| center medium | 2 | 2 mm | 5 mm |
| right deep | 4 | 2 mm | 0 mm |

Interpretation:

The detector can find variable-depth multi-rebar seeds in this first smoke,
but it also returns false shallow/deep aliases in the top list. The refinement
stage must therefore consume top-k windows with confidence filtering rather
than trusting only rank 1 per target.

## Updated Stage 10 Decision

Evidence so far:

```text
detector x/z seeding is strong in controlled 2D synthetic cases,
source-time offset must be modelled as a nuisance parameter,
radius still belongs to FWI/source-profiled refinement,
full 1 mm source-profiled refinement is too expensive for every detector seed.
```

Next development step:

```text
build a two-stage detector-to-refinement runner:
  stage A: detector top-k windows
  stage B: cheap 2 mm coarse geometry/radius/source screen per window
  stage C: 1 mm source-profiled polish only for selected windows
```

This should become the first candidate for the full 2D rebar detection
pipeline.

## 116-117: Manual Two-Stage Refinement Smoke

Purpose:

```text
test whether a coarse screen plus narrow 1 mm polish can recover the same
radius result at lower runtime than experiment 111.
```

### 116: 2 mm Coarse Screen

Output:

```text
outputs/experiments/116_detection_seeded_coarse_2mm_screen_smoke
```

Configuration:

```text
x = 250 mm
z = 80:105:5 mm
radius = 5.4:7.4:0.2 mm
source frequency scales = 0.9, 1.0, 1.1
source time shifts = -50, 0, 50 ps
amplitude fitted
```

Result:

```text
best: x=250 mm, z=90 mm, r=6.0 mm
candidate count: 66
runtime: 238.5 s
radius margin: 0.0
```

Interpretation:

The 2 mm screen finds the true branch quickly enough, but radius margin is zero
because coarse-grid aliasing creates ties. Use this only as a screening stage,
not as the final estimator.

### 117: Narrow 1 mm Polish

Output:

```text
outputs/experiments/117_detection_seeded_narrow_1mm_polish_smoke
```

Configuration:

```text
x = 250 mm
z = 88:92:1 mm
radius = 5.8:6.2:0.2 mm
same source-profile grid as 116
```

Result:

```text
best: x=250 mm, z=90 mm, r=6.0 mm
candidate count: 15
runtime: 240.3 s
radius margin: 9.814769770963429e-04
```

Comparison:

| Path | Runtime | Final radius | Radius margin |
| --- | ---: | ---: | ---: |
| direct 1 mm grid, exp 111 | 1060.8 s | 6.0 mm | 9.8148e-04 |
| 2 mm screen + narrow 1 mm polish, exp 116-117 | 478.8 s | 6.0 mm | 9.8148e-04 |

Decision:

The two-stage idea works on the first smoke and cuts runtime by about 55% while
preserving the final radius result. The next code task should package this as
a repeatable runner so benchmark scenarios can call the same coarse-to-fine
logic without manual command chaining.

## 118: Packaged Two-Stage Refinement Smoke

Implementation:

```text
run_detection_seeded_two_stage_refinement.py
tests/test_detection_seeded_two_stage_refinement.py
```

Output:

```text
outputs/experiments/118_detection_seeded_two_stage_refinement_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_detection_seeded_two_stage_refinement.py \
  --backend gpu-cpml \
  --run-name detection_seeded_two_stage_refinement_smoke
```

Pipeline:

```text
stage A: detector offset-grid seed
stage B: 2 mm source-profiled coarse screen
stage C: narrow 1 mm source-profiled polish
```

Selected detector seed:

```text
rank 1: x=250 mm, z=95 mm, detector time offset=500 ps
truth: x=250 mm, z=90 mm, r=6 mm
```

Coarse screen:

```text
x values = [250]
z values = 80:110:5 mm
radius values = 5.4:7.4:0.2 mm
candidate count = 77
best = x=250 mm, z=90 mm, r=6.0 mm
radius margin = 0.0
reported runtime = 278.9 s
```

Fine polish:

```text
x values = [250]
z values = 88:92:1 mm
radius values = 5.8:6.2:0.2 mm
candidate count = 15
best = x=250 mm, z=90 mm, r=6.0 mm
truth errors = x 0 mm, z 0 mm, radius 0 mm
radius margin = 9.814769770963429e-04
reported runtime = 235.7 s
```

Overall runtime:

```text
545.6 s wall clock including detector and child-process overhead
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.94
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.22
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.98
```

Figure notes:

```text
stages/detection/figures/FIGURE_NOTES.md
stages/coarse_screen/figures/FIGURE_NOTES.md
stages/fine_polish/figures/FIGURE_NOTES.md
```

Interpretation:

The packaged runner reproduced the manual 116-117 conclusion in a single
numbered experiment. The coarse stage is good enough to find the true branch,
but it still has zero radius margin and must not be reported as the final
radius estimate. The fine 1 mm stage restores the same radius margin as the
direct 1 mm experiment while evaluating only 15 final candidates.

## Updated Decision After 118

Promote the packaged two-stage runner as the default single-rebar prototype,
with one required development step before broader benchmark use:

```text
refactor source-profiled polish to accept arbitrary single-rebar truth geometry,
then run a small 2-3 scenario replication matrix using the packaged runner
under source mismatch and 5-10% noise.
```

The detector is no longer the main blocker for single-rebar synthetic cases.
The next blocker is making refinement scenario-aware without copying or
duplicating FDTD/FWI logic.

## Scenario-Aware Refinement Refactor

Implementation:

```text
run_single_rebar_source_profiled_polish.py now accepts:
  --truth-x-mm
  --truth-z-mm
  --truth-radius-mm
  optional --initial-x-mm / --initial-z-mm / --initial-radius-mm

run_detection_seeded_two_stage_refinement.py passes the truth geometry into
both the coarse and fine source-profiled stages.
```

Validation:

```text
tests/test_source_profiled_polish_runner.py
tests/test_detection_seeded_two_stage_refinement.py
focused tests: 11 passed
py_compile passed for both runners
```

## 119: Non-Default Depth/Radius Two-Stage Smoke

Purpose:

```text
verify that the packaged two-stage runner is no longer hard-wired to the
default x=250 mm, z=90 mm, r=6 mm truth.
```

Output:

```text
outputs/experiments/119_detection_seeded_two_stage_refinement_depth110_r8_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_detection_seeded_two_stage_refinement.py \
  --backend gpu-cpml \
  --run-name detection_seeded_two_stage_refinement_depth110_r8_smoke \
  --truth-z-mm 110 \
  --truth-radius-mm 8 \
  --detector-z-values-mm 75:150:5 \
  --coarse-z-min-mm 70 \
  --coarse-z-max-mm 160 \
  --coarse-radius-min-mm 7.4 \
  --coarse-radius-max-mm 8.6 \
  --fine-radius-min-mm 6 \
  --fine-radius-max-mm 10
```

Truth:

```text
x=250 mm, z=110 mm, r=8 mm
```

Result:

```text
detector rank 1: x=250 mm, z=110 mm
coarse screen: 49 candidates, best x=250 mm, z=110 mm, r=8.0 mm,
  radius margin=0.0
fine polish: 15 candidates, best x=250 mm, z=110 mm, r=8.0 mm,
  radius margin=2.187052651811233e-03
truth errors: x 0 mm, z 0 mm, radius 0 mm
overall wall time: 449.4 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.85
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.32
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.75
```

Interpretation:

The scenario-aware refactor works on the first non-default case. The same
pattern repeats: the 2 mm stage selects the correct branch but has zero radius
margin, while the 1 mm stage provides the actual radius decision. The next
stress should add controlled source mismatch and 5-10% noise using the same
packaged runner.

## 120: Non-Default Depth/Radius With Source Mismatch And 10% Noise

Purpose:

```text
stress the packaged runner after the scenario-aware refactor with the same
non-default geometry as 119, but with source mismatch and noise.
```

Output:

```text
outputs/experiments/120_detection_seeded_two_stage_refinement_depth110_r8_mismatch_noise10
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_detection_seeded_two_stage_refinement.py \
  --backend gpu-cpml \
  --run-name detection_seeded_two_stage_refinement_depth110_r8_mismatch_noise10 \
  --truth-z-mm 110 \
  --truth-radius-mm 8 \
  --observed-frequency-scale 1.1 \
  --observed-time-shift-ps -50 \
  --observed-amplitude-scale 1.1 \
  --observed-noise-rms-fraction 0.10 \
  --noise-seed 13 \
  --detector-z-values-mm 75:150:5 \
  --coarse-z-min-mm 70 \
  --coarse-z-max-mm 160 \
  --coarse-radius-min-mm 7.4 \
  --coarse-radius-max-mm 8.6 \
  --fine-radius-min-mm 6 \
  --fine-radius-max-mm 10
```

Observed source:

```text
frequency scale = 1.1
time shift = -50 ps
amplitude scale = 1.1
noise = 10% of clean RMS
```

Result:

```text
detector rank 1: x=250 mm, z=110 mm
coarse screen: best x=250 mm, z=110 mm, r=8.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.08994,
  radius margin=0.0
fine polish: best x=250 mm, z=110 mm, r=8.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.09609,
  radius margin=2.430253492953227e-03 absolute, 1.288% relative
truth errors: x 0 mm, z 0 mm, radius 0 mm
overall wall time: 448.0 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.39
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.31
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.43
```

Interpretation:

This is the strongest single-rebar packaged-pipeline result so far: the
detector seed, source-profile recovery, final depth, and final radius all
remain correct under controlled source mismatch and 10% noise. The recovered
source profile is physically consistent with the imposed mismatch, so the
radius is not being used as a proxy for source error in this case.

Next decision:

```text
run one shallow/small-radius stress where detector aliases and radius
resolution should be harder, then decide whether to build a batch replication
runner for multiple packaged two-stage scenarios.
```

## 121: Shallow Small-Radius Source-Mismatch/Noise Stress

Purpose:

```text
test a harder radius-confidence case: a shallow 4 mm rebar with source
mismatch and 10% noise.
```

Output:

```text
outputs/experiments/121_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_detection_seeded_two_stage_refinement.py \
  --backend gpu-cpml \
  --run-name detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10 \
  --truth-z-mm 70 \
  --truth-radius-mm 4 \
  --observed-frequency-scale 1.1 \
  --observed-time-shift-ps -50 \
  --observed-amplitude-scale 1.1 \
  --observed-noise-rms-fraction 0.10 \
  --noise-seed 13 \
  --detector-z-values-mm 50:120:5 \
  --coarse-z-min-mm 45 \
  --coarse-z-max-mm 140 \
  --coarse-radius-min-mm 3.4 \
  --coarse-radius-max-mm 4.6 \
  --fine-radius-min-mm 2 \
  --fine-radius-max-mm 8
```

Result:

```text
detector rank 1: x=250 mm, z=75 mm
truth: x=250 mm, z=70 mm, r=4 mm
coarse screen: best x=250 mm, z=70 mm, r=4.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.10453,
  radius margin=0.0
fine polish: best x=250 mm, z=70 mm, r=4.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.09765,
  radius margin=5.999968000857114e-04 absolute, 0.203% relative
truth errors: x 0 mm, z 0 mm, radius 0 mm
overall wall time: 422.0 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.64
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.64
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.03
```

Interpretation:

This is a pass on the point estimate but not a high-confidence result. The
detector seed was 5 mm deep relative to truth, the coarse screen corrected it,
and the fine polish recovered the true radius. However, the final relative
margin is only about 0.2%, much weaker than the deeper 8 mm case. This is the
first clear evidence that shallow/small-radius single-rebar cases need
replication and confidence thresholds before being called robust.

Next decision:

```text
build a small batch/aggregate layer for packaged two-stage runs, then replicate
the shallow r=4 mm mismatch/noise case across noise seeds before expanding to
larger benchmark matrices.
```

## Aggregate Reporting Layer

Implementation:

```text
run_two_stage_refinement_aggregate.py
tests/test_two_stage_refinement_aggregate.py
```

Purpose:

```text
scan packaged two-stage summaries and produce a comparable table/plot of
point errors, radius margins, recovered source profile, runtime, and a simple
confidence label.
```

Validation:

```text
focused aggregate/two-stage/polish tests: 14 passed
py_compile passed
```

## 122: Aggregate Report For Packaged Runs 118-121

Output:

```text
outputs/experiments/122_two_stage_refinement_aggregate_118_121
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_two_stage_refinement_aggregate.py \
  --run-name two_stage_refinement_aggregate_118_121 \
  --run-dirs \
    outputs/experiments/118_detection_seeded_two_stage_refinement_smoke \
    outputs/experiments/119_detection_seeded_two_stage_refinement_depth110_r8_smoke \
    outputs/experiments/120_detection_seeded_two_stage_refinement_depth110_r8_mismatch_noise10 \
    outputs/experiments/121_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10
```

Aggregate result:

| Run | Truth z/r | Noise/source | Final error | Fine margin | Confidence |
| --- | --- | --- | --- | ---: | --- |
| 118 | 90 mm / 6 mm | nominal | x/z/r all 0 | 9.8148e-04 | strong |
| 119 | 110 mm / 8 mm | nominal | x/z/r all 0 | 2.1871e-03 | strong |
| 120 | 110 mm / 8 mm | source mismatch + 10% noise | x/z/r all 0 | 2.4303e-03 | strong |
| 121 | 70 mm / 4 mm | source mismatch + 10% noise | x/z/r all 0 | 5.99997e-04 | weak |

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 64.56
```

Figure notes:

```text
outputs/experiments/122_two_stage_refinement_aggregate_118_121/figures/FIGURE_NOTES.md
```

Interpretation:

The packaged runner has recovered all tested single-rebar point estimates so
far, including non-default depth/radius and source-mismatch/noise cases. The
aggregate view makes the important caveat visible: experiment 121 is correct
but weakly separated from the next radius. This is exactly the type of case
that should drive the next replication matrix.

## 123: Shallow Small-Radius Replication, Noise Seed 21

Purpose:

```text
repeat the weak-margin shallow r=4 mm mismatch/noise case with a new noise
seed to test whether the low confidence in 121 was a one-seed accident.
```

Output:

```text
outputs/experiments/123_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10_seed21
```

Result:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 21
detector rank 1: x=250 mm, z=75 mm
coarse screen: best x=250 mm, z=70 mm, r=4.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.10366,
  radius margin=0.0
fine polish: best x=250 mm, z=70 mm, r=4.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.08687,
  radius margin=6.620668456095435e-04 absolute, 0.225% relative
truth errors: x 0 mm, z 0 mm, radius 0 mm
overall wall time: 446.4 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.64
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.62
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.07
```

Interpretation:

Seed 21 repeats the seed 13 pattern. The final radius is correct, the source
profile is physically consistent, and the margin remains weak. That makes the
confidence warning more credible: shallow 4 mm rebars under source mismatch
and 10% noise should be reported with lower confidence unless more information
or a sharper objective is added.

Next decision:

```text
run at least one more shallow r=4 mm seed, then regenerate the aggregate
report. If the third seed also has weak-but-correct behavior, promote
"weak confidence but correct point estimate" as the current known failure mode
for the single-rebar packaged pipeline.
```

## 124: Shallow Small-Radius Replication, Noise Seed 34

Purpose:

```text
third seed for the shallow r=4 mm source-mismatch/noise case.
```

Output:

```text
outputs/experiments/124_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10_seed34
```

Result:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 34
detector rank 1: x=250 mm, z=75 mm
coarse screen: best x=250 mm, z=70 mm, r=4.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.10576,
  radius margin=0.0
fine polish: best x=250 mm, z=70 mm, r=4.0 mm,
  source profile frequency scale=1.1, time shift=-50 ps, amplitude=1.09842,
  radius margin=5.67544475815418e-04 absolute, 0.194% relative
truth errors: x 0 mm, z 0 mm, radius 0 mm
overall wall time: 445.6 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.68
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.71
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.74
```

Interpretation:

The third seed confirms the pattern from 121 and 123. The packaged pipeline
gets the right point estimate for shallow 4 mm rebars under source mismatch
and 10% noise, but the radius decision is consistently weak. This should be
treated as a confidence/reporting limitation until a sharper objective,
additional bandwidth, denser radius sampling, or stronger regularization is
tested.

## 125: Aggregate Report After Shallow r=4 mm Replication

Output:

```text
outputs/experiments/125_two_stage_refinement_aggregate_118_124
```

Aggregate result:

| Run | Case | Final error | Fine margin | Confidence |
| --- | --- | --- | ---: | --- |
| 118 | z=90, r=6, nominal | x/z/r all 0 | 9.8148e-04 | strong |
| 119 | z=110, r=8, nominal | x/z/r all 0 | 2.1871e-03 | strong |
| 120 | z=110, r=8, mismatch + 10% noise | x/z/r all 0 | 2.4303e-03 | strong |
| 121 | z=70, r=4, mismatch + 10% noise, seed 13 | x/z/r all 0 | 5.99997e-04 | weak |
| 123 | z=70, r=4, mismatch + 10% noise, seed 21 | x/z/r all 0 | 6.62067e-04 | weak |
| 124 | z=70, r=4, mismatch + 10% noise, seed 34 | x/z/r all 0 | 5.67544e-04 | weak |

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 60.16
```

Interpretation:

The point estimator is strong across this small package of scenarios: every
run recovered x, z, and radius exactly. Confidence is not uniform. The three
shallow 4 mm noisy/source-mismatched replications are all weak by the current
margin label. This is not a failure of point estimation, but it is a failure
of high-confidence size reporting for that scenario family.

Next decision:

```text
test whether denser radius sampling around 4 mm reveals a stable minimum
around 4.0 mm or a genuinely flat radius objective. If the objective is flat,
the pipeline should report a radius interval rather than a single confident
size for shallow/small bars.
```

## 126: Dense Radius Diagnostic For Shallow r=4 mm Case

Purpose:

```text
rerun the shallow r=4 mm mismatch/noise seed-13 case with 0.1 mm fine-radius
spacing to see whether the weak margin is a sampling artifact or a flat
objective.
```

Output:

```text
outputs/experiments/126_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10_fine01
```

Fine grid:

```text
x = 250 mm
z = 68:72:1 mm
radius = 3.7:4.3:0.1 mm
candidate count = 35
```

Result:

```text
best: x=250 mm, z=70 mm, r=4.0 mm
next radius: r=4.1 mm
fine radius margin: 0.0
truth errors: x 0 mm, z 0 mm, radius 0 mm
fine reported runtime: 557.4 s
```

Important local objective values:

```text
z=70 mm, r=3.7/3.8/3.9 mm: objective 0.2960123712
z=70 mm, r=4.0/4.1 mm: objective 0.2952422893
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.64
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.64
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.78
```

Interpretation:

The denser radius grid proves the weak-margin issue is not just because the
previous grid skipped intermediate radii. The objective is flat enough that
`4.0 mm` and `4.1 mm` tie exactly under the current 1 mm hard-grid geometry and
source-profiled least-squares objective. The correct report for this branch is
therefore an ambiguity interval, not a confident single radius.

Next decision:

```text
add an ambiguity-interval calculation to the packaged runner/aggregate report.
Then test whether subcell geometry on the 1 mm fine stage can reduce the
4.0-4.1 mm tie without introducing the earlier radius artifacts.
```

## Radius Ambiguity Interval Implementation

Implementation:

```text
inversion/radius_confidence.py
run_single_rebar_source_profiled_polish.py
run_detection_seeded_two_stage_refinement.py
run_two_stage_refinement_aggregate.py
tests/test_radius_confidence.py
```

Behavior:

```text
exact_tie interval: radii with objective equal to the best objective within
  1e-12 absolute tolerance
weak_interval: radii within max(1e-3 absolute, 0.5% relative) of the best
  objective
```

Validation:

```text
focused radius/two-stage/aggregate/polish tests: 17 passed
py_compile passed
```

## 127: Aggregate Report With Radius Intervals

Output:

```text
outputs/experiments/127_two_stage_refinement_aggregate_118_126_intervals
```

Key interval results:

| Run | Case | Exact interval | Weak interval | Confidence |
| --- | --- | --- | --- | --- |
| 118 | z=90, r=6, nominal | 6.0-6.0 mm | 6.0-6.2 mm | strong |
| 119 | z=110, r=8, nominal | 8.0-8.0 mm | 8.0-8.0 mm | strong |
| 120 | z=110, r=8, mismatch + noise | 8.0-8.0 mm | 8.0-8.0 mm | strong |
| 121 | z=70, r=4, mismatch + noise | 4.0-4.0 mm | 3.8-4.2 mm | weak |
| 123 | z=70, r=4, mismatch + noise seed 21 | 4.0-4.0 mm | 3.8-4.2 mm | weak |
| 124 | z=70, r=4, mismatch + noise seed 34 | 4.0-4.0 mm | 3.8-4.2 mm | weak |
| 126 | z=70, r=4, dense 0.1 mm radius | 4.0-4.1 mm | 3.7-4.2 mm | weak |

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 57.25
```

Interpretation:

The interval report makes the radius ambiguity explicit. The three standard
0.2 mm-grid shallow runs look like exact `4.0 mm` point estimates, but their
weak intervals span `3.8-4.2 mm`. The denser 0.1 mm run is more revealing:
`4.0` and `4.1 mm` are an exact tie, and the weak interval spans `3.7-4.2 mm`.

Decision:

```text
for shallow/small-radius source-mismatched noisy data, report a radius interval
instead of a confident scalar size unless a later objective variant separates
the interval.
```

## Geometry Mode Refactor

Implementation:

```text
run_single_rebar_source_profiled_polish.py:
  --geometry-mode hard|subcell
  --subcell-samples

run_detection_seeded_two_stage_refinement.py:
  --detection-geometry-mode hard|subcell
  --detection-subcell-samples
  --refinement-geometry-mode hard|subcell
  --refinement-subcell-samples
```

Validation:

```text
focused tests: 17 passed
py_compile passed
```

## 128: Dense Radius Subcell Geometry Diagnostic

Purpose:

```text
repeat experiment 126 with subcell geometry in detection and refinement to
test whether the hard-grid 4.0-4.1 mm tie is a geometry quantization artifact.
```

Output:

```text
outputs/experiments/128_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10_fine01_subcell
```

Result:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 13
geometry: subcell, 5 samples
detector rank 1: x=250 mm, z=75 mm
coarse screen: best x=250 mm, z=70 mm, r=4.0 mm,
  radius margin=1.2718045926601862e-04
fine polish: best x=250 mm, z=70 mm, r=4.0 mm,
  next r=3.9 mm,
  radius margin=8.619911281693149e-05 absolute, 0.0285% relative
exact interval: 4.0-4.0 mm
weak interval: 3.7-4.3 mm
truth errors: x 0 mm, z 0 mm, radius 0 mm
overall wall time: 763.6 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.62
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.18
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.65
```

Interpretation:

Subcell geometry removes the exact hard-grid tie between 4.0 and 4.1 mm, so
part of experiment 126 was geometry quantization. It does not solve radius
confidence. The fine margin remains extremely small, and the weak interval
still spans most of the tested 3.7-4.3 mm range. The conservative conclusion is
that subcell geometry helps smooth the radius objective but does not provide a
confident scalar size for shallow 4 mm bars under this noise/source condition.

Next decision:

```text
keep interval reporting as the default for this branch. The next possible
physics test is whether a broader/multifrequency fine objective sharpens the
radius interval more than geometry smoothing alone.
```

## 129: Aggregate Report With Hard/Subcell Geometry Comparison

Output:

```text
outputs/experiments/129_two_stage_refinement_aggregate_118_128_geometry
```

Key comparison:

| Run | Geometry/fine grid | Exact interval | Weak interval | Fine margin | Confidence |
| --- | --- | --- | --- | ---: | --- |
| 126 | hard, 0.1 mm radius | 4.0-4.1 mm | 3.7-4.2 mm | 0.0 | weak |
| 128 | subcell, 0.1 mm radius | 4.0-4.0 mm | 3.7-4.3 mm | 8.6199e-05 | weak |

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 55.14
```

Interpretation:

Subcell geometry fixed the exact tie but not the practical ambiguity. The weak
interval remains broad. The current best scientific description is:

```text
for shallow 4 mm rebar under this source/noise condition, the pipeline finds
the correct location and includes the true radius, but the supported radius
range is broad enough that a single high-confidence size estimate would be
misleading.
```

## Aggregate Plot Repair

Problem found from user review:

```text
the top panel in the aggregate plot showed final radius error, but every run
had exactly 0 mm error. The old bar-only plot therefore looked blank even
though the data were valid.
```

Implementation:

```text
run_two_stage_refinement_aggregate.py now draws explicit point markers on the
zero-error line and adds a short note when all runs have 0.000 mm final radius
error.
```

Validation:

```text
tests/test_two_stage_refinement_aggregate.py includes all-zero axis coverage
focused aggregate tests passed
```

## 130: Repaired Aggregate Figure

Output:

```text
outputs/experiments/130_two_stage_refinement_aggregate_118_128_geometry_plotfix
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 56.34
```

Figure notes:

```text
outputs/experiments/130_two_stage_refinement_aggregate_118_128_geometry_plotfix/figures/FIGURE_NOTES.md
```

Interpretation:

This replaces the visually misleading aggregate plot. The top panel now shows
markers on the zero line for the zero-error radius estimates, so an exact
point estimate is visible rather than appearing as a missing plot.

## Multifrequency Source-Profiled Refinement Implementation

Implementation:

```text
run_single_rebar_source_profiled_polish.py:
  --frequencies-ghz
  --frequency-weights
  shared source frequency-scale/time-shift across all base frequencies
  per-frequency amplitude fit and per-frequency misfit reporting

run_detection_seeded_two_stage_refinement.py:
  --refinement-frequencies-ghz
  --refinement-frequency-weights
```

Validation:

```text
focused source-profiled/two-stage tests: 13 passed
py_compile passed
```

## 131: Two-Frequency Dense Radius Diagnostic

Purpose:

```text
test whether adding a lower base frequency to the source-profiled fine
objective sharpens the shallow r=4 mm radius interval.
```

Output:

```text
outputs/experiments/131_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10_fine01_multifreq
```

Configuration:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 13
refinement base frequencies: 1.0 and 1.5 GHz
geometry: hard
fine grid: x=250 mm, z=68:72:1 mm, radius=3.7:4.3:0.1 mm
```

Result:

```text
best: x=250 mm, z=70 mm, r=4.0 mm
next radius: r=4.1 mm
fine radius margin: 0.0
exact interval: 4.0-4.1 mm
weak interval: 3.7-4.3 mm
source profile: frequency scale=1.1, time shift=-50 ps
per-frequency misfit at best: 1.0 GHz = 0.02213, 1.5 GHz = 0.28732
overall wall time: 1514.5 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.64
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.86
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.25
```

Interpretation:

The 1.0+1.5 GHz objective did not improve the shallow-radius ambiguity. It
kept the correct point estimate and recovered the source profile, but the
fine-radius exact tie between `4.0` and `4.1 mm` remained. The weak interval
expanded to the full tested radius range, `3.7-4.3 mm`. Runtime also doubled
relative to the single-frequency dense run.

Decision:

```text
do not promote equal-weight 1.0+1.5 GHz refinement. The lower frequency has a
small misfit and appears to dilute rather than sharpen the radius decision.
The next bandwidth test should favor higher frequencies, such as 1.5+2.0 GHz
or high-frequency-weighted 1.0+1.5 GHz.
```

## 132: High-Frequency Dense Radius Diagnostic

Purpose:

```text
test whether a higher-frequency pair, 1.5+2.0 GHz, sharpens the shallow r=4 mm
radius interval better than equal-weight 1.0+1.5 GHz.
```

Output:

```text
outputs/experiments/132_detection_seeded_two_stage_refinement_depth70_r4_mismatch_noise10_fine01_highfreq
```

Configuration:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 13
refinement base frequencies: 1.5 and 2.0 GHz
geometry: hard
fine grid: x=250 mm, z=68:72:1 mm, radius=3.7:4.3:0.1 mm
```

Result:

```text
best: x=250 mm, z=70 mm, r=4.0 mm
next radius: r=4.1 mm
fine radius margin: 0.0
exact interval: 4.0-4.1 mm
weak interval: 3.7-4.3 mm
source profile: frequency scale=1.1, time shift=-50 ps
per-frequency misfit at best: 1.5 GHz = 0.29524, 2.0 GHz = 0.70423
overall wall time: 1514.7 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.64
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.49
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.44
```

Interpretation:

The high-frequency pair also failed to sharpen the radius interval. The point
estimate and source profile remain correct, but `4.0` and `4.1 mm` are still
an exact tie and the weak interval spans the whole tested range. The 2.0 GHz
component has much larger normalized misfit than 1.5 GHz, so simply adding it
with equal weight raises the objective value without improving radius
separation.

Decision:

```text
do not keep brute-force equal-weight multifrequency LS as the next main branch.
The next useful step is reporting/diagnostics around interval behavior or a
more selective objective, not another full two-frequency grid without a better
weighting principle.
```

## 133: Multifrequency Aggregate Report

Purpose:

```text
combine the baseline, shallow noisy/source-mismatched, dense-radius, subcell,
and equal-weight multifrequency two-stage runs into one comparison table and
margin plot.
```

Output:

```text
outputs/experiments/133_two_stage_refinement_aggregate_118_132_multifreq
```

Rows:

```text
118, 119, 120, 121, 123, 124, 126, 128, 131, 132
```

Weak-confidence rows:

```text
121, 123, 124, 126, 128, 131, 132
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 52.91
```

Interpretation:

Every included run has zero final radius error, so the point estimate alone
looks successful. The confidence margins tell the more important story:
the shallow `z=70 mm`, `r=4 mm` noisy/source-mismatched cases remain weak.
The equal-weight multifrequency runs do not improve that conclusion.

## 134: Interval And Runtime Aggregate Report

Purpose:

```text
make radius ambiguity and runtime visible in the aggregate report instead of
leaving them only in the CSV columns.
```

Output:

```text
outputs/experiments/134_two_stage_refinement_aggregate_118_132_interval_runtime
```

Implementation:

```text
run_two_stage_refinement_aggregate.py now writes:
  two_stage_margin_summary.png
  two_stage_interval_runtime_summary.png
  FIGURE_NOTES.md explaining both figures in plain language
```

Result:

```text
weak-margin runs: 121, 123, 124, 126, 128, 131, 132
widest weak interval width: 0.600 mm
widest weak interval runs: 128, 131, 132
131 runtime: 1514.5 s
132 runtime: 1514.7 s
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 52.91
two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 60.34
```

Interpretation:

The new interval/runtime plot confirms the current verdict. Equal-weight
multifrequency preserves the correct point radius but gives no practical
radius-confidence gain. It keeps the widest weak interval at `0.600 mm` and
roughly doubles runtime. The next development step should improve diagnostic
information per candidate, especially per-frequency misfit curves, before
spending more GPU time on full multifrequency grids.

## 135: Per-Frequency Candidate Diagnostics Smoke

Purpose:

```text
verify that multifrequency source-profiled polish now records per-candidate
per-frequency misfit and amplitude fields, and writes a frequency-term
decomposition plot.
```

Output:

```text
outputs/experiments/135_single_rebar_source_profiled_multifreq_csv_plot_smoke
```

Configuration:

```text
backend: gpu-cpml
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 13
candidate grid: x=250 mm, z=70 mm, r=3.9,4.0,4.1 mm
refinement frequencies: 1.0 and 1.5 GHz
source profile grid: frequency scale=1.0,1.1 and time shift=-50,0 ps
```

Implementation:

```text
source_profiled_polish_candidates.csv now includes:
  frequency_misfit_1GHz
  frequency_misfit_1.5GHz
  frequency_amplitude_scale_1GHz
  frequency_amplitude_scale_1.5GHz

source_profiled_frequency_radius_profile.png decomposes the combined-best
radius curve into per-frequency objective terms.
```

Result:

```text
best radius: 4.0 mm
next radius: 4.1 mm
radius margin: 0.0
exact interval: 4.0-4.1 mm
weak interval: 3.9-4.1 mm
best source profile: frequency scale=1.1, time shift=-50 ps
best per-frequency misfit: 1.0 GHz=0.02031, 1.5 GHz=0.26119
runtime: 41.4 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.59
source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 36.25
```

Interpretation:

The diagnostic instrumentation works. Scientifically, this small grid shows
that the 4.0 mm and 4.1 mm candidates are identical in both the combined
objective and the stored per-frequency terms. That means the shallow-radius
ambiguity is not just an artifact of averaging the two frequencies in this
case. The next stage should inspect whether the duplicate behavior is caused
by grid rasterization of the small hard-geometry circle before launching a
larger weighted-frequency sweep.

## 136: Geometry Quantization Diagnostic

Purpose:

```text
test whether the hard-grid material representation actually changes between
nearby shallow-radius candidates.
```

Output:

```text
outputs/experiments/136_single_rebar_geometry_quantization_radius37_43
```

Configuration:

```text
grid step: 1 mm
center: x=250 mm, z=70 mm
radii: 3.7:4.3:0.1 mm
geometries: hard and subcell
subcell samples: 5x5
```

Result:

```text
hard zero adjacent log-conductivity deltas at radii: 3.8, 3.9, 4.1 mm
hard 4.0 -> 4.1 mm adjacent log-conductivity delta: 0.000
subcell 4.0 -> 4.1 mm adjacent log-conductivity delta: 23.400
```

Plot validation:

```text
geometry_quantization_metrics.png: 1583x1379 px, dynamic range 255, std 35.97
```

Interpretation:

The hard-grid exact tie between `4.0` and `4.1 mm` is not an optimizer failure
and not a frequency-weighting failure. At 1 mm spacing, those two radii produce
identical hard-grid conductivity geometry, so FDTD sees the same model. Subcell
geometry does change continuously enough to break this exact tie, which
explains why experiment 128 removed the exact 4.0-4.1 hard-grid tie. The weak
interval remains broad, so the next productive branch is a subcell-centered
fine diagnostic or a finer forward grid, not more hard-grid objective tuning.

## 137: Subcell Multifrequency Tie Diagnostic

Purpose:

```text
repeat the small multifrequency diagnostic from 135 with subcell geometry to
test whether the 4.0/4.1 mm tie disappears when the material model changes
smoothly with radius.
```

Output:

```text
outputs/experiments/137_single_rebar_source_profiled_multifreq_subcell_tie_smoke
```

Configuration:

```text
backend: gpu-cpml
geometry: subcell, 5x5 samples
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 13
candidate grid: x=250 mm, z=70 mm, r=3.9,4.0,4.1 mm
refinement frequencies: 1.0 and 1.5 GHz
```

Result:

```text
best radius: 3.9 mm
next radius: 4.0 mm
radius margin: 3.2492e-05
exact interval: 3.9-3.9 mm
weak interval: 3.9-4.0 mm
best per-frequency misfit:
  1.0 GHz=0.02044
  1.5 GHz=0.26718
runtime: 40.6 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.93
source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 36.17
```

Interpretation:

Subcell geometry removes the exact 4.0/4.1 hard-grid tie, but it does not
create a high-confidence radius. The best radius shifts slightly low to
`3.9 mm`, and the margin against the true `4.0 mm` radius is only
`3.2492e-05`. The practical conclusion remains an interval: the shallow
4 mm case is localizable in x/z, but radius needs subcell/finer-grid modeling
plus uncertainty reporting. The next test should separate two possibilities:
whether more subcell samples stabilize the low bias, or whether a finer
forward grid is needed.

## 138: Subcell-Sample Convergence Diagnostic

Purpose:

```text
repeat the subcell tie diagnostic with 9x9 subcell samples to check whether
the 5x5 low-radius preference is stable.
```

Output:

```text
outputs/experiments/138_single_rebar_source_profiled_multifreq_subcell9_tie_smoke
```

Configuration:

```text
same as experiment 137 except subcell samples: 9x9
```

Result:

```text
best radius: 4.0 mm
next radius: 3.9 mm
radius margin: 1.13348e-05
exact interval: 4.0-4.0 mm
weak interval: 3.9-4.1 mm
best per-frequency misfit:
  1.0 GHz=0.02047
  1.5 GHz=0.27011
runtime: 40.9 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.91
source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 36.15
```

Interpretation:

Increasing subcell samples from 5x5 to 9x9 moves the best point estimate back
to the true `4.0 mm` radius. That is encouraging, but the margin is extremely
small and the weak interval spans every tested radius, `3.9-4.1 mm`. The
sample convergence result supports using higher subcell sampling for radius
diagnostics, but it still does not justify a high-confidence point-size
claim for this shallow noisy/source-mismatched case.

## 139: Wider 9x9 Subcell Radius Profile

Purpose:

```text
extend the 9x9 subcell diagnostic to the full recent dense-radius range,
3.7-4.3 mm, while keeping x/z fixed at the true location.
```

Output:

```text
outputs/experiments/139_single_rebar_source_profiled_multifreq_subcell9_radius37_43
```

Configuration:

```text
backend: gpu-cpml
geometry: subcell, 9x9 samples
truth and candidate x/z: x=250 mm, z=70 mm
radii: 3.7:4.3:0.1 mm
refinement frequencies: 1.0 and 1.5 GHz
source/noise: same as 137-138
```

Result:

```text
best radius: 4.0 mm
next radius: 3.9 mm
radius margin: 1.13348e-05
exact interval: 4.0-4.0 mm
weak interval: 3.7-4.1 mm
best per-frequency misfit:
  1.0 GHz=0.02047
  1.5 GHz=0.27011
runtime: 94.7 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.07
source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 35.24
```

Interpretation:

The wider profile confirms the current best state for this branch: 9x9 subcell
geometry gives the correct point radius at the true x/z location, but the
objective landscape is still flat enough that `3.7-4.1 mm` must be treated as
a weak-supported interval. The per-frequency terms do not reveal a frequency
that sharply separates the true radius. More frequency weighting is therefore
not the next best lever; the next useful escalation is either more acquisition
information, a calibrated noise/uncertainty threshold, or a finer forward grid
smoke to see whether physical resolution improves.

## 140: Wider 9x9 Subcell Profile With 9 Sources

Purpose:

```text
test whether denser acquisition, represented by 9 source/receiver positions
instead of 3, sharpens the shallow-radius profile.
```

Output:

```text
outputs/experiments/140_single_rebar_source_profiled_multifreq_subcell9_radius37_43_src9
```

Configuration:

```text
same as experiment 139 except sources: 9
```

Result:

```text
best radius: 4.0 mm
next radius: 3.9 mm
radius margin: 8.08056e-05
exact interval: 4.0-4.0 mm
weak interval: 3.7-4.0 mm
best per-frequency misfit:
  1.0 GHz=0.02338
  1.5 GHz=0.25533
runtime: 267.2 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.28
source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 35.25
```

Interpretation:

More acquisition positions help. The radius margin increases from
`1.13348e-05` in the 3-source run to `8.08056e-05`, and the weak interval
shrinks from `3.7-4.1 mm` to `3.7-4.0 mm`. This is still weak by the current
confidence rule, but it is the first branch in this series that clearly
improves the interval without changing the true point estimate.

## 141: Post-Hoc Frequency Reweighting Diagnostic

Purpose:

```text
reuse experiment 140 per-frequency candidate terms to test whether heavier
1.5 GHz weighting would shrink the radius interval before paying for another
GPU run.
```

Output:

```text
outputs/experiments/141_frequency_reweight_diagnostic_exp140_subcell9_src9
```

Weight cases:

```text
equal: 1GHz=1, 1.5GHz=1
hi2:   1GHz=1, 1.5GHz=2
hi4:   1GHz=1, 1.5GHz=4
hi8:   1GHz=1, 1.5GHz=8
hi16:  1GHz=1, 1.5GHz=16
```

Result:

```text
equal margin: 8.08056e-05, weak interval 3.7-4.0 mm
hi16 margin: 1.31868e-04, weak interval 3.7-4.0 mm
best radius for all cases: 4.0 mm
```

Plot validation:

```text
frequency_reweight_radius_profiles.png: 1617x937 px, dynamic range 255, std 32.70
```

Interpretation:

The 1.5 GHz term carries more radius separation than the 1 GHz term, so
post-hoc high-frequency weighting increases the numeric margin. It does not
shrink the weak interval, even with a 16x 1.5 GHz weight. Because this is a
cheap diagnostic and still negative on the interval metric, a full weighted
GPU rerun is not the next best use of time. Acquisition density or calibrated
uncertainty reporting is the stronger branch.

## 142-143: Noise-Seed Robustness For Current Best Fixed-Location Setup

Purpose:

```text
repeat the best current fixed-location profile from 140 with two additional
noise seeds to test whether the 4.0 mm best radius is stable.
```

Outputs:

```text
outputs/experiments/142_single_rebar_source_profiled_multifreq_subcell9_radius37_43_src9_seed21
outputs/experiments/143_single_rebar_source_profiled_multifreq_subcell9_radius37_43_src9_seed34
```

Configuration:

```text
same as experiment 140 except noise_seed=21 and noise_seed=34
```

Results:

```text
experiment 142:
  best radius: 4.0 mm
  next radius: 3.9 mm
  margin: 1.68790e-04
  exact interval: 4.0-4.0 mm
  weak interval: 3.7-4.0 mm
  runtime: 273.1 s

experiment 143:
  best radius: 4.0 mm
  next radius: 3.9 mm
  margin: 8.52847e-05
  exact interval: 4.0-4.0 mm
  weak interval: 3.7-4.0 mm
  runtime: 270.9 s
```

Plot validation:

```text
142 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.98
142 source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 35.23
143 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 28.85
143 source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 35.24
```

Interpretation:

The best radius is stable across three noise seeds: 13, 21, and 34 all choose
`4.0 mm`. The weak interval is also stable: `3.7-4.0 mm`. That means the
current best fixed-location setup has good point-estimate robustness but still
needs interval reporting on the lower-radius side.

## 144: Source-Profiled Polish Robustness Aggregate

Purpose:

```text
aggregate experiments 140, 142, and 143 into one CSV and one plot so the
noise-seed robustness result is easy to read.
```

Output:

```text
outputs/experiments/144_source_profiled_polish_aggregate_subcell9_src9_noise_seeds
```

Rows:

```text
140, 142, 143
```

Result:

```text
best radii: 4.0, 4.0, 4.0 mm
radius errors: 0.0, 0.0, 0.0 mm
weak intervals: 3.7-4.0 mm for all three seeds
margin range: 8.08056e-05 to 1.68790e-04
```

Plot validation:

```text
source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 71.01
```

Interpretation:

This is the current best state of the shallow `z=70 mm`, `r=4 mm` fixed-x/z
radius branch: with 1 mm grid, 9x9 subcell geometry, 9 source positions, and
1.0+1.5 GHz source-profiled objective, the point radius is robustly correct
across three noise seeds. The supported radius interval remains `3.7-4.0 mm`,
so the result should be reported as a correct point estimate with lower-side
uncertainty, not as a high-confidence exact diameter measurement.

## 145: 0.5 mm Geometry Quantization Diagnostic

Purpose:

```text
check whether a 0.5 mm forward grid makes nearby small-radius candidates more
distinct before running expensive 0.5 mm FDTD simulations.
```

Output:

```text
outputs/experiments/145_single_rebar_geometry_quantization_radius37_43_grid05
```

Configuration:

```text
grid step: 0.5 mm
center: x=250 mm, z=70 mm
radii: 3.7:4.3:0.1 mm
geometries: hard and subcell
subcell samples: 5x5
```

Result:

```text
hard zero adjacent log-conductivity deltas at radii: 3.8 mm only
hard 4.0 -> 4.1 mm adjacent log-conductivity delta: 144.000
subcell 4.0 -> 4.1 mm adjacent log-conductivity delta: 85.320
```

Plot validation:

```text
geometry_quantization_metrics.png: 1583x1379 px, dynamic range 255, std 35.88
```

Interpretation:

At 0.5 mm spacing, the hard-grid model distinguishes `4.0` and `4.1 mm`
clearly. This removes the material-array identity problem that caused the 1 mm
hard-grid exact tie. A small 0.5 mm FDTD smoke is therefore justified, but it
should be tightly scoped because the grid roughly doubles each spatial axis and
doubles the time samples.

## 146: 0.5 mm FDTD Radius Smoke

Purpose:

```text
run the smallest practical 0.5 mm wave simulation to test whether finer
forward-grid geometry improves the 3.9/4.0/4.1 mm radius decision.
```

Output:

```text
outputs/experiments/146_single_rebar_source_profiled_multifreq_grid05_hard_tie_smoke
```

Configuration:

```text
backend: gpu-cpml
grid step: 0.5 mm
geometry: hard
sources: 3
truth and candidate x/z: x=250 mm, z=70 mm
radii: 3.9,4.0,4.1 mm
frequencies: 1.0 and 1.5 GHz
source/noise: frequency scale=1.1, time shift=-50 ps, amplitude=1.1, noise=10%, seed=13
```

Result:

```text
best radius: 4.0 mm
next radius: 3.9 mm
margin: 9.47026e-05
exact interval: 4.0-4.0 mm
weak interval: 3.9-4.1 mm
runtime: 372.9 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.62
source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 36.30
```

Interpretation:

The 0.5 mm forward grid fixes the exact hard-grid identity problem and picks
the true `4.0 mm` radius, but it does not create strong radius confidence. The
weak interval remains `3.9-4.1 mm`, and the run costs about 373 seconds for
only three radii and three source positions. The current verdict is: 0.5 mm is
useful as a verification tool, but too expensive to make the default pipeline
unless a later study shows it shrinks intervals substantially more than 1 mm
9x9 subcell geometry with denser acquisition.

## 147: Local Depth-Radius Coupling Diagnostic

Purpose:

```text
test whether the current best 1 mm setup keeps the true radius when local
depth is allowed to move by +/-1 mm.
```

Output:

```text
outputs/experiments/147_single_rebar_source_profiled_multifreq_subcell9_src9_z69_71_r39_41
```

Configuration:

```text
backend: gpu-cpml
grid step: 1 mm
geometry: subcell, 9x9 samples
sources: 9
x: 250 mm
z values: 69,70,71 mm
radii: 3.9,4.0,4.1 mm
frequencies: 1.0 and 1.5 GHz
source/noise: same as experiment 140
```

Result:

```text
best: x=250 mm, z=70 mm, r=4.0 mm
next radius: r=3.9 mm at z=70 mm
radius margin: 8.08056e-05
exact interval: 4.0-4.0 mm
weak interval across tested radii: 3.9-4.0 mm
runtime: 345.3 s
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.95
source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 36.15
```

Interpretation:

Local depth-radius coupling is not the main remaining problem. The true depth
`z=70 mm` remains best, and the closest competitor is still the lower radius
`3.9 mm` at the same depth. This supports the current pipeline direction:
location/depth can be accurate, while size should be reported with a lower-side
interval unless more acquisition information or a better uncertainty model
shrinks it.

## Guarded Polish Packaging

Implementation:

```text
run_detection_seeded_two_stage_refinement.py now supports an optional guarded
polish stage after the existing detection, coarse screen, and fine polish.
```

New guarded-stage controls:

```text
--enable-guarded-polish
--guarded-sources
--guarded-grid-step-mm
--guarded-x-half-window-mm
--guarded-z-half-window-mm
--guarded-radius-half-window-mm
--guarded-geometry-mode
--guarded-subcell-samples
--guarded-frequencies-ghz
--guarded-frequency-weights
```

The root summary now records:

```text
guarded_grid
guarded_best
guarded_margin
guarded_radius_ambiguity
final_stage
final_best
final_margin
final_radius_ambiguity
```

Validation:

```text
focused guarded-stage tests passed
py_compile passed
```

## 148: Detector-Seeded Guarded Polish Smoke

Purpose:

```text
package the best current shallow-radius strategy as a real detector-seeded
pipeline: cheap detection/coarse/fine stages followed by guarded high-quality
local polish.
```

Output:

```text
outputs/experiments/148_detection_seeded_guarded_polish_depth70_r4_noise10_seed13
```

Configuration:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 13
detection: 2 mm grid, hard geometry
coarse/fine: cheap 1.5 GHz source-profiled stages, 3 sources
guarded polish: 1 mm grid, subcell 9x9, 9 sources, 1.0+1.5 GHz
guarded grid: x=250 mm; z=69,70,71 mm; r=3.9,4.0,4.1 mm
```

Result:

```text
detection rank 1: x=250 mm, z=75 mm
coarse best: x=250 mm, z=70 mm, r=4.0 mm
fine best: x=250 mm, z=70 mm, r=4.0 mm
guarded final best: x=250 mm, z=70 mm, r=4.0 mm
truth errors: x=0.0 mm, z=0.0 mm, r=0.0 mm
guarded margin: 8.08056e-05
guarded exact interval: 4.0-4.0 mm
guarded weak interval: 3.9-4.0 mm
overall runtime: 620.7 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 42.64
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.49
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.96
guarded source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.95
guarded source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 36.15
```

Interpretation:

The guarded stage successfully connects the fixed-location research branch
back into the detector-seeded pipeline. It keeps the correct location and
radius, and it improves the shallow-case weak interval from earlier broad
pipeline intervals to `3.9-4.0 mm`. The final confidence label is still weak,
so the result should be reported as a correct point estimate with a lower-side
interval, not an exact high-confidence size.

## 149: Guarded Pipeline Aggregate

Purpose:

```text
regenerate the two-stage aggregate with experiment 148 and final-stage-aware
reporting so guarded polish is not ignored.
```

Output:

```text
outputs/experiments/149_two_stage_refinement_aggregate_118_148_guarded
```

Rows:

```text
118, 119, 120, 121, 123, 124, 126, 128, 131, 132, 148
```

Result:

```text
all final point radius errors: 0.0 mm
weak confidence rows: 121, 123, 124, 126, 128, 131, 132, 148
guarded run 148 weak interval: 3.9-4.0 mm
widest weak intervals remain runs 128, 131, 132 at 0.600 mm
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 51.78
two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 60.01
```

Interpretation:

The guarded pipeline is now the best detector-seeded form for the shallow
`r=4 mm` case: it preserves zero point error and narrows the practical weak
interval compared with prior dense hard/subcell/multifrequency full-pipeline
runs. The next useful step is robustness: repeat the guarded package on the
same shallow case for additional noise seeds, then decide whether the guarded
stage should become the default final stage.

## 150: Detector-Seeded Guarded Polish, Seed 21

Purpose:

```text
repeat the packaged guarded pipeline on the shallow r=4 mm case with a second
noise seed, to test whether experiment 148 was seed-specific.
```

Output:

```text
outputs/experiments/150_detection_seeded_guarded_polish_depth70_r4_noise10_seed21
```

Configuration:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 21
detection: 2 mm grid, hard geometry
coarse/fine: 1.5 GHz source-profiled stages, 3 sources
guarded polish: 1 mm grid, subcell 9x9, 9 sources, 1.0+1.5 GHz
guarded grid: x=250 mm; z=69,70,71 mm; r=3.9,4.0,4.1 mm
```

Result:

```text
detection rank 1: x=250 mm, z=75 mm
coarse best: x=250 mm, z=70 mm, r=4.0 mm
fine best: x=250 mm, z=70 mm, r=4.0 mm
guarded final best: x=250 mm, z=70 mm, r=4.0 mm
truth errors: x=0.0 mm, z=0.0 mm, r=0.0 mm
fine margin: 5.19916e-04
guarded margin: 1.68790e-04
guarded exact interval: 4.0-4.0 mm
guarded weak interval: 3.9-4.0 mm
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.19
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.47
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.05
guarded source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.84
guarded source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 37.07
```

Interpretation:

Seed 21 matches seed 13 on the final estimate and the practical confidence
interval. The guarded stage again turns the detector-seeded result into a
correct point estimate with a one-sided weak interval, not yet a strong
radius claim. The next decision is to finish the same run for seed 34 and then
aggregate the three guarded package runs.

## 151: Detector-Seeded Guarded Polish, Seed 34

Purpose:

```text
complete the three-seed guarded-package replication for the shallow r=4 mm
case under source mismatch and 10% noise.
```

Output:

```text
outputs/experiments/151_detection_seeded_guarded_polish_depth70_r4_noise10_seed34
```

Configuration:

```text
truth: x=250 mm, z=70 mm, r=4 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 34
detection: 2 mm grid, hard geometry
coarse/fine: 1.5 GHz source-profiled stages, 3 sources
guarded polish: 1 mm grid, subcell 9x9, 9 sources, 1.0+1.5 GHz
guarded grid: x=250 mm; z=69,70,71 mm; r=3.9,4.0,4.1 mm
```

Result:

```text
detection rank 1: x=250 mm, z=75 mm
coarse best: x=250 mm, z=70 mm, r=4.0 mm
fine best: x=250 mm, z=70 mm, r=4.0 mm
guarded final best: x=250 mm, z=70 mm, r=4.0 mm
truth errors: x=0.0 mm, z=0.0 mm, r=0.0 mm
fine margin: 6.73085e-04
guarded margin: 8.52847e-05
guarded exact interval: 4.0-4.0 mm
guarded weak interval: 3.9-4.0 mm
overall runtime: 624.3 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.22
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.42
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.25
guarded source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.36
guarded source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 37.04
```

Interpretation:

Seed 34 matches seeds 13 and 21. The detector still places the first depth
peak slightly too deep (`75 mm`), but the FWI stages consistently recover the
true `70 mm` depth and `4.0 mm` radius. The repeated weak interval
`3.9-4.0 mm` is now a reproducible confidence statement rather than a
single-seed accident.

## 152: Guarded Pipeline Seed Aggregate

Purpose:

```text
aggregate the three packaged guarded-polish runs so the robustness verdict is
visible in one CSV and two checked summary figures.
```

Output:

```text
outputs/experiments/152_guarded_pipeline_seed_aggregate_148_151
```

Rows:

```text
148, 150, 151
```

Result:

```text
all final stages: guarded_polish
all final point estimates: x=250 mm, z=70 mm, r=4.0 mm
all truth errors: x=0.0 mm, z=0.0 mm, r=0.0 mm
guarded margins: 8.08056e-05, 1.68790e-04, 8.52847e-05
all exact intervals: 4.0-4.0 mm
all weak intervals: 3.9-4.0 mm
wall runtimes: 620.7 s, 629.2 s, 624.3 s
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 46.58
two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 91.90
```

Interpretation:

The guarded polish package should now be treated as the recommended
detector-seeded final confidence stage for this shallow single-rebar branch.
It gives exact point estimates across three noise seeds, and its uncertainty
report is stable: the data support `r=4.0 mm` as best, while `3.9 mm` remains
close enough that we should report the practical radius interval as
`3.9-4.0 mm`. The next research step should test whether the same guarded
package generalizes to a larger/deeper rebar before expanding optimizer
complexity.

## 153: Detector-Seeded Guarded Polish, Deep r=8 mm

Purpose:

```text
test whether the guarded final stage generalizes from the shallow r=4 mm
branch to the earlier deeper/larger r=8 mm source-mismatch case.
```

Output:

```text
outputs/experiments/153_detection_seeded_guarded_polish_depth110_r8_noise10_seed13
```

Configuration:

```text
truth: x=250 mm, z=110 mm, r=8 mm
observed source: frequency scale=1.1, time shift=-50 ps, amplitude=1.1
noise: 10%, seed 13
detection: 2 mm grid, hard geometry, detector z=75:150:5 mm
coarse/fine: 1.5 GHz source-profiled stages, 3 sources
guarded polish: 1 mm grid, subcell 9x9, 9 sources, 1.0+1.5 GHz
guarded grid: x=250 mm; z=109,110,111 mm; r=7.9,8.0,8.1 mm
```

Result:

```text
detection rank 1: x=250 mm, z=110 mm
coarse best: x=250 mm, z=110 mm, r=8.0 mm
fine best: x=250 mm, z=110 mm, r=8.0 mm
guarded final best: x=250 mm, z=110 mm, r=8.0 mm
truth errors: x=0.0 mm, z=0.0 mm, r=0.0 mm
fine margin: 2.36584e-03
fine weak interval: 8.0-8.0 mm
guarded margin: 1.14084e-04
guarded weak interval: 7.9-8.0 mm
overall runtime: 628.2 s
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 44.97
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.49
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.83
guarded source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.11
guarded source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 37.54
```

Interpretation:

The guarded stage generalizes in point accuracy: it preserves the exact
location and radius for the deeper/larger target. It does not preserve the
strong fine-stage confidence label, because the 9-source subcell
multifrequency comparison brings `7.9 mm` close to the `8.0 mm` best radius.
The practical conclusion is to keep both confidence views: fine hard-grid
polish says the `8.0 mm` radius is strongly separated at 0.2 mm spacing, while
guarded subcell polish says the final high-quality report should still include
the lower-side `7.9-8.0 mm` interval at 0.1 mm spacing.

## 154: Fine-Versus-Final Stage Confidence Aggregate

Purpose:

```text
make the confidence-stage distinction visible after experiment 153 showed that
guarded polish can preserve point accuracy while lowering the final margin.
```

Output:

```text
outputs/experiments/154_guarded_stage_confidence_120_153
```

Rows:

```text
120, 148, 150, 151, 153
```

New reporting fields:

```text
fine_stage_radius_mm
fine_stage_margin_abs
fine_stage_margin_rel
fine_stage_confidence
final_radius_mm
final_margin_abs
final_margin_rel
final_confidence
```

Result:

```text
120: fine=strong, final=strong, weak interval=8.0-8.0 mm
148: fine=weak, final=weak, weak interval=3.9-4.0 mm
150: fine=weak, final=weak, weak interval=3.9-4.0 mm
151: fine=weak, final=weak, weak interval=3.9-4.0 mm
153: fine=strong, final=weak, weak interval=7.9-8.0 mm
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 56.65
two_stage_stage_confidence_summary.png: 1889x835 px, dynamic range 255, std 53.34
two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 88.93
```

Interpretation:

This aggregate resolves the reporting issue. The final-stage plot remains the
conservative report, but the new stage-confidence figure prevents the earlier
fine-stage evidence from being hidden. Experiment 153 is the key case: the
hard-grid fine stage strongly separates `8.0 mm`, while the guarded subcell
stage says `7.9 mm` is still close enough that the final size should be
reported as `7.9-8.0 mm`. The next development should investigate why the
guarded subcell/multifrequency objective lowers the margin: frequency
contributions, subcell-radius sensitivity, or source-amplitude fitting.

## 155-158: r=8 mm Guarded Margin Diagnostics

Purpose:

```text
explain why experiment 153 preserved the exact r=8 mm point estimate but
downgraded radius confidence from strong at the fine stage to weak at the
guarded stage.
```

Outputs:

```text
155: outputs/experiments/155_single_rebar_r8_guarded_hard_local_multifreq
156: outputs/experiments/156_single_rebar_r8_guarded_subcell9_src9_15ghz_only
157: outputs/experiments/157_single_rebar_r8_guarded_subcell9_src9_10ghz_only
158: outputs/experiments/158_r8_guarded_frequency_geometry_diagnostic_153_157
```

Shared local grid:

```text
truth: x=250 mm, z=110 mm, r=8 mm
x grid: 250 mm
z grid: 109,110,111 mm
radius grid: 7.9,8.0,8.1 mm
sources: 9
source profile: frequency scale=1.0,1.1; time shift=-50,0 ps; fit amplitude
observed source mismatch/noise: scale=1.1, shift=-50 ps, amplitude=1.1, 10% noise, seed 13
```

Results:

```text
153 guarded subcell 1.0+1.5 GHz: best r=8.0 mm, margin=1.14084e-04,
  weak interval=7.9-8.0 mm
155 hard 1.0+1.5 GHz: best r=8.0 mm, margin=2.42030e-04,
  weak interval=7.9-8.0 mm
156 subcell 1.5 GHz only: best r=8.0 mm, margin=5.09885e-04,
  weak interval=7.9-8.0 mm
157 subcell 1.0 GHz only: best r=8.0 mm, margin=1.70963e-05,
  weak interval=7.9-8.1 mm
```

Plot validation:

```text
155 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.06
155 source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 37.66
156 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.36
157 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.50
158 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 77.60
```

Interpretation:

The weak guarded interval is not a failure to find the correct radius: every
diagnostic still chooses `8.0 mm`. The weak confidence is caused by the
objective landscape being shallow at 0.1 mm radius spacing. The 1.0 GHz band
is almost insensitive to the `7.9` versus `8.0 mm` size change, the 1.5 GHz
band is more sensitive but still below the strong-margin threshold, and hard
geometry improves the margin only modestly. The next useful step is not a
broader search; it is a targeted objective-design check: compare frequency
weights or source-amplitude fitting choices on this same small grid.

## 159-161: r=8 mm Amplitude-Fit Diagnostic

Purpose:

```text
test whether source-amplitude fitting is merely reducing the radius margin, or
whether it is required for accurate radius selection under the known 1.1
observed amplitude mismatch.
```

Outputs:

```text
159: outputs/experiments/159_single_rebar_r8_guarded_subcell9_src9_multifreq_no_amp_fit
160: outputs/experiments/160_r8_guarded_objective_design_diagnostic_153_159
161: outputs/experiments/161_r8_guarded_objective_design_diagnostic_153_159_with_amp_mode
```

Experiment 159 configuration:

```text
same local grid as 153, 156, and 157
frequencies: 1.0+1.5 GHz
geometry: subcell 9x9
sources: 9
source profile: frequency scale=1.0,1.1; time shift=-50,0 ps
amplitude fitting: disabled
```

Result:

```text
159 no amplitude fit:
  best r=7.9 mm
  truth radius error=0.1 mm
  next r=8.1 mm
  margin=7.09571e-04
  weak interval=7.9-8.1 mm

161 aggregate:
  amplitude-fit variants keep best r=8.0 mm
  no-amplitude-fit variant shifts best radius to 7.9 mm
```

Plot validation:

```text
159 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.93
159 source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 37.69
161 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 79.07
```

Interpretation:

Amplitude fitting should stay in the objective for source-mismatch cases. It
does reduce apparent radius separation, but disabling it produces a biased
best radius because the objective tries to explain the 1.1 amplitude mismatch
with geometry. The correct scientific report is therefore: amplitude-profiled
guarded polish gives the right radius point estimate, and the remaining
`7.9-8.0 mm` or `7.9-8.1 mm` interval is a real confidence limit rather than
something to remove by freezing amplitude.

## 162-163: Gentle High-Frequency Weighting Diagnostic

Purpose:

```text
test whether downweighting the weakly size-sensitive 1.0 GHz band improves
r=8 mm radius confidence while keeping amplitude fitting enabled.
```

Outputs:

```text
162: outputs/experiments/162_single_rebar_r8_guarded_subcell9_src9_weighted025_1
163: outputs/experiments/163_r8_guarded_objective_design_diagnostic_153_162_with_weights
```

Experiment 162 configuration:

```text
same local grid as 153 and 159
frequencies: 1.0+1.5 GHz
frequency weights: 1.0 GHz = 0.25, 1.5 GHz = 1.0
geometry: subcell 9x9
sources: 9
amplitude fitting: enabled
```

Result:

```text
162 weighted objective:
  best r=8.0 mm
  truth radius error=0.0 mm
  next r=7.9 mm
  margin=1.72277e-04
  weak interval=7.9-8.0 mm

comparison:
  equal 1.0+1.5 GHz weights, fitted amplitude: margin=1.14084e-04
  0.25/1.0 weights, fitted amplitude: margin=1.72277e-04
  1.5 GHz only, fitted amplitude: margin=5.09885e-04
```

Plot validation:

```text
162 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.50
162 source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 38.02
163 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 79.25
```

Interpretation:

Gentle high-frequency weighting is directionally helpful and does not bias the
best radius, but it does not remove the weak interval. The strongest accurate
diagnostic remains 1.5 GHz only, but that changes the acquisition objective
more aggressively. For the current two-frequency guarded stage, the correct
default is still equal or mildly high-frequency-weighted amplitude-profiled
misfit with explicit interval reporting, not a forced single-radius decision.

## 164-165: Shallow r=4 mm Weighting Cross-Check

Purpose:

```text
check whether the same gentle high-frequency weighting that helped r=8 mm
also improves the shallow r=4 mm guarded stage enough to change the final
confidence interval.
```

Outputs:

```text
164: outputs/experiments/164_single_rebar_r4_guarded_subcell9_src9_weighted025_1_seed13
165: outputs/experiments/165_r4_guarded_weighting_diagnostic_148_164
```

Experiment 164 configuration:

```text
truth: x=250 mm, z=70 mm, r=4 mm
local grid: x=250 mm; z=69,70,71 mm; r=3.9,4.0,4.1 mm
frequencies: 1.0+1.5 GHz
frequency weights: 1.0 GHz = 0.25, 1.5 GHz = 1.0
geometry: subcell 9x9
sources: 9
amplitude fitting: enabled
noise/source mismatch: same as guarded experiment 148, seed 13
```

Result:

```text
164 weighted objective:
  best r=4.0 mm
  truth radius error=0.0 mm
  next r=3.9 mm
  margin=1.15528e-04
  weak interval=3.9-4.0 mm

comparison to 148 equal weights:
  equal weights margin=8.08056e-05
  weighted margin=1.15528e-04
  both weak intervals=3.9-4.0 mm
```

Plot validation:

```text
164 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.74
164 source_profiled_frequency_radius_profile.png: 1515x886 px, dynamic range 255, std 37.60
165 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 86.68
```

Interpretation:

The weighting behavior is consistent across shallow and deep cases: it
improves the objective margin slightly while preserving the correct point
estimate, but it does not remove the weak interval. This is not enough to make
frequency weighting a default final-stage change. Keep it as a diagnostic and
continue reporting uncertainty intervals.

## 166-168: Shallow r=4 mm High-Band Acquisition Diagnostic

Purpose:

```text
test the paper-backed idea that progressively higher bandwidth can improve
small-radius discrimination, using controlled synthetic acquisitions at
2.0 GHz and 2.5 GHz on the same shallow r=4 mm local grid.
```

Outputs:

```text
166: outputs/experiments/166_single_rebar_r4_highband2ghz_subcell9_src9_seed13
167: outputs/experiments/167_single_rebar_r4_highband25ghz_subcell9_src9_seed13
168: outputs/experiments/168_r4_highband_acquisition_diagnostic_148_167
```

Shared configuration:

```text
truth: x=250 mm, z=70 mm, r=4 mm
local grid: x=250 mm; z=69,70,71 mm; r=3.9,4.0,4.1 mm
geometry: subcell 9x9
sources: 9
amplitude fitting: enabled
source mismatch/noise: frequency scale=1.1, time shift=-50 ps,
  amplitude=1.1, 10% noise, seed 13
```

Result:

```text
baseline guarded 1.0+1.5 GHz: best r=4.0 mm, margin=8.08056e-05
weighted 1.0+1.5 GHz: best r=4.0 mm, margin=1.15528e-04
2.0 GHz only: best r=4.0 mm, margin=7.41854e-04
2.5 GHz only: best r=4.0 mm, margin=1.85997e-03
all weak intervals: 3.9-4.0 mm
```

Plot validation:

```text
166 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.45
167 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.95
168 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 81.33
```

Interpretation:

Higher-band acquisition is the first knob that gives a large margin gain
without moving the best radius. The 2.5 GHz synthetic acquisition clears the
absolute strong-margin threshold, but the conservative weak-interval rule
still includes `3.9 mm` because the relative tolerance is larger at that
objective scale. This supports a future bandwidth ladder, but it should be
reported as an acquisition-design result, not as something recoverable from
the existing 1.0+1.5 GHz guarded data.

## 169-171: r=8 mm 2.5 GHz High-Band Cross-Check

Purpose:

```text
check whether the 2.5 GHz acquisition-design result generalizes from shallow
r=4 mm to the deeper/larger r=8 mm case.
```

Outputs:

```text
169: outputs/experiments/169_single_rebar_r8_highband25ghz_subcell9_src9_seed13
170: outputs/experiments/170_highband25_acquisition_diagnostic_r4_r8
171: outputs/experiments/171_highband25_acquisition_diagnostic_r4_r8_labeled
```

Experiment 169 configuration:

```text
truth: x=250 mm, z=110 mm, r=8 mm
local grid: x=250 mm; z=109,110,111 mm; r=7.9,8.0,8.1 mm
frequency: 2.5 GHz
geometry: subcell 9x9
sources: 9
amplitude fitting: enabled
source mismatch/noise: frequency scale=1.1, time shift=-50 ps,
  amplitude=1.1, 10% noise, seed 13
```

Result:

```text
169 2.5 GHz:
  best r=8.0 mm
  truth radius error=0.0 mm
  next r=7.9 mm
  margin=3.05578e-03
  exact interval=8.0-8.0 mm
  weak interval=8.0-8.0 mm

171 aggregate:
  1.0+1.5 GHz r=4 baseline margin=8.08056e-05, weak interval=3.9-4.0 mm
  2.5 GHz r=4 margin=1.85997e-03, weak interval=3.9-4.0 mm
  1.0+1.5 GHz r=8 baseline margin=1.14084e-04, weak interval=7.9-8.0 mm
  2.5 GHz r=8 margin=3.05578e-03, weak interval=8.0-8.0 mm
```

Plot validation:

```text
169 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.78
171 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 80.12
```

Interpretation:

The 2.5 GHz high-band acquisition diagnostic is now the clearest evidence for
improving radius confidence. It strongly resolves the r=8 mm case and greatly
improves the r=4 mm margin, although the r=4 mm weak interval still includes
`3.9 mm` under the current relative-tolerance rule. This supports developing
a progressive-bandwidth experiment branch, with careful labeling that these
are higher-band synthetic acquisitions rather than post-processing of the
existing lower-band data.

## 172-174: Shallow r=4 mm 2.5 GHz Seed Replication

Purpose:

```text
replicate the promising 2.5 GHz shallow r=4 mm acquisition diagnostic across
noise seeds 13, 21, and 34.
```

Outputs:

```text
172: outputs/experiments/172_single_rebar_r4_highband25ghz_subcell9_src9_seed21
173: outputs/experiments/173_single_rebar_r4_highband25ghz_subcell9_src9_seed34
174: outputs/experiments/174_r4_highband25_seed_aggregate_148_173
```

Result:

```text
seed 13: best r=4.0 mm, margin=1.85997e-03, weak interval=3.9-4.0 mm
seed 21: best r=4.0 mm, margin=1.17733e-03, weak interval=3.9-4.0 mm
seed 34: best r=4.0 mm, margin=1.38477e-03, weak interval=3.9-4.0 mm
all point radius errors: 0.0 mm
all exact intervals: 4.0-4.0 mm
```

Plot validation:

```text
172 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.53
173 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.13
174 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 80.36
```

Interpretation:

The 2.5 GHz shallow result is reproducible across the same three noise seeds
used for the guarded low-band package. It consistently gives the correct
`4.0 mm` point estimate and clears the absolute strong-margin threshold. The
weak interval remains `3.9-4.0 mm`, so the scientific statement is improved
confidence, not complete elimination of radius uncertainty.

## 175-177: r=8 mm 2.5 GHz Seed Replication

Purpose:

```text
replicate the r=8 mm 2.5 GHz acquisition diagnostic across noise seeds 13,
21, and 34.
```

Outputs:

```text
175: outputs/experiments/175_single_rebar_r8_highband25ghz_subcell9_src9_seed21
176: outputs/experiments/176_single_rebar_r8_highband25ghz_subcell9_src9_seed34
177: outputs/experiments/177_r8_highband25_seed_aggregate_153_176
```

Result:

```text
seed 13: best r=8.0 mm, margin=3.05578e-03, weak interval=8.0-8.0 mm
seed 21: best r=8.0 mm, margin=3.25265e-03, weak interval=8.0-8.0 mm
seed 34: best r=8.0 mm, margin=3.14797e-03, weak interval=8.0-8.0 mm
all point radius errors: 0.0 mm
```

Plot validation:

```text
175 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.82
176 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.84
177 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 79.88
```

Interpretation:

The 2.5 GHz r=8 mm result is stronger than the shallow r=4 mm result: across
all three seeds, the high-band local objective gives the correct point
estimate and collapses the weak radius interval to exactly `8.0-8.0 mm`. This
is the best evidence so far that high-band final-size data can resolve the
radius ambiguity that remains in the lower-band guarded pipeline.

## 178-180: Packaged High-Band Pipeline Smoke

Purpose:

```text
turn the high-band acquisition diagnostics into an optional detector-seeded
pipeline stage: lower-band detection/coarse/fine for location, then a separate
2.5 GHz local polish for final radius confidence.
```

Code change:

```text
run_detection_seeded_two_stage_refinement.py now supports
--enable-highband-polish and highband_* local-grid/source/geometry options.
run_two_stage_refinement_aggregate.py recognizes highband_polish as a final
stage and writes high-band-aware figure notes.
```

Outputs:

```text
178: outputs/experiments/178_detection_seeded_highband_polish_depth70_r4_noise10_seed13
179: outputs/experiments/179_packaged_highband_comparison_148_178
180: outputs/experiments/180_packaged_highband_comparison_148_178_notes_v2
```

Experiment 178 result:

```text
detection rank 1: x=250 mm, z=75 mm
coarse best: x=250 mm, z=70 mm, r=4.0 mm
fine best: x=250 mm, z=70 mm, r=4.0 mm
highband final best: x=250 mm, z=70 mm, r=4.0 mm
truth errors: x=0.0 mm, z=0.0 mm, r=0.0 mm
fine margin: 3.96915e-04
highband/final margin: 1.85997e-03
final exact interval: 4.0-4.0 mm
final weak interval: 3.9-4.0 mm
overall runtime: 435.0 s
```

Plot validation:

```text
178 detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.20
178 coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.15
178 fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.96
178 highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.95
180 two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 74.87
180 two_stage_stage_confidence_summary.png: 1889x835 px, dynamic range 255, std 51.99
180 two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 87.64
```

Interpretation:

The packaged high-band stage reproduces the standalone high-band diagnostic
inside the detector-seeded pipeline. It upgrades the final confidence label
from weak to strong while preserving exact point location and radius. The
final weak interval still includes `3.9 mm`, so the high-band stage improves
confidence but does not justify dropping interval reporting.

## 181-183: Packaged High-Band Shallow Seed Replication

Purpose:

```text
replicate the packaged high-band detector-to-radius pipeline on shallow
r=4 mm noise seeds 13, 21, and 34.
```

Outputs:

```text
181: outputs/experiments/181_detection_seeded_highband_polish_depth70_r4_noise10_seed21
182: outputs/experiments/182_detection_seeded_highband_polish_depth70_r4_noise10_seed34
183: outputs/experiments/183_packaged_highband_seed_aggregate_148_182
```

Result:

```text
seed 13 packaged highband: final r=4.0 mm, margin=1.85997e-03,
  weak interval=3.9-4.0 mm, point errors all 0.0 mm
seed 21 packaged highband: final r=4.0 mm, margin=1.17733e-03,
  weak interval=3.9-4.0 mm, point errors all 0.0 mm
seed 34 packaged highband: final r=4.0 mm, margin=1.38477e-03,
  weak interval=3.9-4.0 mm, point errors all 0.0 mm
```

Plot validation:

```text
181 detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.19
181 highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.53
182 detection_overlay.png: 1885x1209 px, dynamic range 255, std 45.22
182 highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 32.13
183 two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 78.51
183 two_stage_stage_confidence_summary.png: 1889x835 px, dynamic range 255, std 53.35
183 two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 83.12
```

Interpretation:

The packaged high-band shallow branch is now replicated across the same three
noise seeds used for earlier guarded runs. It keeps exact point estimates and
upgrades final radius confidence from weak to strong on all three seeds. The
weak interval remains `3.9-4.0 mm`, so final reporting must still include the
interval, but the packaged high-band stage is clearly better than the
low-band guarded final stage for this shallow radius case.

## 184-188: Packaged High-Band r=8 mm Seed Replication

Purpose:

```text
verify that the optional high-band polish stage also works in the full
detector-seeded pipeline for the deeper/larger r=8 mm case, then replicate it
on three noise seeds and compare against the older low-band and guarded runs.
```

Outputs:

```text
184: outputs/experiments/184_detection_seeded_highband_polish_depth110_r8_noise10_seed13
185: outputs/experiments/185_packaged_highband_r8_comparison_120_184
186: outputs/experiments/186_detection_seeded_highband_polish_depth110_r8_noise10_seed21
187: outputs/experiments/187_detection_seeded_highband_polish_depth110_r8_noise10_seed34
188: outputs/experiments/188_packaged_highband_r8_seed_aggregate_120_187
```

Experiment 184 result:

```text
detection rank 1: x=250 mm, z=110 mm
coarse best: x=250 mm, z=110 mm, r=8.0 mm
fine best: x=250 mm, z=110 mm, r=8.0 mm
highband final best: x=250 mm, z=110 mm, r=8.0 mm
truth errors: x=0.0 mm, z=0.0 mm, r=0.0 mm
fine margin: 2.36584e-03
highband/final margin: 3.05578e-03
final exact interval: 8.0-8.0 mm
final weak interval: 8.0-8.0 mm
overall runtime: 441.2 s
```

Seed replication result:

```text
seed 13 packaged highband: final r=8.0 mm, margin=3.05578e-03,
  weak interval=8.0-8.0 mm, point errors all 0.0 mm
seed 21 packaged highband: final r=8.0 mm, margin=3.25265e-03,
  weak interval=8.0-8.0 mm, point errors all 0.0 mm
seed 34 packaged highband: final r=8.0 mm, margin=3.14797e-03,
  weak interval=8.0-8.0 mm, point errors all 0.0 mm
```

Plot validation:

```text
184 detection_overlay.png: 1885x1209 px, dynamic range 255, std 44.97
184 highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 33.78
186 detection_overlay.png: 1885x1209 px, dynamic range 255, std 43.36
186 highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.84
187 detection_overlay.png: 1885x1209 px, dynamic range 255, std 43.42
187 highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.87
185 two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 78.89
185 two_stage_stage_confidence_summary.png: 1889x835 px, dynamic range 255, std 62.55
185 two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 83.06
188 two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 76.04
188 two_stage_stage_confidence_summary.png: 1889x835 px, dynamic range 255, std 60.33
188 two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 72.23
```

Interpretation:

The packaged high-band r=8 mm branch is now replicated on seeds 13, 21, and
34. All three runs have exact detector seed, exact FWI location, exact radius,
strong final margin, and collapsed weak interval. Compared with guarded run
153, the high-band stage removes the `7.9-8.0 mm` final ambiguity while
keeping the same point estimate. In aggregate 188, the only weak-confidence
row is guarded run 153; the older low-band fine run 120 and all high-band
replicates are strong under the current margin rule.

Pause-and-ponder decision:

```text
the high-band final polish is now the best supported single-rebar radius
confidence stage for the r=8 mm case. It also improves shallow r=4 mm margins,
but shallow r=4 mm still keeps a 3.9-4.0 mm weak interval. The next research
branch should therefore focus on why the shallow small-radius case keeps a
lower-side weak interval: subcell convergence, radius sampling below 0.1 mm,
or source/material coupling near the high-band candidate.
```

## 189-193: Shallow r=4 High-Band Subcell and Source-Coupling Diagnostics

Purpose:

```text
explain why the shallow r=4 mm high-band branch keeps a weak radius interval
even after the point estimate is exact and the final margin improves.
```

Outputs:

```text
189: outputs/experiments/189_single_rebar_r4_subcell13_geometry_quantization_005mm
190: outputs/experiments/190_single_rebar_r4_highband25ghz_subcell13_src9_seed13
191: outputs/experiments/191_single_rebar_r4_highband25ghz_subcell13_fine_radius0025_seed13
192: outputs/experiments/192_single_rebar_r4_highband25ghz_subcell13_fine_radius0025_seed13_noamp
193: outputs/experiments/193_shallow_r4_highband_subcell_radius_source_aggregate_167_192
```

Result:

```text
189 material diagnostic:
  hard-grid 4.0 -> 4.1 mm adjacent log-conductivity delta: 0.000
  subcell-13 4.0 -> 4.1 mm adjacent log-conductivity delta: 11.716

190 subcell-13 coarse high-band curve:
  best r=4.0 mm, next r=4.1 mm, margin=1.96456e-03
  weak interval=4.0-4.1 mm

191 subcell-13 fine radius curve, amplitude fitted:
  best r=4.0 mm, next r=3.975 mm, margin=4.52983e-05
  weak interval=3.925-4.100 mm

192 subcell-13 fine radius curve, no amplitude fitting:
  best r=4.025 mm, next r=4.050 mm, margin=7.26993e-04
  weak interval=3.925-4.100 mm
```

Plot and note validation:

```text
189 geometry_quantization_metrics.png: 1583x1379 px, dynamic range 255, std 36.97
190 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.06
191 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.98
192 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.15
193 source_profiled_polish_aggregate.png: 1685x1583 px, dynamic range 255, std 78.87
```

Reporting correction:

```text
while validating experiment 192, the figure note rounded r=4.025 mm to
r=4.0 mm. The objective summary and CSV were correct; the plain-language note
writer was patched to preserve fine radius steps, covered by a focused test,
and FIGURE_NOTES.md was regenerated for runs 190-192.
```

Interpretation:

The shallow r=4 mm high-band point estimate is stable when amplitude is fitted,
but the fine-radius curve shows a broad objective valley around the truth.
The interval is not just hard-grid quantization: subcell-13 changes geometry
smoothly, yet radii from about `3.925` to `4.100 mm` remain close under the
current weak-interval tolerance. Removing amplitude fitting does not solve the
problem; it shifts the point estimate to `4.025 mm` and keeps the same weak
interval. Therefore amplitude uncertainty should remain explicit, and shallow
4 mm size should currently be reported as an interval rather than a single
high-confidence radius.

Pause-and-ponder decision:

```text
do not claim sub-0.1 mm shallow radius precision from the present high-band
least-squares objective. The next useful branch is material/source ambiguity:
test whether small concrete permittivity/conductivity or source-wavelet
changes explain the same objective valley before adding a more complex
optimizer.
```

## 194: Shallow r=4 Material/Source Tradeoff

Purpose:

```text
test whether material freedom can mimic the shallow r=4 mm high-band radius
valley when source frequency, time shift, and amplitude are also profiled.
```

Code change:

```text
run_single_rebar_material_tradeoff.py now accepts explicit truth x/z/r,
observed source mismatch/noise, source-profiled candidate comparison,
geometry-mode/subcell-sample settings, radius ambiguity reporting, and
FIGURE_NOTES.md generation.
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_material_tradeoff_runner.py tests/test_source_profiled_polish_runner.py
13 passed

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_single_rebar_material_tradeoff.py run_single_rebar_source_profiled_polish.py
passed
```

Output:

```text
outputs/experiments/194_single_rebar_r4_material_source_tradeoff_highband_subcell13_seed13
```

Run matrix:

```text
truth: x=250 mm, z=70 mm, r=4.0 mm
frequency: 2.5 GHz
source mismatch/noise: frequency scale=1.1, time shift=-50 ps,
  amplitude scale=1.1, noise RMS fraction=0.1, seed=13
geometry: subcell, 13 samples
radius values: 3.95, 4.0, 4.025, 4.05, 4.1 mm
concrete epsr values: 5.8, 6.0, 6.2
rebar log10 sigma values: 6, 7
candidate count: 30
```

Result:

```text
best candidate:
  r=4.05 mm, concrete epsr=6.0, rebar log10 sigma=6.0
  source frequency scale=1.1, time shift=-50 ps, amplitude=1.0792
  objective=0.5737832812

next radius:
  r=4.025 mm, concrete epsr=6.0, rebar log10 sigma=6.0
  objective=0.5737960653

true-material radius candidate:
  r=4.0 mm, concrete epsr=6.0, rebar log10 sigma=7.0
  objective=0.5738037013

radius margin:
  1.27841e-05

weak radius interval:
  3.95-4.10 mm
```

Plot/animation validation:

```text
material_profiled_radius.png: 1464x869 px, dynamic range 255, std 32.78
true_r4_sigma1e7_observed_source_wavefield.gif: 48 frames, 1000x600 px,
  max dynamic range 255, mean frame std 34.46
candidate_r405_sigma1e6_profiled_source_wavefield.gif: 48 frames,
  1000x600 px, max dynamic range 255, mean frame std 34.51
```

Interpretation:

Concrete permittivity remains strongly identified at the true value 6.0; the
tested 5.8 and 6.2 cases are much worse. Effective rebar conductivity is the
important nuisance parameter: allowing log10 sigma 6 instead of the nominal
7 shifts the best radius from 4.0 to 4.05 mm while producing an almost tied
objective. This does not prove the radius is 4.05 mm. It proves that shallow
small-radius confidence is sensitive to effective conductivity/source
assumptions, so a single point radius is too strong unless those nuisance
parameters are calibrated or explicitly bounded.

Pause-and-ponder decision:

```text
for shallow r=4 mm, the current best output should be:
  location: high confidence,
  point radius under nominal material/source profiling: 4.0 mm,
  interval with material/source ambiguity: approximately 3.95-4.10 mm.

next, test whether the same material/source ambiguity affects the r=8 branch.
If r=8 remains stable under the same nuisance profiling, then the ambiguity is
primarily a shallow/small-radius limitation; if r=8 also shifts, the final
pipeline needs material-calibrated radius intervals by default.
```

## 195: r=8 Material/Source Tradeoff Control

Purpose:

```text
repeat the bounded material/source profiling from experiment 194 on the
deeper/larger r=8 mm case to see whether the material ambiguity is general or
mainly a shallow small-radius limitation.
```

Output:

```text
outputs/experiments/195_single_rebar_r8_material_source_tradeoff_highband_subcell13_seed13
```

Run matrix:

```text
truth: x=250 mm, z=110 mm, r=8.0 mm
frequency: 2.5 GHz
source mismatch/noise: frequency scale=1.1, time shift=-50 ps,
  amplitude scale=1.1, noise RMS fraction=0.1, seed=13
geometry: subcell, 13 samples
radius values: 7.9, 8.0, 8.05, 8.1, 8.2 mm
concrete epsr values: 5.8, 6.0, 6.2
rebar log10 sigma values: 6, 7
candidate count: 30
```

Result:

```text
best candidate:
  r=8.0 mm, concrete epsr=6.0, rebar log10 sigma=7.0
  source frequency scale=1.1, time shift=-50 ps, amplitude=1.09687
  objective=0.1984729962

nearest competing radius:
  r=8.05 mm, concrete epsr=6.0, rebar log10 sigma=6.0
  objective=0.1984741368

radius margin:
  1.14060e-06

weak radius interval:
  8.0-8.05 mm
```

Plot/animation validation:

```text
material_profiled_radius.png: 1464x869 px, dynamic range 255, std 30.83
true_r8_sigma1e7_observed_source_wavefield.gif: 48 frames, 1000x600 px,
  max dynamic range 255, mean frame std 34.35
candidate_r805_sigma1e6_profiled_source_wavefield.gif: 48 frames,
  1000x600 px, max dynamic range 255, mean frame std 34.66
```

Interpretation:

The deeper/larger r=8 case remains point-stable under the bounded
material/source profile: the best candidate is still the true radius and
nominal effective rebar conductivity. However, the `8.05 mm` candidate with
lower effective rebar conductivity is nearly tied. This means material/source
uncertainty should still widen the radius interval, but the point estimate is
more stable than the shallow r=4 case.

Pause-and-ponder decision:

```text
current best reporting policy:
  r=4 shallow: point 4.0 mm, material/source-aware interval about 3.95-4.10 mm
  r=8 deeper: point 8.0 mm, material/source-aware interval about 8.00-8.05 mm

next stage should turn this into a reusable reporting product: combine nominal
high-band radius confidence with an optional material/source-profiled interval
instead of forcing users to inspect separate diagnostic folders manually.
```

## 196-197: Radius Uncertainty Reporting Product

Purpose:

```text
turn the nominal high-band and material/source-aware radius diagnostics into a
single reusable report so the final pipeline can show point estimate and
interval evidence together.
```

Code change:

```text
added run_radius_uncertainty_report.py with tests. It reads nominal
source-profiled or two-stage summaries plus material-tradeoff summaries,
writes CSV/JSON, plots nominal vs material/source-aware intervals, and creates
plain-language FIGURE_NOTES.md.
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_radius_uncertainty_report.py
5 passed

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_radius_uncertainty_report.py
passed
```

Outputs:

```text
196: outputs/experiments/196_single_rebar_r8_highband25ghz_subcell13_fine_radius005_seed13
197: outputs/experiments/197_radius_uncertainty_report_r4_r8_material_source_191_196
```

Experiment 196 nominal r=8 fine-radius result:

```text
best r=8.0 mm
next r=8.05 mm
margin=1.44889e-03
weak interval=8.0-8.0 mm
```

Experiment 197 report rows:

```text
shallow_r4:
  nominal point=4.0 mm, nominal interval=3.925-4.100 mm
  material/source-aware point=4.05 mm, interval=3.950-4.100 mm
  material best: concrete epsr=6.0, rebar log10 sigma=6.0

deeper_r8:
  nominal point=8.0 mm, nominal interval=8.000-8.000 mm
  material/source-aware point=8.0 mm, interval=8.000-8.050 mm
  material best: concrete epsr=6.0, rebar log10 sigma=7.0
```

Plot validation:

```text
196 source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.91
197 radius_uncertainty_report.png: 1804x835 px, dynamic range 255, std 26.90
```

Interpretation:

The report makes the current policy concrete. The shallow r=4 result has an
exact nominal point estimate, but material/source profiling can move the best
point to 4.05 mm. The deeper r=8 result keeps the point at 8.0 mm, but
material/source profiling adds 8.05 mm to the weak interval. Therefore the
pipeline should report both the nominal point estimate and a material/source
aware interval when nuisance properties are not independently calibrated.

Pause-and-ponder decision:

```text
next implementation step: integrate this reporting product into the packaged
detector-seeded flow as an optional post-processing/reporting stage, not as a
default optimizer step. Keep the expensive material/source grid bounded and
explicitly labeled as uncertainty calibration.
```

## 198: Packaged Material-Uncertainty Report Smoke

Purpose:

```text
verify that the detector-seeded packaged runner can run the optional
material/source uncertainty report after high-band polish without changing the
final point estimate.
```

Code change:

```text
run_detection_seeded_two_stage_refinement.py now supports:
  --enable-material-uncertainty-report
  bounded material/source tradeoff options
  automatic run_radius_uncertainty_report.py post-processing
  root summary paths for material_uncertainty and radius_uncertainty_report
```

Focused validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_detection_seeded_two_stage_refinement.py \
  tests/test_radius_uncertainty_report.py \
  tests/test_material_tradeoff_runner.py
21 passed
```

Output:

```text
outputs/experiments/198_detection_seeded_highband_material_uncertainty_smoke_depth70_r4_seed13
```

Result:

```text
final packaged estimate:
  stage=highband_polish
  x=250.0 mm, z=70.0 mm, r=4.0 mm
  truth errors all 0.0 mm
  high-band margin=1.85997e-03
  nominal weak interval=3.9-4.0 mm

material uncertainty stage:
  radius values=3.95, 4.0, 4.05 mm
  concrete epsr=6.0
  rebar log10 sigma=6, 7
  best material/source-aware radius=4.05 mm
  material/source-aware interval=3.95-4.05 mm
```

Plot validation:

```text
detection_overlay.png: 1885x1209 px, dynamic range 255, std 43.76
coarse source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.58
fine source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.02
highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.99
material_profiled_radius.png: 1464x869 px, dynamic range 255, std 31.75
radius_uncertainty_report.png: 1804x835 px, dynamic range 255, std 29.60
```

Interpretation:

The optional packaged uncertainty report is wired correctly. The final
optimizer result remains the high-band point estimate, while the material
uncertainty stage exposes a separate nuisance-aware radius interval. This is
the right behavior: uncertainty calibration informs reporting, but it does not
silently overwrite the recovered geometry.

Pause-and-ponder decision:

```text
the next development step should improve report ergonomics, not optimizer
aggression: make aggregate summaries compare nominal point error, nominal
interval, material/source-aware interval, and runtime across packaged cases.
```

## 199: Packaged Material-Uncertainty Aggregate

Purpose:

```text
surface optional material/source uncertainty fields in the packaged aggregate
instead of leaving them buried inside stage folders.
```

Code change:

```text
run_two_stage_refinement_aggregate.py now reads
radius_uncertainty_report_summary paths from packaged root summaries, adds
material/source-aware radius columns to CSV/JSON, and writes
two_stage_material_uncertainty_summary.png when any included run has the
optional uncertainty stage.
```

Focused validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_two_stage_refinement_aggregate.py \
  tests/test_detection_seeded_two_stage_refinement.py \
  tests/test_radius_uncertainty_report.py
26 passed
```

Output:

```text
outputs/experiments/199_packaged_highband_material_uncertainty_aggregate_178_198
```

Rows:

```text
178:
  final r=4.0 mm, final margin=1.85997e-03
  material uncertainty: not enabled

198:
  final r=4.0 mm, final margin=1.85997e-03
  material/source-aware r=4.05 mm
  material/source-aware interval=3.95-4.05 mm
  material minus nominal point shift=+0.05 mm
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 84.62
two_stage_stage_confidence_summary.png: 1889x835 px, dynamic range 255, std 55.22
two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 78.95
two_stage_material_uncertainty_summary.png: 1855x1175 px, dynamic range 255, std 65.06
```

Interpretation:

The aggregate makes the distinction explicit: experiments 178 and 198 have the
same nominal high-band result, but 198 carries an extra material/source-aware
uncertainty report. This lets future summaries compare point accuracy and
nuisance-aware uncertainty without conflating them.

Pause-and-ponder decision:

```text
the packaged single-rebar reporting stack is now usable for nominal and
material/source-aware radius uncertainty. Next work should either:
  1. run a packaged r=8 material-uncertainty smoke for symmetry, or
  2. start extending the same reporting discipline to multi-rebar cases.
Given the current single-rebar evidence, a packaged r=8 smoke is the cleaner
short-term validation before returning to multi-rebar.
```

## 200-201: Packaged r=8 Material-Uncertainty Smoke and r4/r8 Aggregate

Purpose:

```text
run the same optional packaged material/source uncertainty branch on the r=8
case, then aggregate r4 and r8 packaged runs with and without the uncertainty
stage.
```

Outputs:

```text
200: outputs/experiments/200_detection_seeded_highband_material_uncertainty_smoke_depth110_r8_seed13
201: outputs/experiments/201_packaged_highband_material_uncertainty_r4_r8_178_200
```

Experiment 200 result:

```text
final packaged estimate:
  stage=highband_polish
  x=250.0 mm, z=110.0 mm, r=8.0 mm
  truth errors all 0.0 mm
  high-band margin=3.05578e-03
  nominal weak interval=8.0-8.0 mm

material uncertainty stage:
  radius values=7.95, 8.0, 8.05 mm
  concrete epsr=6.0
  rebar log10 sigma=6, 7
  best material/source-aware radius=8.0 mm
  material/source-aware interval=8.0-8.05 mm
```

Experiment 201 aggregate rows:

```text
178 r4 nominal only: final r=4.0 mm
184 r8 nominal only: final r=8.0 mm
198 r4 with material report: final r=4.0 mm,
  material/source-aware r=4.05 mm, interval=3.95-4.05 mm
200 r8 with material report: final r=8.0 mm,
  material/source-aware r=8.0 mm, interval=8.0-8.05 mm
```

Plot validation:

```text
200 detection_overlay.png: 1885x1209 px, dynamic range 255, std 43.36
200 highband source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 31.81
200 material_profiled_radius.png: 1464x869 px, dynamic range 255, std 30.57
200 radius_uncertainty_report.png: 1804x835 px, dynamic range 255, std 28.76
201 two_stage_material_uncertainty_summary.png: 1855x1175 px, dynamic range 255, std 54.89
```

Interpretation:

The optional material/source report is now validated inside the packaged flow
for both shallow r=4 and deeper r=8 cases. The final high-band point estimate
stays exact in both. The material/source branch changes reporting, not the
optimizer: r4 gets a shifted nuisance-aware point and interval; r8 keeps the
point but gets an upper-side nuisance-aware interval.

Pause-and-ponder decision:

```text
the single-rebar packaged pipeline now has a defensible reporting story:
exact detector/final location, exact nominal radius point on tested cases,
nominal high-band interval, and optional material/source-aware interval. The
next research stage should return to multi-rebar cases and apply the same
discipline: avoid only reporting best points, add interval and nuisance-aware
reporting where ambiguity is observed.
```

## 228: Two-Stage Aggregate Plot Missing-Data Notice Fix

Purpose:

```text
regenerate the older 118-128 single-rebar aggregate after tightening the plot
code so an apparently blank radius-error panel must carry an explicit
all-zero or missing-data notice.
```

Output:

```text
outputs/experiments/228_two_stage_refinement_aggregate_118_128_nan_notice_plotfix
```

Implementation change:

```text
run_two_stage_refinement_aggregate.py now annotates the radius-error panel
when all finite errors are exactly zero and/or when runs are missing finite
error values. This prevents a visually empty panel from being mistaken for a
plotting failure.
```

Result:

```text
rows: 8
weak confidence runs: 121, 123, 124, 126, 128
```

Plot validation:

```text
two_stage_margin_summary.png: 1855x1243 px, dynamic range 255, std 56.33
two_stage_stage_confidence_summary.png: 1889x835 px, dynamic range 255, std 48.94
two_stage_interval_runtime_summary.png: 1855x1243 px, dynamic range 255, std 65.79
FIGURE_NOTES.md exists.
```

Interpretation:

The top radius-error panel is valid for this aggregate because all included
runs have zero final radius error. The improved plot now says that plainly in
the panel, while the bottom panels still show the important result: several
runs have weak radius margins even when their point radius is exact.
