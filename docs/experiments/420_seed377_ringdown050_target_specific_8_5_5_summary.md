# Experiment 420: Seed377 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 886 summarizes the completed seed377 full-ringdown050 policy branch.

## Results

Output:

```text
outputs/experiments/886_seed377_ringdown050_target_specific_8_5_5_summary
```

Promoted rows:

| Target | Run | Tracker | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 883 | 417 | 8 | 5.527795e-04 | +5.278e-05 | accepted |
| 1 | 885 | 419 | 5 | 5.619730e-04 | +6.197e-05 | accepted |
| 2 | 884 | 418 | 5 | 5.096084e-04 | +9.608e-06 | accepted |

Seed377 passes as a full-ringdown050 `8/5/5` seed, but target 2 is the
limiting low-reserve row.

Objective diagnostics:

```text
diagnostic rows: 18
truth-preserving diagnostic rows: 18
diagnostic rows above cutoff: 15
sub-cutoff diagnostics: target0 late, target0 late_high, target2 early_high
```

## Interpretation

Seed377 joins seed13, seed55, seed144, and seed233 as an `8/5/5` seed. Its
target-2 row is only `+9.608e-06` above cutoff, making it the weakest accepted
target-2 5-source row so far.

## Validation

```text
JSON parse: seed377_ringdown050_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18, target2 cross-seed rows=7
source validation: promoted truth rows=3/3, promoted rows above cutoff=3/3
diagnostic validation: 18/18 diagnostics preserve truth, 15/18 diagnostics clear cutoff
figure validation: base margins plot is 1376x864 RGBA with nonwhite_fraction=0.436385 and full 0-255 dynamic range
figure validation: objective heatmap is 1792x912 RGBA with nonwhite_fraction=0.629922 and full 0-255 dynamic range
figure validation: target2 comparison plot is 1664x880 RGBA with nonwhite_fraction=0.426109 and full 0-255 dynamic range
visual inspection: all three figures are readable; target2 low-reserve row is clear
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Use run 886 as the seed377 policy input to the next cross-seed synthesis and
continue target-0 lower-tail replication with seed610.
