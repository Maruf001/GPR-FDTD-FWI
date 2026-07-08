# Experiment 820: Synthetic 2D Resolution-Claim Map

Date: 2026-06-18

## Purpose

Build a compact paper-facing map of what the current synthetic 2D evidence can
and cannot claim about resolution. This is a CPU-only synthesis over existing
policy outputs; it does not launch a new optimizer run.

## Output

```text
1307_synthetic_2d_resolution_claim_map_current
```

Key artifacts:

```text
outputs/experiments/1307_synthetic_2d_resolution_claim_map_current/data/synthetic_2d_resolution_claim_map_rows.csv
outputs/experiments/1307_synthetic_2d_resolution_claim_map_current/data/synthetic_2d_resolution_claim_map_summary.json
outputs/experiments/1307_synthetic_2d_resolution_claim_map_current/figures/synthetic_2d_resolution_claim_map.png
```

## Result

```text
policy label:                         synthetic_2d_resolution_claim_map_close14_close50_current_cpu_no_gpu
map rows:                             8
physical non-overlap guardrail:       14 mm
overlap-stress min clean spacing:     10 mm
target2 close14 strong rows:          6
target2 close14 0.5x near-tie rows:   6
target2 close50 seed count:           3
target2 close50 strict-clean seeds:   2
target2 close50 ambiguous seed:       seed13
conditional GPU candidates:           0
gpu priority:                         none_now
```

The row map separates:

```text
physical_nonoverlap_guardrail
overlap_stress_test_boundary
target0_claim_tier
target1_claim_tier
target2_claim_tier
target2_close14_source5_txrx45_objective_limit
target2_close50_linear29p5_seed_frequency
current_synthetic_gpu_queue
```

## Interpretation

The current synthetic evidence supports a cautious resolution table, not a
universal rebar-spacing law:

```text
close14: tangent non-overlap guardrail for the 6 mm + 8 mm target1/target2 pair
close10/close12: overlapping-cylinder algorithmic stress tests only
target2 close14 source5 / TxRx45: truth and strong radius confidence, but not objective-unique
target2 close50 linear 29.5 mm: exact/strong across three seeds, but not clean-replicated
current GPU queue: zero conditional candidates under the current local 2D policy
```

This table should be used with the refreshed claim-boundary CSV from run 1305.
It complements run 1306: run 1306 says no immediate GPU work remains; run 1307
summarizes the current resolution-language boundary for manuscript use.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_resolution_claim_map.py
3 passed
```

Figure validation:

```text
1307 synthetic_2d_resolution_claim_map.png: 2314x1294, dynamic range=255
```
