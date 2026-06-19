# Experiment 863: Close-Spacing Matched Source3 Policy Synthesis

Date: 2026-06-19

## Purpose

Synthesize the completed close14 and close50 matched source3 probe aggregates
from experiments `859` and `862` into a paper-facing claim/gate table.

This is CPU-only synthesis of saved synthetic 2D summaries. It does not run
FDTD/FWI, GPU kernels, detector-seeded FWI, field FWI, 3D/HPC work, or
neural-network training.

## Output

```text
outputs/summary_tables/121_close_spacing_matched_source3_policy_synthesis
```

Key artifacts:

```text
data/close_spacing_matched_source3_family_rows.csv
data/close_spacing_matched_source3_claim_rows.csv
data/close_spacing_matched_source3_gate_rows.csv
data/close_spacing_matched_source3_policy_summary.json
figures/close_spacing_matched_source3_policy_synthesis.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                                close_spacing_matched_source3_policy_synthesis
queue complete:                              true
close14 truth-geometry fraction:             1.0
close50 truth-geometry fraction:             0.0
close14 all truth and strong:                true
close50 replicated wrong branch:             true
guarded acquisition/geometry contrast ready: true
spacing-only causal generalization ready:    false
ready for broad GPU queue:                   false
ready for field FWI:                         false
ready for 3D/HPC handoff:                    false
ready for neural-network training:           false
gpu priority:                                none
recommended next local mode:                 cpu_manuscript_policy_or_field_collection_packet
```

Family rows:

```text
close14 source3 Tx/Rx40:
  target1-target2 gap: 14 mm
  target2 truth:       x=264 mm, z=90 mm, r=8 mm
  truth rows:          6/6
  confidence labels:   strong=6
  mean radius margin:  0.003478

close50 source3 Tx/Rx45:
  target1-target2 gap: 50 mm
  target2 truth:       x=300 mm, z=90 mm, r=8 mm
  selected branch:     x=299 mm, z=90 mm, r=7.5 mm
  truth rows:          0/6
  confidence labels:   moderate=4, strong=2
  mean radius margin:  0.000906
```

Claim gates:

```text
ready:   matched source3 queue complete
ready:   close14 Tx/Rx40 exact/strong result
ready:   close50 Tx/Rx45 replicated near-truth wrong branch
ready:   guarded acquisition/geometry-aware contrast
blocked: spacing-only causal generalization
blocked: broad GPU queue
blocked: field FWI or field 3D/HPC from current local field archive
```

## Interpretation

The completed matched-source3 queue supports a guarded
acquisition/geometry-aware contrast. It is now fair to say that close14
source3 survives the reciprocal Tx/Rx40 control while close50 source3 does not
survive the reciprocal Tx/Rx45 control.

It is still not fair to say that target spacing alone controls the outcome.
The absolute target2 position changes with the target1-target2 gap, and the
close50 result is a stable near-truth wrong branch rather than a truth-selected
ambiguity interval. The next local step should be manuscript synthesis or
field-collection packet work, not a broad GPU branch.

## Validation

Focused tests:

```text
tests/test_close_spacing_matched_source3_policy_synthesis.py
2 passed
```

Figure validation:

```text
close_spacing_matched_source3_policy_synthesis.png: 2739x903,
nonwhite=0.2677, dynamic range=255
```
