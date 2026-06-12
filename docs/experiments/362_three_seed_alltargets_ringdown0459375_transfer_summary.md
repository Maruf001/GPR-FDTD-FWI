# Experiment 362: Three-Seed All-Targets Ringdown0459375 Transfer Summary

## Purpose

Run 828 aggregates the complete cross-seed all-target transfer result at
ringdown0459375. It combines seed13 summary run 818, seed89 summary run 824,
and seed21 summary run 827.

## 828: Three-Seed All-Targets Ringdown0459375 Transfer Summary

Output:

```text
outputs/experiments/828_three_seed_alltargets_ringdown0459375_transfer_summary
```

Source summaries:

| Seed | Summary run | Tracker | Source runs | Limiting target | Limiting base margin | Offset from cutoff |
| ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 13 | 818 | 352 | 817, 814, 816 | 1 | 5.007215e-04 | +7.215e-07 |
| 89 | 824 | 358 | 823, 819, 822 | 1 | 5.314442e-04 | +3.144e-05 |
| 21 | 827 | 361 | 826, 820, 825 | 0 | 5.151442e-04 | +1.514e-05 |

## Result

Ringdown0459375 transfers across all three tested seeds under the
target-specific 8/9/9 source-count policy. All nine production base rows are
exact and production-moderate. The global limiting row is seed13 target 1 from
run 814, with a `5.007215e-04` margin only `7.215e-07` above the cutoff.

Per-target limiting rows:

| Target | Limiting seed | Run | Base margin | Offset from cutoff |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 21 | 826 | 5.151442e-04 | +1.514e-05 |
| 1 | 13 | 814 | 5.007215e-04 | +7.215e-07 |
| 2 | 21 | 825 | 5.252174e-04 | +2.522e-05 |

All 54 diagnostic objective rows preserve true geometry. Seven diagnostic rows
are below `5e-04`, and all are truth-preserving:

```text
seed13 target0 late
seed13 target2 early_high
seed89 target0 late
seed89 target0 late_high
seed21 target0 late
seed21 target0 late_high
seed21 target2 early_high
```

## Interpretation

The cross-seed policy result is positive, but the stress level is already at
the boundary. The strongest evidence for caution is not a geometry failure; it
is the seed13 target-1 margin from run 814, which is almost exactly on the
production cutoff. Seed21 target 0 is the second limiting production row, and
its late-window diagnostics are weak.

This means ringdown0459375 can be reported as a reproduced all-target pass, but
the next scientific question is whether the limiting seed13 target-1 case can
be strengthened, not whether a blind ringdown increase is justified.

## Validation

```text
JSON parse: three_seed_alltargets_ringdown0459375_summary.json and run_manifest.json pass
CSV rows: base rows=9, objective rows=54, summary inputs=3
figure validation: three_seed_base_margin_heatmap.png is 1944x1044 RGBA with nonwhite_fraction=0.669 and full 0-255 RGB-converted dynamic range
figure validation: three_seed_limiting_base_margins.png is 1944x1116 RGBA with nonwhite_fraction=0.422 and full 0-255 RGB-converted dynamic range
visual inspection: both summary figures are readable and show seed13 target 1 as the global limiting row
source validation: all base rows exact/moderate; all objective rows truth-preserving
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Investigate seed13 target 1, the global limiting row, before increasing
ringdown stress. A targeted acquisition/objective improvement run is more
justified than a blind higher-ringdown sweep.
