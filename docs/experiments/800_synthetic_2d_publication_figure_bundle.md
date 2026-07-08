# Experiment 800: Synthetic 2D Publication Figure Bundle

Date: 2026-06-17

## Purpose

CPU-only publication-facing synthesis of the current synthetic 2D policy
figures and their claim boundaries. This uses existing outputs only and does
not launch FDTD, FWI, GPU kernels, or new inversion experiments.

Supersession note:

```text
Experiment 822 / run 1309 is the current synthetic paper-facing bundle. It
keeps this bundle's core figures and adds the later 1307 resolution-claim map
and 1308 close50 legacy midpoint refresh.
```

## Output

```text
outputs/experiments/1278_synthetic_2d_publication_figure_bundle
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
synthetic_2d_publication_bundle_ready_gpu_priority_none
```

Summary:

```text
figure count:                  5
validated figure count:        5
claim boundary count:          4
gpu priority:                  none
ready for manuscript draft:    true
```

Included synthetic figure rows:

| Figure key | Source run | Status |
| --- | --- | --- |
| `resolution_envelope` | 1239 | acquisition-aware close-spacing policy |
| `weak_exact_secondary_confirmation` | 1262 | diagnostic weak-exact confirmation |
| `close50_sub30_boundary` | 1275 | sub-30 linear receiver caveat |
| `target0_exception_closure` | 1276 | source-density closure for target0 |
| `modern_ringdown050_gpu_queue` | 1277 | no open modern ringdown050 GPU priority |

## Interpretation

Use the five listed synthetic figures as publication-facing policy figures with
the claim boundaries in:

```text
data/synthetic_2d_publication_claim_boundaries.csv
```

This bundle does not justify a GPU run. It explicitly preserves the current
synthetic position:

```text
Do not launch broad GPU sweeps without a new objective, geometry, or
acquisition question.
```

It also keeps field and synthetic evidence separate:

```text
Do not use field QC to change known-truth synthetic confidence labels.
```

## Validation

Focused tests:

```text
tests/test_synthetic_2d_publication_figure_bundle.py: 4 passed
```

Figure validation:

```text
synthetic_2d_publication_figure_bundle.png: 2739x903,
nonwhite=0.3510, dynamic range=255
```
