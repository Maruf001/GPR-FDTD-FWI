# Experiment 810: Synthetic Claim Tier Table

Date: 2026-06-17

## Purpose

CPU-only manuscript-facing table that merges geometry-clean tiers from
experiment 807 with raw competing-geometry objective separation from experiment
809.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1288_synthetic_claim_tier_table
```

Artifacts:

```text
data/synthetic_claim_tier_rows.csv
data/synthetic_claim_tier_summary.json
data/figure_validation.csv
figures/synthetic_claim_tier_table.png
run_manifest.json
```

## Result

Policy label:

```text
synthetic_claim_tiers_geometry_clean_and_objective_unique_separated_cpu_no_gpu
```

Summary:

```text
targets:                              3
exact-strong rows:                    323
geometry-clean rows:                  302
objective-unique rows:                284
reported-width near ties:             21
zero-width competing-geometry ties:   18
geometry-clean fraction:              0.934985
objective-unique fraction:            0.879257
gpu priority:                         none_now
```

Target table:

```text
target0: exact strong 3,   geometry clean 3,   objective unique 3
target1: exact strong 53,  geometry clean 53,  objective unique 44
target2: exact strong 267, geometry clean 246, objective unique 237
```

## Interpretation

Manuscript tables should distinguish three levels:

```text
exact-strong
geometry-clean
objective-unique
```

Objective uniqueness must use raw competitor threshold separation, not
ambiguity-width fields alone. Target0 supports all three levels. Target1
supports geometry-clean wording but needs objective-uniqueness caveats. Target2
needs both geometry-clean and objective-uniqueness caveats.

No broad GPU run is justified by this table.

## Validation

Focused tests:

```text
tests/test_synthetic_claim_tier_table.py: 3 passed
```

Figure validation:

```text
synthetic_claim_tier_table.png: 2229x835,
nonwhite=0.3673, dynamic range=255
```
