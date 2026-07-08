# Field Experiment 310: Real-Return Post Acceptance Gate Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `309` field post-acceptance claim-boundary validator with
controlled damaged variants.

## Result

```text
scenarios:                         11
expected pass:                     1
observed pass:                     1
expected failures:                 10
observed failures:                 10
unexpected outcomes:               0
sensitivity ready:                 true
accepts exact run 308:             true
rejects damaged variants:          true
real packet files present:         false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

Use runs `308-310` as the guarded field post-acceptance claim-boundary block.

Figure validation:

```text
3365x909, dynamic range=255
```
