# Experiment 361: Seed21 All-Targets Ringdown0459375 Transfer Summary

## Purpose

Run 827 aggregates the seed21 target-specific 8/9/9 policy at
ringdown0459375. It combines target 0 run 826, target 1 run 820, and target 2
run 825 to close the seed21 all-target transfer branch.

## 827: Seed21 All-Targets Ringdown0459375 Transfer Summary

Output:

```text
outputs/experiments/827_seed21_alltargets_ringdown0459375_transfer_summary
```

Source runs:

| Run | Tracker | Target | Sources | Baseline run | Base margin | Retention vs ringdown035 | Offset from cutoff | Confidence |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 826 | 360 | 0 | 8 | 802 | 5.151442e-04 | 0.946 | +1.514e-05 | moderate |
| 820 | 354 | 1 | 9 | 803 | 5.560564e-04 | 0.978 | +5.606e-05 | moderate |
| 825 | 359 | 2 | 9 | 804 | 5.252174e-04 | 0.984 | +2.522e-05 | moderate |

## Result

Seed21 passes the all-target ringdown0459375 transfer check. All three base
rows are exact and production-moderate under the target-specific 8/9/9
source-count policy. Target 0 is the limiting production row with a
`5.151442e-04` margin, while target 1 is `5.560564e-04` and target 2 is
`5.252174e-04`.

All base rows recover the exact geometry:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

All 18 diagnostic objective rows preserve the true target geometry. Three
diagnostic rows fall below `5e-04`: target 0 `late` at `3.215678e-04`, target
0 `late_high` at `4.034978e-04`, and target 2 `early_high` at
`4.929564e-04`.

## Interpretation

The seed21 all-target result is positive but narrower than seed89. Target 0 is
only `1.514e-05` above the cutoff, and the retention range versus ringdown035
is 0.946-0.984. The limiting target also changes by seed: seed89 was limited
by target 1, while seed21 is limited by target 0.

The diagnostic pattern is consistent with prior runs. Late windows are fragile
for the shallow target, and early_high is slightly weak for the deep/larger
target. None of those weak-margin diagnostics change the selected geometry.

## Validation

```text
JSON parse: seed21_alltargets_ringdown0459375_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18
figure validation: seed21_alltargets_base_margins.png is 1944x1116 RGBA with nonwhite_fraction=0.427 and full 0-255 RGB-converted dynamic range
figure validation: seed21_alltargets_objective_margin_heatmap.png is 2088x1044 RGBA with nonwhite_fraction=0.662 and full 0-255 RGB-converted dynamic range
visual inspection: both summary figures are readable and show target 0 as the limiting seed21 production row
source validation: all base rows exact/moderate; all objective rows truth-preserving
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Create a cross-seed all-target ringdown0459375 summary from seed13 run 818,
seed89 run 824, and seed21 run 827 before increasing ringdown stress.
