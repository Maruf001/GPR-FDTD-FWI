# Experiment 519: Seed2178309 Ringdown050 Target-Specific Unresolved Summary

## Purpose

Run 985 summarizes seed2178309 after target1 stayed exact but weak through
source-density escalation.

## 985: Seed2178309 Ringdown050 Target-Specific Unresolved Summary

Output:

```text
outputs/experiments/985_seed2178309_ringdown050_target_specific_unresolved_summary
```

Source runs:

```text
980: target0, sources=8, accepted with late-window caveat
981: target2, sources=5, accepted with early_high razor caveat
982: target1, sources=5, weak control
983: target1, sources=9, weak rescue
984: target1, sources=11, weak escalation
```

## Results

Seed2178309 is accepted on target0 and target2, but target1 is unresolved
under source-density escalation:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 980 | 8 | 5.177171e-04 | +1.772e-05 | accepted with late-window caveat |
| target2 | 981 | 5 | 5.425578e-04 | +4.256e-05 | accepted with early_high razor caveat |
| target1 | 982 | 5 | 4.821346e-04 | -1.787e-05 | unresolved; best of 5/9/11 source rows |

Rejected truth-preserving rows: 982, 983, 984.

## Interpretation

The branch is not a localization failure: every tested row picks the true
target geometry. It is a confidence-reserve failure for target1. Because the
5/9/11 source trend worsens, the next run should test receiver/acquisition
mechanics rather than source count.

## Validation

```text
summary JSON: parsed; row_count=5; diagnostic_row_count=30
accepted runs: 980, 981
rejected truth-preserving runs: 982, 983, 984
branch summary CSV rows: 5
objective diagnostics CSV rows: 30
figure validation: seed2178309_base_margins_by_run.png=1920x960 RGBA nonwhite_fraction=0.535650; seed2178309_objective_margin_heatmap.png=1920x992 RGBA nonwhite_fraction=0.724398; seed2178309_target1_source_density_trend.png=1536x960 RGBA nonwhite_fraction=0.025350
visual inspection: base-margin chart, objective heatmap, and target1 source-density trend are readable and support the unresolved target1 decision
figure notes: figures/FIGURE_NOTES.md present
resources: no new FDTD scene; GPU moved to the linear receiver mechanism test
```

## Next Decision

Run seed2178309 target1 with the same 5-source Tx/Rx=60 setup but linear
receiver sampling. That mechanism test is underway as experiment 986.
