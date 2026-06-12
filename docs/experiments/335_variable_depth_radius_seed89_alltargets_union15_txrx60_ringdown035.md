# Experiment 335: Seed89 All-Targets Union15 Tx/Rx=60 Ringdown035

## Purpose

Run 801 tests a single common aperture built from the union of the target-0
8-source layout and the target-1/target-2 9-source layout. The goal is to see
whether keeping all previously useful source positions can produce one
all-target policy under the stronger ringdown035 source stress.

## 801: Coordinate Optimizer Variable-Depth/Radius Seed89 All-Targets Union15 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/801_coordinate_optimizer_variable_depth_radius_seed89_alltargets_union15_txrx60_ringdown035_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 15 \
  --scan-x-values-mm 50,98,106,146,162,194,218,250,274,298,330,346,386,394,450 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 0,1,2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown035_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_alltargets_union15_txrx60_ringdown035_objectives
```

## Results

Final recovered state:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence rows:

| Target | Best x mm | Best z mm | Best r mm | Next r mm | Base margin | Confidence |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 150 | 80 | 5.0 | 5.25 | 4.521727e-04 | weak |
| 1 | 250 | 100 | 6.0 | 6.25 | 5.560820e-04 | moderate |
| 2 | 350 | 120 | 8.0 | 8.75 | 5.822071e-04 | moderate |

Baseline comparisons:

| Comparison | Ratio | Decision |
| --- | ---: | --- |
| target 0 union15 vs target-0 8-source ringdown035 run 795 | 0.759 | worse |
| target 0 union15 vs target-0 9-source ringdown035 run 797 | 0.909 | worse |
| target 0 union15 vs target-0 60.5 mm linear run 800 | 0.911 | worse |
| target 1 union15 vs target-1 9-source ringdown035 run 794 | 1.025 | better |
| target 2 union15 vs target-2 9-source ringdown035 run 796 | 0.961 | slightly worse |

## Interpretation

Run 801 rejects the union-of-helpful-positions aperture as a common all-target
base policy. The final geometry is exact for all three targets, and the dense
15-position aperture preserves moderate rows for targets 1 and 2, but target 0
falls to a weak 4.522e-04 base margin. That is worse than the previous weak
9-source target-0 rows and only 0.759x the target-0 8-source ringdown035 row
from run 795.

The result strengthens the current conclusion that target 0 is not simply
starved for more views. Its weak behavior is coupled to aperture placement, and
adding the target-1/target-2-friendly source positions can make target 0 worse.
Therefore a single dense union aperture should not replace the target-specific
8/9/9 source-count policy.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=3, objective diagnostics=18, objective top candidates=216, state history=4, candidate grids=12/12/12
figure validation: coordinate_confidence_margins.png is 1545x903 RGB with nonwhite_fraction=0.234 and full 0-255 dynamic range
visual inspection: confidence figure is readable with one weak target-0 bar and two moderate target-1/2 bars
figure notes: figures/FIGURE_NOTES.md present and identifies weak target 0
metadata validation: truth_radius_values_mm is [5,6,8]; the legacy scalar truth_radius_mm is not used for per-target interpretation in this all-target run
resources: GPU utilization held mostly 91-94%; Python RSS stayed about 443-473 MiB; RAM stayed about 98-99 GiB available
elapsed: 3921.51 s
```

## Next Decision

Do not continue with denser union apertures as the next default branch. The
next GPU branch should either test a deliberately target-0-preserving aperture
with a formal selection criterion, or move back to the target-specific 8/9/9
source-count policy and stress it under a new seed/case instead of trying to
force one common aperture.
