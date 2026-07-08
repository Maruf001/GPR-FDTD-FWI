# Experiment 1548: Two-Sided Edge Follow-Up Offset Probe Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1547` validator for the executed two-sided edge follow-up
offset probe.

Run `1546` executed the five planned offsets from run `1543` as a bounded
20-case CPU probe. Run `1547` validated the saved artifacts. This run asks
whether that validator rejects plausible artifact drift instead of only
accepting the exact saved run.

## Output

```text
outputs/experiments/1548_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_validation_sensitivity
```

## Result

```text
scenario count:                       13
expected pass count:                  1
observed pass count:                  1
expected failure count:               12
observed failure count:               12
unexpected outcomes:                  0
validation sensitivity ready:         true
validator accepts exact run 1546:     true
validator rejects damaged variants:   true
planned case count:                   20
any-failure model count:              20
all-objective-failure model count:    0
new physical claim ready:             false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

The exact run `1546` artifacts pass. Twelve damaged variants fail as expected:
source identity drift, planned-case count drift, grid-model count drift,
objective-row count drift, failure-taxonomy drift, offset-matrix drift,
edge-row drift, false downstream promotion, figure-validation drift, and
script-snapshot drift.

## Interpretation

Runs `1546-1548` now form a closed executed follow-up offset-probe block. The
extra offset samples around 45.0 mm do not support a broader suppression-window
claim: all 20 planned cases still have at least one objective failure, and no
case has all-objective failure.

The result remains a local 2D numerical objective-boundary finding. It does not
justify a new physical acquisition rule, GPU escalation, field transfer, field
FWI, or 3D/HPC escalation.

## Decision

Use runs `1546-1548` as the guarded executed follow-up offset-probe block.
Treat the wider suppression-window and physical-acquisition claims as blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_validation_sensitivity.py
3 passed
```

Figure check:

```text
3653x913, dynamic range=255
```
