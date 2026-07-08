# BEM Experiment 367: Real-Pair Post Acceptance Gate Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `366` BEM post-acceptance claim-boundary validator with
controlled damaged variants.

## Result

```text
scenarios:                    10
expected pass:                1
observed pass:                1
expected failures:            9
observed failures:            9
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 365:        true
rejects damaged variants:     true
real comparison ready:        false
threshold calibration ready:  false
GPU work ready:               false
field transfer ready:         false
3D validation ready:          false
```

Use runs `365-367` as the guarded BEM post-acceptance claim-boundary block.

Figure validation:

```text
3365x909, dynamic range=255
```
