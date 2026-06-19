# Experiment 822: Synthetic 2D Publication Bundle Refresh

Date: 2026-06-18

## Purpose

Refresh the paper-facing synthetic 2D figure bundle after the newer resolution
claim map and close50 270/280 midpoint-aware audit were generated. This is a
CPU-only synthesis over existing outputs; it does not launch FDTD, FWI, GPU
kernels, or new inversion experiments.

This tracker superseded experiment 800 at the time it was written. It has now
been superseded by experiment 830 / run 1320, which keeps the replicated
close50 28.75 mm midpoint evidence and adds the current target1
acquisition-confidence and source-density policy figures.

## Output

```text
outputs/experiments/1309_synthetic_2d_publication_figure_bundle_post_resolution_map_refresh
```

Artifacts:

```text
data/synthetic_2d_publication_figure_rows.csv
data/synthetic_2d_publication_claim_boundaries.csv
data/synthetic_2d_publication_figure_bundle_summary.json
data/figure_validation.csv
figures/synthetic_2d_publication_figure_bundle.png
run_manifest.json
```

## Result

Policy label:

```text
synthetic_2d_publication_bundle_current_resolution_map_ready_gpu_priority_none
```

Summary:

```text
figure count:                  7
validated figure count:        7
claim boundary count:          5
gpu priority:                  none
ready for manuscript draft:    true
```

Included synthetic figure rows:

| Figure key | Source run | Use |
| --- | --- | --- |
| `current_resolution_claim_map` | 1307 | current manuscript resolution claim map |
| `resolution_envelope` | 1239 | acquisition-aware close-spacing policy |
| `weak_exact_secondary_confirmation` | 1262 | diagnostic weak-exact confirmation |
| `close50_sub30_boundary` | 1275 | sub-30 linear receiver caveat |
| `close50_legacy_midpoint_refresh` | 1308 | midpoint-aware 270/280 branch refresh |
| `target0_exception_closure` | 1276 | source-density closure for target0 |
| `modern_ringdown050_gpu_queue` | 1277 | no open modern ringdown050 GPU priority |

## Interpretation

Use run 1309 as the current synthetic paper-facing bundle. It folds the newer
run 1307 resolution-claim map and run 1308 close50 legacy refresh into the
older bundle, while preserving the no-broad-GPU claim boundary.

The current synthetic manuscript boundary is:

```text
Use acquisition- and objective-specific resolution claims.
Keep physical non-overlap, overlap stress tests, objective-uniqueness limits,
seed-frequency caveats, and legacy close50 branch refreshes separate.
Do not present a universal rebar-spacing law.
Do not launch broad GPU sweeps without a new objective, geometry, or acquisition question.
Keep field QC separate from known-truth synthetic confidence labels.
```

## Validation

Focused tests:

```text
tests/test_synthetic_2d_publication_figure_bundle.py
4 passed
```

Figure validation:

```text
synthetic_2d_publication_figure_bundle.png: 2738x903,
nonwhite=0.3508, dynamic range=255
```
