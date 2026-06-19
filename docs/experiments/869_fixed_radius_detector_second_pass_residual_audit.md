# Experiment 869: Fixed-Radius Detector Second Pass And Residual Audit

Date: 2026-06-19

## Purpose

Resolve the next local 2D detector-refinement question after runs `1340` and
`1341`: whether the repaired exact-radius detector seed could remove its
remaining 2 mm lateral residual with one more bounded local pass.

This is still a controlled synthetic fixed-radius study. The radii `[5,6,8]`
mm are controlled priors, not detector-inferred radius estimates. This work
does not authorize broad GPU queues, detector-seeded FWI, field transfer, 3D,
HPC, or neural-network work.

## Guarded GPU Pilot

```text
output:      outputs/experiments/1357_local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu
backend:     gpu-cpml
sources:     5
Tx/Rx:       45 mm
initial:     [191,252,266] / [90,89,91] mm
final:       [190,251,265] / [90,89,91] mm
truth:       [190,250,264] / [90,90,90] mm
radii:       [5,6,8] mm
offsets:     x/z -2,-1,0,1,2 mm
```

The second pass improved the best repaired nominal case from 2 mm max
coordinate error to 1 mm, but did not reach exact recovery.

Resource guard:

```text
return code:     0
aborted:         false
max GPU util:   88%
max RAM used:   14.996%
```

## CPU Synthesis

Run `127` refreshes the fixed-radius pilot outcome selector:

```text
output:                         outputs/summary_tables/127_local_2d_detector_fixed_radius_pilot_outcome_synthesis_post_second_pass
pilot runs included:            3
best final L-infinity error:    1 mm
within-1-mm residual pilots:    1
immediate second-pass ready:    false
broad GPU queue ready:          false
detector-seeded FWI ready:      false
gpu priority:                   none
```

Run `128` audits the candidate tables from `1357`:

```text
output:                                      outputs/summary_tables/128_local_2d_detector_fixed_radius_residual_ambiguity_audit_post_second_pass
selected truth coordinate count:             1 / 3
truth candidate present count:               2 / 3
truth selected but ambiguous count:          1
truth present but neighbor preferred count:  1
truth absent after non-overlap filter count: 1
final x errors:                              [0,1,1] mm
final z errors:                              [0,-1,1] mm
immediate GPU iteration ready:               false
```

Interpretation:

```text
target 0: truth is selected, but with a near tie.
target 1: exact target coordinate is present, but [251,89] has lower misfit.
target 2: exact target coordinate is absent after non-overlap filtering because
          the sequential state still contains the target1 residual.
```

This means the 1 mm residual is not simply a missing-local-samples problem. It
is a coordinate-policy / update-order / non-overlap-coupling issue.

## Manuscript Table Pack

Run `129` folds the new result into the current local 2D and field manuscript
evidence bundle:

```text
output:                           outputs/summary_tables/129_local_2d_field_manuscript_table_pack_post_fixed_radius_residual_audit
metric rows:                      301
auxiliary evidence metrics:       285
fixed-radius pilot runs:          3
best fixed-radius residual:       1 mm
objective-neighbor residuals:     1
non-overlap-absent residuals:     1
gpu priority:                     none
ready for manuscript table use:   true
```

## Locking Policy Validation

Run `130` uses the saved `1357` candidate tables to test a CPU-side
update-order policy. The actionable hypothesis is to lock target 1 to the
truth-coordinate near-tie `[250,90]` instead of the greedy `[251,89]`, because
that removes the downstream non-overlap exclusion for target 2.

```text
output:                                      outputs/summary_tables/130_local_2d_detector_fixed_radius_locking_policy_design
selected lock target:                        1
selected lock coordinate:                    [250,90] mm
selected lock rank:                          2
objective penalty relative to greedy:        0.0341456
downstream truth clearance before lock:      -0.961595 mm
downstream truth clearance after lock:       0 mm
single guarded unlock probe ready:           true
broad GPU queue ready:                       false
detector-seeded FWI ready:                   false
```

Run `1358` executes exactly that one guarded target-2 unlock probe:

```text
output:                    outputs/experiments/1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu
initial state:             [190,250,266] / [90,90,91] mm
final state:               [190,250,264] / [90,90,90] mm
truth:                     [190,250,264] / [90,90,90] mm
final L-infinity error:    0 mm
target updated:            2 only
guard aborted:             false
max GPU utilization:       88%
max RAM used:              14.688%
```

Run `131` synthesizes the validation:

```text
output:                                  outputs/summary_tables/131_local_2d_detector_fixed_radius_locking_policy_validation_post_unlock_probe
exact geometry recovered:                true
truth selected count:                    1 / 1 updated targets
truth selected but ambiguous count:      1
locking mechanism claim ready:           true
general detector policy claim ready:     false
broad GPU queue ready:                   false
detector-seeded FWI ready:               false
field transfer ready:                    false
gpu priority:                            none
```

Run `132` folds the validation into the local 2D and field manuscript table
pack:

```text
output:                              outputs/summary_tables/132_local_2d_field_manuscript_table_pack_post_fixed_radius_locking_validation
metric rows:                         308
auxiliary evidence metrics:          292
locking validation exact:            true
locking mechanism claim ready:       true
locking broad GPU ready:             false
gpu priority:                        none
ready for manuscript table use:      true
```

Interpretation: the fixed-radius near-tie downstream-clearance mechanism is
validated on this repaired `target2_close14|seed21|nominal` branch. This is a
single-branch mechanism result. It does not establish a general detector
policy, does not authorize a broad GPU queue, and does not open
detector-seeded FWI or field transfer.

## Decision

Stop immediate GPU iteration on this branch. The one falsifiable
coordinate-locking hypothesis has now been validated under the resource guard.
The next 2D work should use this as mechanism evidence and continue CPU-side
policy generalization or independent field-QC work; it should not turn this
single exact result into a broad detector or FWI launch claim.
